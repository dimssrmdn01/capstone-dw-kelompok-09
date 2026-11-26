<!-- # Laporan tim — <Nama tim>, kasus <NN> <judul kasus>

Satu dokumen bersama, enam bagian. Angka harus dapat ditarik ulang dari `data/silver`, `data/gold`,
dan `log-keputusan.csv` yang sudah di-*commit*.

## Ringkasan
Kasus, seri yang ditangani, dan satu kalimat temuan utama tentang kualitas datanya.

## Data dan lineage
Sumber dan format mentah, jumlah berkas, cara `_berkas_raw`/`_sha256_raw` dibentuk, dan hasil tarik
ulang API (bila dilakukan): apa yang berubah sejak snapshot 17–20 Oktober 2026.

## Masalah data dan penanganannya
Tabel masalah yang ditemukan (missing, outlier, patahan seri, duplikat, format, wilayah) dengan
jumlah baris terdampak, keputusan, dan alternatif yang ditolak. Rujuk id di `log-keputusan.csv`.

## Integrasi dan rekonsiliasi
Seri utama vs pembanding nasional: selisih, penjelasannya (definisi, metode, vintage, granularitas),
dan hasil analisis revisi dari arsip WDI.

## Validasi dan reproduksibilitas
Skema validasi (aturan, hasil lolos/gagal), waktu `python pipeline.py` dari nol, perbandingan pandas
vs DuckDB/Dask, dan keterbatasan yang tersisa.

## Pembagian kerja
| Anggota | NIM | Komponen | Tugas sampingan | Bagian laporan yang ditulis |
|---|---|---|---|---| -->



# Laporan Tim — Kelompok 09, Kasus 09: Pendidikan dan Akses Digital

Satu dokumen bersama yang merangkum hasil ekstraksi, profiling, pembersihan, transformasi, integrasi, validasi, dan pembagian kerja. Angka pada laporan ini mengikuti artefak yang tersedia dalam repositori proyek dan `log-keputusan.csv`.

## Ringkasan

Kelompok 09 mengolah empat seri utama BPS, yaitu APK PAUD (`var1439`), keterampilan TIK kelompok umur 1 (`var1447`), keterampilan TIK kelompok umur 2 (`var1451`), dan kepemilikan telepon genggam (`var1221`). Dua seri WDI digunakan sebagai pembanding nasional, yaitu `SE.PRE.ENRR` untuk pendidikan prasekolah dan `IT.NET.USER.ZS` untuk konteks penggunaan internet.

Temuan utama kualitas data adalah bahwa sel kosong tidak selalu berarti data hilang: sebagian terjadi karena perubahan batas wilayah atau karena provinsi belum terbentuk/belum memiliki data. Selain itu, ditemukan kandidat outlier dan enam catatan kandidat patahan seri di Papua yang perlu ditafsirkan dengan memperhatikan perubahan cakupan wilayah. Data sumber dipertahankan; tidak dilakukan imputasi atau koreksi nilai tanpa bukti.

## Data dan lineage

### Sumber dan format data mentah

Data mentah berasal dari dua sumber:

1. **BPS**, snapshot 17 Oktober 2026: empat seri utama dalam format CSV dan JSON, yaitu `var1439`, `var1447`, `var1451`, dan `var1221`.
2. **World Development Indicators (WDI)**, snapshot 20 Oktober 2026: dua berkas data indikator dan tiga berkas metadata, termasuk metadata indikator `SE.PRE.ENRR` dan `IT.NET.USER.ZS`.

`data/raw/MANIFEST.csv` memuat 17 entri berkas beserta ukuran dalam byte dan nilai SHA-256. Manifest tersebut menjadi acuan pemeriksaan integritas berkas mentah. Pada catatan ekstraksi anggota NIM 124450030, seluruh 17 berkas berhasil dibaca dan menghasilkan 4.146 baris data mentah. Hasil metrik ekstraksi tersimpan di `results/124450030/metrics.json`.

### Pembentukan lineage

Setiap baris hasil ekstraksi membawa informasi asal berkas melalui `_berkas_raw` dan sidik integritas `_sha256_raw`. `_berkas_raw` menunjukkan jalur/identitas berkas sumber yang menghasilkan baris, sedangkan `_sha256_raw` mengacu pada hash SHA-256 berkas tersebut yang tercatat pada manifest. Dengan demikian, baris hasil olahan dapat ditelusuri kembali ke berkas mentah yang digunakan. Pemeriksaan ekstraksi mencocokkan 17 berkas dengan `MANIFEST.csv`.

### Perubahan snapshot 17–20 Oktober 2026

Snapshot BPS 17 dan 20 Oktober 2026 dibandingkan untuk seri `var1221`. Masing-masing snapshot memiliki 393 observasi. Seluruh 393 kunci observasi cocok dan nilainya sama; tidak ditemukan nilai berbeda. Pada tahap Silver, snapshot terbaru (20 Oktober 2026) dipilih sebagai sumber observasi, sedangkan snapshot 17 Oktober digunakan sebagai pembanding audit. Hasil perbandingan tercatat pada `reports/snapshot-bps.csv`: 393 sel dibandingkan dan 0 nilai berbeda. Pemilihan snapshot dilakukan melalui `pilih_snapshot()` di tahap Silver. Dengan demikian, Silver hanya membawa 393 observasi dari snapshot yang dipilih, bukan menggandakan kedua snapshot sebagai observasi.

Snapshot WDI yang tercantum pada manifest adalah 20 Oktober 2026. Artefak proyek yang diperiksa tidak menyediakan tabel perbandingan antar-vintage WDI yang cukup untuk menghitung perubahan nilai antar-snapshot. Oleh karena itu, laporan ini tidak menyimpulkan ada atau tidaknya revisi nilai WDI antar-vintage.

## Masalah data dan penanganannya

| Masalah | Jumlah baris/observasi terdampak | Keputusan penanganan | Alternatif yang ditolak | Rujukan |
|---|---:|---|---|---|
| Sel kosong kategori `batas_lama` | 36 sel | Dipertahankan sebagai kosong karena periode tersebut memakai batas wilayah lama dan belum dirinci menurut provinsi hasil pemekaran. | Membagi nilai provinsi induk ke provinsi baru, mengisi nol, atau menghapus sel dari grid. | `K-005` |
| Sel kosong kategori `belum_ada` | 84 sel | Dipertahankan sebagai kosong karena provinsi belum terbentuk atau belum memiliki data pada periode terkait. | Mengisi nol, interpolasi, atau mengalokasikan nilai provinsi induk. | `K-006` |
| Sel kosong kategori `missing` | 32 sel | Dipertahankan sebagai missing karena provinsi sudah ada tetapi nilai tidak diterbitkan sumber untuk periode tersebut. | Mengisi nol, memakai nilai tahun sebelumnya, atau memakai nilai provinsi lain. | `K-007` |
| Kandidat anomali | 188 penanda anomali pada hasil terbaru | Nilai sumber tetap dipertahankan dan penanda anomali dibawa ke Gold. Klasifikasi akhir terdiri atas 100 `perbedaan_struktural`, 80 `outlier`, dan 8 `patahan_wilayah`. | Menghapus atau mengoreksi nilai hanya karena terdeteksi anomali tanpa bukti kesalahan sumber. | `reports/anomali.csv` |
| Dugaan patahan seri Papua | Kandidat yang tercatat pada analisis anomali | Lonjakan pada seri TIK di wilayah Papua ditinjau dengan memperhatikan perubahan cakupan geografis dari 34 menjadi 38 provinsi. Penanda anomali dipertahankan untuk pemeriksaan lanjutan dan tidak digunakan sebagai alasan otomatis untuk menghapus nilai. | Mengoreksi nilai Papua tanpa bukti perubahan definisi atau kesalahan input. | `reports/anomali.csv`; `K-011` |
| Duplikat/konsistensi snapshot `var1221` | 393 sel dibandingkan; 0 nilai berbeda | Kunci deduplikasi adalah `seri_kode`, `wilayah_kode`, dan `periode`. Snapshot terbaru dipilih pada tahap Silver; snapshot lama digunakan sebagai pembanding audit. | Menghapus salah satu snapshot atau menimpa snapshot lama tanpa riwayat. | `K-008`, `K-010` |
| Standardisasi satuan/format indikator | 391 baris untuk `var1439`; 0 baris terdampak untuk seri lain menurut log | `var1439` dibakukan menjadi `persen` berdasarkan definisi resmi APK PAUD BPS. `var1447`, `var1451`, dan `var1221` diseragamkan menjadi `persen`; WDI `SE.PRE.ENRR` menjadi `persen` dan `IT.NET.USER.ZS` menjadi `per 100 orang`. | Membiarkan satuan kosong/tidak seragam atau menebak satuan hanya dari rentang angka tanpa memeriksa definisi dan metadata. | `K-002`, `K-003`, `K-004` |
| Galat nilai di luar rentang satuan | 0 baris | Tidak ditemukan nilai di luar rentang satuan pada pemeriksaan Silver; tidak ada koreksi nilai berdasarkan uji rentang. | Mengubah nilai yang hanya tampak ekstrem tanpa bukti salah input. | `reports/anomali.md`; validasi |
| Pemetaan wilayah dan perubahan batas | `K-001`: dampak 0 baris dialokasikan ulang; `K-012`: 88 baris bertambah ke Silver setelah dua alias wilayah dipetakan | Wilayah dipetakan memakai kode BPS pada susunan 38 provinsi tahun 2025. Data historis tidak dialokasikan ulang ke provinsi hasil pemekaran. Nama Kep. Bangka Belitung dan Kep. Riau dinormalisasi melalui alias ke nama kanonis. | Mengalokasikan data historis ke provinsi baru dengan asumsi/bobot; menambahkan baris provinsi secara manual; mengandalkan nama mentah tanpa normalisasi. | `K-001`, `K-012` |

## Integrasi dan rekonsiliasi

### Seri utama dan pembanding nasional

Seri pembanding WDI hanya tersedia pada tingkat nasional (Indonesia/IDN), sehingga perbandingan dilakukan menggunakan agregat nasional BPS (`wilayah_kode=9999`, rincian `total`), bukan data provinsi.

| Seri utama BPS | Pembanding WDI | Irisan tahun yang tersedia | Interpretasi kesebandingan |
|---|---|---|---|
| `var1439` — APK PAUD | `SE.PRE.ENRR` — school enrollment, preprimary (% gross) | 2015–2018 (4 tahun) | Paling dekat secara konsep karena sama-sama berkaitan dengan partisipasi pendidikan prasekolah dan menggunakan satuan persen. Cakupan usia/metode tetap perlu diperhatikan: BPS menyebut usia 3–6 tahun, sedangkan definisi WDI mengikuti rasio pendaftaran bruto prasekolah. |
| `var1221` — kepemilikan telepon genggam | `IT.NET.USER.ZS` — individuals using the Internet (% of population) | 2015–2024 (10 tahun) | Pembanding kontekstual digital, bukan indikator identik. Kepemilikan telepon genggam tidak selalu berarti penggunaan internet. |
| `var1447` dan `var1451` — keterampilan TIK menurut kelompok umur | `IT.NET.USER.ZS` | 2015–2024 (10 tahun) | Pembanding konteks digital, bukan ukuran yang sama. Penggunaan internet tidak otomatis menunjukkan keterampilan TIK. |

WDI `SE.PRE.ENRR` memiliki 49 nilai terisi dari 66 observasi dan mencakup tahun 1970–2018. WDI `IT.NET.USER.ZS` memiliki 32 nilai terisi dari 66 observasi dan mencakup 1990 serta 1994–2024. Untuk periode survei utama, `SE.PRE.ENRR` tersedia pada 2015–2018, sedangkan `IT.NET.USER.ZS` tersedia pada 2015–2024. Nilai WDI tahun 2025 belum tersedia pada snapshot yang diperiksa.

### Seleksi dan pembentukan data Gold

Tahap Gold memilih observasi dari Silver untuk membentuk tabel analitis yang konsisten. Seleksi menggunakan enam seri yang telah ditetapkan dalam konfigurasi, yaitu empat seri BPS dan dua seri WDI. Observasi yang digunakan adalah periode tahunan dengan rincian `total` (termasuk padanan rincian total yang telah dinormalisasi).

Kunci observasi yang digunakan adalah kombinasi `seri_kode`, `wilayah_kode`, dan `periode`. Jika terdapat duplikasi dengan nilai sama, pemilihan dilakukan secara deterministik berdasarkan identitas berkas sumber. Jika ditemukan nilai berbeda pada kunci yang sama, proses dihentikan agar konflik tidak tersembunyi. Seleksi juga mencatat keputusan per seri pada `log-keputusan.csv` dengan ID K-013 sampai K-018. Pada hasil pipeline terakhir, seluruh 1.653 baris Silver terpilih sehingga jumlah baris yang tidak dipilih oleh aturan Gold adalah 0.

Panel provinsi dibentuk dengan menggabungkan indikator pendidikan (`var1439`, `var1447`, `var1451`) dan kepemilikan telepon genggam (`var1221`) pada kunci komposit **`provinsi × tahun`** (`wilayah_kode × periode`), dengan masing-masing seri disajikan sebagai kolom pada panel lebar. Kunci `provinsi × tahun` dipilih karena keempat seri BPS tersebut memiliki tingkat granularitas spasial (38 provinsi) dan frekuensi pencatatan tahunan yang sama, sehingga analisis keterkaitan akses perangkat digital dan capaian pendidikan antarwilayah maupun antarwaktu dapat dilakukan langsung tanpa agregasi ulang atau interpolasi periode. Grid kelengkapan tetap dipakai untuk menunjukkan sel yang tidak memiliki nilai; sel kosong tidak diisi dengan nol atau hasil imputasi. Data nasional dibentuk terpisah dari observasi Indonesia (`wilayah_kode=9999`) dengan rincian `total`, kemudian digunakan untuk rekonsiliasi BPS dan WDI.

Penanda anomali dari `reports/anomali.csv` ikut dibawa ke observasi Gold melalui kolom `anomaly_flag`, `kategori_anomali`, `tindakan_anomali`, dan `bukti_anomali`. Penanda tersebut berfungsi sebagai informasi kualitas data, bukan perintah untuk menghapus observasi. Hasil akhir memuat 188 observasi berpenanda anomali: 100 `perbedaan_struktural`, 80 `outlier`, dan 8 `patahan_wilayah`.

### Penjelasan selisih dan keterbatasan perbandingan

Perbedaan nilai antara BPS dan WDI tidak dapat langsung ditafsirkan sebagai kesalahan salah satu sumber. Interpretasi harus mempertimbangkan:

- **Definisi indikator:** APK PAUD BPS mengacu pada peserta PAUD usia 3–6 tahun, sedangkan WDI memakai definisi school enrollment preprimary (% gross).
- **Metode dan cakupan:** seri kepemilikan telepon genggam BPS, keterampilan TIK BPS, dan penggunaan internet WDI mengukur konsep yang berbeda.
- **Vintage/snapshot:** BPS `var1221` pada 17 dan 20 Oktober 2026 identik pada 393 observasi. WDI yang tersedia pada arsip ini berasal dari snapshot 20 Oktober 2026; bukti pembanding antar-vintage WDI belum tersedia untuk menyimpulkan revisi.
- **Granularitas:** WDI yang diperiksa hanya memiliki data nasional, sedangkan BPS memiliki rincian provinsi serta agregat Indonesia. Karena itu, perbandingan harus memakai baris agregat Indonesia.
- **Perubahan batas wilayah:** seri provinsi sebelum dan sesudah pemekaran tidak sepenuhnya sebanding. Nilai provinsi induk sebelum pemekaran mencakup wilayah yang kemudian menjadi provinsi baru; nilai tersebut tidak dialokasikan ulang.

### Hasil analisis revisi arsip WDI

Arsip proyek mencatat dua berkas data WDI dan metadata indikator pada snapshot 20 Oktober 2026. Namun, tidak ditemukan hasil perbandingan antar-vintage WDI yang menampilkan nilai lama, nilai baru, atau jumlah revisi. Oleh sebab itu, hasil yang dapat dipastikan dari repositori saat ini adalah ketersediaan seri dan metadata definisinya; analisis perubahan/revisi antar-arsip WDI belum dapat dinyatakan selesai berdasarkan bukti yang tersedia.

## Validasi dan reproduksibilitas

### Skema dan hasil validasi

Validasi dilakukan pada `data/silver/silver.parquet`. `reports/validasi.md` mencatat 1.653 baris dan 39 kode wilayah (38 provinsi dan Indonesia), dari sumber BPS dan WDI.

| Aturan validasi | Hasil |
|---|---|
| Kelengkapan kolom wajib | Lolos |
| Rentang nilai indikator persen (0–100) | Lolos |
| Nilai APK tidak negatif | Lolos |
| Keunikan kunci Silver | Lolos |
| Konsistensi satuan | Lolos |
| **Total** | **5 dari 5 aturan lolos** |

Validasi Gold juga dinyatakan **LOLOS**. Pemeriksaan Gold mencakup keberadaan tabel keluaran yang diwajibkan, keunikan kunci panel, kategori kelengkapan yang valid, serta konsistensi antara kategori sel dan kondisi nilai terisi atau kosong. Hasil pipeline terakhir menghasilkan 1.672 sel panel provinsi, 418 baris panel lebar, dan 14 baris rekonsiliasi nasional.

Pemeriksaan anomali juga mencatat 0 galat input di luar rentang satuan. Ini tidak berarti seluruh nilai ekstrem merupakan nilai yang sudah terverifikasi secara substantif; catatan outlier dan kandidat patahan tetap dipertahankan untuk peninjauan.

### Reproduksibilitas dan keterbatasan bukti performa

Repositori menyediakan perintah pipeline `python pipeline.py` sebagai pembangkit laporan profiling, grid kelengkapan, pembanding, metadata, dan anomali. Catatan sprint NIM 124450030 menyebut ekstraksi membaca 17 berkas dan menghasilkan 4.146 baris mentah. Hasil validasi Silver terbaru yang dilaporkan adalah 1.653 baris dengan lima aturan validasi lolos.

Pipeline dapat dijalankan melalui `python pipeline.py`. Pada eksekusi terakhir, pipeline berhasil menyelesaikan ekstraksi, Silver, Gold, dan validasi. Hasilnya mencakup 1.653 baris Silver, 1.653 observasi terpilih di Gold, 1.672 sel panel provinsi, 418 baris panel lebar, dan 14 baris rekonsiliasi nasional. `validasi_silver` dan `validasi_gold` sama-sama LOLOS.

Artefak Gold yang dihasilkan meliputi `observasi_terpilih.parquet`, `panel_provinsi.parquet`, `panel_provinsi_lebar.parquet`, `grid_kelengkapan.parquet`, `nasional.parquet`, dan `rekonsiliasi_nasional.parquet`, serta basis data `gold.sqlite`. Artefak-artefak tersebut telah dimasukkan ke commit implementasi Gold. Waktu eksekusi dari kondisi nol dan benchmark Pandas dibandingkan DuckDB/Dask belum dicatat, sehingga tidak dibuat klaim performa yang belum didukung pengukuran.
## Pembagian kerja

| Anggota | NIM | Komponen | Tugas sampingan | Bagian laporan yang ditulis |
|---|---|---|---|---|
| Michrom Muhammad Kallam | 124450030 | Ekstraksi dan lineage | Analis Utama: memimpin analisis tim, termasuk rekonsiliasi APK PAUD (`var1439`) dengan WDI `SE.PRE.ENRR`, serta `var1221` dengan WDI `IT.NET.USER.ZS`. | Ringkasan; Data dan lineage; Integrasi dan rekonsiliasi |
| Muhammad Rizaldi | 124450093 | Profil dan pembersihan | Penjaga Data & Evaluasi: menjaga kecocokan SHA-256 data mentah dengan `MANIFEST.csv`, memeriksa kualitas data, dan menjaga aturan pemilihan snapshot `var1221`. | Masalah data dan penanganannya |
| Dimas Arya Ramadhan | 124450118 | Transformasi dan panel | Koordinator: mengatur timeline sprint, membagi tugas di Papan Tim, memastikan Log Sprint dan demo tidak terlewat, serta melapor kepada pembimbing bila ada anggota yang merah. | Transformasi dan pembentukan panel; bagian hasil panel pada laporan |
| Euodia Meiliana Friedita | 124450029 | Integrasi, penyimpanan, dan skala | Integrator: menjaga agar `python pipeline.py` tetap dapat dijalankan dan mengatur penggabungan pull request. | Integrasi dan rekonsiliasi; penyimpanan dan skala |
| Shafa Delaila Azzahra | 124450124 | Validasi dan dokumentasi | Reproduksi & Demo: menguji `python pipeline.py` dari klon bersih dan menyiapkan rekaman Demo Sprint 1, 2, dan 3. | Validasi dan reproduksibilitas; dokumentasi |

**Alasan pembagian:** Kelompok beranggotakan lima orang, sehingga setiap anggota memegang tepat satu komponen dan kelima komponen terisi. Pembagian mengikuti urutan tahap pipeline agar hasil satu komponen menjadi masukan bagi komponen berikutnya. Tugas sampingan dipasangkan dengan komponen yang paling dekat agar beban kerja tetap wajar dan tidak ada anggota yang memegang dua komponen yang tidak berhubungan.
