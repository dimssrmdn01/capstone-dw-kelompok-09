"""Aturan seleksi observasi Silver menjadi data Gold."""

import re
from datetime import date
from pathlib import Path

import pandas as pd

from src import konfigurasi as K
from src.laporan import ROOT


KOLOM_KUNCI = ["seri_kode", "wilayah_kode", "periode"]
RINCIAN_TOTAL = {"total", "jumlah", "tidak ada"}
KOLOM_LOG = [
    "id", "tanggal", "nim", "tahap", "seri_kode",
    "keputusan", "alternatif_ditolak", "alasan", "dampak_baris",
]


def _teks_unik(nilai):
    """Gabungkan teks unik yang tidak kosong."""
    hasil = []
    for item in nilai:
        if pd.isna(item):
            continue
        teks = str(item).strip()
        if teks and teks not in hasil:
            hasil.append(teks)
    return " | ".join(hasil)


def _kode_wilayah(nilai):
    """Samakan representasi kode wilayah untuk pencocokan."""
    if pd.isna(nilai):
        return ""
    teks = str(nilai).strip()
    if teks.endswith(".0"):
        teks = teks[:-2]
    return teks


def _gabungkan_anomali(data, lokasi=None):
    """Tambahkan penanda anomali tanpa mengubah atau menghapus nilai."""
    data = data.copy()
    lokasi = lokasi or ROOT / "reports" / "anomali.csv"

    kolom_hasil = [
        "anomaly_flag", "kategori_anomali",
        "tindakan_anomali", "bukti_anomali",
    ]

    if not Path(lokasi).exists():
        data["anomaly_flag"] = False
        for kolom in kolom_hasil[1:]:
            data[kolom] = ""
        return data

    anomali = pd.read_csv(lokasi, dtype=str, low_memory=False)

    kolom_wajib = {"seri_kode", "wilayah_kode", "periode"}
    if not kolom_wajib.issubset(anomali.columns):
        raise ValueError(
            f"Kolom kunci reports/anomali.csv tidak lengkap: "
            f"{sorted(kolom_wajib - set(anomali.columns))}"
        )

    for kolom in ["kategori", "tindakan", "bukti"]:
        if kolom not in anomali.columns:
            anomali[kolom] = ""

    anomali["_wilayah_key"] = anomali["wilayah_kode"].map(_kode_wilayah)
    anomali["_periode_key"] = anomali["periode"].astype(str).str.strip()
    data["_wilayah_key"] = data["wilayah_kode"].map(_kode_wilayah)
    data["_periode_key"] = data["periode"].astype(str).str.strip()

    kunci = ["seri_kode", "_wilayah_key", "_periode_key"]
    ringkas = (
        anomali.groupby(kunci, dropna=False)
        .agg(
            kategori_anomali=("kategori", _teks_unik),
            tindakan_anomali=("tindakan", _teks_unik),
            bukti_anomali=("bukti", _teks_unik),
        )
        .reset_index()
    )
    ringkas["anomaly_flag"] = True

    data = data.merge(ringkas, on=kunci, how="left", validate="many_to_one")
    data["anomaly_flag"] = data["anomaly_flag"].fillna(False).astype(bool)

    for kolom in kolom_hasil[1:]:
        data[kolom] = data[kolom].fillna("")

    return data.drop(columns=["_wilayah_key", "_periode_key"])


def pilih(silver, lokasi_anomali=None):
    """
    Pilih satu observasi tahunan rincian total per seri, wilayah, dan periode.

    Duplikat dengan nilai sama disederhanakan menjadi satu baris.
    Duplikat dengan nilai bertentangan menyebabkan pipeline berhenti.
    """
    wajib = {
        "seri_kode", "wilayah_kode", "periode", "jenis_periode",
        "rincian", "nilai", "_berkas_raw", "_sha256_raw",
    }
    kurang = wajib - set(silver.columns)
    if kurang:
        raise ValueError(f"Kolom Silver tidak lengkap untuk seleksi Gold: {sorted(kurang)}")

    terpilih = []
    catatan = []

    for seri, konfigurasi in K.SERI.items():
        sumber = silver[silver["seri_kode"].astype(str) == str(seri)].copy()

        rincian = sumber["rincian"].astype(str).str.strip().str.lower()
        periode = sumber["periode"].astype(str).str.strip()
        jenis = sumber["jenis_periode"].astype(str).str.strip().str.lower()

        mask_total = rincian.isin(RINCIAN_TOTAL)
        mask_tahunan = jenis.eq("tahun") & periode.str.fullmatch(r"\d{4}", na=False)
        calon = sumber[mask_total & mask_tahunan].copy()

        konflik = (
            calon.groupby(KOLOM_KUNCI, dropna=False)["nilai"]
            .nunique(dropna=False)
        )
        konflik = konflik[konflik > 1]

        if not konflik.empty:
            contoh = konflik.head(10).to_string()
            raise ValueError(
                f"Konflik nilai ditemukan pada {seri}. "
                f"Tidak ada snapshot yang dipilih secara otomatis.\n{contoh}"
            )

        # Nilai sudah dipastikan sama jika terdapat lebih dari satu snapshot.
        # Pemilihan berkas hanya untuk membuat hasil deterministik.
        calon = calon.sort_values(
            ["_berkas_raw", "_sha256_raw"],
            kind="stable",
        )
        calon = calon.drop_duplicates(KOLOM_KUNCI, keep="first").copy()
        calon["periode"] = calon["periode"].astype(str)
        calon["rincian"] = "total"

        jumlah_tidak_dipilih = len(sumber) - len(calon)
        terpilih.append(calon)

        tingkat = konfigurasi.get("tingkat", "tidak diketahui")
        if tingkat == "provinsi":
            tujuan = "panel provinsi"
        elif tingkat == "nasional":
            tujuan = "tabel nasional"
        else:
            tujuan = f"Gold tingkat {tingkat}"

        catatan.append({
            "seri_kode": seri,
            "jumlah_silver": len(sumber),
            "jumlah_gold": len(calon),
            "dampak_baris": jumlah_tidak_dipilih,
            "keputusan": (
                f"Gunakan satu observasi tahunan rincian total per "
                f"wilayah dan periode untuk {tujuan}; duplikat bernilai "
                f"sama disederhanakan secara deterministik."
            ),
            "alternatif_ditolak": (
                "Rincian selain total, periode non-tahunan, serta "
                "duplikat tambahan tidak dimasukkan ke Gold tahunan."
            ),
            "alasan": (
                "Indikator dipertahankan pada frekuensi tahunan dan "
                "rincian total agar satu sel wilayah-periode memiliki "
                "maksimal satu nilai. Data yang tidak terpilih tetap "
                "tersimpan di Silver."
            ),
        })

    hasil = (
        pd.concat(terpilih, ignore_index=True)
        if terpilih
        else silver.iloc[0:0].copy()
    )

    duplikat = hasil.duplicated(KOLOM_KUNCI, keep=False)
    if duplikat.any():
        raise ValueError(
            "Seleksi Gold gagal: masih ada kunci seri-wilayah-periode ganda.\n"
            + hasil.loc[duplikat, KOLOM_KUNCI].head(10).to_string(index=False)
        )

    hasil = _gabungkan_anomali(hasil, lokasi_anomali)
    return hasil, pd.DataFrame(catatan)


def catat_keputusan(catatan, lokasi=None):
    """Perbarui catatan tahap Gold tanpa menggandakan baris saat pipeline diulang."""
    lokasi = Path(lokasi or ROOT / "log-keputusan.csv")

    if lokasi.exists():
        log = pd.read_csv(lokasi, dtype=str).fillna("")
        for kolom in KOLOM_LOG:
            if kolom not in log.columns:
                log[kolom] = ""
        log = log[KOLOM_LOG]
    else:
        log = pd.DataFrame(columns=KOLOM_LOG)

    # Pertahankan NIM yang sudah dipakai pada keputusan proyek sebelumnya.
    nim_lama = log.loc[log["nim"].str.strip() != "", "nim"]
    nim = nim_lama.iloc[0] if not nim_lama.empty else ""

    # Hapus catatan Gold lama agar hasil pencatatan ulang tetap idempotent.
    log = log[log["tahap"].str.lower() != "gold"].copy()

    nomor_terakhir = 0
    for identitas in log["id"].astype(str):
        cocok = re.fullmatch(r"K-(\d+)", identitas.strip())
        if cocok:
            nomor_terakhir = max(nomor_terakhir, int(cocok.group(1)))

    baris_baru = []
    for i, baris in catatan.reset_index(drop=True).iterrows():
        baris_baru.append({
            "id": f"K-{nomor_terakhir + i + 1:03d}",
            "tanggal": date.today().isoformat(),
            "nim": nim,
            "tahap": "gold",
            "seri_kode": baris["seri_kode"],
            "keputusan": baris["keputusan"],
            "alternatif_ditolak": baris["alternatif_ditolak"],
            "alasan": baris["alasan"],
            "dampak_baris": str(int(baris["dampak_baris"])),
        })

    hasil_log = pd.concat(
        [log, pd.DataFrame(baris_baru, columns=KOLOM_LOG)],
        ignore_index=True,
    )
    hasil_log.to_csv(lokasi, index=False, encoding="utf-8-sig")
    return hasil_log
