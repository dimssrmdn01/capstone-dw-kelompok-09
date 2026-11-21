import json
from pathlib import Path

import pandas as pd

from src.common.manifest import RAW, sha256_raw

BERKAS_JSON = (
    "bps/2026-10-17/json/sdg4_4_4_1_a_v1451.json",
    "bps/2026-10-17/json/sdg4_4_4_1_b_v1447.json",
    "bps/2026-10-17/json/sdg4_apk_paud.json",
    "bps/2026-10-17/json/sdg5_5_b_1_v1221.json",
    "bps/2026-10-20/json/sdg5_5_b_1_v1221.json",
)


def _nilai_kode(item: dict, nama: str, berkas: str) -> str:
    if not isinstance(item, dict) or "val" not in item:
        raise ValueError(f"Dimensi '{nama}' tidak memiliki atribut 'val' di {berkas}")
    return str(item["val"])


def _buat_peta_dimensi(objek: dict, berkas: str) -> dict:
    
    dimensi_wajib = ("vervar", "var", "turvar", "tahun", "turtahun")
    for nama in dimensi_wajib:
        if not isinstance(objek.get(nama), list):
            raise ValueError(f"Dimensi '{nama}' harus berupa daftar di {berkas}")

    peta = {}
    for wilayah in objek["vervar"]:
        for variabel in objek["var"]:
            for rincian in objek["turvar"]:
                for tahun in objek["tahun"]:
                    for periode in objek["turtahun"]:
                        # Urutan kode mengikuti struktur kunci datacontent BPS.
                        kunci = "".join((
                            _nilai_kode(wilayah, "vervar", berkas),
                            _nilai_kode(variabel, "var", berkas),
                            _nilai_kode(rincian, "turvar", berkas),
                            _nilai_kode(tahun, "tahun", berkas),
                            _nilai_kode(periode, "turtahun", berkas),
                        ))
                        if kunci in peta:
                            raise ValueError(f"Kunci dimensi ganda '{kunci}' di {berkas}")
                        peta[kunci] = (wilayah, variabel, rincian, tahun, periode)
    return peta


def _ekstrak_objek(objek: dict, berkas: str) -> list[dict]:
    if not isinstance(objek, dict):
        raise ValueError(f"Objek JSON BPS tidak valid di {berkas}")
    if not isinstance(objek.get("datacontent"), dict):
        raise ValueError(f"'datacontent' tidak berbentuk objek di {berkas}")

    peta = _buat_peta_dimensi(objek, berkas)
    baris = []
    for kunci, nilai in objek["datacontent"].items():
        if kunci not in peta:
            raise ValueError(
                f"Kunci datacontent '{kunci}' tidak dapat dipetakan ke dimensi di {berkas}"
            )
        wilayah, variabel, rincian, tahun, periode = peta[kunci]
        subject = (objek.get("subject") or [{}])[0]

        baris.append({
            "status": objek.get("status"),
            "data-availability": objek.get("data-availability"),
            "last_update": objek.get("last_update"),
            "subject_val": subject.get("val"),
            "subject_label": subject.get("label"),
            "var_id": variabel.get("val"),
            "var_label": variabel.get("label"),
            "var_unit": variabel.get("unit"),
            "var_subj": variabel.get("subj"),
            "var_def": variabel.get("def"),
            "var_decimal": variabel.get("decimal"),
            "var_note": variabel.get("note"),
            "wilayah_id": wilayah.get("val"),
            "wilayah": wilayah.get("label"),
            "turvar_id": rincian.get("val"),
            "turvar": rincian.get("label"),
            "tahun_id": tahun.get("val"),
            "tahun": tahun.get("label"),
            "periode_id": periode.get("val"),
            "periode": periode.get("label"),
            "labelvervar": objek.get("labelvervar"),
            "nilai": nilai,
            # Menjaga atribut tambahan JSON agar tidak hilang saat diratakan.
            "related": objek.get("related"),
        })
    return baris


def baca_satu_json(berkas: str, raw: Path = RAW) -> pd.DataFrame:
  
    raw = Path(raw)
    jalur = raw / berkas
    if not jalur.is_file():
        raise FileNotFoundError(f"Berkas JSON BPS tidak ditemukan: {jalur}")

    with jalur.open("r", encoding="utf-8-sig") as file:
        isi = json.load(file)

    if not isinstance(isi, list) or not isi:
        raise ValueError(f"Struktur teratas JSON harus berupa daftar di {berkas}")

    semua_baris = []
    for objek in isi:
        semua_baris.extend(_ekstrak_objek(objek, berkas))

    df = pd.DataFrame(semua_baris)
    df["_berkas_raw"] = berkas
    df["_sha256_raw"] = sha256_raw(berkas, raw=raw)
    return df


def baca_semua_json(raw: Path = RAW) -> dict[str, pd.DataFrame]:
   
    return {berkas: baca_satu_json(berkas, raw=raw) for berkas in BERKAS_JSON}



def main() -> None:
    
    print("=" * 88)
    print("PEMBACA JSON BPS - KASUS 09 / KELOMPOK 9")
    print("=" * 88)
    tabel_per_berkas = baca_semua_json()
    for berkas, df in tabel_per_berkas.items():
        print(f"\nBerkas       : {berkas}")
        print(f"Jumlah baris : {len(df):,}")
        print(f"Jumlah kolom : {len(df.columns)}")
        print("5 DATA TERATAS:")
        with pd.option_context("display.max_columns", None, "display.width", 220, "display.max_colwidth", 30):
            print(df.head(5).to_string(index=False))
    total = sum(len(df) for df in tabel_per_berkas.values())
    print(f"\nTOTAL: {total:,} baris dari {len(tabel_per_berkas)} file JSON")


if __name__ == "__main__":
    main()
