"""Tahap 4-6: seleksi, pembentukan panel, integrasi nasional, dan penyimpanan Gold."""

import sqlite3
import pandas as pd

from src import konfigurasi as K
from src.laporan import ROOT
from src.silver import grid
from src.gold import seleksi
from src.gold.integrasi_nasional import (
    buat_tabel_nasional_dari_silver,
    buat_tabel_rekonsiliasi,
)


def jalankan(silver):
    folder = ROOT / "data" / "gold"
    folder.mkdir(parents=True, exist_ok=True)

    # 1. Seleksi observasi tahunan rincian total dan bawa penanda anomali.
    observasi, catatan = seleksi.pilih(silver)
    seleksi.catat_keputusan(catatan)

    # 2. Bentuk grid kelengkapan wilayah dan periode.
    grid_lengkap = grid.bentuk_grid(silver, {})

    # 3. Gabungkan observasi terpilih ke grid provinsi.
    kolom_nilai = [
        "seri_kode", "wilayah_kode", "periode", "nilai",
        "satuan", "sumber", "anomaly_flag",
        "kategori_anomali", "tindakan_anomali", "bukti_anomali",
    ]
    nilai = observasi[
        observasi["wilayah_kode"].isin(
            silver.loc[silver["wilayah_kode"] != 9999, "wilayah_kode"].unique()
        )
    ][kolom_nilai].copy()
    nilai["periode"] = nilai["periode"].astype(str)

    panel = grid_lengkap[
        grid_lengkap["tingkat"] == "provinsi"
    ].copy()
    panel["periode"] = panel["periode"].astype(str)

    panel = panel.merge(
        nilai,
        on=["seri_kode", "wilayah_kode", "periode"],
        how="left",
        validate="one_to_one",
    )

    panel["anomaly_flag"] = panel["anomaly_flag"].fillna(False).astype(bool)
    for kolom in ["kategori_anomali", "tindakan_anomali", "bukti_anomali"]:
        panel[kolom] = panel[kolom].fillna("")

    # Nilai hanya tersedia pada sel yang dinyatakan terisi.
    panel.loc[panel["kategori"] != "terisi", "nilai"] = pd.NA

    # 4. Bentuk panel lebar. Kunci sudah unik setelah seleksi.
    panel_lebar = (
        panel.pivot(
            index=["wilayah_kode", "nama_wilayah", "periode"],
            columns="seri_kode",
            values="nilai",
        )
        .reset_index()
    )
    panel_lebar.columns.name = None

    # 5. Bentuk tabel nasional dan rekonsiliasi dari observasi terpilih.
    nasional = buat_tabel_nasional_dari_silver(observasi)
    rekonsiliasi = buat_tabel_rekonsiliasi(nasional)

    # 6. Simpan tabel Gold.
    tabel = {
        "observasi_terpilih": observasi,
        "panel_provinsi": panel,
        "panel_provinsi_lebar": panel_lebar,
        "grid_kelengkapan": grid_lengkap,
        "nasional": nasional.reset_index(),
        "rekonsiliasi_nasional": rekonsiliasi,
    }

    for nama, df in tabel.items():
        df.to_parquet(folder / f"{nama}.parquet", index=False)

    # 7. Simpan seluruh tabel Gold ke SQLite.
    db_path = folder / "gold.sqlite"
    with sqlite3.connect(db_path) as conn:
        for nama, df in tabel.items():
            df.to_sql(nama, conn, if_exists="replace", index=False)

    print(f"Gold: {len(observasi):,} observasi terpilih")
    print(f"Gold: {len(panel):,} sel panel provinsi")
    print(f"Gold: {len(panel_lebar):,} baris panel lebar")
    print(f"Gold: {len(rekonsiliasi):,} baris rekonsiliasi")
    print(f"Gold tersimpan di {folder}")

    return tabel
