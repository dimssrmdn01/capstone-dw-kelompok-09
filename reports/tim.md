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

### Penyimpanan SQL dan alasan pilihan basis data

`python pipeline.py` membangun ulang `data/gold/gold.sqlite` dari nol pada setiap eksekusi. Strukturnya mengikuti DDL di `src/gold/skema.sql`, sedangkan pemuatannya dilakukan oleh `src/gold/penyimpanan.py`. Berkas basis data (sekitar 5 MB) tidak di-commit (`*.sqlite` di `.gitignore`) karena selalu dapat dibangun ulang dari `data/raw/`. Setiap tabel memiliki kunci primer dan tipe kolom yang eksplisit. Setelah pemuatan, jumlah baris SQL dicocokkan dengan jumlah baris Parquet; pipeline berhenti bila ada yang berbeda atau bila kolom DataFrame tidak cocok dengan DDL. Hasil pemuatan terakhir dicatat otomatis di `reports/penyimpanan-sql.md`:

| Lapis | Tabel SQL | Kunci primer | Baris SQL = Parquet |
|---|---|---|---:|
| Bronze | `mentah_dokumen` | `_berkas_raw` | 12 dokumen JSON |
| Silver | `silver` | `sumber, seri_kode, wilayah_kode, periode, rincian, _berkas_raw` | 1.653 |
| Gold | `observasi_terpilih` | `seri_kode, wilayah_kode, periode` | 1.653 |
| Gold | `grid_kelengkapan` | `seri_kode, wilayah_kode, periode` | 1.716 |
| Gold | `panel_provinsi` | `seri_kode, wilayah_kode, periode` | 1.672 |
| Gold | `panel_provinsi_lebar` | `wilayah_kode, periode` | 418 |
| Gold | `nasional` | `seri_kode, wilayah_kode, periode` | 125 |
| Gold | `rekonsiliasi_nasional` | `pasangan, periode` | 89 |

Kunci primer Silver sama dengan kunci unik skema minimal starter. Kunci Gold mengikuti aturan satu nilai per sel (`seri_kode × wilayah_kode × periode`). Selain kunci primer, DDL memuat sejumlah `CHECK` yang menegakkan aturan Gold langsung di basis data: `nilai` terisi jika dan hanya jika `kategori = 'terisi'`, `anomaly_flag` bernilai 0/1, `nasional.wilayah_kode = 9999`, dan baris rekonsiliasi berpasangan wajib memiliki selisih serta kategori dari daftar baku. `periode` disimpan sebagai `TEXT` agar format `2020-S1`/`2020-Q3` tetap sah, dan sel kosong disimpan sebagai `NULL`, bukan nol.

**Mengapa SQLite untuk Silver dan Gold.** SQLite dipilih karena tidak membutuhkan server, termasuk dalam pustaka standar Python, dan disimpan sebagai satu berkas. Dengan begitu, `python pipeline.py` dari klon bersih langsung menghasilkan basis data yang sama di laptop setiap anggota tanpa instalasi atau kredensial tambahan. Volume data kecil (ribuan baris), sehingga keunggulan PostgreSQL (konkurensi banyak penulis, hak akses) tidak terpakai. DuckDB lebih cocok untuk agregasi kolumnar berukuran besar dan disiapkan untuk tahap 7 (arsip WDI 142 rilis), tetapi untuk tabel kecil yang menuntut keunikan kunci, kunci primer dan `CHECK` di SQLite sudah memadai.

**Dibandingkan menyimpan respons JSON mentah sebagai dokumen.** Ke-12 berkas JSON mentah tetap disimpan utuh di `mentah_dokumen` (sekitar 3,8 juta karakter, `CHECK (json_valid(isi))`) sebagai salinan Bronze yang dapat diaudit dengan `_sha256_raw`. Namun, dokumen tidak cocok dijadikan lapis analisis:

- **Bentuk tiap sumber berbeda.** BPS menyimpan nilai dalam `datacontent` dengan kunci berupa gabungan kode (`vervar` + `var` + `turvar` + kode tahun + `turtahun`, misalnya `1500143901150`) dan dipecah menjadi empat halaman per berkas, sedangkan WDI berupa larik `[metadata, [observasi]]`. Kueri harus menguraikan struktur yang berbeda untuk setiap sumber.
- **Kueri lebih lambat.** Mengambil `SE.PRE.ENRR` 2015–2018 dari dokumen (`json_each` + `json_extract`) membutuhkan sekitar 48 ms. Kueri yang sama pada tabel `nasional` hanya sekitar 0,2 ms karena memakai indeks kunci primer.
- **Keunikan tidak bisa ditegakkan.** Dokumen tidak dapat menolak observasi ganda. Pada tabel relasional, sisipan duplikat ke `nasional` ditolak (`UNIQUE constraint failed: nasional.seri_kode, nasional.wilayah_kode, nasional.periode`).

Kesimpulannya, pendekatan dokumen dipakai untuk lapis mentah, di mana bentuk asli harus dipertahankan, sedangkan tabel relasional berkunci primer dipakai untuk Silver dan Gold, yang membutuhkan skema tetap, keunikan kunci, dan kueri lintas seri. Keputusan ini dicatat sebagai `K-019`.

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

### Tabel rekonsiliasi dan kategori selisih

`data/gold/rekonsiliasi_nasional.parquet` (juga tabel SQL `rekonsiliasi_nasional`) dibuat oleh `pipeline.py` melalui `src/gold/integrasi_nasional.py`. Satu baris mewakili satu pasangan × periode. Rumusnya `selisih = nilai_utama − nilai_pembanding`. Kolom `status_pasangan` menandai `berpasangan`, `hanya_utama`, atau `hanya_pembanding`, sehingga periode tanpa pasangan tetap tampil. Selisih tidak dihapus, tidak dibulatkan menjadi sama, dan tidak dikoreksi. Teks penjelasan dan bukti setiap pasangan disimpan di `src/konfigurasi.py` (`PASANGAN[*]["rekonsiliasi"]`). Pipeline berhenti bila ada baris berpasangan tanpa kategori, kategori di luar daftar baku, atau baris *belum terjelaskan* tanpa dugaan dan bukti.

| Pasangan | Berpasangan | Hanya utama | Hanya pembanding | Kategori baris berpasangan |
|---|---:|---:|---:|---|
| P-01 `var1439` vs `SE.PRE.ENRR` | 4 (2015–2018) | 7 (2019–2025) | 45 (1970–2014) | 3 *definisi berbeda*, 1 *belum terjelaskan* (2015) |
| P-02 `var1221` vs `IT.NET.USER.ZS` | 10 (2015–2024) | 1 (2025) | 22 (1990, 1994–2014) | 10 *definisi berbeda* |

| Pasangan | Tahun | Utama | Pembanding | Selisih | Kategori |
|---|---|---:|---:|---:|---|
| P-01 | 2015 | 35,18 | 47,35 | −12,17 | belum terjelaskan |
| P-01 | 2016 | 34,62 | 61,88 | −27,26 | definisi berbeda |
| P-01 | 2017 | 33,84 | 63,19 | −29,35 | definisi berbeda |
| P-01 | 2018 | 37,92 | 62,34 | −24,42 | definisi berbeda |
| P-02 | 2015 | 56,92 | 22,06 | 34,86 | definisi berbeda |
| P-02 | 2016 | 58,30 | 25,45 | 32,85 | definisi berbeda |
| P-02 | 2017 | 59,59 | 32,34 | 27,25 | definisi berbeda |
| P-02 | 2018 | 62,41 | 39,90 | 22,51 | definisi berbeda |
| P-02 | 2019 | 63,53 | 47,69 | 15,84 | definisi berbeda |
| P-02 | 2020 | 62,84 | 53,73 | 9,11 | definisi berbeda |
| P-02 | 2021 | 65,87 | 62,10 | 3,77 | definisi berbeda |
| P-02 | 2022 | 67,88 | 66,48 | 1,40 | definisi berbeda |
| P-02 | 2023 | 67,29 | 69,21 | −1,92 | definisi berbeda |
| P-02 | 2024 | 68,65 | 72,78 | −4,13 | definisi berbeda |

Median selisih absolut ke-14 baris berpasangan adalah 19,17 poin.

**P-01, definisi berbeda (2016–2018).** Kelompok umur acuannya berbeda. APK PAUD BPS dihitung terhadap penduduk umur 3–6 tahun dari Susenas (`var.note` di `sdg4_apk_paud.json`: "APK PAUD 3-6 Tahun"). `SE.PRE.ENRR` membagi seluruh peserta prasekolah, berapa pun umurnya, dengan penduduk pada kelompok umur *resmi* jenjang prasekolah (sourceNote di `wdi/2026-10-20/metadata/sumber2_indikator.json`). Kelompok umur resmi lebih sempit daripada 3–6 tahun, sehingga penyebut UIS lebih kecil dan rasionya lebih tinggi; ini konsisten dengan WDI yang selalu berada di atas BPS. Perbedaan sumber (survei rumah tangga vs data administratif UIS) dicatat sebagai perbedaan metode sekunder. Rentang umur resmi prasekolah Indonesia tidak tercantum di berkas mentah, sehingga besaran efek penyebut belum dihitung.

**P-01, belum terjelaskan (2015).** Perbedaan definisi menjelaskan mengapa WDI lebih tinggi, tetapi tidak menjelaskan mengapa selisih 2015 (−12,17) jauh lebih kecil daripada 2016–2018. *Dugaan:* WDI 2015 (47,35) turun 10,53 poin dari 2014 (57,88) lalu naik 14,53 poin ke 2016 (61,88), sementara BPS stabil (35,18 → 34,62). Pola turun-naik satu tahun yang hanya muncul di WDI mengarah ke perubahan cakupan data administratif UIS atau revisi penyebut penduduk pada tahun tersebut. *Bukti yang sudah dicari:* `obs_status` `SE.PRE.ENRR` 2014–2016 di `kelompok-02-hal-01.json` kosong (tidak ditandai estimasi), dan metadata WDI tidak menyebut patahan seri. *Belum diperiksa:* arsip WDI 142 rilis (tahap 7), untuk melihat apakah nilai 2015 berubah antar-rilis. Bila berubah, kategori baris ini akan diganti menjadi *vintage berbeda*.

**P-02, definisi berbeda (2015–2024).** Pasangan ini bersifat kontekstual. `var1221` mengukur individu umur 5 tahun ke atas yang menguasai/memiliki telepon genggam (Susenas Kor), sedangkan `IT.NET.USER.ZS` mengukur individu yang memakai internet dari lokasi dan perangkat apa pun dalam tiga bulan terakhir (ITU), terhadap seluruh penduduk. Selisih positif besar pada 2015 berarti banyak pemilik ponsel belum memakai internet. Selisih menyempit setiap tahun dan berbalik negatif sejak 2023, karena penggunaan internet tumbuh lebih cepat (22,06 → 72,78) daripada kepemilikan ponsel (56,92 → 68,65) dan internet dapat dipakai tanpa memiliki ponsel sendiri. Perbedaan penyebut (umur 5+ vs seluruh penduduk) merupakan perbedaan cakupan sekunder.

Keputusan cakupan tabel (semua periode tampil, satu kategori per baris berpasangan) dicatat sebagai `K-020`, dan klasifikasi P-01 2015 sebagai `K-021`.

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

Validasi Gold juga dinyatakan **LOLOS**. Pemeriksaan Gold mencakup keberadaan tabel keluaran yang diwajibkan, keunikan kunci panel, kategori kelengkapan yang valid, serta konsistensi antara kategori sel dan kondisi nilai terisi atau kosong. Hasil pipeline terakhir menghasilkan 1.672 sel panel provinsi, 418 baris panel lebar, dan 89 baris rekonsiliasi nasional (14 berpasangan).

Pemeriksaan anomali juga mencatat 0 galat input di luar rentang satuan. Ini tidak berarti seluruh nilai ekstrem merupakan nilai yang sudah terverifikasi secara substantif; catatan outlier dan kandidat patahan tetap dipertahankan untuk peninjauan.

### Reproduksibilitas dan keterbatasan bukti performa

Repositori menyediakan perintah pipeline `python pipeline.py` sebagai pembangkit laporan profiling, grid kelengkapan, pembanding, metadata, dan anomali. Catatan sprint NIM 124450030 menyebut ekstraksi membaca 17 berkas dan menghasilkan 4.146 baris mentah. Hasil validasi Silver terbaru yang dilaporkan adalah 1.653 baris dengan lima aturan validasi lolos.

Pipeline dapat dijalankan melalui `python pipeline.py`. Pada eksekusi terakhir, pipeline berhasil menyelesaikan ekstraksi, Silver, Gold, dan validasi. Hasilnya mencakup 1.653 baris Silver, 1.653 observasi terpilih di Gold, 1.672 sel panel provinsi, 418 baris panel lebar, dan 89 baris rekonsiliasi nasional (14 berpasangan). `validasi_silver` dan `validasi_gold` sama-sama LOLOS.

Artefak Gold yang dihasilkan meliputi `observasi_terpilih.parquet`, `panel_provinsi.parquet`, `panel_provinsi_lebar.parquet`, `grid_kelengkapan.parquet`, `nasional.parquet`, dan `rekonsiliasi_nasional.parquet`, serta basis data `gold.sqlite`. Berkas Parquet di-commit; `gold.sqlite` tidak di-commit karena dibangun ulang oleh pipeline dan jumlah barisnya dicocokkan dengan Parquet (lihat *Penyimpanan SQL dan alasan pilihan basis data*). Waktu eksekusi dari kondisi nol dan benchmark Pandas dibandingkan DuckDB/Dask belum dicatat, sehingga tidak dibuat klaim performa yang belum didukung pengukuran.
## Pembagian kerja

| Anggota | NIM | Komponen | Tugas sampingan | Bagian laporan yang ditulis |
|---|---|---|---|---|
| Michrom Muhammad Kallam | 124450030 | Ekstraksi dan lineage | Analis Utama: memimpin analisis tim, termasuk rekonsiliasi APK PAUD (`var1439`) dengan WDI `SE.PRE.ENRR`, serta `var1221` dengan WDI `IT.NET.USER.ZS`. | Ringkasan; Data dan lineage; Integrasi dan rekonsiliasi |
| Muhammad Rizaldi | 124450093 | Profil dan pembersihan | Penjaga Data & Evaluasi: menjaga kecocokan SHA-256 data mentah dengan `MANIFEST.csv`, memeriksa kualitas data, dan menjaga aturan pemilihan snapshot `var1221`. | Masalah data dan penanganannya |
| Dimas Arya Ramadhan | 124450118 | Transformasi dan panel | Koordinator: mengatur timeline sprint, membagi tugas di Papan Tim, memastikan Log Sprint dan demo tidak terlewat, serta melapor kepada pembimbing bila ada anggota yang merah. | Transformasi dan pembentukan panel; bagian hasil panel pada laporan |
| Euodia Meiliana Friedita | 124450029 | Integrasi, penyimpanan, dan skala | Integrator: menjaga agar `python pipeline.py` tetap dapat dijalankan dan mengatur penggabungan pull request. | Integrasi dan rekonsiliasi; penyimpanan dan skala |
| Shafa Delaila Azzahra | 124450124 | Validasi dan dokumentasi | Reproduksi & Demo: menguji `python pipeline.py` dari klon bersih dan menyiapkan rekaman Demo Sprint 1, 2, dan 3. | Validasi dan reproduksibilitas; dokumentasi |

**Alasan pembagian:** Kelompok beranggotakan lima orang, sehingga setiap anggota memegang tepat satu komponen dan kelima komponen terisi. Pembagian mengikuti urutan tahap pipeline agar hasil satu komponen menjadi masukan bagi komponen berikutnya. Tugas sampingan dipasangkan dengan komponen yang paling dekat agar beban kerja tetap wajar dan tidak ada anggota yang memegang dua komponen yang tidak berhubungan.
