"""Pembaca data CSV BPS dari data/raw."""

from pathlib import Path

import pandas as pd

from src.common.manifest import RAW, sha256_raw


def baca():
    """Baca seluruh CSV data BPS dan gabungkan dengan informasi asal berkas."""
    folder = RAW / "bps"
    bagian = []

    for path in sorted(folder.glob("*/sdg*.csv")):
        relatif = path.relative_to(RAW).as_posix()

        data = pd.read_csv(path, dtype={"var_id": "string", "wilayah_id": "string"})

        data["_berkas_raw"] = relatif
        data["_sha256_raw"] = sha256_raw(relatif)

        bagian.append(data)

    if not bagian:
        raise FileNotFoundError("Tidak ditemukan CSV indikator BPS di data/raw/bps.")

    hasil = pd.concat(bagian, ignore_index=True)

    return hasil