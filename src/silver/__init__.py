"""Tahap 2–4 — Profil, pembersihan, dan penyeragaman ke Silver (pertemuan II–VII). Milik tim.

Keluaran: data/silver/silver.parquet dengan skema minimal di src/common/skema.py.
Satu baris = satu seri x wilayah x periode x rincian x berkas sumber. Nilai dari sumber berbeda
TIDAK digabung di sini. Setiap keputusan pembersihan dicatat di log-keputusan.csv.
"""

from src import konfigurasi as K
from src.laporan import ROOT, catat
from src.silver import anomali, bangun, grid, metadata, pembanding, profil

SILVER = ROOT / "data" / "silver" / "silver.parquet"


def jalankan(mentah):
    silver, info = bangun.susun(mentah)

    metadata.jalankan(mentah, info["cakupan_who"])

    katalog_salah = [
        k for k, s in K.SERI.items()
        if s["katalog_satuan"] not in ("—", "Tidak tercantum", s["satuan"])
    ]

    sdg_beda = [
        k for k, s in K.SERI.items()
        if s["katalog_sdg"] not in ("—", s["sdg"])
    ]

    catat(
        baris_bps=int((silver["sumber"] == "bps").sum()),
        baris_koreksi_satuan=int(silver["seri_kode"].isin(katalog_salah).sum()),
        baris_koreksi_sdg=int(silver["seri_kode"].isin(sdg_beda).sum()),
        baris_rujukan=int(silver["rujukan_tahun"].notna().sum()),
        baris_batas_who=int(silver["batas_bawah"].notna().sum())
    )


    katalog_salah = [
        k for k, s in K.SERI.items()
        if s["katalog_satuan"] not in ("—", s["satuan"])
    ]

    sdg_beda = [
        k for k, s in K.SERI.items()
        if s["katalog_sdg"] not in ("—", s["sdg"])
    ]

    catat(
        baris_bps=int((silver["sumber"] == "bps").sum()),
        baris_koreksi_satuan=int(silver["seri_kode"].isin(katalog_salah).sum()),
        baris_koreksi_sdg=int(silver["seri_kode"].isin(sdg_beda).sum()),
        baris_rujukan=int(silver["rujukan_tahun"].notna().sum()),
        baris_batas_who=int(silver["batas_bawah"].notna().sum())
    )

    SILVER.parent.mkdir(parents=True, exist_ok=True)
    silver.to_parquet(SILVER, index=False)

    silver.to_parquet(SILVER, index=False)

    calon = profil.jalankan(silver)
    pembanding.jalankan(silver, mentah)
    grid.jalankan(silver, mentah)
    anomali.jalankan(silver, mentah, calon)

    print(f"Silver: {len(silver):,} baris -> {SILVER.relative_to(ROOT)}")

    return silver