"""Tahap 6: integrasi dan rekonsiliasi pembanding nasional."""

import pandas as pd
from src import konfigurasi as K


def buat_tabel_nasional_dari_silver(df_silver):
    nasional = df_silver[
        (df_silver["wilayah_kode"] == 9999)
        & (df_silver["rincian"] == "total")
    ].copy()

    nasional["periode"] = nasional["periode"].astype(str)

    kunci = ["seri_kode", "wilayah_kode", "periode"]
    duplikat = nasional.duplicated(kunci, keep=False)
    if duplikat.any():
        raise ValueError(
            "Tabel nasional masih memiliki kunci ganda setelah seleksi:\n"
            + nasional.loc[duplikat, kunci].head(10).to_string(index=False)
        )

    return (
        nasional.pivot(
            index="periode",
            columns="seri_kode",
            values="nilai",
        )
        .sort_index()
    )


def buat_tabel_rekonsiliasi(tabel_nasional):
    hasil = []

    for pasangan in K.PASANGAN:
        utama = pasangan["utama"]

        if utama not in tabel_nasional.columns:
            continue

        for pembanding, rincian in pasangan["pembanding"]:
            if pembanding not in tabel_nasional.columns:
                continue

            sub = tabel_nasional[[utama, pembanding]].dropna()

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
                        nilai_utama - nilai_pembanding, 4
                    ),
                    "alasan_perbandingan": pasangan["alasan_rincian"],
                })

    return pd.DataFrame(hasil)


if __name__ == "__main__":
    from pathlib import Path

    lokasi = Path("data/silver/silver.parquet")
    if lokasi.exists():
        df = pd.read_parquet(lokasi)
        nasional = buat_tabel_nasional_dari_silver(df)
        print(buat_tabel_rekonsiliasi(nasional).to_string(index=False))
