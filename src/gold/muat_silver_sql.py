"""Persiapan Tahap 5: Skema DDL & pemuat tabel Silver ke SQLite (data/gold/silver_stage.sqlite)."""
from pathlib import Path
import sqlite3
import pandas as pd

DDL_SILVER = """
CREATE TABLE IF NOT EXISTS silver_observasi (
    indikator_id TEXT NOT NULL,
    wilayah_kode TEXT NOT NULL,
    periode INTEGER NOT NULL,
    nilai REAL,
    satuan TEXT,
    sumber TEXT NOT NULL,
    _berkas_raw TEXT,
    _sha256_raw TEXT,
    PRIMARY KEY (indikator_id, wilayah_kode, periode)
);
"""

CATATAN_BASIS_DATA = """
Alasan Pemilihan SQLite & Perbandingan dengan Dokumen JSON Mentah:
1. SQLite dipilih karena serverless (berkas tunggal portabel), mendukung tipe data eksplisit (TEXT, INTEGER, REAL), serta menegakkan keunikan kunci primer komposit (indikator_id, wilayah_kode, periode) untuk mencegah duplikasi lintas-snapshot.
2. Dibandingkan menyimpan respons JSON mentah sebagai dokumen (yang struktur lariknya bersarang/heterogen antar-API BPS dan WDI serta lambat untuk kueri agregasi lintas-indikator), tabel relasional SQL mempercepat filter wilayah/periode dan validasi integritas skema.
"""

def muat_silver_ke_sqlite(
    silver_path: Path = Path("data/silver/silver.parquet"),
    db_path: Path = Path("data/gold/silver_stage.sqlite"),
) -> int:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.executescript(DDL_SILVER)
        if not silver_path.exists():
            print(f"OK (DDL siap): {db_path} dibuat; menunggu {silver_path} untuk pemuatan baris.")
            return 0
        df = pd.read_parquet(silver_path)
        kolom = ["indikator_id", "wilayah_kode", "periode", "nilai", "satuan", "sumber", "_berkas_raw", "_sha256_raw"]
        tersedia = [c for c in kolom if c in df.columns]
        df_muat = df[tersedia].drop_duplicates(subset=["indikator_id", "wilayah_kode", "periode"])
        conn.execute("DELETE FROM silver_observasi;")
        df_muat.to_sql("silver_observasi", conn, if_exists="append", index=False)
        jml = conn.execute("SELECT COUNT(*) FROM silver_observasi;").fetchone()[0]
        print(f"OK: {jml} baris Silver berhasil dimuat ke {db_path}")
        return jml

if __name__ == "__main__":
    muat_silver_ke_sqlite()
