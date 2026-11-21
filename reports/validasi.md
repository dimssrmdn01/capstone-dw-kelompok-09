# Laporan Validasi Data Silver

## 1. Tujuan
Validasi dilakukan untuk memastikan data Silver memenuhi aturan kualitas data yang telah ditentukan.

## 2. Data yang Divalidasi
Validasi dilakukan pada data Silver pertama dengan jumlah 1.645 baris yang tersimpan di `data/silver/silver.parquet`.

## 3. Hasil Validasi

| No. | Aturan Validasi | Hasil |
|---|---|---|
| 1 | Kelengkapan kolom wajib | Lolos |
| 2 | Rentang nilai indikator persen (0–100) | Lolos |
| 3 | Nilai APK tidak negatif | Lolos |
| 4 | Keunikan kunci Silver | Lolos |
| 5 | Konsistensi satuan | Lolos |

## 4. Kesimpulan
Berdasarkan hasil pengujian, seluruh 5 aturan validasi yang dijalankan berhasil dipenuhi. Data Silver dinyatakan lolos terhadap aturan tersebut.

Catatan: Validasi pemilihan snapshot `var1221` masih perlu dipastikan secara terpisah karena belum muncul pada hasil pengujian yang dilaporkan.