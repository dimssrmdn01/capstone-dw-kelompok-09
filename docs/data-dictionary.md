# Data dictionary — Kelompok 09

Dokumen ini menjelaskan struktur keluaran Silver pada `data/silver/silver.parquet`.
Informasi tipe data mengacu pada hasil pemeriksaan aktual terhadap berkas Silver.
Kolom Gold belum didokumentasikan karena akan ditambahkan pada Sprint 2–3.

## `data/silver/silver.parquet`

| Kolom | Tipe data | Satuan/format | Boleh kosong | Rentang atau nilai sah | Asal (berkas/aturan) | Keterangan |
|---|---|---|---|---|---|---|
| `sumber` | `object` (teks) | Nama sumber | Tidak | `bps`, `wdi` pada data yang diperiksa | Nama sumber pada proses ekstraksi; berkas di `data/raw/` | Menunjukkan sumber data indikator. |
| `seri_kode` | `object` (teks) | Kode seri/indikator | Tidak | Kode seri dari sumber, misalnya `var1221`, `var1439`, `var1447`, `var1451`, `IT.NET.USER.ZS`, `SE.PRE.ENRR` | BPS: metadata/kode seri pada berkas CSV; WDI: kode indikator pada berkas JSON | Identitas indikator dari sumber data. |
| `wilayah_kode` | `int64` | Kode wilayah BPS dikalikan 100 | Tidak | Kode wilayah hasil standardisasi; contoh `1100` untuk Aceh | Pemetaan kode wilayah berdasarkan keputusan `K-001` pada `log-keputusan.csv` | Kode numerik wilayah yang digunakan pada Silver. |
| `nama_wilayah` | `object` (teks) | Nama wilayah | Tidak | Nama wilayah yang dipetakan dari kode wilayah | Berkas sumber dan pemetaan wilayah berdasarkan `K-001` | Nama provinsi/wilayah yang bersesuaian dengan `wilayah_kode`. |
| `periode` | `object` (teks) | Tahun/periode | Tidak | Periode yang tersedia pada sumber; contoh `2015` | Kolom periode pada berkas mentah, dinormalisasi pada proses Silver | Menyatakan periode pengamatan indikator. |
| `jenis_periode` | `object` (teks) | Kategori periode | Tidak | Contoh `tahun` | Standardisasi periode pada proses Silver berdasarkan informasi periode sumber | Menjelaskan jenis periode pengamatan. |
| `rincian` | `object` (teks) | Kategori rincian | Tidak pada data yang diperiksa | Contoh `total`; kategori mengikuti rincian pada sumber | Kolom rincian/kategori pada berkas mentah jika tersedia; standardisasi Silver | Menjelaskan kelompok atau rincian nilai indikator. |
| `nilai` | `float64` | Mengikuti `satuan` | Dapat kosong jika sumber tidak menyediakan nilai | Nilai numerik dari sumber; indikator persentase umumnya 0–100, dengan pengecualian indikator seperti APK yang dapat melebihi 100 | Nilai indikator pada berkas mentah; normalisasi satuan mengacu pada `K-002`, `K-003`, dan `K-004` | Nilai pengamatan indikator. Jangan menerapkan batas 100 secara umum pada APK. |
| `satuan` | `object` (teks) | Satuan indikator | Dapat kosong jika metadata sumber tidak tersedia | Contoh `persen` dan `per 100 orang` | Metadata sumber dan keputusan normalisasi satuan pada `K-002` sampai `K-004` | Satuan yang menjelaskan cara membaca `nilai`. |
| `sdg_kode` | `object` (teks) | Kode target/indikator SDG | Dapat kosong jika tidak tersedia pada sumber | Kode SDG sesuai metadata, misalnya `5.b.1` | Metadata/katalog indikator BPS jika tersedia | Menghubungkan seri dengan kode indikator SDG. |
| `batas_bawah` | `float64` | Mengikuti satuan indikator | Ya | Nilai numerik atau kosong (`NaN`) | Metadata sumber jika tersedia; dipertahankan kosong jika tidak tersedia | Batas bawah/rentang acuan indikator jika disediakan sumber. |
| `batas_atas` | `float64` | Mengikuti satuan indikator | Ya | Nilai numerik atau kosong (`NaN`) | Metadata sumber jika tersedia; dipertahankan kosong jika tidak tersedia | Batas atas/rentang acuan indikator jika disediakan sumber. |
| `rujukan_tahun` | `Int64` (integer nullable) | Tahun | Ya | Tahun numerik atau kosong (`<NA>`) | Metadata sumber jika tersedia; dipertahankan kosong jika tidak tersedia | Tahun rujukan yang menyertai indikator jika disediakan sumber. |
| `_berkas_raw` | `object` (teks) | Path relatif dari berkas mentah | Tidak | Path berkas di bawah `data/raw/` | Diisi oleh proses ekstraksi/provenance pipeline | Menyimpan lokasi berkas mentah asal baris Silver. |
| `_sha256_raw` | `object` (teks) | SHA-256 heksadesimal | Tidak | Hash SHA-256 dari berkas mentah | Dihitung dari berkas mentah oleh proses ekstraksi/provenance pipeline | Sidik jari berkas mentah untuk memeriksa identitas/integritas sumber. |

## Asal berkas sumber yang tercatat

| Sumber/seri | Berkas mentah |
|---|---|
| BPS `var1221` | `bps/2026-10-20/sdg5_5_b_1_v1221.csv` |
| BPS `var1439` | `bps/2026-10-17/sdg4_apk_paud.csv` |
| BPS `var1447` | `bps/2026-10-17/sdg4_4_4_1_b_v1447.csv` |
| BPS `var1451` | `bps/2026-10-17/sdg4_4_4_1_a_v1451.csv` |
| WDI `IT.NET.USER.ZS` | `wdi/2026-10-20/data/kelompok-02-hal-01.json` |
| WDI `SE.PRE.ENRR` | `wdi/2026-10-20/data/kelompok-03-hal-01.json` |

Path di atas merupakan contoh berkas sumber yang teridentifikasi pada data yang diperiksa. Nilai `_berkas_raw` pada setiap baris menunjukkan berkas asal baris tersebut.

## Keputusan pengolahan yang memengaruhi Silver

Keputusan pengolahan dicatat pada `log-keputusan.csv`. Keputusan yang relevan dengan interpretasi kolom Silver antara lain:

- `K-001`: pemetaan 38 provinsi berdasarkan kode BPS; data historis tidak dialokasikan mundur ke provinsi hasil pemekaran.
- `K-002`: satuan indikator BPS `var1439` (APK PAUD usia 3–6 tahun) dinormalisasi menjadi persen.
- `K-003`: satuan indikator BPS `var1447`, `var1451`, dan `var1221` dinormalisasi menjadi persen berdasarkan metadata.
- `K-004`: satuan WDI `SE.PRE.ENRR` dicatat sebagai persen dan `IT.NET.USER.ZS` sebagai `per 100 orang`.
- `K-005` dan `K-006`: nilai kosong akibat batas wilayah lama atau wilayah yang belum terbentuk dipertahankan dengan status yang sesuai.
- `K-007`: nilai kosong karena sumber tidak menerbitkan data dipertahankan sebagai `missing`.
- `K-008`: penanganan duplikasi mempertimbangkan seri, wilayah, dan periode serta tetap menjaga provenance snapshot/revisi.
- `K-009`: kandidat anomali dipertahankan sebagai `outlier_asli`.
- `K-010`: dua snapshot BPS untuk `var1221` dibandingkan; masing-masing berisi 393 observasi, tanpa perubahan, data eksklusif, maupun kunci duplikat.
- `K-011`: enam anomali Papua tahun 2024–2025 pada `var1447` dan `var1451` ditandai sebagai `kandidat_patahan_seri` karena perubahan cakupan provinsi.

## Contoh penelusuran satu baris Silver ke berkas mentah

Contoh berikut diambil dari salah satu baris Silver yang diperiksa:

| Kolom | Nilai contoh |
|---|---|
| `sumber` | `bps` |
| `seri_kode` | `var1221` |
| `wilayah_kode` | `1100` |
| `nama_wilayah` | `Aceh` |
| `periode` | `2015` |
| `jenis_periode` | `tahun` |
| `rincian` | `total` |
| `nilai` | `51.50` |
| `satuan` | `persen` |
| `sdg_kode` | `5.b.1` |
| `batas_bawah` | kosong (`NaN`) |
| `batas_atas` | kosong (`NaN`) |
| `rujukan_tahun` | kosong (`<NA>`) |
| `_berkas_raw` | `bps/2026-10-20/sdg5_5_b_1_v1221.csv` |
| `_sha256_raw` | `f7bfe811359de95b1ea3059dd541a54f62130883ac1e615c5f7f9ce33b0ca39b` |

Cara menelusurinya:

1. Baca nilai `_berkas_raw` untuk mengetahui path relatif berkas mentah asal data.
2. Cari berkas tersebut di bawah direktori `data/raw/`.
3. Cocokkan `_sha256_raw` dengan hash SHA-256 berkas mentah untuk memastikan berkas yang digunakan sama dengan berkas sumber yang tercatat.
4. Gunakan `seri_kode`, `wilayah_kode`, dan `periode` untuk menemukan observasi yang bersesuaian di dalam berkas mentah.

## data/gold/

Kolom Gold akan ditambahkan pada Sprint 2–3 setelah tabel Gold dibentuk. Karena itu, bagian ini belum diisi.
