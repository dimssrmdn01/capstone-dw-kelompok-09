# Ketersediaan seri pembanding nasional

Dihasilkan `python pipeline.py` (`src/silver/pembanding.py`). Tahun survei seri utama: 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025.

## Ringkasan per seri dan rincian

| seri_kode      | sumber   | rincian   | satuan        |   jumlah_tahun |   awal |   akhir | tahun_survei_utama_tersedia                                | batas_bawah_atas   |
|:---------------|:---------|:----------|:--------------|---------------:|-------:|--------:|:-----------------------------------------------------------|:-------------------|
| IT.NET.USER.ZS | wdi      | total     | per 100 orang |             32 |   1990 |    2024 | 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024 | tidak              |
| SE.PRE.ENRR    | wdi      | total     | persen        |             49 |   1970 |    2018 | 2015, 2016, 2017, 2018                                     | tidak              |

## WDI: baris ada vs nilai ada

Tidak ada seri WDI.

## Ketersediaan pada tahun survei seri utama (1 = ada)

| seri_kode      | rincian   |   2015 |   2016 |   2017 |   2018 |   2019 |   2020 |   2021 |   2022 |   2023 |   2024 |
|:---------------|:----------|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|-------:|
| IT.NET.USER.ZS | total     |      1 |      1 |      1 |      1 |      1 |      1 |      1 |      1 |      1 |      1 |
| SE.PRE.ENRR    | total     |      1 |      1 |      1 |      1 |      0 |      0 |      0 |      0 |      0 |      0 |

## Rincian yang kandidat sebanding

| pasangan   | seri_utama   | pembanding             | alasan                                                                                                                                                                                                                                                                                                                                                                                             |
|:-----------|:-------------|:-----------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| P-01       | var1439      | SE.PRE.ENRR (total)    | Dipilih agregat nasional (wilayah_kode=9999, rincian=total) karena WDI hanya menyediakan data tingkat negara. SE.PRE.ENRR dipilih untuk dibandingkan dengan var1439 (APK PAUD) karena sama-sama mengukur Angka Partisipasi Kasar jenjang prasekolah dalam satuan persen (irisan tahun 2015-2018), dengan catatan beda cakupan usia (BPS 3-6 tahun vs UIS usia resmi).                              |
| P-02       | var1221      | IT.NET.USER.ZS (total) | Dipilih agregat nasional (wilayah_kode=9999, rincian=total) karena WDI hanya menyediakan data tingkat negara. IT.NET.USER.ZS dipilih sebagai pembanding kontekstual bagi var1221 (kepemilikan telepon genggam) serta var1447/var1451 (keterampilan TIK) karena tidak tersedia seri kepemilikan ponsel identik di WDI dan keduanya merepresentasikan penetrasi digital nasional (irisan 2015-2024). |

Matriks lengkap seri x rincian x tahun: `reports/ketersediaan-pembanding.csv`.