"""Tahap 5 (tugas #22): simpan Silver dan Gold ke SQLite dengan DDL berkunci primer.

    python -m src.gold.penyimpanan        # muat ulang dari Parquet yang sudah ada

Basis data dibangun ulang dari nol setiap kali `python pipeline.py` dijalankan:
DDL dibaca dari src/gold/skema.sql, setiap tabel diisi dari DataFrame yang juga ditulis ke
Parquet, lalu jumlah baris di SQL dicocokkan dengan jumlah baris Parquet. Bila ada yang tidak
cocok (atau kolom DataFrame berbeda dari DDL), pipeline berhenti.

Respons JSON mentah dari data/raw ikut disimpan utuh di tabel `mentah_dokumen` sebagai
pembanding pendekatan dokumen.
"""
import json
import sqlite3
from pathlib import Path

import pandas as pd

from src.common.manifest import RAW, baca
from src.laporan import ROOT

DDL = Path(__file__).with_name("skema.sql")
DB = ROOT / "data" / "gold" / "gold.sqlite"
SILVER = ROOT / "data" / "silver" / "silver.parquet"
GOLD = ROOT / "data" / "gold"

# Tabel SQL -> berkas Parquet yang menjadi acuan jumlah baris.
PARQUET = {
    "silver": SILVER,
    "observasi_terpilih": GOLD / "observasi_terpilih.parquet",
    "grid_kelengkapan": GOLD / "grid_kelengkapan.parquet",
    "panel_provinsi": GOLD / "panel_provinsi.parquet",
    "panel_provinsi_lebar": GOLD / "panel_provinsi_lebar.parquet",
    "nasional": GOLD / "nasional.parquet",
    "rekonsiliasi_nasional": GOLD / "rekonsiliasi_nasional.parquet",
}


def _kolom_ddl(conn, tabel):
    return [baris[1] for baris in conn.execute(f"PRAGMA table_info({tabel})")]


def _ke_baris(df, kolom):
    """DataFrame -> tuple Python murni: NaN/NA -> None, bool -> 0/1, numpy -> Python."""
    data = df[kolom].astype(object).where(df[kolom].notna(), None)
    for nama in kolom:
        if pd.api.types.is_bool_dtype(df[nama]):
            data[nama] = df[nama].astype(int)
    hasil = []
    for baris in data.itertuples(index=False, name=None):
        hasil.append(tuple(v.item() if hasattr(v, "item") else v for v in baris))
    return hasil


def _muat_tabel(conn, tabel, df):
    kolom = _kolom_ddl(conn, tabel)
    if not kolom:
        raise ValueError(f"Tabel {tabel} tidak ada di {DDL.name}.")
    lebih = sorted(set(df.columns) - set(kolom))
    kurang = sorted(set(kolom) - set(df.columns))
    if lebih or kurang:
        raise ValueError(
            f"Kolom {tabel} tidak cocok dengan DDL. Tidak ada di DDL: {lebih}; "
            f"tidak ada di DataFrame: {kurang}. Perbarui src/gold/skema.sql."
        )
    tanda = ", ".join("?" for _ in kolom)
    conn.executemany(
        f"INSERT INTO {tabel} ({', '.join(kolom)}) VALUES ({tanda})",
        _ke_baris(df, kolom),
    )


def _muat_dokumen(conn, raw=RAW):
    """Simpan setiap berkas JSON mentah utuh sebagai satu dokumen."""
    jumlah = 0
    for berkas, sha in sorted(baca(Path(raw)).items()):
        if not berkas.endswith(".json"):
            continue
        jalur = Path(raw) / berkas
        isi = jalur.read_text(encoding="utf-8")
        json.loads(isi)  # gagal keras bila bukan JSON sah
        sumber, snapshot = berkas.split("/")[:2]
        conn.execute(
            "INSERT INTO mentah_dokumen VALUES (?, ?, ?, ?, ?, ?)",
            (berkas, sha, sumber, snapshot, jalur.stat().st_size, isi),
        )
        jumlah += 1
    return jumlah


def simpan(tabel, db=DB, raw=RAW):
    """
    Bangun ulang basis data dari DDL dan muat semua tabel.

    `tabel` = {nama_tabel_sql: DataFrame}. Mengembalikan DataFrame ringkasan jumlah baris
    (SQL vs Parquet) yang juga ditulis ke reports/penyimpanan-sql.md.
    """
    db = Path(db)
    db.parent.mkdir(parents=True, exist_ok=True)
    if db.exists():
        db.unlink()

    conn = sqlite3.connect(db)
    try:
        conn.executescript(DDL.read_text(encoding="utf-8"))
        with conn:
            n_dokumen = _muat_dokumen(conn, raw) if Path(raw).exists() else 0
            for nama, df in tabel.items():
                _muat_tabel(conn, nama, df)

        ringkasan = []
        for nama in tabel:
            n_sql = conn.execute(f"SELECT COUNT(*) FROM {nama}").fetchone()[0]
            n_parquet = len(pd.read_parquet(PARQUET[nama])) if nama in PARQUET else None
            kunci = [b[1] for b in sorted(conn.execute(f"PRAGMA table_info({nama})"), key=lambda b: b[5]) if b[5] > 0]
            ringkasan.append({
                "tabel": nama,
                "kunci_primer": ", ".join(kunci),
                "baris_sql": n_sql,
                "baris_parquet": n_parquet,
                "cocok": n_sql == n_parquet,
            })
        ringkasan.append({
            "tabel": "mentah_dokumen",
            "kunci_primer": "_berkas_raw",
            "baris_sql": n_dokumen,
            "baris_parquet": None,
            "cocok": None,
        })
    finally:
        conn.close()

    ringkasan = pd.DataFrame(ringkasan)
    tidak_cocok = ringkasan[ringkasan["cocok"].eq(False)]
    if not tidak_cocok.empty:
        raise ValueError(
            "Jumlah baris SQL tidak sama dengan Parquet:\n" + tidak_cocok.to_string(index=False)
        )

    _tulis_laporan(ringkasan, db)
    print(f"SQL: {len(tabel)} tabel + {n_dokumen} dokumen JSON mentah -> {db}")
    return ringkasan


def _tulis_laporan(ringkasan, db):
    baris = [
        "# Penyimpanan SQL — hasil pemuatan terakhir",
        "",
        "Dibuat otomatis oleh `src/gold/penyimpanan.py` saat `python pipeline.py` dijalankan.",
        f"Basis data: `{Path(db).relative_to(ROOT).as_posix()}` (tidak di-commit); DDL: `src/gold/skema.sql`.",
        "",
        "| Tabel | Kunci primer | Baris SQL | Baris Parquet | Cocok |",
        "|---|---|---:|---:|---|",
    ]
    for r in ringkasan.itertuples(index=False):
        parquet = "—" if pd.isna(r.baris_parquet) else f"{int(r.baris_parquet):,}"
        cocok = "—" if r.cocok is None or pd.isna(r.cocok) else ("ya" if r.cocok else "TIDAK")
        baris.append(f"| `{r.tabel}` | {r.kunci_primer} | {r.baris_sql:,} | {parquet} | {cocok} |")
    baris.append("")
    tujuan = ROOT / "reports" / "penyimpanan-sql.md"
    tujuan.write_text("\n".join(baris), encoding="utf-8")


def muat_dari_parquet(db=DB):
    """Bangun ulang basis data dari Parquet yang sudah ada (tanpa menjalankan pipeline)."""
    return simpan({nama: pd.read_parquet(jalur) for nama, jalur in PARQUET.items()}, db)


if __name__ == "__main__":
    print(muat_dari_parquet().to_string(index=False))
