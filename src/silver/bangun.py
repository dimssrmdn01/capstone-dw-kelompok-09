import re

import numpy as np
import pandas as pd

from src import konfigurasi as K
from src import wilayah as W
from src.laporan import ROOT, catat

KOLOM = ["sumber", "seri_kode", "wilayah_kode", "nama_wilayah", "periode", "jenis_periode", "rincian", "nilai",
         "satuan", "sdg_kode", "batas_bawah", "batas_atas", "rujukan_tahun", "_berkas_raw", "_sha256_raw"]

BULAN = {"januari": "01", "februari": "02", "maret": "03", "april": "04", "mei": "05", "juni": "06", "juli": "07",
         "agustus": "08", "september": "09", "oktober": "10", "november": "11", "desember": "12"}


def periode_bps(tahun, turtahun):
    """Label tahun + label turtahun BPS -> (periode baku, jenis_periode)."""
    t = str(tahun).strip()
    p = str(turtahun).strip().lower()
    if p in ("tahun", "tahunan"):
        return t, "tahun"
    if m := re.fullmatch(r"semester\s*(1|2|i|ii)(\s*\(\w+\))?", p):
        return f"{t}-S{'1' if m.group(1) in ('1', 'i') else '2'}", "semester"
    if m := re.fullmatch(r"triwulan\s*(i{1,3}|iv|[1-4])", p):
        no = {"i": 1, "ii": 2, "iii": 3, "iv": 4}.get(m.group(1)) or int(m.group(1))
        return f"{t}-Q{no}", "triwulan"
    if p in BULAN:
        return f"{t}-{BULAN[p]}", "bulan"
    raise ValueError(f"label periode BPS belum dikenal: {turtahun!r}")


def rincian_teks(pasangan):
    """[(nama_dimensi, nilai), ...] -> 'nama=nilai;nama=nilai' terurut, atau 'total' bila kosong."""
    bagian = sorted(f"{k}={v}" for k, v in pasangan)
    return ";".join(bagian) or "total"


def kode_rincian(teks):
    """'Dokter Umum' -> 'dokter_umum'; 'SD/sederajat' -> 'sd_sederajat'."""
    return re.sub(r"[^a-z0-9]+", "_", str(teks).strip().lower()).strip("_")


def rincian_bps(seri, turvar):
    """Label turvar BPS -> rincian Silver. Nama dimensi dan kamus kode dari RINCIAN_BPS di konfigurasi;
    label yang berarti keseluruhan (RINCIAN_TOTAL_BPS, misalnya 'Tidak ada', 'Jumlah') menjadi 'total'."""
    t = str(turvar).strip()
    if t.lower() in K.RINCIAN_TOTAL_BPS:
        return "total"
    dim, kamus = getattr(K, "RINCIAN_BPS", {}).get(seri, ("rincian_bps", {}))
    return f"{dim}={kamus.get(t, kode_rincian(t))}"


def _tingkat(kode):
    return "nasional" if kode == W.INDONESIA else "provinsi"


def dari_bps(mentah):
    if K.FORMAT_BPS == "json":
        d = mentah["bps_json"].copy()
        d["seri_kode"] = "var" + d["var_id"]
    else:
        d = mentah["bps_csv"].rename(columns={"periode": "turtahun"}).copy()
        d["seri_kode"] = "var" + d["var_id"]

    d = d[d["seri_kode"].isin(K.SERI)]
    d = pilih_snapshot(d)

    # Memetakan nama wilayah agar mengikuti kode internal proyek.
    kode = d["wilayah"].map(W.dari_nama)
    tidak_dikenal = kode.isna()

    catat(baris_kabkota_dibuang=int(tidak_dikenal.sum()))

    d = d.loc[~tidak_dikenal].copy()
    kode = kode.loc[~tidak_dikenal].astype(int)

    per = [
        periode_bps(t, p)
        for t, p in zip(d["tahun"], d["turtahun"])
    ]

    out = pd.DataFrame({
        "sumber": "bps",
        "seri_kode": d["seri_kode"].values,
        "wilayah_kode": kode.values,
        "nama_wilayah": kode.map(W.NAMA).values,
        "periode": [p for p, _ in per],
        "jenis_periode": [j for _, j in per],
        "rincian": [
            rincian_bps(s, r)
            for s, r in zip(d["seri_kode"], d["turvar"])
        ],
        "nilai": pd.to_numeric(d["nilai"], errors="coerce").values,
        "_berkas_raw": d["_berkas_raw"].values,
        "_sha256_raw": d["_sha256_raw"].values
    })

    out["rujukan_tahun"] = [
        K.RUJUKAN_TAHUN.get((s, _tingkat(w)))
        for s, w in zip(out["seri_kode"], out["wilayah_kode"])
    ]

    return out

def pilih_snapshot(d):
    """Seri BPS yang ada di lebih dari satu snapshot (bps/<tanggal>/...): snapshot terbaru dipakai.
    Nilai snapshot lain dibandingkan dan hasilnya ditulis ke reports/snapshot-bps.csv."""
    d = d.assign(_snapshot=d["_berkas_raw"].str.split("/").str[1])
    laporan = []
    pakai = []
    for seri, g in d.groupby("seri_kode"):
        snap = sorted(g["_snapshot"].unique())
        baru = g[g["_snapshot"] == snap[-1]]
        pakai.append(baru)
        kunci = ["wilayah_id", "turvar", "tahun", "turtahun"]
        for lama in snap[:-1]:
            a = g[g["_snapshot"] == lama].set_index(kunci)["nilai"].astype(float)
            b = baru.set_index(kunci)["nilai"].astype(float)
            sama = a.index.intersection(b.index)
            laporan.append({"seri_kode": seri, "snapshot_dipakai": snap[-1], "snapshot_lain": lama,
                            "baris_lain": len(a), "baris_dipakai": len(b), "sel_sama": len(sama),
                            "nilai_berbeda": int(((a[sama] - b[sama]).abs() > 1e-9).sum())})
    if laporan:
        (ROOT / "reports").mkdir(exist_ok=True)
        pd.DataFrame(laporan).to_csv(ROOT / "reports" / "snapshot-bps.csv", index=False)
    catat(bps_snapshot_ganda=len(laporan), bps_snapshot_beda=int(sum(r["nilai_berbeda"] for r in laporan)))
    return pd.concat(pakai).drop(columns="_snapshot") if pakai else d.drop(columns="_snapshot")


def _label_statis(c, level, teks):
    """Label header/kolom tabel statis -> label baku: buang tanda catatan kaki ('Gas/Elpiji 1', 'Lainnya 2'),
    jadikan kode pendek, lalu terapkan kamus_header konfigurasi bila ada."""
    t = re.sub(r"\s+\d+\)?$", "", str(teks).strip())
    k = kode_rincian(t)
    return c.get("kamus_header", {}).get(level, {}).get(k, k)


def _rincian_statis(c, nilai_level):
    pas = []
    for level, (dim, kamus) in c["dimensi"].items():
        v = nilai_level[level]
        if v in c.get("total", ()):
            continue
        pas.append((dim, kamus.get(v, v)))
    return rincian_teks(pas)


def dari_statis(mentah):
    """Tabel statis BPS: angka dari HTML di JSON (diratakan di src/ekstraksi/bps.py), diuji silang dengan
    CSV pratampil (nama wilayah, tanpa kode). Konfigurasi TABEL_STATIS menentukan nama tiap tingkat header,
    tingkat mana yang menjadi rincian (dan kamus kodenya), label total, dan pemecah seri (misalnya luas vs
    persen menjadi dua seri karena satuannya berbeda). Hasil uji silang: reports/uji-silang-statis.csv."""
    bagian, kosong, uji = [], 0, []
    h_all = mentah["bps_statis_html"]
    c_all = mentah.get("bps_statis", pd.DataFrame(columns=["_berkas_raw"]))
    for seri, c in K.TABEL_STATIS.items():
        d = h_all[h_all["_berkas_raw"].str.endswith(c["berkas"] + ".json")].copy()
        for n, level in enumerate(c["header"], start=1):
            d[level] = [_label_statis(c, level, x) for x in d[f"h{n}"]]
        if "pisah" in c:
            d = d[d[c["pisah"][0]] == c["pisah"][1]]
        d = d[d["tahun"].astype(str).str.fullmatch(r"\d{4}")]      # kolom judul sumbu ('Tahun', 'Klasifikasi Daerah') dilewati
        kosong += int(d["nilai"].isna().sum())
        d = d[d["nilai"].notna()]
        d["rincian"] = [_rincian_statis(c, r) for r in d[list(c["header"])].to_dict("records")]
        d["periode"] = d["tahun"].astype(str)
        bagian.append(pd.DataFrame({
            "sumber": "bps", "seri_kode": seri, "wilayah_kode": d["wilayah_kode"].astype(int).values,
            "nama_wilayah": d["wilayah_kode"].map(W.NAMA).values, "periode": d["periode"].values,
            "jenis_periode": "tahun", "rincian": d["rincian"].values, "nilai": d["nilai"].astype(float).values,
            "_berkas_raw": d["_berkas_raw"].values, "_sha256_raw": d["_sha256_raw"].values}))
        # uji silang dengan CSV pratampil
        cv = c_all[c_all["_berkas_raw"].str.endswith(c["berkas"] + ".csv")].copy()
        if len(cv):
            for level in c["header"]:
                cv[level] = [_label_statis(c, level, x) for x in cv[level]] if level != "tahun" else cv[level].astype(str)
            if "pisah" in c:
                cv = cv[cv[c["pisah"][0]] == c["pisah"][1]]
            cv = cv[pd.to_numeric(cv["nilai"], errors="coerce").notna()]
            kc = {(W.dari_nama(r["wilayah"]), str(r["tahun"]), _rincian_statis(c, r)): float(r["nilai"])
                  for r in cv.to_dict("records")}
            kh = {(int(k), p, r): v for k, p, r, v in zip(d["wilayah_kode"], d["periode"], d["rincian"], d["nilai"])}
            sama = set(kc) & set(kh)
            uji.append({"seri_kode": seri, "baris_html": len(kh), "baris_csv": len(kc), "pasangan_sama": len(sama),
                        "hanya_html": len(set(kh) - set(kc)), "hanya_csv": len(set(kc) - set(kh)),
                        "nilai_berbeda": sum(abs(kh[x] - kc[x]) > 1e-6 for x in sama)})
    if uji:
        pd.DataFrame(uji).to_csv(ROOT / "reports" / "uji-silang-statis.csv", index=False)
    catat(statis_kosong_dibuang=kosong, statis_uji_beda=int(sum(u["nilai_berbeda"] + u["hanya_html"] + u["hanya_csv"] for u in uji)))
    return pd.concat(bagian, ignore_index=True)


def dari_wdi(mentah):
    d = mentah["wdi_data"]
    kosong = int(d["value"].isna().sum())
    d = d[d["value"].notna()]
    out = pd.DataFrame({
        "sumber": "wdi", "seri_kode": d["indicator_id"].values,
        "wilayah_kode": [W.dari_negara("wdi", c) for c in d["country_id"]],
        "periode": d["date"].astype(str).values, "jenis_periode": "tahun", "rincian": "total",
        "nilai": d["value"].astype(float).values,
        "_berkas_raw": d["_berkas_raw"].values, "_sha256_raw": d["_sha256_raw"].values})
    out["nama_wilayah"] = out["wilayah_kode"].map(W.NAMA)
    return out, kosong


ABAIKAN_DIM = {"DIM_TIME", "DIM_TIME_TYPE", "DIM_GEO_CODE_M49", "DIM_GEO_CODE_TYPE", "DIM_PUBLISH_STATE_CODE"}



def dari_who(mentah):
    from src.ekstraksi.who_gho import kolom_nilai

    potong, kosong, cakupan = [], 0, {}

    for jalur, d in mentah["who_csv"].items():
        seri = d["IND_CODE"].unique()

        if len(seri) != 1 or seri[0] not in K.SERI:
            raise ValueError(
                f"{jalur}: IND_CODE {list(seri)} bukan satu seri kasus"
            )

        seri = seri[0]

        if set(d["DIM_TIME_TYPE"]) != {"YEAR"}:
            raise ValueError(
                f"{jalur}: DIM_TIME_TYPE {set(d['DIM_TIME_TYPE'])}; "
                "hanya YEAR yang ditangani"
            )

        kn = kolom_nilai(d)
        nilai = pd.to_numeric(
            d[kn["nilai"]].replace("", np.nan),
            errors="coerce"
        )

        kosong += int(nilai.isna().sum())

        dims = [
            k for k in d.columns
            if k.startswith("DIM_") and k not in ABAIKAN_DIM
        ]

        tetap = [k for k in dims if d[k].nunique() == 1]
        cakupan[seri] = {k: d[k].iloc[0] for k in tetap}

        berubah = [k for k in dims if k not in tetap]
        rinci = []

        for _, r in d[berubah].iterrows():
            pas = []

            for k in berubah:
                v = r[k].strip()

                if v in K.RINCIAN_TOTAL_WHO:
                    continue

                v = K.RINCIAN_NILAI.get(k, {}).get(v, v)
                pas.append((K.RINCIAN_DIMENSI.get(k, k.lower()), v))

            rinci.append(rincian_teks(pas))

        bagian = pd.DataFrame({
            "sumber": "who_gho",
            "seri_kode": seri,
            "wilayah_kode": [
                W.dari_negara("who_gho", c)
                for c in d["DIM_GEO_CODE_M49"]
            ],
            "periode": d["DIM_TIME"].astype(str).values,
            "jenis_periode": "tahun",
            "rincian": rinci,
            "nilai": nilai.values,
            "batas_bawah": (
                pd.to_numeric(d[kn["bawah"]], errors="coerce").values
                if kn["bawah"] else np.nan
            ),
            "batas_atas": (
                pd.to_numeric(d[kn["atas"]], errors="coerce").values
                if kn["atas"] else np.nan
            ),
            "_berkas_raw": d["_berkas_raw"].values,
            "_sha256_raw": d["_sha256_raw"].values
        })

        potong.append(bagian[bagian["nilai"].notna()])

    if not potong:
        return pd.DataFrame(), kosong, cakupan, (0, 0)

    out = pd.concat(potong, ignore_index=True)
    out, kembar, tentang = buang_kembar_setara(out)
    out["nama_wilayah"] = out["wilayah_kode"].map(W.NAMA)

    return out, kosong, cakupan, (kembar, tentang)


def buang_kembar_setara(d):
    """Beberapa baris WHO menulis rincian yang sama dengan cara berbeda (semua DIM_* kosong, semua TOTAL,
    atau sebagian TOTAL), sehingga setelah dienkode kuncinya sama.
    - kembar setara (nilai sama persis): satu baris dipakai (urutan pertama di berkas), sisanya dibuang;
    - kembar bertentangan (nilai berbeda): berkas tidak memberi cara memilih, jadi semua baris kelompok itu
      tidak masuk Silver.
    Keduanya ditulis ke reports/kembar-who.csv dan dicatat di log-keputusan.csv."""
    kunci = ["seri_kode", "wilayah_kode", "periode", "rincian", "_berkas_raw"]
    ragam = d.groupby(kunci)["nilai"].transform("nunique")
    ukuran = d.groupby(kunci)["nilai"].transform("size")
    bertentangan = ragam > 1
    setara = (ukuran > 1) & ~bertentangan
    laporan = d[setara | bertentangan].assign(jenis=["bertentangan" if b else "setara" for b in bertentangan[setara | bertentangan]])
    if len(laporan):
        (ROOT / "reports").mkdir(exist_ok=True)
        laporan[kunci + ["nilai", "jenis"]].sort_values(kunci).to_csv(ROOT / "reports" / "kembar-who.csv", index=False)
    buang_setara = d.duplicated(kunci) & setara
    hasil = d[~(buang_setara | bertentangan)].reset_index(drop=True)
    return hasil, int(buang_setara.sum()), int(bertentangan.sum())


def dari_ilostat(mentah):
    """CSV SDMX ILOSTAT -> Silver. Rincian dari kolom dimensi lewat src/kamus_ilo.py; FREQ A -> AAAA (tahun),
    Q -> AAAA-Qn (triwulan). OBS_VALUE kosong tidak masuk Silver. Kode OBS_STATUS dan catatan seri
    dilaporkan di reports/ilostat-status.csv (B = patahan seri, disertai NOTE_INDICATOR 'Break in series')."""
    from src import kamus_ilo
    from src.ekstraksi.ilostat import dimensi
    d = mentah["ilo_csv"].copy()
    d = d[d["seri_kode"].isin(K.SERI)]
    kosong = int((d["OBS_VALUE"] == "").sum())
    d = d[d["OBS_VALUE"] != ""]
    dims = dimensi(d)
    d[dims] = d[dims].fillna("")          # berkas berbeda punya dimensi berbeda; dimensi yang tidak ada = kosong
    dims = [k for k in dims if d[k].ne("").any()]
    rinci = []
    for r in d[dims].to_dict("records"):
        pas = [kamus_ilo.kode(k, r[k]) for k in dims if r[k]]
        rinci.append(rincian_teks([p for p in pas if p]))
    jenis = d["FREQ"].map({"A": "tahun", "Q": "triwulan", "M": "bulan"})
    out = pd.DataFrame({
        "sumber": "ilostat", "seri_kode": d["seri_kode"].values,
        "wilayah_kode": [W.dari_negara("ilostat", c) for c in d["REF_AREA"]],
        "periode": d["TIME_PERIOD"].values, "jenis_periode": jenis.values, "rincian": rinci,
        "nilai": pd.to_numeric(d["OBS_VALUE"]).values,
        "batas_bawah": pd.to_numeric(d["LOWER_BOUND"].replace("", np.nan)).values,
        "batas_atas": pd.to_numeric(d["UPPER_BOUND"].replace("", np.nan)).values,
        "status_obs": d["OBS_STATUS"].replace("", None).values,
        "_berkas_raw": d["_berkas_raw"].values, "_sha256_raw": d["_sha256_raw"].values})
    out["nama_wilayah"] = out["wilayah_kode"].map(W.NAMA)
    status = (d.assign(OBS_STATUS=d["OBS_STATUS"].replace("", "(kosong)"))
              .groupby(["seri_kode", "OBS_STATUS", "NOTE_INDICATOR", "SOURCE"]).agg(
                  baris=("OBS_VALUE", "size"), periode_awal=("TIME_PERIOD", "min"), periode_akhir=("TIME_PERIOD", "max"))
              .reset_index())
    (ROOT / "reports").mkdir(exist_ok=True)
    status.to_csv(ROOT / "reports" / "ilostat-status.csv", index=False)
    patah = d[d["OBS_STATUS"] == "B"]
    catat(ilo_kosong_dibuang=kosong, ilo_status_b=len(patah), ilo_status_u=int((d["OBS_STATUS"] == "U").sum()),
          ilo_triwulan=int((d["FREQ"] == "Q").sum()))
    return out, patah[["seri_kode", "TIME_PERIOD"]].drop_duplicates()


def _ukuran_bnpb(tata, resource, kolom, jenis_baris):
    """(seri, rincian) satu sel BNPB. Tabel satu ukuran (jenis, tahun): seri dari judul resource; tabel rekap
    dan nilai: seri dari kepala kolom. Jenis bencana dari kolom (tata jenis) atau dari kolom 'Jenis Bencana'."""
    from src import kamus_bnpb as KB
    from src.ekstraksi.bnpb import POLA_TAHUN
    tambah = {}
    if tata in ("jenis", "tahun") and (kolom in KB.KOLOM_JENIS or POLA_TAHUN.match(kolom)):
        seri = KB.ukuran_resource(resource)
        if seri is None:
            raise ValueError(f"judul resource {resource!r} belum ada di kamus_bnpb.UKURAN_RESOURCE")
    else:
        u = KB.ukuran_label(kolom)
        if u is None:
            raise ValueError(f"kepala kolom BNPB {kolom!r} ({resource!r}) belum ada di kamus_bnpb.UKURAN_LABEL")
        seri, tambah = u
    if tata == "jenis" and kolom in KB.KOLOM_JENIS:
        jenis = KB.jenis(kolom)
    elif tata in ("rekap", "rekap_nasional", "tahun") and jenis_baris:
        jenis = KB.jenis(jenis_baris)
    else:
        jenis = None                       # tata nilai: 'Jenis Bencana' teks bebas, bukan kategori
    return seri, rincian_teks(([("jenis_bencana", jenis)] if jenis else []) + sorted(tambah.items()))


def dari_bnpb(mentah):
    """Sel BNPB -> Silver. Kab/kota dijumlahkan ke provinsi (kode Kemendagri empat digit -> provinsi, atau kolom
    Provinsi); jumlah kab/kota per angka di reports/bnpb-agregasi.csv. Sel yang tidak masuk Silver (periode lebih
    dari satu tahun, pecahan pada satuan cacah) di reports/bnpb-dibuang.csv. Semua berkas dipertahankan:
    observasi yang sama dari beberapa berkas dibandingkan di reports/bnpb-lintas-berkas.csv."""
    from src import kamus_bnpb as KB
    d = mentah["bnpb_sel"].copy()
    pasang = [_ukuran_bnpb(*r) for r in d[["tata", "resource_nama", "kolom", "jenis_baris"]].itertuples(index=False)]
    d["seri_kode"] = [p[0] for p in pasang]
    d["rincian"] = [p[1] for p in pasang]
    lain = int((~d["seri_kode"].isin(K.SERI)).sum())
    d = d[d["seri_kode"].isin(K.SERI)].copy()
    dibuang = []
    tunggal = d["periode_teks"].str.fullmatch(r"(19|20)\d\d(\.0)?")
    dibuang.append(d[~tunggal].assign(alasan="periode lebih dari satu tahun (usulan beberapa tahun kejadian)"))
    d = d[tunggal].copy()
    d["periode"] = d["periode_teks"].str[:4]
    d["nilai"] = pd.to_numeric(d["nilai_teks"], errors="raise")
    cacah = d["seri_kode"].map(lambda s: K.SERI[s]["satuan"] in KB.CACAH)
    bulat = d["nilai"].round()
    hampir = cacah & ((d["nilai"] - bulat).abs() < 1e-6) & (d["nilai"] != bulat)
    pecahan = cacah & ((d["nilai"] - bulat).abs() >= 1e-6)
    dibuang.append(d[pecahan].assign(alasan="pecahan pada satuan cacah"))
    d.loc[hampir, "nilai"] = bulat[hampir]
    d = d[~pecahan].copy()

    def wilayah(r):
        if r.tingkat_tabel == "indonesia":
            return W.INDONESIA
        if r.kode_wilayah:
            return W.dari_kemendagri(r.kode_wilayah, r.nama_wilayah if r.tingkat_tabel == "provinsi" else "")
        return W.dari_nama(r.nama_wilayah if r.tingkat_tabel == "provinsi" else r.provinsi)
    d["wilayah_kode"] = [wilayah(r) for r in d.itertuples(index=False)]
    kunci = ["seri_kode", "wilayah_kode", "periode", "rincian", "_berkas_raw"]
    kab = d[d["tingkat_tabel"] == "kabkota"]
    usulan = usulan_berulang(kab)
    agg = (kab.groupby(kunci + ["_sha256_raw"])
           .agg(nilai=("nilai", "sum"), baris_kabkota=("nilai", "size"), kabkota_unik=("nama_wilayah", "nunique"))
           .reset_index())
    lang = d[d["tingkat_tabel"] != "kabkota"]
    ganda = lang[lang.duplicated(kunci, keep=False)]
    if len(ganda):
        raise ValueError(f"baris provinsi/Indonesia ganda dalam satu berkas: {ganda[kunci].head().to_dict('records')}")
    (ROOT / "reports").mkdir(exist_ok=True)
    agg[kunci + ["baris_kabkota", "kabkota_unik", "nilai"]].to_csv(ROOT / "reports" / "bnpb-agregasi.csv", index=False)
    buang = pd.concat(dibuang, ignore_index=True)
    buang[["_berkas_raw", "baris", "seri_kode", "nama_wilayah", "provinsi", "periode_teks", "nilai_teks", "alasan"]].to_csv(
        ROOT / "reports" / "bnpb-dibuang.csv", index=False)
    out = pd.concat([lang[kunci + ["nilai", "_sha256_raw"]], agg[kunci + ["nilai", "_sha256_raw"]]], ignore_index=True)
    out["sumber"] = "bnpb"
    out["jenis_periode"] = "tahun"
    out["nama_wilayah"] = out["wilayah_kode"].map(W.NAMA)
    lintas = lintas_berkas(out)
    uji = kabkota_vs_provinsi(lang, agg)
    catat(bnpb_sel=len(mentah["bnpb_sel"]), bnpb_sel_seri_lain=lain, bnpb_kabkota_baris=len(kab),
          bnpb_angka_agregat=len(agg), bnpb_periode_jamak=int((buang["alasan"].str.startswith("periode")).sum()),
          bnpb_pecahan_dibuang=int(pecahan.sum()), bnpb_hampir_bulat=int(hampir.sum()),
          bnpb_lintas_kelompok=len(lintas), bnpb_lintas_beda=int((lintas["sama"] == "tidak").sum()) if len(lintas) else 0,
          bnpb_kab_pasangan=len(uji), bnpb_kab_sama=int((uji["selisih"] == 0).sum()),
          bnpb_kab_kejadian_lebih=int(((uji["seri_kode"] == "kejadian") & (uji["selisih"] > 0)).sum()),
          bnpb_kab_kejadian_kurang=int(((uji["seri_kode"] == "kejadian") & (uji["selisih"] < 0)).sum()),
          bnpb_kab_lain_beda=int(((uji["seri_kode"] != "kejadian") & (uji["selisih"] != 0)).sum()),
          bnpb_usulan_berulang=len(usulan))
    return out


def usulan_berulang(kab):
    """Tabel nilai (usulan rehabilitasi-rekonstruksi): kab/kota yang muncul lebih dari sekali untuk tahun kejadian
    yang sama di satu berkas (usulan beberapa tahun proposal, atau beberapa kejadian). Semua dijumlahkan; daftar ini
    untuk diputuskan di Sprint 2 -> reports/bnpb-usulan-berulang.csv."""
    n = kab[kab["tata"] == "nilai"].copy()
    if n.empty:
        return n
    n["kab_baku"] = n["nama_wilayah"].str.upper().str.replace(r"[^A-Z ]", "", regex=True).str.strip()
    n = n[n["seri_kode"] == n["seri_kode"].iloc[0]]          # satu ukuran cukup: satu baris = satu usulan
    g = (n.groupby(["_berkas_raw", "wilayah_kode", "periode", "kab_baku"])
         .agg(usulan=("nilai", "size"), nilai_min=("nilai", "min"), nilai_maks=("nilai", "max"),
              baris=("baris", lambda s: ",".join(map(str, s)))).reset_index())
    g = g[g["usulan"] > 1]
    g.to_csv(ROOT / "reports" / "bnpb-usulan-berulang.csv", index=False)
    return g


def kabkota_vs_provinsi(provinsi, kabkota):
    """Angka jumlahan kab/kota dibanding angka provinsi yang diterbitkan untuk seri, wilayah, periode, dan rincian
    yang sama (berkas berbeda). Satu baris per nilai unik pasangan -> reports/bnpb-kabkota-vs-provinsi.csv."""
    k = ["seri_kode", "wilayah_kode", "periode", "rincian"]
    p = provinsi[provinsi["wilayah_kode"] != W.INDONESIA]
    m = kabkota[k + ["nilai", "_berkas_raw", "baris_kabkota"]].merge(p[k + ["nilai", "_berkas_raw"]], on=k,
                                                                      suffixes=("_kabkota", "_provinsi"))
    m = m.drop_duplicates(k + ["nilai_kabkota", "nilai_provinsi"]).copy()
    m["selisih"] = m["nilai_kabkota"] - m["nilai_provinsi"]
    m.to_csv(ROOT / "reports" / "bnpb-kabkota-vs-provinsi.csv", index=False)
    return m


def lintas_berkas(silver_bnpb):
    """Observasi yang sama (seri x wilayah x periode x rincian) dari dua berkas atau lebih: sama atau berbeda?"""
    k = ["seri_kode", "wilayah_kode", "periode", "rincian"]
    g = silver_bnpb.groupby(k)
    t = g.agg(berkas=("_berkas_raw", "nunique"), nilai_min=("nilai", "min"), nilai_maks=("nilai", "max")).reset_index()
    t = t[t["berkas"] > 1].copy()
    t["sama"] = (t["nilai_min"] == t["nilai_maks"]).map({True: "ya", False: "tidak"})
    daftar = g["_berkas_raw"].apply(lambda s: " | ".join(sorted(x.split("/")[-1][:8] for x in s)))
    t = t.merge(daftar.rename("berkas_id").reset_index(), on=k)
    t.to_csv(ROOT / "reports" / "bnpb-lintas-berkas.csv", index=False)
    return t


def terapkan_galat(s):
    """Galat input yang diputuskan per baris di konfigurasi (GALAT_INPUT): kunci (seri, wilayah, periode, rincian)
    -> dict(tindakan='buang' atau nilai pengganti, bukti=..., berkas=pola _berkas_raw opsional). Hanya untuk nilai
    yang mustahil; daftar dan buktinya di reports/galat-input.csv. Kunci yang tidak cocok satu baris pun = galat."""
    from fnmatch import fnmatch
    aturan = getattr(K, "GALAT_INPUT", {})
    catatan, buang = [], pd.Series(False, index=s.index)
    for (seri, wil, per, rinci), a in aturan.items():
        cocok = (s["seri_kode"] == seri) & (s["wilayah_kode"] == wil) & (s["periode"] == per) & (s["rincian"] == rinci)
        cocok &= s["_berkas_raw"].map(lambda b: fnmatch(b, a.get("berkas", "*")))
        if not cocok.any():
            raise ValueError(f"GALAT_INPUT {(seri, wil, per, rinci)} tidak cocok dengan baris Silver mana pun")
        for i in s.index[cocok]:
            catatan.append({"seri_kode": seri, "wilayah_kode": wil, "periode": per, "rincian": rinci,
                            "nilai_asli": s.at[i, "nilai"], "tindakan": str(a["tindakan"]), "bukti": a["bukti"],
                            "_berkas_raw": s.at[i, "_berkas_raw"]})
        if a["tindakan"] == "buang":
            buang |= cocok
        else:
            s.loc[cocok, "nilai"] = float(a["tindakan"])
    hasil = pd.DataFrame(catatan, columns=["seri_kode", "wilayah_kode", "periode", "rincian", "nilai_asli", "tindakan",
                                           "bukti", "_berkas_raw"])
    if len(hasil):
        (ROOT / "reports").mkdir(exist_ok=True)
        hasil.to_csv(ROOT / "reports" / "galat-input.csv", index=False)
    catat(galat_ditangani=len(hasil))
    return s[~buang].reset_index(drop=True), hasil


def _siapkan_mentah(mentah):
    """Konversi DataFrame gabungan hasil ekstraksi menjadi dict sumber untuk bangun.susun()."""
    if not isinstance(mentah, pd.DataFrame):
        return mentah
    b = mentah["_berkas_raw"].astype(str)
    out = {}
    mask_bps_json = b.str.startswith("bps/") & b.str.contains("/json/") & b.str.endswith(".json")
    mask_bps_csv = b.str.startswith("bps/") & b.str.endswith(".csv")
    mask_wdi_data = b.str.startswith("wdi/") & b.str.contains("/data/") & b.str.endswith(".json")
    if mask_bps_json.any():
        d = mentah[mask_bps_json].copy()
        d["var_id"] = pd.to_numeric(d["var_id"], errors="coerce").astype("Int64").astype(str)
        out["bps_json"] = d
    if mask_bps_csv.any():
        d = mentah[mask_bps_csv].copy()
        d["var_id"] = pd.to_numeric(d["var_id"], errors="coerce").astype("Int64").astype(str)
        out["bps_csv"] = d
    if mask_wdi_data.any():
        d = mentah[mask_wdi_data].copy()
        if "indicator_id" not in d.columns and "indicator.id" in d.columns:
            d["indicator_id"] = d["indicator.id"]
        if "country_iso3" not in d.columns and "countryiso3code" in d.columns:
            d["country_iso3"] = d["countryiso3code"]
        if "country_id" not in d.columns:
            d["country_id"] = d["country.id"] if "country.id" in d.columns else d.get("countryiso3code")
        out["wdi_data"] = d
    return out


def susun(mentah):
    mentah = _siapkan_mentah(mentah)
    """Kembalikan (silver, catatan) — catatan berisi angka dan temuan untuk laporan."""
    bagian, info = [], {"cakupan_who": {}}
    if "bps_json" in mentah or "bps_csv" in mentah:
        bagian.append(dari_bps(mentah))
    if getattr(K, "TABEL_STATIS", None):
        bagian.append(dari_statis(mentah))
    if "wdi_data" in mentah:
        wdi, info["wdi_null"] = dari_wdi(mentah)
        bagian.append(wdi)
    if "ilo_csv" in mentah:
        ilo, info["ilo_patah"] = dari_ilostat(mentah)
        bagian.append(ilo)
    if "bnpb_sel" in mentah:
        bagian.append(dari_bnpb(mentah))
    if mentah.get("who_csv"):
        who, info["who_kosong"], info["cakupan_who"], info["who_kembar"] = dari_who(mentah)
        bagian.append(who)
    s = pd.concat(bagian, ignore_index=True)
    s, info["galat"] = terapkan_galat(s)
    s["satuan"] = s["seri_kode"].map(lambda k: K.SERI[k]["satuan"])
    s["sdg_kode"] = s["seri_kode"].map(lambda k: K.SERI[k]["sdg"])
    for k in ("batas_bawah", "batas_atas"):
        if k not in s:
            s[k] = np.nan
    s["rujukan_tahun"] = pd.array(s.get("rujukan_tahun", pd.Series([None] * len(s))), dtype="Int64")
    s["wilayah_kode"] = s["wilayah_kode"].astype("int64")
    s["nilai"] = s["nilai"].astype("float64")
    # kolom tambahan status_obs (OBS_STATUS ILOSTAT) hanya bila kasus punya seri ILOSTAT
    kolom = KOLOM[:-2] + ["status_obs"] + KOLOM[-2:] if "status_obs" in s else KOLOM
    if "status_obs" in s:
        s["status_obs"] = s["status_obs"].astype("string")
    s = s[kolom].sort_values(["sumber", "seri_kode", "wilayah_kode", "periode", "rincian"]).reset_index(drop=True)
    catat(baris_silver=len(s), seri_silver=int(s["seri_kode"].nunique()),
          rincian_dienkode=int(s["rincian"].nunique()), wdi_null_dibuang=info.get("wdi_null", 0),
          who_kosong_dibuang=info.get("who_kosong", 0), who_kembar_setara=info.get("who_kembar", (0, 0))[0],
          who_kembar_bertentangan=info.get("who_kembar", (0, 0))[1])
    return s, info
