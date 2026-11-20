"""Tahap 1: satukan semua pembaca menjadi satu tabel mentah ber-lineage."""

import json
import re
from pathlib import Path

import pandas as pd

from src.common.manifest import RAW, baca as baca_manifest, periksa, sha256_raw
from .bps_csv import baca_semua_csv
from .bps_json import baca_semua_json
from .wdi import baca_paket_wdi

BERKAS_METADATA_BPS = (
    "bps/2026-10-17/manifest_asal.json",
    "bps/2026-10-20/manifest_asal.json",
)
KODE_APK_PAUD = "1439"


def _satuan_apk_paud_dari_katalog(root: Path) -> str:
    """Ambil satuan seri var1439 dari katalog kasus, bukan hardcode nilai."""
    katalog = root / "data" / "KASUS.md"
    if not katalog.is_file():
        raise FileNotFoundError(f"Katalog kasus tidak ditemukan: {katalog}")

    for baris in katalog.read_text(encoding="utf-8").splitlines():
        if not baris.lstrip().startswith("|"):
            continue
        kolom = [bagian.strip().strip("`") for bagian in baris.strip().strip("|").split("|")]
        if len(kolom) >= 5 and kolom[0].lower() == "bps" and kolom[1] == f"var{KODE_APK_PAUD}":
            satuan = kolom[3]
            if satuan:
                return satuan
            raise ValueError(f"Satuan var{KODE_APK_PAUD} kosong di {katalog}")

    raise ValueError(f"Seri BPS var{KODE_APK_PAUD} tidak ditemukan di {katalog}")


def _tetapkan_satuan_khusus(kumpulan: dict[str, pd.DataFrame], satuan: str) -> None:
    """Isi metadata satuan APK PAUD yang kosong; tidak melakukan normalisasi umum."""
    for nama_berkas, df in kumpulan.items():
        if "sdg4_apk_paud" not in nama_berkas:
            continue

        if "var_id" in df.columns:
            mask = pd.to_numeric(df["var_id"], errors="coerce").eq(int(KODE_APK_PAUD))
        else:
            continue

        for kolom in ("satuan", "var_unit"):
            if kolom in df.columns:
                df[kolom] = df[kolom].astype("object")
                kosong = df[kolom].isna() | df[kolom].astype(str).str.strip().eq("")
                df.loc[mask & kosong, kolom] = satuan


def _baca_metadata_bps(raw: Path) -> dict[str, pd.DataFrame]:
    """Baca dua manifest_asal BPS sebagai tabel metadata dengan lineage."""
    hasil = {}
    for berkas in BERKAS_METADATA_BPS:
        jalur = raw / berkas
        if not jalur.is_file():
            raise FileNotFoundError(f"Metadata BPS tidak ditemukan: {jalur}")

        with jalur.open("r", encoding="utf-8-sig") as file:
            metadata = json.load(file)

        tabel_metadata = metadata.get("tabel") if isinstance(metadata, dict) else None
        if not isinstance(tabel_metadata, dict):
            raise ValueError(f"Struktur metadata BPS tidak valid: {berkas}")

        df = pd.DataFrame.from_dict(tabel_metadata, orient="index")
        df.index.name = "nama_tabel"
        df = df.reset_index()
        for kolom in ("sumber", "domain", "diunduh", "skrip"):
            df[kolom] = metadata.get(kolom)

        df["_berkas_raw"] = berkas
        df["_sha256_raw"] = sha256_raw(berkas, raw=raw)
        hasil[berkas] = df

    return hasil


def jalankan(raw: Path = RAW) -> pd.DataFrame:
    """Gabungkan seluruh keluaran pembaca menjadi satu DataFrame mentah ber-lineage."""
    raw = Path(raw)
    root = Path(__file__).resolve().parents[2]

    jumlah_manifest, berkas_tidak_valid = periksa(raw)
    if berkas_tidak_valid:
        raise ValueError(
            "Pemeriksaan SHA256 gagal untuk: " + ", ".join(berkas_tidak_valid)
        )

    manifest = baca_manifest(raw)
    satuan_apk_paud = _satuan_apk_paud_dari_katalog(root)

    hasil_csv = baca_semua_csv(raw=raw)
    hasil_json = baca_semua_json(raw=raw)
    hasil_wdi = baca_paket_wdi(raw=raw)

    # Ketentuan khusus tugas: satuan var1439 diambil dari katalog kasus.
    _tetapkan_satuan_khusus(hasil_csv, satuan_apk_paud)
    _tetapkan_satuan_khusus(hasil_json, satuan_apk_paud)

    hasil_metadata_bps = _baca_metadata_bps(raw)
    kelompok = (
        ("BPS CSV", hasil_csv),
        ("BPS JSON", hasil_json),
        ("WDI", hasil_wdi),
        ("Metadata BPS", hasil_metadata_bps),
    )

    seluruh_tabel = []
    for sumber, hasil in kelompok:
        if not isinstance(hasil, dict):
            raise TypeError(f"Keluaran {sumber} harus berupa dictionary.")

        for nama_berkas, df in hasil.items():
            if not isinstance(df, pd.DataFrame):
                raise TypeError(f"{sumber}/{nama_berkas} bukan DataFrame.")

            kolom_lineage = {"_berkas_raw", "_sha256_raw"}
            if not kolom_lineage.issubset(df.columns):
                raise ValueError(f"Kolom lineage tidak lengkap pada {nama_berkas}.")
            if df[list(kolom_lineage)].isna().any().any():
                raise ValueError(f"Lineage kosong ditemukan pada {nama_berkas}.")

            pasangan = df[["_berkas_raw", "_sha256_raw"]].drop_duplicates()
            for berkas, hash_baris in pasangan.itertuples(index=False, name=None):
                if berkas not in manifest:
                    raise ValueError(f"{berkas} tidak tercatat di MANIFEST.csv.")
                if manifest[berkas] != hash_baris:
                    raise ValueError(f"SHA256 tidak cocok untuk {berkas}.")

            seluruh_tabel.append(df)
            print(f"{sumber:<14} | {nama_berkas} | {len(df):,} baris")

    if not seluruh_tabel:
        raise ValueError("Tidak ada DataFrame hasil pembacaan.")

    tabel_mentah = pd.concat(seluruh_tabel, ignore_index=True, sort=False)

    berkas_terbaca = set(tabel_mentah["_berkas_raw"].astype(str))
    berkas_manifest = set(manifest)
    berkas_terlewat = berkas_manifest - berkas_terbaca
    berkas_tidak_dikenal = berkas_terbaca - berkas_manifest

    if berkas_terlewat or berkas_tidak_dikenal:
        raise ValueError(
            "Cakupan berkas tidak sesuai MANIFEST.csv. "
            f"Terlewat: {sorted(berkas_terlewat)}; "
            f"Tidak dikenal: {sorted(berkas_tidak_dikenal)}"
        )

    print("\nRINGKASAN EKSTRAKSI")
    print(f"Berkas pada MANIFEST.csv : {jumlah_manifest}")
    print(f"Berkas berhasil dibaca   : {len(berkas_terbaca)}")
    print(f"Jumlah DataFrame sumber  : {len(seluruh_tabel)}")
    print(f"Jumlah baris mentah      : {len(tabel_mentah):,}")
    print(f"Jumlah kolom gabungan    : {len(tabel_mentah.columns)}")
    print(f"Berkas terlewat          : {len(berkas_terlewat)}")
    print(f"Satuan APK PAUD dari katalog: {satuan_apk_paud}")
    print("Lineage                  : lengkap")
    print("STATUS EKSTRAKSI: BERHASIL")

    return tabel_mentah