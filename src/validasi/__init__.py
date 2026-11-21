"""Tahap 8 — Validasi dan dokumentasi (pertemuan XIV–XV). Milik tim.

Tulis skema validasi Silver dan Gold (pandera atau Great Expectations): rentang nilai per satuan,
kelengkapan wilayah, keunikan kunci, konsistensi provinsi vs nasional bila relevan. Laporan
validasi ditulis ke reports/validasi.md. Data dictionary di docs/data-dictionary.md.
"""


def jalankan(silver, gold):
    raise NotImplementedError("Tahap 8: skema pandera/GE untuk Silver dan Gold")



import pandas as pd
from pathlib import Path


def validasi_silver(df):
    hasil = {}

    # 1. Validasi kolom wajib
    kolom_wajib = [
        "sumber", "seri_kode", "wilayah_kode",
        "periode", "jenis_periode", "rincian",
        "nilai", "satuan", "_berkas_raw"
    ]

    hasil["kolom_wajib"] = all(
        kolom in df.columns for kolom in kolom_wajib
    )

    if not hasil["kolom_wajib"]:
        return hasil

    # 2. Validasi nilai persentase
    seri_persen = ["var1447", "var1451", "var1221"]
    data_persen = df[df["seri_kode"].isin(seri_persen)]

    hasil["rentang_persen"] = bool(
        data_persen["nilai"].between(0, 100).all()
    )

    # 3. Validasi APK PAUD
    apk = df[df["seri_kode"] == "var1439"]

    hasil["apk_nonnegatif"] = bool(
        (apk["nilai"] >= 0).all()
    )

    # 4. Validasi keunikan data
    kunci = [
        "sumber", "seri_kode", "wilayah_kode",
        "periode", "jenis_periode", "rincian",
        "_berkas_raw"
    ]

    hasil["keunikan_silver"] = not df.duplicated(
        subset=kunci
    ).any()

    # 5. Validasi konsistensi satuan
    jumlah_satuan = df.groupby("seri_kode")["satuan"].nunique()

    hasil["konsistensi_satuan"] = bool(
        (jumlah_satuan <= 1).all()
    )

    # Tampilkan hasil
    print("\n=== HASIL VALIDASI SILVER ===")

    for aturan, status in hasil.items():
        print(f"{aturan}: {'LOLOS' if status else 'GAGAL'}")

    if not all(hasil.values()):
        raise ValueError("Validasi Silver gagal!")

    print("\nSemua validasi Silver berhasil!")

    return hasil


def jalankan():
    lokasi = Path("data/silver/silver.parquet")

    df = pd.read_parquet(lokasi)

    print(f"\nData Silver: {len(df)} baris")

    return validasi_silver(df)
