import re
from fnmatch import fnmatch

import pandas as pd

from src import konfigurasi as K
from src.laporan import ROOT

JUMLAH = "jumlah"


def daftar():
    """[(label, seri, rincian)] untuk semua seri tingkat provinsi."""
    hasil = []
    for seri, s in K.SERI.items():
        if s["tingkat"] != "provinsi":
            continue
        for r in getattr(K, "DERET", {}).get(seri, ["total"]):
            hasil.append((label(seri, r), seri, r))
    return hasil


def label(seri, rincian):
    return seri if rincian == "total" else f"{seri} [{rincian}]"


def dasar(lbl):
    """Kode seri dari label deret."""
    return lbl.split(" [")[0]


def nama_berkas(lbl):
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", lbl).strip("_")


def jumlah_rincian(silver, seri):
    """Satu baris per wilayah x periode x berkas: baris 'total' bila ada, kalau tidak jumlah semua rincian."""
    s = silver[silver["seri_kode"] == seri]
    k = ["wilayah_kode", "periode", "_berkas_raw"]
    total = s[s["rincian"] == "total"]
    sisa = s[(s["rincian"] != "total") & ~s.set_index(k).index.isin(total.set_index(k).index)]
    jml = (sisa.groupby(k, as_index=False)
           .agg(**{c: (c, "first") for c in s.columns if c not in k + ["nilai"]}, nilai=("nilai", "sum"),
                rincian_dijumlah=("rincian", "size")))
    hasil = pd.concat([total.assign(rincian_dijumlah=0), jml], ignore_index=True)
    hasil["rincian"] = JUMLAH
    return hasil[list(s.columns) + ["rincian_dijumlah"]]


def peringkat(berkas):
    pola = getattr(K, "URUTAN_BERKAS", [])
    return next((i for i, (p, _) in enumerate(pola) if fnmatch(berkas, p)), len(pola))


def satu_per_sel(g):
    """Bila satu wilayah x periode punya beberapa berkas, ambil satu menurut URUTAN_BERKAS (lalu jalur terurut)."""
    if not g.duplicated(["wilayah_kode", "periode"]).any():
        return g, pd.DataFrame()
    g = g.assign(_peringkat=g["_berkas_raw"].map(peringkat)).sort_values(["_peringkat", "_berkas_raw"])
    pakai = g.drop_duplicates(["wilayah_kode", "periode"])
    lain = (g.groupby(["wilayah_kode", "periode"])["_berkas_raw"].agg(lambda s: len(s) - 1).rename("berkas_lain"))
    catatan = pakai[["seri_kode", "wilayah_kode", "periode", "_berkas_raw"]].merge(lain.reset_index())
    return pakai.drop(columns="_peringkat"), catatan[catatan["berkas_lain"] > 0]


def berlabel(silver):
    """Baris Silver deret utama (semua wilayah) dengan kolom seri_kode diganti label deret."""
    bagian, catatan = [], []
    for lbl, seri, r in daftar():
        if r == JUMLAH:
            g = jumlah_rincian(silver, seri)
        else:
            g = silver[(silver["seri_kode"] == seri) & (silver["rincian"] == r)].copy()
        g["seri_kode"] = lbl
        g, c = satu_per_sel(g)
        bagian.append(g)
        catatan.append(c)
    catatan = [c for c in catatan if len(c)]
    if catatan:
        (ROOT / "reports").mkdir(exist_ok=True)
        pd.concat(catatan, ignore_index=True).to_csv(ROOT / "reports" / "deret-berkas.csv", index=False)
    return pd.concat(bagian, ignore_index=True) if bagian else silver.iloc[0:0].copy()