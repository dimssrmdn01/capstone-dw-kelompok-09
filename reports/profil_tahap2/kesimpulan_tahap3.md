# Kesimpulan Tahap 3 – Pemeriksaan dan Klasifikasi Anomali

## 1. Tujuan

Tahap 3 dilakukan untuk memeriksa kandidat anomali yang telah ditemukan pada tahap profiling data. Pemeriksaan bertujuan membedakan tiga kondisi, yaitu:

1. **Outlier asli**, yaitu observasi yang memiliki nilai ekstrem dibandingkan pola data lainnya, tetapi belum terbukti sebagai kesalahan input.
2. **Patahan seri**, yaitu perubahan pola data yang dapat disebabkan oleh perubahan definisi, metode pengukuran, atau cakupan geografis.
3. **Kesalahan input**, yaitu nilai yang terbukti tidak sesuai dengan sumber atau terjadi akibat kesalahan pencatatan.

Prinsip utama yang digunakan adalah hanya memperbaiki kesalahan input yang memiliki bukti pendukung. Outlier asli dan patahan seri tidak dihapus atau diubah, tetapi dipertahankan dan diberi penjelasan.

## 2. Metode Pemeriksaan

Pemeriksaan dilakukan melalui beberapa langkah:

### 2.1 Pemeriksaan kandidat anomali

Kandidat anomali diperiksa berdasarkan hasil deteksi statistik, termasuk:

- IQR antarprovinsi untuk mengidentifikasi nilai yang ekstrem dibandingkan wilayah lain.
- IQR temporal untuk mengidentifikasi perubahan nilai yang ekstrem dalam suatu seri waktu.

Hasil kedua metode digunakan sebagai dasar pemeriksaan lebih lanjut, bukan sebagai bukti otomatis bahwa suatu nilai merupakan kesalahan input.

### 2.2 Pemeriksaan pola temporal dan perbandingan wilayah

Nilai anomali dibandingkan dengan observasi pada tahun sebelumnya dan sesudahnya serta dengan wilayah lain.

Pemeriksaan ini dilakukan untuk melihat apakah nilai ekstrem merupakan bagian dari pola data, perubahan cakupan, atau indikasi kesalahan pencatatan.

### 2.3 Pemeriksaan perubahan cakupan wilayah Papua

Pada indikator 1447 dan 1451 ditemukan perubahan jumlah provinsi dari 34 menjadi 38 mulai tahun 2024.

Empat provinsi baru di wilayah Papua mulai memiliki observasi tersendiri pada periode tersebut. Pada saat yang sama, nilai indikator untuk Papua (kode wilayah 9400) mengalami peningkatan tajam dari tahun 2023 ke 2024.

Rincian perubahan:

- Indikator 1451: nilai Papua meningkat dari 36,81 pada 2023 menjadi 76,75 pada 2024.
- Indikator 1447: nilai Papua meningkat dari 33,84 pada 2023 menjadi 72,34 pada 2024.

Temuan tersebut menunjukkan adanya potensi perubahan cakupan geografis sehingga perbandingan langsung antara periode sebelum dan sesudah 2024 perlu dilakukan secara hati-hati.

Namun, bukti yang tersedia belum cukup untuk memastikan adanya perubahan definisi atau metode pengukuran. Oleh karena itu, kasus ini ditetapkan sebagai kandidat patahan seri dan masih memerlukan verifikasi metadata dari BPS.

### 2.4 Pemeriksaan konsistensi snapshot

Snapshot indikator 1221 tanggal 17 Oktober 2026 dibandingkan dengan snapshot tanggal 20 Oktober 2026.

Hasil pemeriksaan:

- Snapshot 17 Oktober: 393 observasi.
- Snapshot 20 Oktober: 393 observasi.
- Nilai berubah: 0.
- Observasi eksklusif: 0.
- Kunci ganda: 0.

Kedua snapshot memiliki isi yang identik dan tetap dipertahankan sebagai provenance untuk kebutuhan audit.

## 3. Hasil Klasifikasi Anomali

Total catatan anomali yang diperiksa adalah 152.

| Kategori akhir | Jumlah |
|---|---:|
| outlier_asli | 146 |
| kandidat_patahan_seri | 6 |
| **Total** | **152** |

Rincian status:

| Status | Jumlah |
|---|---:|
| Perlu verifikasi | 146 |
| Perlu verifikasi sumber | 6 |
| **Total** | **152** |

Enam catatan yang diklasifikasikan sebagai kandidat patahan seri adalah:

- ANM-027
- ANM-028
- ANM-135
- ANM-136
- ANM-137
- ANM-138

Catatan tersebut berkaitan dengan indikator 1447 dan 1451 untuk wilayah Papua pada tahun 2024–2025.

Beberapa catatan merujuk pada observasi yang sama tetapi berasal dari metode deteksi berbeda. Catatan tetap dipertahankan agar jejak hasil setiap metode tidak hilang.

## 4. Keputusan Penanganan Anomali

Keputusan penanganan dilakukan berdasarkan bukti pemeriksaan.

1. Sebanyak 146 catatan tetap dikategorikan sebagai outlier_asli.
2. Enam catatan Papua dikategorikan sebagai kandidat_patahan_seri.
3. Tidak ada nilai sumber yang dikoreksi, dihapus, atau diinterpolasi.
4. Kedua file register diperbarui secara konsisten.
5. Setiap keputusan penanganan didokumentasikan dalam log-keputusan.csv.

Keputusan penting yang terdokumentasi:

- K-010: pencatatan klasifikasi awal kandidat anomali.
- K-011: dokumentasi perbandingan snapshot indikator 1221.
- K-012: penyesuaian klasifikasi enam catatan anomali Papua menjadi kandidat patahan seri.

Seluruh keputusan tetap disimpan untuk menjaga keterlacakan proses analisis.

## 5. Validasi Akhir

Validasi dilakukan terhadap anomaly_register.csv, klasifikasi_anomali.csv, dan log-keputusan.csv.

Hasil validasi:

| Pemeriksaan | Hasil |
|---|---|
| Jumlah anomaly register | 152 |
| Jumlah klasifikasi anomali | 152 |
| Jumlah outlier_asli | 146 |
| Jumlah kandidat_patahan_seri | 6 |
| ID anomali ganda | Tidak ditemukan |
| Konsistensi kedua file | Lulus |
| Jumlah keputusan dalam log | 12 |
| Keberadaan file backup | Ditemukan |

Kedua file register memiliki jumlah baris dan isi yang konsisten. Tidak ditemukan ID anomali ganda.

File backup tersedia untuk kedua register sebelum perubahan klasifikasi tanggal 20 November 2026.

## 6. Keterbatasan Analisis

Beberapa keterbatasan yang perlu diperhatikan:

1. Klasifikasi outlier_asli tidak berarti seluruh nilai telah terbukti benar. Nilai tersebut tetap memerlukan verifikasi apabila ditemukan bukti tambahan.
2. Enam catatan Papua masih berstatus kandidat patahan seri karena perubahan cakupan geografis belum sepenuhnya menjelaskan perubahan definisi atau metode pengukuran.
3. Perbandingan nilai Papua sebelum dan sesudah 2024 perlu memperhatikan perubahan administrasi wilayah.
4. Persentase dari beberapa provinsi tidak boleh langsung dirata-ratakan untuk membentuk nilai gabungan tanpa memperhatikan bobot populasi dan metodologi penghitungan.
5. Perubahan data pada snapshot yang berbeda harus diperiksa sebagai kemungkinan revisi sumber, bukan langsung dianggap sebagai duplikasi atau kesalahan.

Dengan demikian, seluruh nilai sumber dipertahankan sampai tersedia bukti yang cukup untuk melakukan koreksi.

## 7. Daftar File Pendukung

File utama:

- `anomaly_register.csv`
- `klasifikasi_anomali.csv`
- `log-keputusan.csv`

File hasil pemeriksaan dan pendukung:

- `hasil_iqr_lengkap.csv`
- `hasil_iqr_temporal.csv`
- `kandidat_anomali_iqr.csv`
- `kandidat_anomali_temporal.csv`
- `ketersediaan_seri_pembanding.csv`
- `pemeriksaan_kandidat_temporal.csv`
- `perubahan_snapshot_var1221.csv`
- `profil_seri_pembanding.md`
- `ringkasan_iqr_per_tahun.csv`
- `statistik_deskriptif_per_wilayah.csv`

File backup:

- `anomaly_register.csv.backup_20261120_075025`
- `klasifikasi_anomali.csv.backup_20261120_075025`
- `anomaly_register_backup.csv`
- `anomaly_register_sebelum_tahap3.csv`

## 8. Kesimpulan

Berdasarkan pemeriksaan dan validasi yang telah dilakukan, Tahap 3 telah selesai secara operasional.

Sebanyak 152 catatan anomali berhasil diklasifikasikan, dengan 146 catatan sebagai outlier_asli dan enam catatan sebagai kandidat_patahan_seri.

Tidak ditemukan ID anomali ganda dan kedua file register telah dinyatakan konsisten. Seluruh keputusan penanganan juga telah dicatat dalam log-keputusan.csv.

Tidak ada nilai sumber yang diubah atau dihapus tanpa bukti. Enam catatan anomali Papua masih memerlukan verifikasi metadata BPS sebelum dapat ditetapkan sebagai patahan seri yang terkonfirmasi.

Dokumentasi ini menjadi dasar keterlacakan hasil pemeriksaan dan referensi untuk melanjutkan tahapan pengolahan data berikutnya.

---

**Tanggal penyelesaian:** 20 November 2026
**Tahap:** 3 – Pemeriksaan dan Klasifikasi Anomali
**Status:** Selesai secara operasional
