# Laporan Validasi Data Silver

## 1. Tujuan

Validasi dilakukan untuk memastikan data Silver memenuhi aturan kualitas data yang telah ditentukan.

## 2. Data yang Divalidasi

Validasi dilakukan pada data Silver terbaru yang tersimpan di `data/silver/silver.parquet`, dengan rincian:
- Jumlah baris: 1.653
- Jumlah kode wilayah: 39 (38 provinsi dan Indonesia)
- Sumber data: BPS dan WDI

## 3. Hasil Validasi

| No. | Aturan Validasi | Hasil |
|---|---|---|
| 1 | Kelengkapan kolom wajib | Lolos |
| 2 | Rentang nilai indikator persen (0-100) | Lolos |
| 3 | Nilai APK tidak negatif | Lolos |
| 4 | Keunikan kunci Silver | Lolos |
| 5 | Konsistensi satuan | Lolos |

## 4. Kesimpulan

Berdasarkan pengujian terhadap 1.653 baris data Silver, seluruh 5 aturan validasi berhasil dipenuhi. Data Silver dinyatakan lolos terhadap aturan kualitas data yang diuji.

Validasi snapshot `var1221` juga telah diperiksa secara terpisah. Snapshot 2026-10-20 digunakan sebagai snapshot terbaru dan dibandingkan dengan snapshot 2026-10-17. Masing-masing berisi 393 baris, dengan 393 sel bernilai sama dan 0 nilai berbeda.
