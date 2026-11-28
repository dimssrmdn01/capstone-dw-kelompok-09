
"""Tahap 8: validasi Silver, Gold, dan rekonsiliasi."""

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


def validasi_gold(silver, gold):
    wajib = [
        "panel_provinsi", "panel_provinsi_lebar",
        "grid_kelengkapan", "nasional", "rekonsiliasi_nasional",
    ]
    kurang = [nama for nama in wajib if nama not in gold]
    if kurang:
        raise ValueError(f"Tabel Gold tidak lengkap: {kurang}")

    panel = gold["panel_provinsi"]
    rekonsiliasi = gold["rekonsiliasi_nasional"]

    kolom_panel = [
        "seri_kode", "wilayah_kode", "periode", "kategori",
        "nilai", "satuan", "rincian", "_berkas_raw",
    ]
    kurang_panel = [c for c in kolom_panel if c not in panel.columns]
    if kurang_panel:
        raise ValueError(f"Kolom panel Gold tidak lengkap: {kurang_panel}")

    kategori_valid = [
        "terisi", "missing", "belum_ada",
        "tidak_diterbitkan", "batas_lama",
    ]
    if not panel["kategori"].isin(kategori_valid).all():
        raise ValueError("Kategori Gold tidak dikenal.")

    terisi = panel["kategori"] == "terisi"
    if panel.loc[terisi, "nilai"].isna().any():
        raise ValueError("Ada sel terisi tanpa nilai.")
    if panel.loc[~terisi, "nilai"].notna().any():
        raise ValueError("Ada nilai pada sel yang tidak terisi.")

    # Aturan 1: kunci panel Gold harus unik.
    kunci_panel = ["seri_kode", "wilayah_kode", "periode"]
    aturan_1 = not panel.duplicated(kunci_panel).any()

    # Aturan 2: satu indikator hanya memiliki satu satuan.
    satuan = panel.groupby("seri_kode")["satuan"].nunique()
    aturan_2 = not (satuan > 1).any()

    # Aturan 3: setiap sel Gold terisi memiliki pasangan Silver.
    kolom_kunci = [
        "seri_kode", "wilayah_kode", "periode",
        "rincian", "_berkas_raw",
    ]
    pasangan = panel.loc[terisi, kolom_kunci].merge(
        silver[kolom_kunci].drop_duplicates(),
        on=kolom_kunci,
        how="left",
        indicator=True,
    )
    aturan_3 = (pasangan["_merge"] == "both").all()

    # Aturan 4: rekonsiliasi berpasangan harus memiliki kategori.
    kolom_rek = ["status_pasangan", "kategori_selisih"]
    kurang_rek = [c for c in kolom_rek if c not in rekonsiliasi.columns]
    if kurang_rek:
        raise ValueError(f"Kolom rekonsiliasi tidak lengkap: {kurang_rek}")

    berpasangan = rekonsiliasi[
        rekonsiliasi["status_pasangan"] == "berpasangan"
    ]
    aturan_4 = (
        berpasangan["kategori_selisih"].notna()
        & berpasangan["kategori_selisih"].astype(str).str.strip().ne("")
    ).all()

    return {
        "kunci_panel_unik": bool(aturan_1),
        "satuan_per_indikator": bool(aturan_2),
        "pasangan_gold_silver": bool(aturan_3),
        "kategori_rekonsiliasi": bool(aturan_4),
    }


def jalankan(silver, gold):
    validasi_silver(silver)
    hasil_gold = validasi_gold(silver, gold)

    folder = Path("reports")
    folder.mkdir(parents=True, exist_ok=True)

    isi = [
        "# Laporan Validasi",
        "",
        "## Validasi Silver",
        "- validasi_silver: LOLOS",
        "",
        "## Validasi Gold dan Rekonsiliasi",
    ]

    for nama, status in hasil_gold.items():
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
    print("validasi_silver: LOLOS")
    for nama, status in hasil_gold.items():
        print(f"{nama}: {'LOLOS' if status else 'GAGAL'}")

    if not all(hasil_gold.values()):
        raise ValueError("Terdapat aturan validasi Gold yang gagal.")

    return {
        "validasi_silver": True,
        "validasi_gold": True,
    }
