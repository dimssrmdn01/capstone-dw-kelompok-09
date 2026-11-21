from pathlib import Path

import pandas as pd

from src.common.manifest import RAW, sha256_raw

BERKAS_CSV = (
    "bps/2026-10-17/sdg4_4_4_1_a_v1451.csv",
    "bps/2026-10-17/sdg4_4_4_1_b_v1447.csv",
    "bps/2026-10-17/sdg4_apk_paud.csv",
    "bps/2026-10-17/sdg5_5_b_1_v1221.csv",
    "bps/2026-10-20/sdg5_5_b_1_v1221.csv",
)

KOLOM_MINIMAL = {
    "var_id", "wilayah_id", "wilayah", "turvar_id", "turvar",
    "tahun_id", "tahun", "periode_id", "periode", "nilai", "satuan",
}


def baca_satu_csv(berkas: str, raw: Path = RAW) -> pd.DataFrame:
    raw = Path(raw)
    jalur = raw / berkas
    if not jalur.is_file():
        raise FileNotFoundError(f"Berkas CSV BPS tidak ditemukan: {jalur}")

    # Pemisah kolom koma, desimal titik, dan encoding UTF-8 (dengan BOM bila ada).
    df = pd.read_csv(
        jalur,
        sep=",",
        decimal=".",
        encoding="utf-8-sig",
        low_memory=False,
        on_bad_lines="error",
    )

    kolom_hilang = KOLOM_MINIMAL - set(df.columns)
    if kolom_hilang:
        raise ValueError(
            f"Kolom wajib tidak ditemukan pada {berkas}: {sorted(kolom_hilang)}"
        )

    hasil = df.copy()
    hasil["_berkas_raw"] = berkas
    hasil["_sha256_raw"] = sha256_raw(berkas, raw=raw)
    return hasil


def baca_semua_csv(raw: Path = RAW) -> dict[str, pd.DataFrame]:
   
    return {berkas: baca_satu_csv(berkas, raw=raw) for berkas in BERKAS_CSV}



def main() -> None:
    
    print("=" * 88)
    print("PEMBACA CSV BPS - KASUS 09 / KELOMPOK 9")
    print("=" * 88)
    tabel_per_berkas = baca_semua_csv()
    for berkas, df in tabel_per_berkas.items():
        print(f"\nBerkas       : {berkas}")
        print(f"Jumlah baris : {len(df):,}")
        print(f"Jumlah kolom : {len(df.columns)}")
        print("5 DATA TERATAS:")
        with pd.option_context("display.max_columns", None, "display.width", 220, "display.max_colwidth", 30):
            print(df.head(5).to_string(index=False))
    total = sum(len(df) for df in tabel_per_berkas.values())
    print(f"\nTOTAL: {total:,} baris dari {len(tabel_per_berkas)} file CSV")


if __name__ == "__main__":
    main()
