import numpy as np
import pytest

from modulationBPSK import (add_awgn, ber_theory, bpsk_demodulation,
                            bpsk_modulation, simulate_ber)

FC, FS, TB = 10e3, 100e3, 1e-3


def test_noiseless_roundtrip():
    bits = np.random.default_rng(1).integers(0, 2, 200)
    _, tx = bpsk_modulation(bits, FC, FS, TB)
    decoded, _ = bpsk_demodulation(tx, FC, FS, TB)
    assert np.array_equal(decoded, bits)


def test_phase_inversion_and_length():
    t, tx = bpsk_modulation([1, 0], FC, FS, TB)
    n = int(FS * TB)
    assert len(t) == len(tx) == 2 * n
    assert np.allclose(tx[:n], -tx[n:])


def test_invalid_inputs():
    with pytest.raises(ValueError):
        bpsk_modulation([0, 2], FC, FS, TB)
    with pytest.raises(ValueError):
        bpsk_modulation([0, 1], 60e3, FS, TB)


def test_ber_matches_theory():
    ebn0 = [0, 4]
    sim = simulate_ber(ebn0, nbits=20000, seed=3)
    assert np.allclose(sim, ber_theory(ebn0), rtol=0.2)


def test_noise_power():
    sig = np.zeros(200000)
    noisy = add_awgn(sig, 0, FS, TB, np.random.default_rng(0))
    assert noisy.var() == pytest.approx((TB / 2) * FS / 2, rel=0.02)
