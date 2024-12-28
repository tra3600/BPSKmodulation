import numpy as np
import matplotlib.pyplot as plt

def bpsk_modulation(bits, carrier_freq, sampling_rate, duration):
    """
    Simule la modulation BPSK pour une séquence de bits donnée.

    :param bits: Séquence de bits à moduler.
    :param carrier_freq: Fréquence de la porteuse en Hz.
    :param sampling_rate: Taux d'échantillonnage en Hz.
    :param duration: Durée de chaque bit en secondes.
    :return: Signal modulé BPSK.
    """
    t = np.arange(0, duration * len(bits), 1 / sampling_rate)
    carrier = np.cos(2 * np.pi * carrier_freq * t)
    signal = np.zeros(len(t))

    for i, bit in enumerate(bits):
        if bit == 0:
            signal[i * int(sampling_rate * duration):(i + 1) * int(sampling_rate * duration)] = -carrier[i * int(sampling_rate * duration):(i + 1) * int(sampling_rate * duration)]
        else:
            signal[i * int(sampling_rate * duration):(i + 1) * int(sampling_rate * duration)] = carrier[i * int(sampling_rate * duration):(i + 1) * int(sampling_rate * duration)]

    return t, signal

def main():
    # Paramètres de la simulation
    bits = [0, 1, 0, 1, 1, 0, 1, 0]  # Séquence de bits à moduler
    carrier_freq = 10e3  # Fréquence de la porteuse en Hz
    sampling_rate = 100e3  # Taux d'échantillonnage en Hz
    duration = 0.001  # Durée de chaque bit en secondes

    # Moduler le signal
    t, modulated_signal = bpsk_modulation(bits, carrier_freq, sampling_rate, duration)

    # Afficher le signal modulé
    plt.figure(figsize=(10, 4))
    plt.plot(t, modulated_signal)
    plt.title('Signal Modulé BPSK')
    plt.xlabel('Temps (s)')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()