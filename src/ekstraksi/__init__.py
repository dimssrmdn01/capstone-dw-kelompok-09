"""Tahap 1 — Ekstraksi data mentah."""

from src.ekstraksi import bps_csv


def jalankan():
    """Kembalikan data mentah dalam bentuk dictionary."""
    return {
        "bps_csv": bps_csv.baca(),
    }
