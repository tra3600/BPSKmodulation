"""Simulation d'une chaîne de transmission BPSK (Binary Phase Shift Keying).

Chaîne : bits -> modulation -> canal AWGN -> démodulation cohérente -> bits.
Le script trace aussi la courbe TEB (BER) simulée face à la théorie
Pb = 0.5 * erfc(sqrt(Eb/N0)).

Exemples :
    python modulationBPSK.py                    # affiche les figures
    python modulationBPSK.py --save figures     # enregistre les PNG sans fenêtre
    python modulationBPSK.py --bits 1011001 --ebn0 6
"""
import argparse
import math
import os

import numpy as np


def samples_per_bit(sampling_rate, duration):
    """Nombre (entier) d'échantillons par bit."""
    n = int(round(sampling_rate * duration))
    if n < 2:
        raise ValueError("sampling_rate * duration doit valoir au moins 2 échantillons par bit")
    return n


def _check_bits(bits):
    bits = np.asarray(bits, dtype=int)
    if bits.ndim != 1 or bits.size == 0 or not np.isin(bits, (0, 1)).all():
        raise ValueError("bits doit être une séquence 1D non vide de 0 et de 1")
    return bits


def bpsk_modulation(bits, carrier_freq, sampling_rate, duration):
    """Module une séquence de bits en BPSK.

    bit 1 -> +cos(2*pi*fc*t), bit 0 -> -cos(2*pi*fc*t) (déphasage de pi).

    :param bits: séquence de bits (0/1).
    :param carrier_freq: fréquence de la porteuse (Hz).
    :param sampling_rate: fréquence d'échantillonnage (Hz).
    :param duration: durée d'un bit (s).
    :return: (t, signal) temps et signal modulé (amplitude 1).
    """
    bits = _check_bits(bits)
    if carrier_freq <= 0 or carrier_freq >= sampling_rate / 2:
        raise ValueError("la porteuse doit vérifier 0 < fc < fs/2 (Shannon)")
    n = samples_per_bit(sampling_rate, duration)
    t = np.arange(bits.size * n) / sampling_rate
    symbols = np.repeat(2 * bits - 1, n)  # {0,1} -> {-1,+1}
    return t, symbols * np.cos(2 * np.pi * carrier_freq * t)


def add_awgn(signal, ebn0_db, sampling_rate, duration, rng=None):
    """Ajoute un bruit blanc gaussien pour un rapport Eb/N0 donné (dB).

    Pour une porteuse d'amplitude 1 : Eb = Tb/2 et la variance du bruit par
    échantillon vaut sigma^2 = N0 * fs / 2.
    """
    rng = np.random.default_rng() if rng is None else rng
    eb = duration / 2
    n0 = eb / (10 ** (ebn0_db / 10))
    sigma = math.sqrt(n0 * sampling_rate / 2)
    return signal + rng.normal(0.0, sigma, size=np.shape(signal))


def bpsk_demodulation(received, carrier_freq, sampling_rate, duration):
    """Démodulation cohérente : corrélation avec la porteuse sur chaque bit.

    :return: (bits décidés, statistiques de décision par bit).
    """
    n = samples_per_bit(sampling_rate, duration)
    received = np.asarray(received, dtype=float)
    nbits = received.size // n
    if nbits == 0:
        raise ValueError("signal reçu trop court")
    t = np.arange(nbits * n) / sampling_rate
    mixed = received[: nbits * n] * np.cos(2 * np.pi * carrier_freq * t)
    stats = mixed.reshape(nbits, n).sum(axis=1) / sampling_rate  # intégrale sur Tb
    return (stats > 0).astype(int), stats


def ber_theory(ebn0_db):
    """TEB théorique BPSK sur canal AWGN."""
    ebn0 = 10 ** (np.asarray(ebn0_db, dtype=float) / 10)
    return 0.5 * np.vectorize(math.erfc)(np.sqrt(ebn0))


def simulate_ber(ebn0_db_list, nbits=20000, carrier_freq=10e3, sampling_rate=100e3,
                 duration=1e-3, seed=0):
    """Estime le TEB par Monte-Carlo (simulation vectorisée au niveau bit)."""
    rng = np.random.default_rng(seed)
    results = []
    for ebn0_db in ebn0_db_list:
        bits = rng.integers(0, 2, nbits)
        t, tx = bpsk_modulation(bits, carrier_freq, sampling_rate, duration)
        rx = add_awgn(tx, ebn0_db, sampling_rate, duration, rng)
        decoded, _ = bpsk_demodulation(rx, carrier_freq, sampling_rate, duration)
        results.append(np.mean(decoded != bits))
    return np.array(results)


def parse_bits(text):
    if not text or set(text) - {"0", "1"}:
        raise argparse.ArgumentTypeError("--bits doit être une chaîne de 0 et de 1")
    return [int(c) for c in text]


def main():
    p = argparse.ArgumentParser(description="Simulation BPSK (modulation, AWGN, démodulation, TEB)")
    p.add_argument("--bits", type=parse_bits, default="01011010", help="séquence de bits (ex. 01011010)")
    p.add_argument("--fc", type=float, default=10e3, help="fréquence porteuse (Hz)")
    p.add_argument("--fs", type=float, default=100e3, help="fréquence d'échantillonnage (Hz)")
    p.add_argument("--tb", type=float, default=1e-3, help="durée d'un bit (s)")
    p.add_argument("--ebn0", type=float, default=4.0, help="Eb/N0 pour la démo (dB)")
    p.add_argument("--nbits", type=int, default=20000, help="bits par point de la courbe TEB")
    p.add_argument("--seed", type=int, default=0, help="graine aléatoire")
    p.add_argument("--save", metavar="DOSSIER", help="enregistre les figures au lieu de les afficher")
    args = p.parse_args()
    if isinstance(args.bits, str):
        args.bits = parse_bits(args.bits)

    import matplotlib
    if args.save:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    rng = np.random.default_rng(args.seed)
    bits = np.array(args.bits)
    t, tx = bpsk_modulation(bits, args.fc, args.fs, args.tb)
    rx = add_awgn(tx, args.ebn0, args.fs, args.tb, rng)
    decoded, stats = bpsk_demodulation(rx, args.fc, args.fs, args.tb)
    errors = int(np.sum(decoded != bits))
    print(f"Bits émis    : {''.join(map(str, bits))}")
    print(f"Bits décodés : {''.join(map(str, decoded))}  ({errors} erreur(s) à Eb/N0 = {args.ebn0} dB)")

    # Figure 1 : chaîne de transmission
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    axes[0].step(np.arange(bits.size + 1) * args.tb, np.append(bits, bits[-1]), where="post")
    axes[0].set(title="Bits émis", ylabel="Bit", yticks=[0, 1])
    axes[1].plot(t, tx)
    axes[1].set(title="Signal BPSK modulé", ylabel="Amplitude")
    axes[2].plot(t, rx, lw=0.6)
    axes[2].set(title=f"Signal bruité (Eb/N0 = {args.ebn0} dB)", xlabel="Temps (s)", ylabel="Amplitude")
    for ax in axes:
        ax.grid(True)
    fig.tight_layout()

    # Figure 2 : constellation (statistiques de décision normalisées)
    fig2, ax = plt.subplots(figsize=(6, 3))
    ref = args.tb / 2
    ax.scatter(stats / ref, np.zeros_like(stats), c=np.where(bits == 1, "tab:blue", "tab:red"))
    ax.axvline(0, color="k", lw=0.8)
    ax.set(title="Constellation BPSK (rouge = 0, bleu = 1)", xlabel="Statistique de décision normalisée", yticks=[])
    ax.grid(True)
    fig2.tight_layout()

    # Figure 3 : TEB simulé vs théorique
    ebn0s = np.arange(0, 11)
    sim = simulate_ber(ebn0s, args.nbits, args.fc, args.fs, args.tb, args.seed)
    fig3, ax = plt.subplots(figsize=(7, 5))
    ax.semilogy(ebn0s, ber_theory(ebn0s), "k-", label="Théorie 0.5·erfc(√(Eb/N0))")
    floor = 1 / (2 * args.nbits)
    ax.semilogy(ebn0s, np.maximum(sim, floor), "o", label=f"Simulation ({args.nbits} bits/point)")
    ax.set(title="TEB de la BPSK sur canal AWGN", xlabel="Eb/N0 (dB)", ylabel="TEB")
    ax.grid(True, which="both")
    ax.legend()
    fig3.tight_layout()

    if args.save:
        os.makedirs(args.save, exist_ok=True)
        for name, f in (("chaine.png", fig), ("constellation.png", fig2), ("teb.png", fig3)):
            f.savefig(os.path.join(args.save, name), dpi=120)
        print(f"Figures enregistrées dans {args.save}/")
    else:
        plt.show()


if __name__ == "__main__":
    main()
