"""Tahap 8: validasi Silver dan Gold."""

from pathlib import Path
import pandas as pd


def validasi_silver(df):
    wajib = [
        "sumber", "seri_kode", "wilayah_kode", "periode",
        "jenis_periode", "rincian", "nilai", "satuan",
        "_berkas_raw", "_sha256_raw",
    ]

    kurang = [c for c in wajib if c not in df.columns]
    if kurang:
        raise ValueError(f"Kolom Silver tidak lengkap: {kurang}")

    if df.empty:
        raise ValueError("Silver kosong.")

    kunci = [
        "sumber", "seri_kode", "wilayah_kode",
        "periode", "rincian", "_berkas_raw",
    ]
    if df.duplicated(kunci).any():
        raise ValueError("Ditemukan duplikasi kunci Silver.")

    if not pd.api.types.is_numeric_dtype(df["nilai"]):
        raise ValueError("Kolom nilai Silver harus numerik.")

    seri_persen = ["var1447", "var1451", "var1221"]
    data_persen = df[df["seri_kode"].isin(seri_persen)]
    if not data_persen["nilai"].between(0, 100).all():
        raise ValueError("Nilai indikator persen di luar 0-100.")

    apk = df[df["seri_kode"] == "var1439"]
    if (apk["nilai"] < 0).any():
        raise ValueError("Nilai APK PAUD negatif.")

    satuan = df.groupby("seri_kode")["satuan"].nunique()
    if (satuan > 1).any():
        raise ValueError("Satuan tidak konsisten dalam satu seri.")

    return True


def validasi_gold(gold):
    wajib = [
        "panel_provinsi",
        "panel_provinsi_lebar",
        "grid_kelengkapan",
        "nasional",
        "rekonsiliasi_nasional",
    ]

    kurang = [nama for nama in wajib if nama not in gold]
    if kurang:
        raise ValueError(f"Tabel Gold tidak lengkap: {kurang}")

    panel = gold["panel_provinsi"]
    kunci = ["seri_kode", "wilayah_kode", "periode"]

    if panel.duplicated(kunci).any():
        raise ValueError("Ditemukan duplikasi sel panel Gold.")

    if not panel["kategori"].isin([
        "terisi", "missing", "belum_ada",
        "tidak_diterbitkan", "batas_lama",
    ]).all():
        raise ValueError("Kategori grid Gold tidak dikenal.")

    terisi = panel["kategori"] == "terisi"
    if panel.loc[terisi, "nilai"].isna().any():
        raise ValueError("Ada sel berstatus terisi tanpa nilai.")

    if panel.loc[~terisi, "nilai"].notna().any():
        raise ValueError("Ada nilai pada sel yang tidak berstatus terisi.")

    return True


def jalankan(silver, gold):
    hasil = {
        "validasi_silver": validasi_silver(silver),
        "validasi_gold": validasi_gold(gold),
    }

    folder = Path("reports")
    folder.mkdir(parents=True, exist_ok=True)

    isi = [
        "# Laporan Validasi",
        "",
        "## Hasil pemeriksaan",
    ]

    for nama, status in hasil.items():
        isi.append(f"- {nama}: {'LOLOS' if status else 'GAGAL'}")

    isi.extend([
        "",
        f"- Jumlah baris Silver: {len(silver):,}",
        f"- Jumlah sel panel Gold: {len(gold['panel_provinsi']):,}",
        f"- Jumlah baris rekonsiliasi: {len(gold['rekonsiliasi_nasional']):,}",
    ])

    (folder / "validasi.md").write_text(
        "\n".join(isi), encoding="utf-8"
    )

    print("\n=== HASIL VALIDASI ===")
    for nama, status in hasil.items():
        print(f"{nama}: {'LOLOS' if status else 'GAGAL'}")

    return hasil
