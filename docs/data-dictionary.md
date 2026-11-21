# Data Dictionary Silver — Kelompok 09

## 1. Deskripsi

Data dictionary ini menjelaskan struktur data pada tahap Silver untuk proyek Capstone Data Wrangling Kelompok 09: Keterampilan TIK dan Pendidikan Anak Usia Dini.

Data Silver disimpan dalam format Parquet pada `data/silver/silver.parquet`. Dataset terdiri dari 1.645 baris dan 15 kolom. Dokumentasi mencakup nama kolom, tipe data, satuan, arti, serta asal data atau keputusan transformasi yang diterapkan.

## 2. Data Dictionary Kolom Silver

| No. | Nama Kolom | Tipe Data | Satuan | Arti | Asal |
|---|---|---|---|---|---|
| 1 | `sumber` | object | - | Menunjukkan sumber data, yaitu BPS atau WDI. | Berkas mentah BPS dan WDI |
| 2 | `seri_kode` | object | - | Kode unik indikator yang digunakan untuk membedakan setiap seri data. | CSV BPS dan JSON WDI |
| 3 | `wilayah_kode` | int64 | - | Kode numerik wilayah untuk mengidentifikasi provinsi atau Indonesia. | Kode wilayah BPS; pemetaan wilayah berdasarkan keputusan K-001 |
| 4 | `nama_wilayah` | object | - | Nama wilayah yang berhubungan dengan kode wilayah. | Berkas mentah BPS dan hasil pemetaan wilayah K-001 |
| 5 | `periode` | object | Tahun | Menunjukkan periode waktu pengamatan suatu indikator. | Berkas mentah BPS dan WDI |
| 6 | `jenis_periode` | object | - | Menunjukkan jenis periode pengamatan, misalnya tahunan. | Berkas mentah dan proses standardisasi Silver |
| 7 | `rincian` | object | - | Menunjukkan kategori atau rincian pengamatan, misalnya total. | Berkas mentah BPS |
| 8 | `nilai` | float64 | Mengikuti kolom `satuan` | Nilai numerik dari indikator pada wilayah dan periode tertentu. | Berkas mentah BPS dan WDI |
| 9 | `satuan` | object | Persen atau per 100 orang | Menunjukkan satuan pengukuran indikator. | Metadata sumber dan keputusan K-002, K-003, serta K-004 |
| 10 | `sdg_kode` | object | - | Kode tujuan atau target indikator Sustainable Development Goals (SDG). | Metadata indikator BPS |
| 11 | `batas_bawah` | float64 | Mengikuti metadata sumber | Batas bawah nilai indikator jika tersedia. Nilai kosong menunjukkan informasi tidak tersedia. | Metadata atau berkas mentah WDI |
| 12 | `batas_atas` | float64 | Mengikuti metadata sumber | Batas atas nilai indikator jika tersedia. Nilai kosong menunjukkan informasi tidak tersedia. | Metadata atau berkas mentah WDI |
| 13 | `rujukan_tahun` | Int64 (nullable) | Tahun | Tahun referensi yang menyertai data jika tersedia. | Metadata atau berkas mentah WDI |
| 14 | `_berkas_raw` | object | - | Lokasi relatif berkas mentah yang menjadi asal suatu baris data. | Jalur berkas pada `data/raw/` |
| 15 | `_sha256_raw` | object | - | Nilai hash SHA-256 untuk memverifikasi identitas dan integritas berkas mentah. | Hasil perhitungan hash berkas mentah |

## 3. Asal Data Indikator

Berikut pemetaan indikator Silver terhadap berkas mentah yang digunakan.

| Sumber | Kode Seri | Indikator | Berkas Mentah |
|---|---|---|---|
| BPS | `var1221` | Kepemilikan telepon genggam (SDG 5.b.1) | `bps/2026-10-20/sdg5_5_b_1_v1221.csv` |
| BPS | `var1439` | Angka Partisipasi Kasar PAUD (SDG 4.2.2) | `bps/2026-10-17/sdg4_apk_paud.csv` |
| BPS | `var1447` | Indikator keterampilan TIK (SDG 4.4.1) | `bps/2026-10-17/sdg4_4_4_1_b_v1447.csv` |
| BPS | `var1451` | Indikator keterampilan TIK (SDG 4.4.1) | `bps/2026-10-17/sdg4_4_4_1_a_v1451.csv` |
| WDI | `IT.NET.USER.ZS` | Pengguna internet (% populasi) | `wdi/2026-10-20/data/kelompok-02-hal-01.json` |
| WDI | `SE.PRE.ENRR` | Angka partisipasi kasar pendidikan prasekolah | `wdi/2026-10-20/data/kelompok-03-hal-01.json` |

## 4. Keputusan Transformasi dan Standardisasi

Beberapa kolom Silver terbentuk melalui keputusan pengolahan data yang dicatat dalam `log-keputusan.csv`.

| ID Keputusan | Seri/Kolom Terkait | Keputusan |
|---|---|---|
| K-001 | `wilayah_kode`, `nama_wilayah` | Pemetaan wilayah menggunakan susunan 38 provinsi tahun 2025 berdasarkan kode wilayah BPS. |
| K-002 | `satuan`, `seri_kode` | Satuan indikator `var1439` dibakukan menjadi persen berdasarkan definisi resmi indikator APK PAUD. |
| K-003 | `satuan`, `seri_kode` | Satuan indikator `var1447`, `var1451`, dan `var1221` dibakukan menjadi persen. |
| K-004 | `satuan`, `seri_kode` | Satuan indikator WDI ditetapkan berdasarkan metadata resmi masing-masing indikator. |
| K-005 | `nilai` | Data yang belum dirinci berdasarkan batas wilayah baru dipertahankan sebagai kategori `batas_lama`. |
| K-006 | `nilai` | Data pada periode ketika provinsi belum terbentuk dipertahankan sebagai kategori `belum_ada`. |
| K-007 | `nilai` | Data yang tidak diterbitkan oleh sumber dipertahankan sebagai `missing`, bukan diisi nol. |
| K-008 | `seri_kode`, `wilayah_kode`, `periode` | Deduplikasi dan penanganan perbedaan nilai antar-snapshot dilakukan dengan mempertahankan riwayat provenance. |
| K-009 | `nilai` | Kandidat anomali yang tidak terbukti sebagai kesalahan input dipertahankan sebagai `outlier_asli`. |
| K-010 | `var1221` | Dua snapshot BPS dibandingkan dan dipertahankan sebagai provenance karena tidak ditemukan perubahan nilai. |
| K-011 | `var1447`, `var1451` | Anomali pada Papua tahun 2024–2025 diklasifikasikan sebagai kandidat patahan seri karena perubahan cakupan wilayah. |

## 5. Contoh Penelusuran Data (Data Lineage)

Setiap baris Silver dapat ditelusuri kembali ke berkas mentah melalui kolom `_berkas_raw` dan `_sha256_raw`.

Contoh salah satu baris pada Silver:

| Atribut | Nilai |
|---|---|
| `sumber` | bps |
| `seri_kode` | var1221 |
| `wilayah_kode` | 1100 |
| `nama_wilayah` | Aceh |
| `periode` | 2015 |
| `nilai` | 51.50 |
| `satuan` | persen |
| `_berkas_raw` | `bps/2026-10-20/sdg5_5_b_1_v1221.csv` |
| `_sha256_raw` | `f7bfe811359de95b1ea3059dd541a54f62130883ac1e615c5f7f9ce33b0ca39b` |

Berdasarkan contoh tersebut, data indikator `var1221` untuk wilayah Aceh pada tahun 2015 berasal dari berkas mentah `sdg5_5_b_1_v1221.csv` pada snapshot 20 Oktober 2026.

Nilai `_sha256_raw` digunakan untuk mencocokkan integritas berkas dengan hash SHA-256 berkas mentah. Dengan demikian, asal setiap baris Silver dapat diperiksa kembali tanpa mengubah berkas Bronze.

## 6. Catatan

- Tipe data yang dicantumkan mengikuti hasil pembacaan aktual `silver.parquet` menggunakan pandas.
- Tipe `Int64` pada `rujukan_tahun` merupakan tipe integer nullable yang memungkinkan nilai kosong.
- Nilai kosong pada `batas_bawah`, `batas_atas`, dan `rujukan_tahun` tidak otomatis dianggap sebagai nol.
- Kolom Gold belum dimasukkan karena dokumentasi ini khusus untuk tahap Silver. Kolom Gold akan ditambahkan pada Sprint 2–3.
- Seluruh keputusan transformasi dan standardisasi dapat diperiksa kembali melalui `log-keputusan.csv`.