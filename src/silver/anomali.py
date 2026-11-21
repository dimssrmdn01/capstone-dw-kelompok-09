import pandas as pd

from src import konfigurasi as K
from src import wilayah as W
from src.laporan import ROOT, catat, tabel_md, tulis
from src.silver import deret


def galat_rentang(silver):
    baris = []
    for satuan, (lo, hi) in K.RENTANG.items():
        s = silver[(silver["satuan"] == satuan) & ((silver["nilai"] < lo) | (silver["nilai"] > hi))]
        for r in s.itertuples():
            baris.append({"seri_kode": deret.label(r.seri_kode, r.rincian), "wilayah_kode": r.wilayah_kode, "periode": r.periode,
                          "rincian": r.rincian, "nilai": r.nilai, "aturan": f"{satuan} harus di [{lo}, {hi}]"})
    return pd.DataFrame(baris, columns=["seri_kode", "wilayah_kode", "periode", "rincian", "nilai", "aturan"])


def uji_patahan(silver):
    """Per seri provinsi dan per pergantian periode: porsi provinsi yang berubah > ambang relatif ke arah sama."""
    hasil = []
    lab = deret.berlabel(silver)
    for seri, _, _ in deret.daftar():
        g = lab[(lab["seri_kode"] == seri) & (lab["wilayah_kode"] != W.INDONESIA)]
        lebar = g.pivot_table(index="wilayah_kode", columns="periode", values="nilai").sort_index(axis=1)
        per = list(lebar.columns)
        if K.SERI[deret.dasar(seri)]["satuan"].endswith("per_tahun"):
            hasil.append({"seri_kode": seri, "pergantian": "—", "provinsi": len(lebar), "porsi_naik": None, "porsi_turun": None,
                          "patahan": "tidak diuji",
                          "keterangan": "seri laju pertumbuhan: perubahan relatif laju tidak bermakna (bisa berganti tanda); "
                                        "patahan diuji pada seri tingkat"})
            continue
        if len(per) < 3:
            hasil.append({"seri_kode": seri, "pergantian": "—", "provinsi": 0, "porsi_naik": None, "porsi_turun": None,
                          "patahan": "tidak dapat diuji",
                          "keterangan": f"hanya {len(per)} periode; pola serentak dari dua titik tidak bisa dibedakan dari perubahan sungguhan"})
            continue
        for a, b in zip(per, per[1:]):
            rel = ((lebar[b] - lebar[a]) / lebar[a].abs()).dropna()
            minimal = K.ANOMALI.get("min_provinsi_patahan", 0)
            if len(rel) < minimal:
                hasil.append({"seri_kode": seri, "pergantian": f"{a}→{b}", "provinsi": len(rel), "porsi_naik": None,
                              "porsi_turun": None, "patahan": "tidak dapat diuji",
                              "keterangan": f"hanya {len(rel)} provinsi punya angka di kedua periode (minimal {minimal})"})
                continue
            amb = K.ANOMALI["lompat_relatif"]
            naik, turun = (rel > amb).mean(), (rel < -amb).mean()
            patah = max(naik, turun) >= K.ANOMALI["porsi_patahan"]
            hasil.append({"seri_kode": seri, "pergantian": f"{a}→{b}", "provinsi": len(rel),
                          "porsi_naik": round(naik, 2), "porsi_turun": round(turun, 2),
                          "patahan": "ya" if patah else "tidak",
                          "keterangan": f"ambang lompat {amb:.0%}, porsi serentak ≥ {K.ANOMALI['porsi_patahan']:.0%}"})
    return pd.DataFrame(hasil)


def patahan_wilayah(silver):
    """Provinsi induk yang wilayahnya mengecil karena pemekaran terbit di tengah panel."""
    hasil = []
    lab = deret.berlabel(silver)
    for seri, _, _ in deret.daftar():
        g = lab[lab["seri_kode"] == seri]
        ada = {w: sorted(x["periode"]) for w, x in g.groupby("wilayah_kode")}
        nilai = g.set_index(["wilayah_kode", "periode"])["nilai"]
        for induk in sorted(set(W.INDUK.values())):
            # anak dikelompokkan per angkatan pemekaran (tahun pembentukan yang sama)
            angkatan = {}
            for k, i in W.INDUK.items():
                if i == induk and k in ada:
                    angkatan.setdefault(W.PROVINSI[k][1], []).append(k)
            for anak in angkatan.values():
                if induk not in ada:
                    continue
                pertama = min(min(ada[k]) for k in anak)
                sebelum = [p for p in ada[induk] if p < pertama]
                if not sebelum or pertama not in ada[induk]:
                    continue
                hasil.append({"seri_kode": seri, "induk": W.NAMA[induk], "wilayah_kode": induk, "periode": pertama,
                              "anak": ", ".join(W.NAMA[k] for k in anak),
                              "nilai_sebelum": nilai[(induk, sebelum[-1])], "nilai_sesudah": nilai[(induk, pertama)]})
    return pd.DataFrame(hasil, columns=["seri_kode", "induk", "wilayah_kode", "periode", "anak", "nilai_sebelum", "nilai_sesudah"])


def bandingkan_format_bps(mentah):
    """Duplikat dua format: CSV dan JSON BPS untuk seri yang sama (kunci wilayah, rincian, tahun, periode)."""
    if "bps_json" not in mentah or "bps_csv" not in mentah:
        return pd.DataFrame()
    j, c = mentah["bps_json"], mentah["bps_csv"]
    baris = []
    for var, gj in j.groupby("var_id"):
        gc = c[c["var_id"] == var]
        kj = {(r.wilayah_id, r.turvar.strip(), r.tahun, r.turtahun.strip()): float(r.nilai) for r in gj.itertuples()}
        kc = {(r.wilayah_id, str(r.turvar).strip(), r.tahun, str(r.periode).strip()): float(r.nilai) for r in gc.itertuples()}
        sama = set(kj) & set(kc)
        beda = sum(abs(kj[x] - kc[x]) > 1e-9 for x in sama)
        baris.append({"seri": "var" + var, "baris_json": len(kj), "baris_csv": len(kc),
                      "pasangan_sama": len(sama), "hanya_json": len(set(kj) - set(kc)), "hanya_csv": len(set(kc) - set(kj)),
                      "nilai_berbeda": beda, "satuan_csv": ",".join(sorted(set(gc.get("satuan", pd.Series([""]))))) or "(kosong)"})
    return pd.DataFrame(baris)


def galat_ditangani():
    """Galat input yang sudah diputuskan sebelum Silver (src/silver/bangun.py terapkan_galat)."""
    jalur = ROOT / "reports" / "galat-input.csv"
    return pd.read_csv(jalur) if jalur.exists() and getattr(K, "GALAT_INPUT", {}) else pd.DataFrame()


def jalankan(silver, mentah, calon):
    galat = galat_rentang(silver)
    ditangani = galat_ditangani()
    patah = uji_patahan(silver)
    definisi = getattr(K, "PATAHAN_DEFINISI", {})
    parsial = getattr(K, "CAKUPAN_PARSIAL", {})
    wil = patahan_wilayah(silver)
    kunci_wil = {(r.seri_kode, r.wilayah_kode, r.periode) for r in wil.itertuples()}
    tahun_patah = {(r.seri_kode, r.pergantian.split("→")[1]) for r in patah.itertuples() if r.patahan == "ya"}
    kunci_galat = {(r.seri_kode, r.wilayah_kode, r.periode) for r in galat.itertuples()}
    kat = []
    for lbl, seri, _ in deret.daftar():
        for per in definisi.get(seri, {}):
            tahun_patah.add((lbl, per))
    for r in calon.itertuples():
        dasar = deret.dasar(r.seri_kode)
        if (r.seri_kode, r.wilayah_kode, r.periode) in kunci_galat:
            k, t, b = "galat_input", "perbaiki lewat kode bila koreksinya jelas, catat di log", "nilai di luar rentang satuan"
        elif r.wilayah_kode in parsial.get((dasar, r.periode), ()):
            k, t, b = "cakupan_parsial", "tandai; jangan bandingkan dengan periode lain", \
                "penerbit menyatakan pencacahan provinsi ini hanya sebagian pada periode ini"
        elif (r.seri_kode, r.wilayah_kode, r.periode) in kunci_wil:
            k, t, b = "patahan_wilayah", "tandai; jangan bandingkan induk sebelum dan sesudah pemekaran", \
                "provinsi induk kehilangan wilayah pemekaran pada periode ini"
        elif r.periode in definisi.get(dasar, {}):
            k, t, b = "patahan_seri", "tandai; definisi berganti menurut penerbit", definisi[dasar][r.periode]
        elif r.berulang:
            k, t, b = "perbedaan_struktural", "tandai sekali per provinsi; bukan kejadian satu tahun", \
                "provinsi ini di luar batas IQR antarprovinsi pada sebagian besar periode"
        elif (r.seri_kode, r.periode) in tahun_patah:
            k, t, b = "patahan_seri", "tandai; cari catatan metode", "sebagian besar provinsi melompat ke arah sama"
        else:
            k, t, b = "outlier", "tandai, nilai tidak diubah", "menyimpang dari provinsi lain; tidak ada bukti galat atau patahan"
        kat.append({**r._asdict(), "kategori": k, "tindakan": t, "bukti": b})
    kat = pd.DataFrame(kat).drop(columns=["Index"], errors="ignore")
    kat.to_csv(ROOT / "reports" / "anomali.csv", index=False)
    fmt = bandingkan_format_bps(mentah)
    kembar = int(silver.duplicated(["sumber", "seri_kode", "wilayah_kode", "periode", "rincian", "_berkas_raw"]).sum())
    catat(outlier_ditandai=int((kat.get("kategori", pd.Series(dtype=str)) == "outlier").sum()),
          patahan_ditandai=int((kat.get("kategori", pd.Series(dtype=str)) == "patahan_seri").sum()),
          struktural_ditandai=int((kat.get("kategori", pd.Series(dtype=str)) == "perbedaan_struktural").sum()),
          provinsi_struktural=int(kat.loc[kat.get("kategori", pd.Series(dtype=str)) == "perbedaan_struktural", "wilayah_kode"].nunique()) if len(kat) else 0,
          patahan_wilayah=len(wil), galat_input=len(galat) + len(ditangani), kunci_kembar=kembar,
          patahan_definisi=sum(len(v) for v in definisi.values()),
          parsial_ditandai=int((kat.get("kategori", pd.Series(dtype=str)) == "cakupan_parsial").sum()))
    tulis("anomali.md", "\n\n".join([
        "# Kategori anomali dan duplikat",
        "Dihasilkan `python pipeline.py` (`src/silver/anomali.py`). Nilai di Silver tidak diubah kecuali galat input "
        "yang koreksinya jelas.",
        f"## Galat input (semua baris Silver diperiksa terhadap rentang satuan): {len(galat)}",
        tabel_md(galat) if len(galat) else "Tidak ada nilai di luar rentang satuannya.",
        *(["### Galat input yang diputuskan sebelum Silver (`GALAT_INPUT` di `src/konfigurasi.py`)",
           tabel_md(ditangani.drop(columns="_berkas_raw")),
           "Berkas sumber dan buktinya: `reports/galat-input.csv`."] if len(ditangani) else []),
        "## Uji patahan seri", tabel_md(patah),
        "## Pergantian definisi yang dinyatakan penerbit",
        "\n".join(f"- `{s}` mulai {p}: {b}" for s, v in definisi.items() for p, b in v.items()) or "Tidak ada.",
        "## Cakupan parsial yang dinyatakan penerbit",
        "\n".join(f"- `{s}` {p}: " + ", ".join(W.NAMA[k] for k in v) for (s, p), v in parsial.items()) or "Tidak ada.",
        f"## Perubahan batas wilayah di tengah panel: {len(wil)}",
        (tabel_md(wil) + "\n\nNilai induk sebelum periode ini mencakup wilayah provinsi pemekaran; sesudahnya tidak. "
         "Perubahannya bukan tren dan tidak diratakan.") if len(wil) else
        "Tidak ada: tidak ada provinsi pemekaran yang mulai terbit di tengah panel seri provinsi.",
        f"## Calon anomali dan kategorinya ({len(kat)})",
        tabel_md(kat[["seri_kode", "nama_wilayah", "periode", "nilai", "arah", "kategori", "tindakan"]]) if len(kat) else "Tidak ada.",
        "Outlier di sini adalah outlier statistik. Menyebutnya *outlier asli* butuh penjelasan dunia nyata "
        "(kebijakan, bencana, cakupan survei); kolom itu diisi tim saat Sprint 2 bila buktinya ditemukan.",
        "## Duplikat dua format BPS (CSV vs JSON)",
        tabel_md(fmt) if len(fmt) else "Tidak ada seri BPS dua format.",
        f"## Kunci Silver kembar: {kembar}",
    ]))
    return kat
    