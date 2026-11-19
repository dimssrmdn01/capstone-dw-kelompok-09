import re

import pandas as pd

from src import konfigurasi as K
from src.laporan import ROOT, catat, tabel_md, tulis


def _bersih(teks):
    """Buang tag HTML dan spasi berlebih untuk versi yang enak dibaca (teks asli tetap disimpan)."""
    t = re.sub(r"<[^>]+>", " ", str(teks or ""))
    return re.sub(r"\s+", " ", t).strip()


def nama_dari_berkas(mentah):
    """{seri: (nama di berkas mentah, asal)}"""
    nama = {}
    if "bps_meta" in mentah:
        for r in mentah["bps_meta"].drop_duplicates("var_id").to_dict("records"):
            nama["var" + r["var_id"]] = (r["judul"], f"{r['_berkas_raw']} var.label")
    if "bps_statis_meta" in mentah:
        for seri, c in getattr(K, "TABEL_STATIS", {}).items():
            m = mentah["bps_statis_meta"]
            m = m[m["_berkas_raw"].str.endswith(c["berkas"] + ".json")]
            if len(m):
                nama[seri] = (m["title"].iloc[0], f"{m['_berkas_raw'].iloc[0]} data.title")
    if "ilo_dataflow" in mentah:
        for r in mentah["ilo_dataflow"].to_dict("records"):
            nama[r["seri_kode"]] = (r["nama"], f"{r['_berkas_raw']} dataflow name")
    if "wdi_meta" in mentah:
        for r in mentah["wdi_meta"].drop_duplicates("id").to_dict("records"):
            nama[r["id"]] = (r["name"], f"{r['_berkas_raw']} name")
    if "bnpb_sel" in mentah:
        from src import kamus_bnpb as KB
        u = mentah["bnpb_sel"][["resource_nama", "kolom", "tata", "_berkas_raw"]].drop_duplicates()
        for r in u.sort_values("_berkas_raw").to_dict("records"):
            seri = KB.ukuran_resource(r["resource_nama"]) if r["tata"] in ("jenis", "tahun") else None
            if seri and seri not in nama:
                nama[seri] = (r["resource_nama"], f"{r['_berkas_raw']} judul resource (katalog CKAN)")
            lab = KB.ukuran_label(r["kolom"])
            if lab and lab[0] not in nama and r["tata"] in ("rekap", "rekap_nasional", "jenis"):
                nama[lab[0]] = (f"kolom '{r['kolom']}' di {r['resource_nama']}", f"{r['_berkas_raw']} kepala kolom")
    for jalur, d in (mentah.get("who_csv") or {}).items():
        nama[d["IND_CODE"].iloc[0]] = (d["IND_NAME"].iloc[0], f"{jalur} IND_NAME")
    return nama


def periksa_metadata_ganda(mentah):
    """Indikator WDI yang muncul di lebih dari satu berkas metadata: apakah isinya sama?"""
    if "wdi_meta" not in mentah:
        return pd.DataFrame()
    m = mentah["wdi_meta"]
    baris = []
    for kode, g in m.groupby("id"):
        if len(g) < 2:
            continue
        sama = all(g[k].nunique(dropna=False) == 1 for k in ("name", "sourceNote", "sourceOrganization") if k in g)
        baris.append({"seri": kode, "jumlah_entri": len(g), "berkas": ", ".join(sorted(g["_berkas_raw"].str.split("/").str[-1])),
                      "isi_sama": "ya" if sama else "tidak"})
    return pd.DataFrame(baris)


def jalankan(mentah, cakupan_who):
    nama = nama_dari_berkas(mentah)
    baris = []
    for kode, s in K.SERI.items():
        nb, asal = nama.get(kode, ("", ""))
        cakup = s.get("cakupan", "")
        if kode in cakupan_who and cakupan_who[kode]:
            tetap = "; ".join(f"{k}={v}" for k, v in cakupan_who[kode].items())
            cakup = f"{cakup} [dimensi tetap di berkas: {tetap}]".strip()
        baris.append({
            "sumber": s["sumber"], "seri_kode": kode, "tingkat": s["tingkat"],
            "nama_di_berkas": nb.strip(), "asal_nama": asal, "nama_baku": s["nama"],
            "satuan": s["satuan"], "bukti_satuan": s["bukti_satuan"],
            "sdg_kode": s["sdg"], "bukti_sdg": s["bukti_sdg"], "cakupan": cakup,
            "katalog_satuan": s["katalog_satuan"], "katalog_sdg": s["katalog_sdg"],
            "koreksi_katalog": s.get("koreksi", ""),
        })
    seri = pd.DataFrame(baris)
    (ROOT / "docs").mkdir(exist_ok=True)
    seri.to_csv(ROOT / "docs" / "seri.csv", index=False)

    ganda = periksa_metadata_ganda(mentah)
    spasi = [k for k, (nb, _) in nama.items() if nb != nb.strip()]
    catatan_bps = ""
    if "bps_meta" in mentah:
        cb = mentah["bps_meta"].drop_duplicates("var_id")[["var_id", "catatan"]].copy()
        cb["catatan (tanpa tag HTML)"] = cb["catatan"].map(_bersih)
        catatan_bps = tabel_md(cb[["var_id", "catatan (tanpa tag HTML)"]])
    koreksi = seri[seri["koreksi_katalog"] != ""]
    catat(koreksi_katalog=len(koreksi), metadata_ganda=len(ganda))
    tulis("metadata.md", "\n\n".join([
        "# Metadata seri: nama, satuan, kode SDG",
        "Dihasilkan `python pipeline.py` dari berkas mentah dan `src/konfigurasi.py`. Tabel lengkap ada di "
        "`docs/seri.csv`. Bila katalog dan berkas mentah berbeda, berkas mentah yang dipakai dan koreksinya "
        "dicatat di `log-keputusan.csv`.",
        "## Nama di berkas mentah dan nama baku",
        tabel_md(seri[["seri_kode", "nama_di_berkas", "nama_baku"]]),
        "## Satuan dan kode SDG",
        tabel_md(seri[["seri_kode", "katalog_satuan", "satuan", "bukti_satuan", "katalog_sdg", "sdg_kode"]]),
        "## Koreksi katalog",
        tabel_md(koreksi[["seri_kode", "koreksi_katalog"]]) if len(koreksi) else "Tidak ada.",
        "## Catatan BPS (var.note)",
        catatan_bps or "Tidak ada seri BPS.",
        "## Metadata WDI yang muncul di lebih dari satu berkas",
        tabel_md(ganda) if len(ganda) else "Tidak ada.",
        "## Judul dengan spasi di awal/akhir",
        (", ".join(spasi) + ": teks asli disimpan, versi rapi di kolom nama_di_berkas.") if spasi else "Tidak ada.",
    ]))
    return seri
    