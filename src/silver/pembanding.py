import pandas as pd

from src import konfigurasi as K
from src import wilayah as W
from src.laporan import ROOT, catat, tabel_md, tulis


def jalankan(silver, mentah):
    utama = [k for k, s in K.SERI.items() if s["tingkat"] == "provinsi"]
    banding = [k for k, s in K.SERI.items() if s["tingkat"] != "provinsi"]
    tahun_utama = sorted(silver.loc[silver["seri_kode"].isin(utama), "periode"].unique())
    nas = silver[silver["seri_kode"].isin(banding) & (silver["wilayah_kode"] == W.INDONESIA)]
    ring = []
    for (seri, rinci), g in nas.groupby(["seri_kode", "rincian"]):
        per = sorted(g["periode"].unique())
        iris = [t for t in tahun_utama if t in per]
        ring.append({"seri_kode": seri, "sumber": K.SERI[seri]["sumber"], "rincian": rinci, "satuan": K.SERI[seri]["satuan"],
                     "jumlah_tahun": len(per), "awal": per[0], "akhir": per[-1],
                     "tahun_survei_utama_tersedia": ", ".join(iris) or "(tidak ada)",
                     "batas_bawah_atas": "ada" if g["batas_bawah"].notna().any() else "tidak"})
    ring = pd.DataFrame(ring)
    wdi = pd.DataFrame()
    if "wdi_data" in mentah:
        d = mentah["wdi_data"]
        wdi = d.groupby("indicator_id").agg(baris_ada=("date", "size"), nilai_ada=("value", lambda v: int(v.notna().sum()))).reset_index()
    sel = nas.assign(ada=1).pivot_table(index=["seri_kode", "rincian"], columns="periode", values="ada", aggfunc="max")
    kol = [t for t in sel.columns if t in tahun_utama]
    irisan = sel[kol].fillna(0).astype(int).reset_index() if kol else pd.DataFrame()
    nas[["seri_kode", "rincian", "periode"]].drop_duplicates().to_csv(ROOT / "reports" / "ketersediaan-pembanding.csv", index=False)
    kandidat = [{"pasangan": p["id"], "seri_utama": p["utama"], "pembanding": ", ".join(f"{s} ({r})" for s, r in p["pembanding"]),
                 "alasan": p["alasan_rincian"]} for p in K.PASANGAN]
    catat(tahun_survei_utama=", ".join(tahun_utama))
    tulis("ketersediaan-pembanding.md", "\n\n".join([
        "# Ketersediaan seri pembanding nasional",
        "Dihasilkan `python pipeline.py` (`src/silver/pembanding.py`). Tahun survei seri utama: "
        + (", ".join(tahun_utama) or "—") + ".",
        "## Ringkasan per seri dan rincian", tabel_md(ring),
        "## WDI: baris ada vs nilai ada", tabel_md(wdi) if len(wdi) else "Tidak ada seri WDI.",
        "## Ketersediaan pada tahun survei seri utama (1 = ada)",
        tabel_md(irisan) if len(irisan) else "Tidak ada pembanding pada tahun survei.",
        "## Rincian yang kandidat sebanding", tabel_md(pd.DataFrame(kandidat)),
        "Matriks lengkap seri x rincian x tahun: `reports/ketersediaan-pembanding.csv`.",
    ]))
    return ring