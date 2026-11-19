
import pandas as pd

from src import wilayah as W
from src.laporan import ROOT, catat, tabel_md, tulis
from src.silver import deret


def hitung_profil(silver):
    """Menghitung statistik dasar setiap seri."""
    lab = deret.berlabel(silver)

    if lab.empty:
        return pd.DataFrame()

    hasil = (
        lab.groupby("seri_kode")
        .agg(
            jumlah_data=("nilai", "count"),
            jumlah_wilayah=("wilayah_kode", "nunique"),
            jumlah_periode=("periode", "nunique"),
            minimum=("nilai", "min"),
            maksimum=("nilai", "max"),
            rata_rata=("nilai", "mean"),
            median=("nilai", "median"),
            standar_deviasi=("nilai", "std"),
        )
        .reset_index()
    )

    return hasil.round(3)


def hitung_profil_wilayah(silver):
    """Menghitung statistik nilai setiap provinsi pada masing-masing seri."""
    lab = deret.berlabel(silver)

    if lab.empty:
        return pd.DataFrame()

    prov = lab[lab["wilayah_kode"] != W.INDONESIA].copy()

    hasil = (
        prov.groupby(["seri_kode", "wilayah_kode"])
        .agg(
            jumlah_periode=("nilai", "count"),
            rata_rata=("nilai", "mean"),
            median=("nilai", "median"),
            minimum=("nilai", "min"),
            maksimum=("nilai", "max"),
        )
        .reset_index()
    )

    hasil["nama_wilayah"] = hasil["wilayah_kode"].map(W.NAMA)
    return hasil.round(3)



def tandai_struktural(observasi):
    """
    Mengidentifikasi observasi yang menyimpang berdasarkan IQR
    dan menandai apakah penyimpangan provinsi terjadi berulang.
    """
    if observasi.empty:
        hasil = observasi.copy()
        hasil["berulang"] = False
        hasil["arah"] = "normal"
        return hasil

    lab = observasi.copy()
    lab["_arah_simpangan"] = "normal"

    # Menghitung batas IQR untuk setiap seri dan periode.
    for _, indeks in lab.groupby(
        ["seri_kode", "periode"]
    ).groups.items():

        nilai = lab.loc[indeks, "nilai"]

        q1 = nilai.quantile(0.25)
        q3 = nilai.quantile(0.75)
        iqr = q3 - q1

        batas_bawah = q1 - 1.5 * iqr
        batas_atas = q3 + 1.5 * iqr

        lab.loc[indeks[nilai < batas_bawah], "_arah_simpangan"] = "rendah"
        lab.loc[indeks[nilai > batas_atas], "_arah_simpangan"] = "tinggi"

    # Menghitung frekuensi penyimpangan setiap provinsi.
    ringkasan = (
        lab.assign(
            _menyimpang=lab["_arah_simpangan"] != "normal"
        )
        .groupby(["seri_kode", "wilayah_kode"])
        .agg(
            jumlah_periode=("periode", "nunique"),
            jumlah_simpangan=("_menyimpang", "sum"),
        )
        .reset_index()
    )

    ringkasan["berulang"] = (
        ringkasan["jumlah_simpangan"] /
        ringkasan["jumlah_periode"] > 0.5
    )

    hasil = lab.merge(
        ringkasan[["seri_kode", "wilayah_kode", "berulang"]],
        on=["seri_kode", "wilayah_kode"],
        how="left",
    )

    # Pertahankan hanya observasi yang benar-benar menyimpang.
    hasil = hasil[
        hasil["_arah_simpangan"] != "normal"
    ].copy()

    # Arah menunjukkan penyimpangan pada periode tersebut.
    hasil["arah"] = hasil["_arah_simpangan"]
    hasil["nama_wilayah"] = hasil["wilayah_kode"].map(W.NAMA)

    return hasil.drop(columns=["_arah_simpangan"])


def jalankan(silver):
    """Menjalankan profiling dan menghasilkan calon anomali."""
    profil_seri = hitung_profil(silver)
    profil_wilayah = hitung_profil_wilayah(silver)

    # Calon anomali harus tetap memiliki seri, wilayah, periode, dan nilai.
    lab = deret.berlabel(silver)
    provinsi = lab[lab["wilayah_kode"] != W.INDONESIA].copy()
    calon = tandai_struktural(provinsi)

    folder = ROOT / "reports"
    folder.mkdir(parents=True, exist_ok=True)

    profil_seri.to_csv(folder / "profil-seri.csv", index=False)
    profil_wilayah.to_csv(folder / "profil-wilayah.csv", index=False)
    calon.to_csv(folder / "calon-anomali.csv", index=False)

    catat(
        jumlah_seri_profil=len(profil_seri),
        jumlah_provinsi_profil=len(profil_wilayah),
        calon_struktural=(
            calon.loc[
                calon["berulang"],
                ["seri_kode", "wilayah_kode"]
            ].drop_duplicates().shape[0]
            if len(calon) else 0
        ),
    )

    tulis(
        "profil.md",
        "\n\n".join([
            "# Profil Data Silver",
            "## Statistik setiap seri",
            tabel_md(profil_seri),
            "## Statistik setiap provinsi",
            tabel_md(profil_wilayah),
            "## Calon perbedaan struktural",
            tabel_md(calon[calon["berulang"]]) if len(calon) else "Tidak ada.",
            "Penandaan ini bersifat statistik dan belum membuktikan adanya kesalahan data."
        ])
    )

    return calon
