"""Tahap 6: integrasi dan rekonsiliasi pembanding nasional."""

import pandas as pd
from src import konfigurasi as K


def buat_tabel_nasional_dari_silver(df_silver):
    kolom_wajib = [
        "wilayah_kode",
        "rincian",
        "periode",
        "seri_kode",
        "nilai",
    ]

    for kolom in kolom_wajib:
        if kolom not in df_silver.columns:
            raise ValueError(
                f"Kolom wajib tidak ditemukan: {kolom}"
            )

    nasional = df_silver[
        (df_silver["wilayah_kode"] == 9999)
        & (
            df_silver["rincian"]
            .astype(str)
            .str.strip()
            .str.lower()
            == "total"
        )
    ].copy()

    kolom_tabel = [
        "periode",
        "seri_kode",
        "wilayah_kode",
        "nilai",
    ]

    kolom_opsional = [
        "nama_wilayah",
        "satuan",
        "sumber",
        "rincian",
        "_berkas_raw",
        "_sha256_raw",
    ]

    for kolom in kolom_opsional:
        if kolom in nasional.columns:
            kolom_tabel.append(kolom)

    nasional = nasional[kolom_tabel].copy()
    nasional["periode"] = nasional["periode"].astype(str)

    kunci = [
        "seri_kode",
        "wilayah_kode",
        "periode",
    ]

    duplikat = nasional.duplicated(kunci, keep=False)

    if duplikat.any():
        raise ValueError(
            "Tabel nasional memiliki kunci ganda:\n"
            + nasional.loc[duplikat, kunci]
            .head(10)
            .to_string(index=False)
        )

    return nasional.sort_values(
        ["seri_kode", "periode"]
    ).reset_index(drop=True)


KOLOM_REKONSILIASI = [
    "pasangan", "periode",
    "seri_utama", "nilai_utama",
    "seri_pembanding", "rincian_pembanding", "nilai_pembanding",
    "selisih", "status_pasangan", "kategori_selisih",
    "penjelasan", "dugaan", "bukti", "alasan_perbandingan",
]


def _penjelasan_tanpa_pasangan(seri_ada, seri_kosong, periode):
    return (
        f"Hanya {seri_ada} yang memiliki nilai pada {periode}; {seri_kosong} tidak tersedia "
        f"pada periode ini di snapshot yang dipakai. Baris dipertahankan agar celah periode terlihat."
    )


def buat_tabel_rekonsiliasi(tabel_nasional):
    """
    Tahap 6: pasangkan seri utama dengan pembanding nasional per periode.

    Satu baris = satu pasangan x periode. Semua periode yang punya nilai di salah satu
    seri ikut tampil (status_pasangan menandai berpasangan / hanya_utama / hanya_pembanding).
    Selisih = nilai_utama - nilai_pembanding dan tidak pernah dihapus atau dipaksa sama.
    Setiap baris berpasangan diberi satu kategori dari K.KATEGORI_SELISIH.
    """
    hasil = []

    lebar = tabel_nasional.pivot(
        index="periode",
        columns="seri_kode",
        values="nilai",
    ).sort_index()

    for pasangan in K.PASANGAN:
        utama = pasangan["utama"]
        aturan = pasangan.get("rekonsiliasi", {})
        pengecualian = aturan.get("pengecualian", {})

        if utama not in lebar.columns:
            raise ValueError(f"Seri utama {utama} ({pasangan['id']}) tidak ada di tabel nasional.")

        for pembanding, rincian in pasangan["pembanding"]:
            if pembanding not in lebar.columns:
                raise ValueError(
                    f"Seri pembanding {pembanding} ({pasangan['id']}) tidak ada di tabel nasional."
                )

            sub = lebar[[utama, pembanding]].dropna(how="all")

            for periode, baris in sub.iterrows():
                periode = str(periode)
                ada_utama = pd.notna(baris[utama])
                ada_pembanding = pd.notna(baris[pembanding])
                nilai_utama = float(baris[utama]) if ada_utama else None
                nilai_pembanding = float(baris[pembanding]) if ada_pembanding else None

                if ada_utama and ada_pembanding:
                    status = "berpasangan"
                    khusus = pengecualian.get(periode, {})
                    kategori = khusus.get("kategori", aturan.get("kategori"))
                    penjelasan = khusus.get("penjelasan", aturan.get("penjelasan", ""))
                    dugaan = khusus.get("dugaan", "")
                    bukti = khusus.get("bukti", aturan.get("bukti", ""))
                    selisih = round(nilai_utama - nilai_pembanding, 4)
                elif ada_utama:
                    status, kategori, selisih = "hanya_utama", None, None
                    penjelasan = _penjelasan_tanpa_pasangan(utama, pembanding, periode)
                    dugaan, bukti = "", ""
                else:
                    status, kategori, selisih = "hanya_pembanding", None, None
                    penjelasan = _penjelasan_tanpa_pasangan(pembanding, utama, periode)
                    dugaan, bukti = "", ""

                hasil.append({
                    "pasangan": pasangan["id"],
                    "periode": periode,
                    "seri_utama": utama,
                    "nilai_utama": nilai_utama,
                    "seri_pembanding": pembanding,
                    "rincian_pembanding": rincian,
                    "nilai_pembanding": nilai_pembanding,
                    "selisih": selisih,
                    "status_pasangan": status,
                    "kategori_selisih": kategori,
                    "penjelasan": penjelasan,
                    "dugaan": dugaan,
                    "bukti": bukti,
                    "alasan_perbandingan": pasangan["alasan_rincian"],
                })

    tabel = pd.DataFrame(hasil, columns=KOLOM_REKONSILIASI)
    for kolom in ["nilai_utama", "nilai_pembanding", "selisih"]:
        tabel[kolom] = tabel[kolom].astype("float64")

    berpasangan = tabel["status_pasangan"] == "berpasangan"
    tanpa_kategori = berpasangan & tabel["kategori_selisih"].isna()
    if tanpa_kategori.any():
        raise ValueError(
            "Baris berpasangan tanpa kategori selisih:\n"
            + tabel.loc[tanpa_kategori, ["pasangan", "periode"]].to_string(index=False)
        )
    tidak_dikenal = berpasangan & ~tabel["kategori_selisih"].isin(K.KATEGORI_SELISIH)
    if tidak_dikenal.any():
        raise ValueError(
            "Kategori selisih tidak dikenal: "
            + str(sorted(tabel.loc[tidak_dikenal, "kategori_selisih"].unique()))
        )
    belum = berpasangan & tabel["kategori_selisih"].eq("belum terjelaskan")
    if (tabel.loc[belum, "dugaan"].str.strip().eq("") | tabel.loc[belum, "bukti"].str.strip().eq("")).any():
        raise ValueError("Baris 'belum terjelaskan' wajib memuat dugaan dan bukti yang sudah dicari.")

    return tabel.sort_values(["pasangan", "periode"]).reset_index(drop=True)


if __name__ == "__main__":
    from pathlib import Path

    lokasi = Path("data/silver/silver.parquet")

    if lokasi.exists():
        df = pd.read_parquet(lokasi)

        nasional = buat_tabel_nasional_dari_silver(df)

        print("TABEL NASIONAL")
        print(nasional.head().to_string(index=False))

        rekonsiliasi = buat_tabel_rekonsiliasi(nasional)

        print("\nTABEL REKONSILIASI")
        print(rekonsiliasi.to_string(index=False))
