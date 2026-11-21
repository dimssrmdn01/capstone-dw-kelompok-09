"""Tahap 6: Integrasi dan rekonsiliasi pembanding nasional dari lapis Silver (Kelompok 9)."""
from pathlib import Path
import pandas as pd


def buat_tabel_nasional_dari_silver(df_silver: pd.DataFrame) -> pd.DataFrame:
    """Menyaring observasi nasional (wilayah_kode == 9999) dari Silver menjadi tabel periode x seri."""
    nasional = df_silver[
        (df_silver["wilayah_kode"] == 9999) & (df_silver["rincian"] == "total")
    ].copy()
    nasional["periode"] = nasional["periode"].astype(str)
    return (
        nasional.pivot_table(
            index="periode",
            columns="seri_kode",
            values="nilai",
            aggfunc="first",
        )
        .sort_index()
    )


def buat_tabel_rekonsiliasi(tabel_nasional: pd.DataFrame) -> pd.DataFrame:
    """Menyusun tabel rekonsiliasi pasangan wajib Kelompok 9 beserta kategori selisih."""
    pasangan = [
        ("var1439 vs SE.PRE.ENRR", "var1439", "SE.PRE.ENRR", "Definisi berbeda"),
        ("var1221 vs IT.NET.USER.ZS", "var1221", "IT.NET.USER.ZS", "Definisi berbeda"),
    ]
    hasil = []
    for label, utama, pembanding, kategori in pasangan:
        if utama not in tabel_nasional.columns or pembanding not in tabel_nasional.columns:
            continue
        sub = tabel_nasional[[utama, pembanding]].dropna().reset_index()
        for _, r in sub.iterrows():
            hasil.append({
                "pasangan": label,
                "periode": r["periode"],
                "seri_utama": utama,
                "nilai_seri_utama": float(r[utama]),
                "seri_pembanding": pembanding,
                "nilai_pembanding": float(r[pembanding]),
                "selisih": round(float(r[utama]) - float(r[pembanding]), 4),
                "kategori_penjelasan": kategori,
            })
    return pd.DataFrame(hasil)


if __name__ == "__main__":
    silver_path = Path("data/silver/silver.parquet")
    if silver_path.exists():
        df_s = pd.read_parquet(silver_path)
        tabel = buat_tabel_nasional_dari_silver(df_s)
        print(buat_tabel_rekonsiliasi(tabel).to_string(index=False))
    else:
        print("OK: Modul integrasi siap dipanggil dari src/gold/__init__.py setelah silver.parquet tersedia.")
