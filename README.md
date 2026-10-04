# BPSKmodulation

Simulation d'une chaîne de transmission numérique **BPSK** (Binary Phase Shift Keying) en Python :

bits → modulation → canal AWGN → démodulation cohérente → bits décodés

## Installation

```
pip install numpy matplotlib
```

## Utilisation

```
python modulationBPSK.py                          # affiche les figures
python modulationBPSK.py --save figures           # enregistre les PNG (sans fenêtre)
python modulationBPSK.py --bits 1011001 --ebn0 6  # séquence et Eb/N0 personnalisés
python modulationBPSK.py --help
```

Le programme affiche les bits émis/décodés et trace :
1. la chaîne (bits, signal modulé, signal bruité) ;
2. la constellation BPSK en sortie du démodulateur ;
3. le taux d'erreur binaire (TEB) simulé comparé à la théorie `Pb = ½·erfc(√(Eb/N0))`.

## Principe

- bit 1 → `+cos(2π·fc·t)`, bit 0 → `−cos(2π·fc·t)` (déphasage de π) ;
- bruit blanc gaussien calibré en Eb/N0 (dB) ;
- démodulation par corrélation avec la porteuse sur chaque durée-bit, décision au signe.

## Fonctions principales

`bpsk_modulation`, `add_awgn`, `bpsk_demodulation`, `ber_theory`, `simulate_ber`.

## Tests

```
pip install pytest
pytest
```
