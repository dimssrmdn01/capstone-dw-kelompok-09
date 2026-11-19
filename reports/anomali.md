# Kategori anomali dan duplikat

Dihasilkan `python pipeline.py` (`src/silver/anomali.py`). Nilai di Silver tidak diubah kecuali galat input yang koreksinya jelas.

## Galat input (semua baris Silver diperiksa terhadap rentang satuan): 0

Tidak ada nilai di luar rentang satuannya.

## Uji patahan seri

| seri_kode   | pergantian   |   provinsi |   porsi_naik |   porsi_turun | patahan   | keterangan                              |
|:------------|:-------------|-----------:|-------------:|--------------:|:----------|:----------------------------------------|
| var1439     | 2015→2016    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1439     | 2016→2017    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1439     | 2017→2018    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1439     | 2018→2019    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1439     | 2019→2020    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1439     | 2020→2021    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1439     | 2021→2022    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1439     | 2022→2023    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1439     | 2023→2024    |         34 |         0.03 |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1439     | 2024→2025    |         37 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1451     | 2015→2016    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1451     | 2016→2017    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1451     | 2017→2018    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1451     | 2018→2019    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1451     | 2019→2020    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1451     | 2020→2021    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1451     | 2021→2022    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1451     | 2022→2023    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1451     | 2023→2024    |         34 |         0.03 |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1451     | 2024→2025    |         37 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1447     | 2015→2016    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1447     | 2016→2017    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1447     | 2017→2018    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1447     | 2018→2019    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1447     | 2019→2020    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1447     | 2020→2021    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1447     | 2021→2022    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1447     | 2022→2023    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1447     | 2023→2024    |         34 |         0.03 |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1447     | 2024→2025    |         37 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1221     | 2015→2016    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1221     | 2016→2017    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1221     | 2017→2018    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1221     | 2018→2019    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1221     | 2019→2020    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1221     | 2020→2021    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1221     | 2021→2022    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1221     | 2022→2023    |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1221     | 2023→2024    |         34 |         0.03 |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |
| var1221     | 2024→2025    |         37 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak ≥ 50% |

## Pergantian definisi yang dinyatakan penerbit

Tidak ada.

## Cakupan parsial yang dinyatakan penerbit

Tidak ada.

## Perubahan batas wilayah di tengah panel: 4

| seri_kode   | induk   |   wilayah_kode |   periode | anak        |   nilai_sebelum |   nilai_sesudah |
|:------------|:--------|---------------:|----------:|:------------|----------------:|----------------:|
| var1439     | Papua   |           9100 |      2024 | Papua Barat |           25.66 |           31.92 |
| var1451     | Papua   |           9100 |      2024 | Papua Barat |           76.93 |           80.17 |
| var1447     | Papua   |           9100 |      2024 | Papua Barat |           70.38 |           73.44 |
| var1221     | Papua   |           9100 |      2024 | Papua Barat |           65.76 |           68.29 |

Nilai induk sebelum periode ini mencakup wilayah provinsi pemekaran; sesudahnya tidak. Perubahannya bukan tren dan tidak diratakan.

## Calon anomali dan kategorinya (128)

| seri_kode   | nama_wilayah        |   periode |   nilai | arah   | kategori             | tindakan                                                      |
|:------------|:--------------------|----------:|--------:|:-------|:---------------------|:--------------------------------------------------------------|
| var1439     | DI Yogyakarta       |      2015 |   70.11 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta       |      2016 |   68.47 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta       |      2017 |   69.14 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta       |      2018 |   69.8  | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta       |      2019 |   67.75 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta       |      2020 |   67.46 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta       |      2021 |   64.76 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta       |      2022 |   62.98 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta       |      2023 |   63.06 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta       |      2024 |   65.67 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta       |      2025 |   67.63 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur          |      2015 |   52.89 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur          |      2016 |   51.9  | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur          |      2017 |   51.85 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur          |      2018 |   56.9  | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur          |      2019 |   55.7  | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur          |      2020 |   56.24 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur          |      2021 |   53.33 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur          |      2022 |   52.18 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur          |      2023 |   53.54 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur          |      2024 |   53.92 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur          |      2025 |   55.6  | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua Tengah        |      2017 |   10.68 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua Tengah        |      2018 |   13.17 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua Tengah        |      2019 |   11.66 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua Tengah        |      2020 |   11.47 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua Tengah        |      2021 |   10.51 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua Tengah        |      2022 |   12.71 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua Tengah        |      2023 |   11.94 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua Barat Daya    |      2024 |    9.98 | rendah | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | DI Yogyakarta       |      2015 |   83.22 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Nusa Tenggara Timur |      2020 |   58.4  | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Nusa Tenggara Timur |      2021 |   75.2  | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Nusa Tenggara Timur |      2022 |   77.3  | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Nusa Tenggara Timur |      2023 |   79.65 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Nusa Tenggara Timur |      2024 |   82.5  | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Nusa Tenggara Timur |      2025 |   86.4  | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Maluku              |      2022 |   78.51 | rendah | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Maluku              |      2023 |   82.8  | rendah | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Maluku              |      2024 |   83.22 | rendah | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Maluku Utara        |      2021 |   70.33 | rendah | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Maluku Utara        |      2022 |   77.48 | rendah | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Maluku Utara        |      2023 |   81.01 | rendah | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Maluku Utara        |      2024 |   84.92 | rendah | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Maluku Utara        |      2025 |   89.2  | rendah | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua               |      2021 |   74.27 | rendah | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua               |      2022 |   76.29 | rendah | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua               |      2023 |   76.93 | rendah | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua               |      2024 |   80.17 | rendah | patahan_wilayah      | tandai; jangan bandingkan induk sebelum dan sesudah pemekaran |
| var1451     | Papua               |      2025 |   83.62 | rendah | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua Barat         |      2024 |   79.71 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Barat         |      2025 |   82.98 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Tengah        |      2018 |   33.48 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Tengah        |      2019 |   32.88 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Tengah        |      2020 |   39.06 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Tengah        |      2021 |   34.95 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Tengah        |      2022 |   33.06 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Tengah        |      2023 |   36.81 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Tengah        |      2024 |   76.75 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Tengah        |      2025 |   78.79 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Pegunungan    |      2024 |   56.08 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Pegunungan    |      2025 |   57.49 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Barat Daya    |      2024 |   33.31 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Barat Daya    |      2025 |   37.06 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Kepulauan Riau      |      2015 |   43.42 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | Kepulauan Riau      |      2016 |   50.1  | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | Kepulauan Riau      |      2019 |   77.18 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | Kepulauan Riau      |      2021 |   89.06 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | DKI Jakarta         |      2015 |   53.25 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | DKI Jakarta         |      2016 |   58.4  | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | DKI Jakarta         |      2017 |   71.39 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | DKI Jakarta         |      2018 |   77.14 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | DKI Jakarta         |      2019 |   85.17 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | DKI Jakarta         |      2020 |   88.08 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | DKI Jakarta         |      2021 |   91.79 | tinggi | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | DI Yogyakarta       |      2015 |   43.16 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | DI Yogyakarta       |      2016 |   49.23 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | DI Yogyakarta       |      2018 |   68.82 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | DI Yogyakarta       |      2021 |   84.72 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | Papua Tengah        |      2018 |   24.23 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Tengah        |      2019 |   26.45 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Tengah        |      2020 |   30.93 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Tengah        |      2021 |   30.58 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Tengah        |      2022 |   29.82 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Tengah        |      2023 |   33.84 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Pegunungan    |      2024 |   58.01 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Pegunungan    |      2025 |   59.14 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Barat Daya    |      2024 |   31.5  | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Barat Daya    |      2025 |   35.18 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Kepulauan Riau      |      2021 |   81.83 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Kepulauan Riau      |      2024 |   83.9  | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Kepulauan Riau      |      2025 |   82.18 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | DKI Jakarta         |      2017 |   76.99 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | DKI Jakarta         |      2022 |   82.27 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | DKI Jakarta         |      2023 |   82.47 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | DKI Jakarta         |      2024 |   83.43 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | DKI Jakarta         |      2025 |   84.47 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Nusa Tenggara Timur |      2016 |   37.96 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Nusa Tenggara Timur |      2017 |   40.97 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Nusa Tenggara Timur |      2018 |   43.91 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Nusa Tenggara Timur |      2019 |   45.01 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Nusa Tenggara Timur |      2020 |   44.12 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Nusa Tenggara Timur |      2021 |   51.92 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Nusa Tenggara Timur |      2022 |   52.73 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Nusa Tenggara Timur |      2023 |   51.36 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Nusa Tenggara Timur |      2024 |   53.96 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Nusa Tenggara Timur |      2025 |   55.97 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Kalimantan Timur    |      2021 |   81.1  | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Kalimantan Timur    |      2022 |   82.37 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Kalimantan Timur    |      2023 |   81.75 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Kalimantan Timur    |      2024 |   83.1  | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Kalimantan Timur    |      2025 |   84.04 | tinggi | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Papua Tengah        |      2015 |   32.04 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Tengah        |      2016 |   34.24 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Tengah        |      2017 |   36.31 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Tengah        |      2018 |   40.46 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Tengah        |      2019 |   38.5  | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Tengah        |      2020 |   40.44 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Tengah        |      2021 |   38.94 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Tengah        |      2022 |   35.33 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Tengah        |      2023 |   37.95 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Pegunungan    |      2024 |   50.08 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Pegunungan    |      2025 |   50.67 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Barat Daya    |      2024 |   33.7  | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Barat Daya    |      2025 |   37.35 | rendah | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua               |      2024 |   31.92 | normal | patahan_wilayah      | tandai; jangan bandingkan induk sebelum dan sesudah pemekaran |
| var1447     | Papua               |      2024 |   73.44 | normal | patahan_wilayah      | tandai; jangan bandingkan induk sebelum dan sesudah pemekaran |
| var1221     | Papua               |      2024 |   68.29 | normal | patahan_wilayah      | tandai; jangan bandingkan induk sebelum dan sesudah pemekaran |

Outlier di sini adalah outlier statistik. Menyebutnya *outlier asli* butuh penjelasan dunia nyata (kebijakan, bencana, cakupan survei); kolom itu diisi tim saat Sprint 2 bila buktinya ditemukan.

## Duplikat dua format BPS (CSV vs JSON)

Tidak ada seri BPS dua format.

## Kunci Silver kembar: 0