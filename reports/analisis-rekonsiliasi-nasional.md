# Analisis Rekonsiliasi Indikator Nasional

## 1. Pendahuluan

Rekonsiliasi indikator nasional dilakukan untuk membandingkan nilai indikator yang bersumber dari BPS dengan indikator pembanding dari World Development Indicators (WDI). Tujuannya adalah mengetahui perbedaan nilai antarindikator serta memberikan penjelasan berdasarkan definisi dan cakupan pengukurannya.

Data yang digunakan merupakan agregat nasional dengan `wilayah_kode = 9999` dan `rincian = total`. Pemilihan agregat nasional dilakukan karena data WDI yang digunakan tersedia pada tingkat negara.

## 2. Hasil Rekonsiliasi

Hasil pengolahan menghasilkan 14 baris rekonsiliasi yang terdiri dari dua pasangan indikator, yaitu P-01 dan P-02.

### 2.1 Pasangan P-01: APK PAUD

Indikator utama:
- Kode seri BPS: `var1439`
- Nama indikator: Angka Partisipasi Kasar (APK) PAUD
- Indikator pembanding: `SE.PRE.ENRR`
- Sumber pembanding: World Development Indicators (WDI)
- Periode perbandingan: 2015–2018

| Tahun | Nilai BPS | Nilai WDI | Selisih |
|---|---:|---:|---:|
| 2015 | 35,18 | 47,3484 | -12,1684 |
| 2016 | 34,62 | 61,8764 | -27,2564 |
| 2017 | 33,84 | 63,1931 | -29,3531 |
| 2018 | 37,92 | 62,3437 | -24,4237 |

**Analisis perbedaan:**

Berdasarkan hasil perbandingan, nilai APK PAUD dari BPS lebih rendah dibandingkan indikator `SE.PRE.ENRR` dari WDI pada seluruh periode pengamatan. Selisih terbesar terjadi pada tahun 2017, yaitu sebesar -29,3531 poin.

Perbedaan tersebut dapat berkaitan dengan cakupan pengukuran yang tidak sepenuhnya sama. Data BPS menggunakan kelompok usia 3–6 tahun, sedangkan indikator UIS menggunakan kelompok usia resmi jenjang prasekolah. Oleh karena itu, kedua indikator memiliki keterkaitan konsep, tetapi tidak dapat dianggap mengukur populasi yang sepenuhnya identik.

### 2.2 Pasangan P-02: Kepemilikan Telepon Genggam

Indikator utama:
- Kode seri BPS: `var1221`
- Nama indikator: Kepemilikan telepon genggam
- Indikator pembanding: `IT.NET.USER.ZS`
- Sumber pembanding: World Development Indicators (WDI)
- Periode perbandingan: 2015–2024

| Tahun | Nilai BPS | Nilai WDI | Selisih |
|---|---:|---:|---:|
| 2015 | 56,92 | 22,0627 | 34,8573 |
| 2016 | 58,30 | 25,4474 | 32,8526 |
| 2017 | 59,59 | 32,3358 | 27,2542 |
| 2018 | 62,41 | 39,9046 | 22,5054 |
| 2019 | 63,53 | 47,6906 | 15,8394 |
| 2020 | 62,84 | 53,7265 | 9,1135 |
| 2021 | 65,87 | 62,1045 | 3,7655 |
| 2022 | 67,88 | 66,4846 | 1,3954 |
| 2023 | 67,29 | 69,2084 | -1,9184 |
| 2024 | 68,65 | 72,7808 | -4,1308 |

**Analisis perbedaan:**

Pada tahun 2015, nilai indikator kepemilikan telepon genggam BPS sebesar 56,92, sedangkan indikator penggunaan internet WDI sebesar 22,0627. Selisih kedua indikator tersebut mencapai 34,8573 poin.

Selisih semakin kecil hingga tahun 2022 dan kemudian berubah menjadi negatif pada tahun 2023 dan 2024. Perubahan ini menunjukkan bahwa nilai penggunaan internet pada periode tersebut lebih tinggi daripada nilai kepemilikan telepon genggam.

Perbedaan terjadi karena kedua indikator mengukur aspek yang berbeda. Indikator BPS mengukur kepemilikan perangkat telepon genggam, sedangkan indikator WDI mengukur persentase individu yang menggunakan internet. Seseorang dapat menggunakan internet tanpa memiliki telepon genggam pribadi, misalnya melalui perangkat milik orang lain atau komputer.

Dengan demikian, `IT.NET.USER.ZS` digunakan sebagai pembanding kontekstual untuk melihat perkembangan penetrasi digital nasional, bukan sebagai indikator yang identik dengan kepemilikan telepon genggam.

## 3. Metode Perhitungan Selisih

Selisih antara indikator utama dan indikator pembanding dihitung menggunakan rumus:

**Selisih = Nilai indikator utama - Nilai indikator pembanding**

Interpretasi:
- Selisih positif menunjukkan nilai indikator utama lebih tinggi daripada pembanding.
- Selisih negatif menunjukkan nilai indikator utama lebih rendah daripada pembanding.
- Selisih mendekati nol menunjukkan kedua nilai semakin berdekatan, tetapi tidak berarti definisi indikatornya identik.

Seluruh perhitungan dilakukan berdasarkan pasangan indikator dan periode yang tersedia pada kedua sumber data.

## 4. Alasan Pemilihan Data

Data yang digunakan dalam rekonsiliasi merupakan agregat nasional karena WDI menyediakan data pada tingkat negara. Oleh karena itu, data BPS difilter menggunakan `wilayah_kode = 9999` dan `rincian = total`.

Pemilihan indikator pembanding mempertimbangkan keterkaitan konsep, satuan pengukuran, dan ketersediaan periode yang beririsan. Apabila tidak tersedia indikator dengan definisi yang benar-benar sama, indikator yang paling relevan digunakan sebagai pembanding kontekstual dengan mencantumkan keterbatasannya.

## 5. Kesimpulan

Berdasarkan hasil rekonsiliasi, terdapat 14 baris data yang berasal dari dua pasangan indikator, yaitu P-01 dan P-02.

Pasangan P-01 menunjukkan bahwa nilai APK PAUD BPS lebih rendah daripada indikator partisipasi prasekolah WDI selama periode 2015–2018. Perbedaan dapat berkaitan dengan cakupan usia yang digunakan oleh masing-masing sumber.

Pasangan P-02 menunjukkan perubahan selisih antara indikator kepemilikan telepon genggam dan penggunaan internet selama 2015–2024. Perbedaan tersebut terjadi karena kedua indikator memiliki definisi pengukuran yang berbeda.

Dengan demikian, hasil rekonsiliasi tidak digunakan untuk menyatakan bahwa salah satu sumber data salah, tetapi untuk mengidentifikasi perbedaan nilai, memahami karakteristik indikator, dan memberikan konteks dalam analisis data nasional.

## 6. Sumber Data

- Data indikator utama: BPS, sesuai seri yang tercatat dalam dataset proyek.
- Data indikator pembanding: World Development Indicators (WDI).
- Hasil pengolahan: `data/gold/rekonsiliasi_nasional.parquet`.
- Fungsi pembentukan tabel: `src/gold/integrasi_nasional.py`.