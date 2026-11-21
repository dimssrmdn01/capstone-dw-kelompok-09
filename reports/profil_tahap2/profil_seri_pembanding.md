# Profil Seri Pembanding WDI dan BPS

## 1. Tujuan

Profil ini mengidentifikasi ketersediaan dua seri pembanding World Development Indicators (WDI), yaitu SE.PRE.ENRR dan IT.NET.USER.ZS, serta mencocokkannya dengan seri utama BPS berdasarkan wilayah, periode, rincian, dan satuan.

## 2. Hasil pemeriksaan WDI

| Kode | Indikator | Observasi | Nilai terisi | Nilai kosong | Tahun dengan nilai |
|---|---|---:|---:|---:|---|
| SE.PRE.ENRR | School enrollment, preprimary (% gross) | 66 | 49 | 17 | 1970-2018 |
| IT.NET.USER.ZS | Individuals using the Internet (% of population) | 66 | 32 | 34 | 1990; 1994-2024 |

Kedua indikator hanya memiliki observasi untuk Indonesia (IDN), tanpa rincian provinsi, jenis kelamin, atau kelompok umur pada data yang diperiksa.

Kolom unit pada data dan metadata WDI kosong. Satuan diidentifikasi berdasarkan definisi indikator:
- SE.PRE.ENRR: persentase bruto (gross enrollment ratio).
- IT.NET.USER.ZS: persentase penduduk yang menggunakan internet.

Kedua kode ditemukan pada metadata sumber2 dan sumber46. Kemunculan pada dua metadata tersebut dicatat sebagai informasi sumber, bukan dianggap sebagai observasi tambahan.

## 3. Hasil pemeriksaan seri utama BPS

Empat seri BPS yang diperiksa memiliki baris agregat nasional (INDONESIA), rincian Tidak ada, dan tahun tercantum 2015-2025.

| Kode | Indikator | Rincian | Satuan pada CSV |
|---|---|---|---|
| 1439 | APK PAUD | Tidak ada | Kosong |
| 1447 | Keterampilan TIK kelompok umur 1 | Tidak ada | Persen |
| 1451 | Keterampilan TIK kelompok umur 2 | Tidak ada | Persen |
| 1221 | Kepemilikan telepon seluler | Tidak ada | Persen |

Satuan APK PAUD (var1439) belum dapat dipastikan dari kolom satuan CSV yang diperiksa. Karena itu, satuannya tidak diasumsikan.

## 4. Irisan periode

- SE.PRE.ENRR memiliki nilai pada 2015-2018, sehingga beririsan empat tahun dengan periode BPS 2015-2025.
- IT.NET.USER.ZS memiliki nilai pada 2015-2024, sehingga beririsan sepuluh tahun dengan periode BPS 2015-2025.
- Tahun 2025 belum memiliki nilai untuk IT.NET.USER.ZS pada berkas yang diperiksa.
- Keempat seri BPS memiliki 11 dari 11 nilai nasional terisi pada periode 2015-2025. Dengan demikian, seluruh tahun tersebut benar-benar tersedia untuk analisis.

## 5. Kandidat seri yang sebanding

### SE.PRE.ENRR dengan BPS var1439 (APK PAUD)

**Kandidat utama.** Keduanya berkaitan dengan partisipasi pendidikan anak usia prasekolah dan memiliki agregat wilayah Indonesia. Definisi WDI menggunakan rasio pendaftaran bruto, sehingga kesebandingan konsep cukup dekat dengan APK PAUD. Irisan periode yang memiliki nilai WDI adalah 2015-2018.

Keterbatasannya adalah satuan var1439 masih kosong pada kolom sumber yang diperiksa. Definisi operasional dan kesesuaian metodologi perlu dipastikan sebelum analisis langsung.

### IT.NET.USER.ZS dengan BPS var1447 dan var1451

**Kandidat pembanding konteks digital, bukan ukuran identik.** WDI mengukur proporsi penduduk pengguna internet, sedangkan kedua seri BPS mengukur keterampilan TIK menurut kelompok umur. Penggunaan internet tidak otomatis menunjukkan tingkat keterampilan TIK.

Keduanya memiliki agregat Indonesia dan irisan tahun 2015-2024. Perbedaan konsep dan rincian kelompok umur harus dipertahankan dalam interpretasi.

### IT.NET.USER.ZS dengan BPS var1221

**Kandidat pembanding konteks digital, bukan ukuran identik.** WDI mengukur penggunaan internet, sedangkan BPS var1221 mengukur kepemilikan telepon seluler. Kepemilikan perangkat tidak selalu berarti seseorang menggunakan internet.

Keduanya memiliki agregat Indonesia dan irisan tahun 2015-2024.

## 6. Kesimpulan

SE.PRE.ENRR merupakan kandidat pembanding paling dekat untuk APK PAUD (var1439), dengan irisan empat tahun. IT.NET.USER.ZS dapat digunakan sebagai indikator konteks digital untuk seri keterampilan TIK maupun kepemilikan telepon seluler, dengan irisan sepuluh tahun, tetapi tidak boleh diperlakukan sebagai ukuran yang sama.

Karena seri WDI yang diperiksa hanya tersedia pada tingkat nasional, perbandingan langsung harus menggunakan agregat Indonesia dari BPS, bukan data provinsi. Nilai kosong tidak boleh dianggap sebagai nol atau diimputasi tanpa dasar.

## 7. Sumber data

- WDI: data/raw/wdi/2026-10-20/data/kelompok-02-hal-01.json
- WDI: data/raw/wdi/2026-10-20/data/kelompok-03-hal-01.json
- WDI metadata: data/raw/wdi/2026-10-20/metadata/sumber2_indikator.json
- WDI metadata: data/raw/wdi/2026-10-20/metadata/sumber46_indikator.json
- BPS: data/raw/bps/2026-10-17/sdg4_apk_paud.csv
- BPS: data/raw/bps/2026-10-17/sdg4_4_4_1_a_v1451.csv
- BPS: data/raw/bps/2026-10-17/sdg4_4_4_1_b_v1447.csv
- BPS: data/raw/bps/2026-10-17/sdg5_5_b_1_v1221.csv

