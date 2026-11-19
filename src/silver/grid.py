import pandas as pd

from src import konfigurasi as K
from src import wilayah as W
from src.laporan import ROOT, catat, tabel_md, tulis
from src.silver import deret


def periode_terbit(mentah, seri, silver):
    per_silver = sorted(silver.loc[silver["seri_kode"] == seri, "periode"].unique())
    if any(len(p) > 4 for p in per_silver):       # semester/triwulan: daftar tahun JSON tidak cukup
        return per_silver
    if "bps_meta" in mentah:
        m = mentah["bps_meta"]
        th = m.loc["var" + m["var_id"] == seri, "tahun_terbit"]
        if len(th):
            return sorted({t for x in th for t in x.split(",")})
    return sorted(silver.loc[silver["seri_kode"] == seri, "periode"].unique())


def bentuk_grid(silver, mentah):
    baris = []
    lab = deret.berlabel(silver)
    for label, seri, _ in deret.daftar():
        ada = lab[lab["seri_kode"] == label]
        terisi = set(zip(ada["wilayah_kode"], ada["periode"]))
        for per in periode_terbit(mentah, seri, silver):
            for kode in list(W.PROVINSI) + [W.INDONESIA]:
                tingkat = "nasional" if kode == W.INDONESIA else "provinsi"
                if (kode, per) in terisi:
                    kat, bukti = "terisi", ""
                elif not W.sudah_ada(kode, per):
                    kat, bukti = "belum_ada", f"provinsi dibentuk; data penuh mulai {W.PROVINSI[kode][1]}"
                elif (seri, kode, per) in K.TIDAK_TERBIT or (seri, tingkat, per) in K.TIDAK_TERBIT:
                    # pernyataan penerbit (bukti di konfigurasi) didahulukan dari dugaan batas lama
                    kat = "tidak_diterbitkan"
                    bukti = K.TIDAK_TERBIT.get((seri, kode, per)) or K.TIDAK_TERBIT[(seri, tingkat, per)]
                elif kode in W.INDUK and (W.INDUK[kode], per) in terisi and \
                        not any(w == kode and p < per for w, p in terisi) and \
                        not any(W.INDUK.get(k) == W.INDUK[kode] and W.PROVINSI[k][1] == W.PROVINSI[kode][1]
                                and (k, per) in terisi for k in W.PROVINSI):
                    kat = "batas_lama"
                    bukti = f"{W.NAMA[W.INDUK[kode]]} masih diterbitkan dengan batas lama pada {per}; angka tidak dipecah"
                else:
                    kat, bukti = "missing", "provinsi sudah ada dan penerbit tidak menyatakan angka itu tidak ada"
                baris.append({"seri_kode": label, "periode": per, "wilayah_kode": kode, "nama_wilayah": W.NAMA[kode],
                              "tingkat": tingkat, "kategori": kat, "bukti": bukti})
    return pd.DataFrame(baris)


def garis_waktu(silver):
    """Bila konfigurasi punya KONSEP: per konsep, seri mana berlaku pada periode berapa dan di mana definisinya berganti."""
    konsep = getattr(K, "KONSEP", {})
    if not konsep:
        return ""
    definisi = getattr(K, "PATAHAN_DEFINISI", {})
    baris = []
    for seri, nama in konsep.items():
        per = sorted(silver.loc[(silver["seri_kode"] == seri) & (silver["rincian"] == "total"), "periode"].unique())
        if not per:
            continue
        tahun = [int(p[:4]) for p in per]
        celah = sorted(set(range(tahun[0], tahun[-1] + 1)) - set(tahun))
        baris.append({"konsep": nama, "seri_kode": seri, "periode_pertama": per[0], "periode_terakhir": per[-1],
                      "jumlah_periode": len(per), "tahun_tidak_terbit": ", ".join(map(str, celah)) or "—",
                      "definisi_berganti": "; ".join(f"mulai {p}" for p in definisi.get(seri, {})) or "—"})
    t = pd.DataFrame(baris).sort_values(["konsep", "periode_pertama"])
    return "\n\n".join(["## Garis waktu konsep",
                         "Seri mana berlaku pada periode berapa. Seri kanonik per konsep per tahun dipilih di Gold (Sprint 2); "
                         "Silver menyimpan semua seri apa adanya.", tabel_md(t)])


def jalankan(silver, mentah):
    g = bentuk_grid(silver, mentah)
    prov = g[g["tingkat"] == "provinsi"]
    kel = (prov.assign(terisi=prov["kategori"] == "terisi",
                       seharusnya=prov["kategori"].isin(["terisi", "missing"]))
           .groupby(["seri_kode", "periode"])
           .agg(sel=("kategori", "size"), terisi=("terisi", "sum"), seharusnya_ada=("seharusnya", "sum"))
           .reset_index())
    kel["persen_dari_38"] = (100 * kel["terisi"] / kel["sel"]).round(1)
    kel["persen_dari_seharusnya"] = (100 * kel["terisi"] / kel["seharusnya_ada"].where(kel["seharusnya_ada"] > 0)).round(1)
    kat = prov.pivot_table(index="seri_kode", columns="kategori", values="wilayah_kode", aggfunc="size", fill_value=0)
    nas = g[g["tingkat"] == "nasional"][["seri_kode", "periode", "kategori", "bukti"]]
    kosong = g[g["kategori"] != "terisi"]
    kosong.to_csv(ROOT / "reports" / "grid-sel-kosong.csv", index=False)
    batas = (g[g["kategori"] == "terisi"].groupby(["seri_kode", "tingkat"])["periode"]
             .agg(periode_pertama="min", periode_terakhir="max", jumlah_periode="nunique").reset_index())
    belum = sorted({W.NAMA[k] for k in prov.loc[prov["kategori"] == "belum_ada", "wilayah_kode"]})
    catat(sel_grid=len(prov), sel_kosong_grid=int((prov["kategori"] != "terisi").sum()),
          sel_missing=int((prov["kategori"] == "missing").sum()),
          sel_belum_ada=int((prov["kategori"] == "belum_ada").sum()),
          sel_tidak_diterbitkan=int((prov["kategori"] == "tidak_diterbitkan").sum()),
          sel_batas_lama=int((prov["kategori"] == "batas_lama").sum()),
          periode_terakhir_panel=str(batas.loc[batas["tingkat"] == "provinsi", "periode_terakhir"].max()))
    tulis("kelengkapan-panel.md", "\n\n".join([
        "# Kelengkapan panel provinsi dan kategori sel kosong",
        "Dihasilkan `python pipeline.py` (`src/silver/grid.py`). Grid = 38 provinsi susunan 2025 x periode yang "
        "diterbitkan seri itu. Persen dari 38 menghitung semua sel; persen dari seharusnya hanya menghitung sel "
        "yang provinsinya sudah ada dan tidak dinyatakan tidak terbit oleh penerbit.",
        "## Persen sel terisi per seri per periode", tabel_md(kel),
        "## Jumlah sel per kategori (provinsi)", tabel_md(kat.reset_index()),
        "## Baris Indonesia", tabel_md(nas),
        "## Batas pemakaian panel",
        tabel_md(batas),
        ("Provinsi yang belum ada pada sebagian periode panel: " + ", ".join(belum) + ".") if belum else "",
        "Tahun sesudah periode terakhir di luar jangkauan panel; panel tidak menggambarkan keadaan tahun itu. "
        "Tahun di antara dua periode survei tidak termasuk grid dan tidak diisi di Silver.",
        "Daftar semua sel kosong beserta buktinya: `reports/grid-sel-kosong.csv`.",
        garis_waktu(silver),
    ]))
    return g