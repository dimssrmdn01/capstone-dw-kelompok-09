import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from src import konfigurasi as K  # noqa: E402
from src import wilayah as W  # noqa: E402
from src.laporan import GAMBAR, ROOT, catat, tabel_md, tulis  # noqa: E402
from src.silver import deret  # noqa: E402

def hitung_profil(silver):
    """Menghitung statistik dasar setiap seri."""
    lab = deret.berlabel(silver)
    if lab.empty:
        return pd.DataFrame()

    hasil = (
        lab.groupby("seri_kode")
        .agg(
            jumlah_data=("nilai", "count"),
            jumlah_wilayah=("wilayah_kode", "nunique"),
            jumlah_periode=("periode", "nunique"),
            minimum=("nilai", "min"),
            maksimum=("nilai", "max"),
            rata_rata=("nilai", "mean"),
            median=("nilai", "median"),
            standar_deviasi=("nilai", "std"),
        )
        .reset_index()
    )
    return hasil.round(3)


def hitung_profil_wilayah(silver):
    """Menghitung statistik nilai setiap provinsi pada masing-masing seri."""
    lab = deret.berlabel(silver)
    if lab.empty:
        return pd.DataFrame()

    prov = lab[lab["wilayah_kode"] != W.INDONESIA].copy()
    hasil = (
        prov.groupby(["seri_kode", "wilayah_kode"])
        .agg(
            jumlah_periode=("nilai", "count"),
            rata_rata=("nilai", "mean"),
            median=("nilai", "median"),
            minimum=("nilai", "min"),
            maksimum=("nilai", "max"),
        )
        .reset_index()
    )
    hasil["nama_wilayah"] = hasil["wilayah_kode"].map(W.NAMA)
    return hasil.round(3)

def seri_utama(silver):
    s = deret.berlabel(silver)
    return s[s["wilayah_kode"] != W.INDONESIA], s[s["wilayah_kode"] == W.INDONESIA]


def batas_iqr(nilai, k):
    q1, q3 = nilai.quantile(0.25), nilai.quantile(0.75)
    return q1 - k * (q3 - q1), q3 + k * (q3 - q1)


def skala_log():
    """ANOMALI['skala'] = 'log1p': IQR dihitung pada log(1 + nilai) untuk cacah yang sangat menceng (korban
    bencana); batas ditulis kembali dalam satuan asli, perubahan dalam kelipatan (1+b)/(1+a)."""
    return K.ANOMALI.get("skala") == "log1p"


def calon_anomali(prov):
    k = K.ANOMALI["k_iqr"]
    log = skala_log()
    f, balik = (np.log1p, np.expm1) if log else ((lambda x: x), (lambda x: x))
    calon = []
    for (seri, per), g in prov.groupby(["seri_kode", "periode"]):
        if len(g) < 8:
            continue
        u = f(g["nilai"])
        lo, hi = batas_iqr(u, k)
        for r in g[(u < lo) | (u > hi)].itertuples():
            calon.append({"seri_kode": seri, "wilayah_kode": r.wilayah_kode, "nama_wilayah": r.nama_wilayah,
                          "periode": per, "nilai": r.nilai, "arah": "ke bawah",
                          "alasan": f"di luar [{balik(lo):.2f}, {balik(hi):.2f}] (IQR x {k}{' pada log(1+x)' if log else ''}) "
                                    f"dibanding {len(g)} provinsi tahun itu"})
    for seri, g in prov.groupby("seri_kode"):
        lebar = g.pivot_table(index="wilayah_kode", columns="periode", values="nilai").sort_index(axis=1)
        per = list(lebar.columns)
        for a, b in zip(per, per[1:]):
            d = (f(lebar[b]) - f(lebar[a])).dropna()
            if len(d) < 8:
                continue
            lo, hi = batas_iqr(d, k)
            for w, v in d[(d < lo) | (d > hi)].items():
                teks = (f"perubahan {a}→{b} x{np.exp(v):.2f} di luar [x{np.exp(lo):.2f}, x{np.exp(hi):.2f}] (pada 1+x)" if log
                        else f"perubahan {a}→{b} sebesar {v:+.2f} di luar [{lo:.2f}, {hi:.2f}]")
                calon.append({"seri_kode": seri, "wilayah_kode": w, "nama_wilayah": W.NAMA[w], "periode": b,
                              "nilai": lebar.loc[w, b], "arah": "perubahan", "alasan": teks})
        if len(per) >= K.ANOMALI["min_titik_samping"]:
            for w, baris in lebar.iterrows():
                x = baris.dropna()
                if len(x) < K.ANOMALI["min_titik_samping"]:
                    continue
                u = f(x)
                lo, hi = batas_iqr(u, k)
                for p, v in x[(u < lo) | (u > hi)].items():
                    calon.append({"seri_kode": seri, "wilayah_kode": w, "nama_wilayah": W.NAMA[w], "periode": p,
                                  "nilai": v, "arah": "ke samping",
                                  "alasan": f"di luar [{balik(lo):.2f}, {balik(hi):.2f}] dibanding {len(x)} tahun di provinsi ini"})
    kolom = ["seri_kode", "wilayah_kode", "nama_wilayah", "periode", "nilai", "arah", "alasan"]
    c = pd.DataFrame(calon, columns=kolom)
    # provinsi yang di luar batas ke bawah pada sebagian besar periode: perbedaan struktural, bukan kejadian
    ada = prov.groupby(["seri_kode", "wilayah_kode"])["periode"].nunique()
    bawah = c[c["arah"] == "ke bawah"].groupby(["seri_kode", "wilayah_kode"])["periode"].nunique()
    berulang = {kunci for kunci, n in bawah.items()
                if n >= 2 and n / ada[kunci] >= K.ANOMALI.get("porsi_berulang", 0.5)}
    # satu baris per sel: arah yang menandai sel yang sama digabung
    c = (c.groupby(["seri_kode", "wilayah_kode", "nama_wilayah", "periode", "nilai"], as_index=False)
         .agg(arah=("arah", " + ".join), alasan=("alasan", "; ".join)))
    c["berulang"] = [(s, w) in berulang for s, w in zip(c["seri_kode"], c["wilayah_kode"])]
    return c[kolom + ["berulang"]].sort_values(["seri_kode", "periode", "wilayah_kode"]).reset_index(drop=True)


def gambar(prov, nas):
    GAMBAR.mkdir(parents=True, exist_ok=True)
    nama = []
    for seri, g in prov.groupby("seri_kode"):
        per = sorted(g["periode"].unique())
        fig, ax = plt.subplots(figsize=(7, 3.6))
        ax.boxplot([g.loc[g["periode"] == p, "nilai"] for p in per])
        ax.set_xticks(range(1, len(per) + 1), per)
        n = nas[nas["seri_kode"] == seri]
        if len(n):
            ax.scatter([per.index(p) + 1 for p in n["periode"] if p in per],
                       [v for p, v in zip(n["periode"], n["nilai"]) if p in per],
                       color="#B3261E", zorder=3, label="Indonesia (9999)")
            ax.legend(loc="best", fontsize=8)
        ax.set_title(f"{seri}: sebaran provinsi per periode", fontsize=10)
        ax.set_ylabel(K.SERI[deret.dasar(seri)]["satuan"], fontsize=9)
        fig.tight_layout()
        f = f"{deret.nama_berkas(seri)}-boxplot.png"
        fig.savefig(GAMBAR / f, dpi=120)
        plt.close(fig)
        nama.append(f)
        if len(per) >= 2:
            fig, ax = plt.subplots(figsize=(7, 3.6))
            lebar = g.pivot_table(index="periode", columns="wilayah_kode", values="nilai")
            ax.plot(lebar.index, lebar.values, color="#9AA5B1", linewidth=0.8, marker="o", markersize=2)
            if len(n):
                ax.plot(n["periode"], n["nilai"], color="#B3261E", linewidth=2, marker="o", label="Indonesia (9999)")
                ax.legend(loc="best", fontsize=8)
            ax.set_title(f"{seri}: deret per provinsi", fontsize=10)
            ax.set_ylabel(K.SERI[deret.dasar(seri)]["satuan"], fontsize=9)
            fig.tight_layout()
            f = f"{deret.nama_berkas(seri)}-deret.png"
            fig.savefig(GAMBAR / f, dpi=120)
            plt.close(fig)
            nama.append(f)
    return nama


def jalankan(silver):

    profil_seri = hitung_profil(silver)
    profil_wilayah = hitung_profil_wilayah(silver)

    folder = ROOT / "reports"
    folder.mkdir(parents=True, exist_ok=True)
    profil_seri.to_csv(folder / "profil-seri.csv", index=False)
    profil_wilayah.to_csv(folder / "profil-wilayah.csv", index=False)
    tulis(
        "profil.md",
        "\n\n".join([
            "# Profil Data Silver",
            "## Statistik setiap seri",
            tabel_md(profil_seri),
            "## Statistik setiap provinsi",
            tabel_md(profil_wilayah),
            "## Catatan",
            "Profil ini bersifat deskriptif. Calon anomali perlu diperiksa "
            "lebih lanjut sebelum dikategorikan sebagai outlier asli, "
            "patahan seri, atau galat input.",
        ])
    )

    prov, nas = seri_utama(silver)
    ring = (prov.groupby(["seri_kode", "periode"])["nilai"]
            .agg(n="size", rerata="mean", simpangan="std", minimum="min",
                 q1=lambda x: x.quantile(0.25), median="median", q3=lambda x: x.quantile(0.75), maksimum="max")
            .reset_index())
    titik = prov.groupby(["seri_kode", "wilayah_kode"])["periode"].nunique().groupby("seri_kode") \
        .agg(min_periode_per_provinsi="min", maks_periode_per_provinsi="max").reset_index()
    calon = calon_anomali(prov)
    calon.to_csv(GAMBAR.parent / "calon-anomali.csv", index=False)
    gb = gambar(prov, nas)
    catat(calon_anomali=len(calon))
    arah = [f"- {s}: {'hanya arah ke bawah dan perubahan' if r.maks_periode_per_provinsi < K.ANOMALI['min_titik_samping'] else 'tiga arah'}"
            f" (periode per provinsi {r.min_periode_per_provinsi}–{r.maks_periode_per_provinsi})"
            for s, r in titik.set_index("seri_kode").iterrows()]
    tulis("profil-seri-utama.md", "\n\n".join([
        "# Profil dan calon anomali seri utama",
        "Dihasilkan `python pipeline.py` (`src/silver/profil.py`). Hanya baris provinsi deret utama (rincian `total`, "
        "atau rincian yang didaftar di `DERET` untuk seri yang terbit per rincian; label `kode [rincian]`); "
        "baris Indonesia ditampilkan terpisah dan tidak ikut statistik antarprovinsi.",
        "## Banyak periode per provinsi (menentukan arah pembanding)",
        tabel_md(titik), "\n".join(arah),
        f"Metode: IQR dengan pengali {K.ANOMALI['k_iqr']}"
        f"{' pada skala log(1 + nilai) (cacah sangat menceng; batas ditulis kembali dalam satuan asli)' if skala_log() else ''}; arah ke samping hanya bila satu provinsi punya paling sedikit "
        f"{K.ANOMALI['min_titik_samping']} periode. Sel yang ditandai lebih dari satu arah ditulis satu baris. Provinsi yang "
        f"di luar batas ke bawah pada ≥ {K.ANOMALI.get('porsi_berulang', 0.5):.0%} periode diberi tanda `berulang`: "
        "itu perbedaan struktural antarprovinsi, bukan kejadian satu tahun. Lihat log untuk alasan memilih IQR.",
        "## Statistik deskriptif per seri per periode (provinsi)", tabel_md(ring),
        "## Baris Indonesia", tabel_md(nas[["seri_kode", "periode", "nilai", "rujukan_tahun"]]) if len(nas) else "Tidak ada.",
        f"## Calon anomali ({len(calon)})",
        "Daftar lengkap di `reports/calon-anomali.csv`; kategorinya di `reports/anomali.csv`.",
        tabel_md(calon) if len(calon) else "Tidak ada calon anomali dengan ambang ini.",
        "## Gambar", "\n".join(f"![{g}](gambar/{g})" for g in gb),
    ]))
    return calon