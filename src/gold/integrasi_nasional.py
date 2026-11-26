
"""Tahap 6: integrasi dan rekonsiliasi pembanding nasional."""

import pandas as pd
from src import konfigurasi as K


def buat_tabel_nasional_dari_silver(df_silver):
    kolom_wajib = [
        "wilayah_kode",
        "rincian",
        "periode",
        "seri_kode",
        "nilai",
    ]

    for kolom in kolom_wajib:
        if kolom not in df_silver.columns:
            raise ValueError(
                f"Kolom wajib tidak ditemukan: {kolom}"
            )

    nasional = df_silver[
        (df_silver["wilayah_kode"] == 9999)
        & (
            df_silver["rincian"]
            .astype(str)
            .str.strip()
            .str.lower()
            == "total"
        )
    ].copy()

    kolom_tabel = [
        "periode",
        "seri_kode",
        "wilayah_kode",
        "nilai",
    ]

    kolom_opsional = [
        "nama_wilayah",
        "satuan",
        "sumber",
        "rincian",
        "_berkas_raw",
        "_sha256_raw",
    ]

    for kolom in kolom_opsional:
        if kolom in nasional.columns:
            kolom_tabel.append(kolom)

    nasional = nasional[kolom_tabel].copy()
    nasional["periode"] = nasional["periode"].astype(str)

    kunci = [
        "seri_kode",
        "wilayah_kode",
        "periode",
    ]

    duplikat = nasional.duplicated(kunci, keep=False)

    if duplikat.any():
        raise ValueError(
            "Tabel nasional memiliki kunci ganda:\n"
            + nasional.loc[duplikat, kunci]
            .head(10)
            .to_string(index=False)
        )

    return nasional.sort_values(
        ["seri_kode", "periode"]
    ).reset_index(drop=True)


def buat_tabel_rekonsiliasi(tabel_nasional):
    hasil = []

    lebar = tabel_nasional.pivot(
        index="periode",
        columns="seri_kode",
        values="nilai",
    ).sort_index()

    for pasangan in K.PASANGAN:
        utama = pasangan["utama"]

        if utama not in lebar.columns:
            continue

        for pembanding, rincian in pasangan["pembanding"]:
            if pembanding not in lebar.columns:
                continue

            sub = lebar[
                [utama, pembanding]
            ].dropna()

            for periode, baris in sub.iterrows():
                nilai_utama = float(baris[utama])
                nilai_pembanding = float(baris[pembanding])

                hasil.append({
                    "pasangan": pasangan["id"],
                    "periode": str(periode),
                    "seri_utama": utama,
                    "nilai_seri_utama": nilai_utama,
                    "seri_pembanding": pembanding,
                    "rincian_pembanding": rincian,
                    "nilai_pembanding": nilai_pembanding,
                    "selisih": round(
                        nilai_utama - nilai_pembanding,
                        4,
                    ),
                    "alasan_perbandingan": (
                        pasangan["alasan_rincian"]
                    ),
                })

    return pd.DataFrame(hasil)


if __name__ == "__main__":
    from pathlib import Path

    lokasi = Path("data/silver/silver.parquet")

    if lokasi.exists():
        df = pd.read_parquet(lokasi)

        nasional = buat_tabel_nasional_dari_silver(df)

        print("TABEL NASIONAL")
        print(nasional.head().to_string(index=False))

        rekonsiliasi = buat_tabel_rekonsiliasi(nasional)

        print("\nTABEL REKONSILIASI")
        print(rekonsiliasi.to_string(index=False))
