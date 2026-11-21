# Laporan Reproduksi Sprint 1

## 1. Tujuan

Reproduksi dilakukan untuk memastikan proses pengunduhan data mentah, ekstraksi, pembentukan data Silver, dan pemeriksaan skema dapat dijalankan kembali dari klon repositori yang bersih.

## 2. Lingkungan Reproduksi

- Repositori: `capstone-dw-kelompok-09`
- Folder reproduksi: `capstone-dw-kelompok-09-reproduksi`
- Branch: `124450124/kerja`

## 3. Pengunduhan Data Mentah

Perintah yang dijalankan:

```bash
python unduh_data.py --kasus 9
```

Hasil:
- Kasus 09 berhasil diunduh.
- Terdapat 17 berkas yang cocok dengan `MANIFEST.csv`.

## 4. Proses Ekstraksi Data

Perintah yang dijalankan:

```bash
python pipeline.py
```

Hasil ekstraksi:

| Keterangan | Hasil |
|---|---:|
| Berkas pada MANIFEST.csv | 17 |
| Berkas berhasil dibaca | 17 |
| Jumlah DataFrame sumber | 16 |
| Jumlah baris mentah | 4.146 |
| Jumlah kolom gabungan | 64 |
| Berkas terlewat | 0 |
| Lineage | Lengkap |
| Status ekstraksi | Berhasil |
| Waktu ekstraksi | 0,6 detik |

## 5. Pembentukan Data Silver

Proses pembentukan Silver berhasil dijalankan dengan hasil:
- Jumlah baris: 1.653
- Lokasi keluaran: `data/silver/silver.parquet`
- Waktu proses: 5,6 detik

## 6. Pemeriksaan Skema Silver

Pemeriksaan dijalankan menggunakan perintah:

```bash
python -c "from src.validasi import jalankan; jalankan()"
```

Hasil pemeriksaan:

| Pemeriksaan | Hasil |
|---|---|
| kolom_wajib | LOLOS |
| rentang_persen | LOLOS |
| apk_nonnegatif | LOLOS |
| keunikan_silver | LOLOS |
| konsistensi_satuan | LOLOS |

Seluruh 5 pemeriksaan validasi Silver berhasil.

## 7. Pemeriksaan Kesamaan dengan Commit

Kesamaan berkas Silver diperiksa menggunakan perintah:

```powershell
git diff --quiet HEAD -- data/silver/silver.parquet; if ($LASTEXITCODE -eq 0) { "SAMA DENGAN COMMIT" } else { "BERBEDA DARI COMMIT" }
```

Hasil:

`SAMA DENGAN COMMIT`

Dengan demikian, berkas Silver hasil reproduksi identik dengan berkas Silver yang tersimpan pada commit.

## 8. Catatan Kendala

Setelah pembentukan Silver berhasil, pipeline berhenti pada tahap Gold karena implementasi tahap 4–6 di `src/gold/__init__.py` masih berupa placeholder dan menghasilkan `NotImplementedError`.

Kendala tersebut tidak mengubah keberhasilan ekstraksi dan pembentukan Silver. Berkas Silver tetap berhasil dibentuk, divalidasi, dan dinyatakan identik dengan commit.

## 9. Kesimpulan

Reproduksi Sprint 1 dari klon repositori berhasil dilakukan sampai tahap pembentukan dan validasi Silver. Seluruh 17 berkas mentah berhasil dibaca, menghasilkan 1.653 baris data Silver. Lima pemeriksaan validasi berhasil dan hasil Silver identik dengan commit yang tersimpan di repositori.