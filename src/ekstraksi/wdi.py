import json
from pathlib import Path

import pandas as pd

from src.common.manifest import RAW, sha256_raw

INDIKATOR_WDI = {"SE.PRE.ENRR", "IT.NET.USER.ZS"}

BERKAS_DATA = (
    "wdi/2026-10-20/data/kelompok-02-hal-01.json",
    "wdi/2026-10-20/data/kelompok-03-hal-01.json",
)

BERKAS_SUMBER = "wdi/2026-10-20/metadata/sumber.json"
BERKAS_INDIKATOR_WDI = "wdi/2026-10-20/metadata/sumber2_indikator.json"
BERKAS_INDIKATOR_SDG = "wdi/2026-10-20/metadata/sumber46_indikator.json"


def _baca_json(raw: Path, berkas: str):
   
    jalur = raw / berkas
    if not jalur.is_file():
        raise FileNotFoundError(f"Berkas WDI tidak ditemukan: {jalur}")

    with jalur.open("r", encoding="utf-8") as file:
        isi = json.load(file)

    if not isinstance(isi, list) or len(isi) != 2:
        raise ValueError(
            f"Struktur JSON tidak sesuai format [metadata, data]: {berkas}"
        )
    if not isinstance(isi[0], dict) or not isinstance(isi[1], list):
        raise ValueError(f"Metadata atau daftar data tidak valid: {berkas}")

    return isi[0], isi[1]


def _tambahkan_lineage(df: pd.DataFrame, raw: Path, berkas: str):
  
    hasil = df.copy()
    hasil["_berkas_raw"] = berkas
    hasil["_sha256_raw"] = sha256_raw(berkas, raw=raw)
    return hasil


def _baca_tabel_metadata(raw: Path, berkas: str, kolom_id: str, nilai_id):
  
    _, records = _baca_json(raw, berkas)
    df = pd.json_normalize(records, sep=".")
    if kolom_id not in df.columns:
        raise ValueError(f"Kolom kunci '{kolom_id}' tidak ditemukan di {berkas}")

    df = df.loc[df[kolom_id].astype(str).isin(set(map(str, nilai_id)))].copy()
    return _tambahkan_lineage(df.reset_index(drop=True), raw, berkas)


def baca_paket_wdi(raw=RAW):
    
    raw = Path(raw)

    # Baca katalog sumber terlebih dahulu untuk menentukan sumber indikator.
    sumber = _baca_tabel_metadata(
        raw, BERKAS_SUMBER, "id", {"2", "46"}
    )

    indikator_wdi = _baca_tabel_metadata(
        raw, BERKAS_INDIKATOR_WDI, "id", INDIKATOR_WDI
    )
    indikator_sdg = _baca_tabel_metadata(
        raw, BERKAS_INDIKATOR_SDG, "id", INDIKATOR_WDI
    )

    # Baca dua berkas observasi dan ratakan objek indicator serta country.
    bagian_observasi = []
    for berkas in BERKAS_DATA:
        _, records = _baca_json(raw, berkas)
        df = pd.json_normalize(records, sep=".")

        kunci = "indicator.id"
        if kunci not in df.columns:
            raise ValueError(f"Kolom '{kunci}' tidak ditemukan di {berkas}")

        df = df.loc[df[kunci].astype(str).isin(INDIKATOR_WDI)].copy()
        df = _tambahkan_lineage(df.reset_index(drop=True), raw, berkas)
        bagian_observasi.append(df)

    observasi = pd.concat(bagian_observasi, ignore_index=True, sort=False)

    # Pastikan kedua seri yang diminta benar-benar ditemukan.
    ditemukan = set(observasi["indicator.id"].dropna().astype(str))
    tidak_ditemukan = INDIKATOR_WDI - ditemukan
    if tidak_ditemukan:
        raise ValueError(
            f"Seri WDI berikut tidak ditemukan dalam berkas data: "
            f"{sorted(tidak_ditemukan)}"
        )

    # Pastikan katalog metadata juga memuat kedua indikator.
    for nama, tabel in (
        ("metadata WDI", indikator_wdi),
        ("metadata SDG", indikator_sdg),
    ):
        metadata_ditemukan = set(tabel["id"].dropna().astype(str))
        hilang = INDIKATOR_WDI - metadata_ditemukan
        if hilang:
            raise ValueError(
                f"{nama} tidak memuat indikator: {sorted(hilang)}"
            )

    return {
        "observasi": observasi,
        "sumber": sumber,
        "indikator_wdi": indikator_wdi,
        "indikator_sdg": indikator_sdg,
    }


def baca_wdi(raw=RAW):
    
    return baca_paket_wdi(raw)["observasi"]



def _tampilkan_head(judul: str, tabel: pd.DataFrame) -> None:
   
    print(f"5 DATA TERATAS ({judul}):")
    if tabel.empty:
        print("(tidak ada baris setelah filter)")
        return
    with pd.option_context(
        "display.max_columns", None,
        "display.width", 220,
        "display.max_colwidth", 35,
    ):
        print(tabel.head(5).to_string(index=False))


def main():
    
    raw = Path(RAW)
    print("=" * 88)
    print("PEMBACA WDI - KASUS 09 / KELOMPOK 9")
    print("=" * 88)

    daftar_berkas = [
        (BERKAS_DATA[0], "data", "indicator.id"),
        (BERKAS_DATA[1], "data", "indicator.id"),
        (BERKAS_SUMBER, "sumber", "id"),
        (BERKAS_INDIKATOR_WDI, "indikator WDI", "id"),
        (BERKAS_INDIKATOR_SDG, "indikator SDG", "id"),
    ]

    for berkas, jenis, kolom_id in daftar_berkas:
        _, records = _baca_json(raw, berkas)
        tabel = pd.json_normalize(records, sep=".")
        if kolom_id not in tabel.columns:
            raise ValueError(f"Kolom '{kolom_id}' tidak ditemukan di {berkas}")

        if jenis == "data":
            tabel = tabel.loc[tabel[kolom_id].astype(str).isin(INDIKATOR_WDI)].copy()
        elif jenis == "sumber":
            tabel = tabel.loc[tabel[kolom_id].astype(str).isin({"2", "46"})].copy()
        else:
            tabel = tabel.loc[tabel[kolom_id].astype(str).isin(INDIKATOR_WDI)].copy()

        tabel = _tambahkan_lineage(tabel.reset_index(drop=True), raw, berkas)
        print(f"\nBerkas       : {berkas}")
        print(f"Jumlah baris : {len(tabel):,} baris (setelah filter)")
        print(f"Jumlah kolom : {len(tabel.columns)}")
        _tampilkan_head(berkas, tabel)

    paket = baca_paket_wdi(raw)
    observasi = paket["observasi"]
    print("\n" + "=" * 88)
    print("RINGKASAN OBSERVASI WDI")
    print("=" * 88)
    print(f"Jumlah total observasi terpilih: {len(observasi):,} baris")
    print("\nJumlah observasi per indikator:")
    print(observasi.groupby("indicator.id").size().to_string())
    print("\nJumlah observasi per berkas data:")
    print(observasi.groupby("_berkas_raw").size().to_string())
    print("\nSTATUS AKHIR WDI: BERHASIL")


if __name__ == "__main__":
    main()
