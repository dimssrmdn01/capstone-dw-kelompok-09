# Kategori anomali dan duplikat

Dihasilkan `python pipeline.py` (`src/silver/anomali.py`). Nilai di Silver tidak diubah kecuali galat input yang koreksinya jelas.

## Galat input (semua baris Silver diperiksa terhadap rentang satuan): 0

Tidak ada nilai di luar rentang satuannya.

## Uji patahan seri

| seri_kode   | pergantian   |   provinsi |   porsi_naik |   porsi_turun | patahan   | keterangan                                |
|:------------|:-------------|-----------:|-------------:|--------------:|:----------|:------------------------------------------|
| var1439     | 2015â†’2016  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1439     | 2016â†’2017  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1439     | 2017â†’2018  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1439     | 2018â†’2019  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1439     | 2019â†’2020  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1439     | 2020â†’2021  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1439     | 2021â†’2022  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1439     | 2022â†’2023  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1439     | 2023â†’2024  |         34 |         0.03 |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1439     | 2024â†’2025  |         38 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1451     | 2015â†’2016  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1451     | 2016â†’2017  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1451     | 2017â†’2018  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1451     | 2018â†’2019  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1451     | 2019â†’2020  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1451     | 2020â†’2021  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1451     | 2021â†’2022  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1451     | 2022â†’2023  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1451     | 2023â†’2024  |         34 |         0.03 |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1451     | 2024â†’2025  |         38 |         0.03 |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1447     | 2015â†’2016  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1447     | 2016â†’2017  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1447     | 2017â†’2018  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1447     | 2018â†’2019  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1447     | 2019â†’2020  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1447     | 2020â†’2021  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1447     | 2021â†’2022  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1447     | 2022â†’2023  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1447     | 2023â†’2024  |         34 |         0.03 |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1447     | 2024â†’2025  |         38 |         0.03 |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1221     | 2015â†’2016  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1221     | 2016â†’2017  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1221     | 2017â†’2018  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1221     | 2018â†’2019  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1221     | 2019â†’2020  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1221     | 2020â†’2021  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1221     | 2021â†’2022  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1221     | 2022â†’2023  |         34 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1221     | 2023â†’2024  |         34 |         0.03 |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |
| var1221     | 2024â†’2025  |         38 |         0    |             0 | tidak     | ambang lompat 50%, porsi serentak â‰¥ 50% |

## Pergantian definisi yang dinyatakan penerbit

Tidak ada.

## Cakupan parsial yang dinyatakan penerbit

Tidak ada.

## Perubahan batas wilayah di tengah panel: 8

| seri_kode   | induk       |   wilayah_kode |   periode | anak                                          |   nilai_sebelum |   nilai_sesudah |
|:------------|:------------|---------------:|----------:|:----------------------------------------------|----------------:|----------------:|
| var1439     | Papua       |           9100 |      2024 | Papua Selatan, Papua Tengah, Papua Pegunungan |           11.94 |           20.5  |
| var1439     | Papua Barat |           9200 |      2024 | Papua Barat Daya                              |           25.66 |           31.92 |
| var1451     | Papua       |           9100 |      2024 | Papua Selatan, Papua Tengah, Papua Pegunungan |           36.81 |           76.75 |
| var1451     | Papua Barat |           9200 |      2024 | Papua Barat Daya                              |           76.93 |           80.17 |
| var1447     | Papua       |           9100 |      2024 | Papua Selatan, Papua Tengah, Papua Pegunungan |           33.84 |           72.34 |
| var1447     | Papua Barat |           9200 |      2024 | Papua Barat Daya                              |           70.38 |           73.44 |
| var1221     | Papua       |           9100 |      2024 | Papua Selatan, Papua Tengah, Papua Pegunungan |           37.95 |           67.97 |
| var1221     | Papua Barat |           9200 |      2024 | Papua Barat Daya                              |           65.76 |           68.29 |

Nilai induk sebelum periode ini mencakup wilayah provinsi pemekaran; sesudahnya tidak. Perubahannya bukan tren dan tidak diratakan.

## Calon anomali dan kategorinya (188)

| seri_kode   | nama_wilayah              |   periode |   nilai | arah                              | kategori             | tindakan                                                      |
|:------------|:--------------------------|----------:|--------:|:----------------------------------|:---------------------|:--------------------------------------------------------------|
| var1221     | Papua                     |      2015 |   32.04 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Nusa Tenggara Timur       |      2016 |   37.96 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua                     |      2016 |   34.24 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | DKI Jakarta               |      2017 |   76.99 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Nusa Tenggara Timur       |      2017 |   40.97 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua                     |      2017 |   36.31 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | DKI Jakarta               |      2018 |   76.16 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Nusa Tenggara Timur       |      2018 |   43.91 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua                     |      2018 |   40.46 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Nusa Tenggara Timur       |      2019 |   45.01 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua                     |      2019 |   38.5  | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Aceh                      |      2020 |   59.6  | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Nusa Tenggara Timur       |      2020 |   44.12 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Sulawesi Barat            |      2020 |   54.41 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Papua                     |      2020 |   40.44 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Kepulauan Riau            |      2021 |   81.83 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | DKI Jakarta               |      2021 |   67.83 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Jawa Barat                |      2021 |   62.76 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Nusa Tenggara Timur       |      2021 |   51.92 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Kalimantan Timur          |      2021 |   81.1  | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Papua                     |      2021 |   38.94 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Kepulauan Bangka Belitung |      2022 |   73.16 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Kepulauan Riau            |      2022 |   79.88 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | DKI Jakarta               |      2022 |   82.27 | ke bawah + perubahan              | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Jawa Barat                |      2022 |   70.37 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Nusa Tenggara Timur       |      2022 |   52.73 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Kalimantan Timur          |      2022 |   82.37 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Papua                     |      2022 |   35.33 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | DKI Jakarta               |      2023 |   82.47 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Nusa Tenggara Timur       |      2023 |   51.36 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Kalimantan Timur          |      2023 |   81.75 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Papua                     |      2023 |   37.95 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Kepulauan Riau            |      2024 |   83.9  | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | DKI Jakarta               |      2024 |   83.43 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Kalimantan Timur          |      2024 |   83.1  | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Papua                     |      2024 |   67.97 | perubahan + ke samping            | patahan_wilayah      | tandai; jangan bandingkan induk sebelum dan sesudah pemekaran |
| var1221     | Papua Selatan             |      2024 |   50.08 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Tengah              |      2024 |   33.7  | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Pegunungan          |      2024 |   15.76 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Kepulauan Riau            |      2025 |   82.18 | ke bawah + perubahan              | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | DKI Jakarta               |      2025 |   84.47 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Nusa Tenggara Timur       |      2025 |   55.97 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Kalimantan Timur          |      2025 |   84.04 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Maluku                    |      2025 |   68.64 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1221     | Papua                     |      2025 |   68.56 | ke samping                        | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Selatan             |      2025 |   50.67 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Tengah              |      2025 |   37.35 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1221     | Papua Pegunungan          |      2025 |   22.49 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta             |      2015 |   70.11 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur                |      2015 |   52.89 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Nusa Tenggara Timur       |      2015 |   23.42 | ke samping                        | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Gorontalo                 |      2015 |   45.29 | ke samping                        | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Sumatera Selatan          |      2016 |   20.78 | ke samping                        | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | DI Yogyakarta             |      2016 |   68.47 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur                |      2016 |   51.9  | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Kalimantan Utara          |      2016 |   28.02 | ke samping                        | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Gorontalo                 |      2016 |   45.29 | ke samping                        | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Sulawesi Barat            |      2016 |   38.84 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | DI Yogyakarta             |      2017 |   69.14 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur                |      2017 |   51.85 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua                     |      2017 |   10.68 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Kepulauan Riau            |      2018 |   28.31 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | DI Yogyakarta             |      2018 |   69.8  | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur                |      2018 |   56.9  | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Kalimantan Selatan        |      2018 |   47.27 | ke samping                        | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Sulawesi Tengah           |      2018 |   41.77 | ke samping                        | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Maluku                    |      2018 |   30.77 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Papua                     |      2018 |   13.17 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DKI Jakarta               |      2019 |   43.08 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | DI Yogyakarta             |      2019 |   67.75 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur                |      2019 |   55.7  | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Sulawesi Tenggara         |      2019 |   34.69 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Papua                     |      2019 |   11.66 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Lampung                   |      2020 |   35.13 | ke samping                        | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | DKI Jakarta               |      2020 |   39.44 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | DI Yogyakarta             |      2020 |   67.46 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur                |      2020 |   56.24 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Banten                    |      2020 |   30.44 | ke samping                        | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Papua                     |      2020 |   11.47 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Aceh                      |      2021 |   32.7  | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | DI Yogyakarta             |      2021 |   64.76 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur                |      2021 |   53.33 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Nusa Tenggara Timur       |      2021 |   32.59 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Gorontalo                 |      2021 |   50.18 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Sulawesi Barat            |      2021 |   43.38 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Maluku Utara              |      2021 |   38.76 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Papua                     |      2021 |   10.51 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta             |      2022 |   62.98 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur                |      2022 |   52.18 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua                     |      2022 |   12.71 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta             |      2023 |   63.06 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur                |      2023 |   53.54 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua                     |      2023 |   11.94 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta             |      2024 |   65.67 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur                |      2024 |   53.92 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua                     |      2024 |   20.5  | perubahan + ke samping            | patahan_wilayah      | tandai; jangan bandingkan induk sebelum dan sesudah pemekaran |
| var1439     | Papua Barat               |      2024 |   31.92 | perubahan + ke samping            | patahan_wilayah      | tandai; jangan bandingkan induk sebelum dan sesudah pemekaran |
| var1439     | Papua Tengah              |      2024 |    9.98 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Papua Pegunungan          |      2024 |    3.08 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | DI Yogyakarta             |      2025 |   67.63 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Jawa Timur                |      2025 |   55.6  | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Sulawesi Barat            |      2025 |   39.22 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Maluku Utara              |      2025 |   31.4  | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Papua                     |      2025 |   21.71 | ke samping                        | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1439     | Papua Barat               |      2025 |   25.27 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1439     | Papua Pegunungan          |      2025 |    3.1  | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Kepulauan Riau            |      2015 |   43.42 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | DKI Jakarta               |      2015 |   53.25 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | DI Yogyakarta             |      2015 |   43.16 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | Kepulauan Riau            |      2016 |   50.1  | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | DKI Jakarta               |      2016 |   58.4  | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | DI Yogyakarta             |      2016 |   49.23 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | Kalimantan Timur          |      2016 |   46.11 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | DKI Jakarta               |      2017 |   71.39 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | DKI Jakarta               |      2018 |   77.14 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | DI Yogyakarta             |      2018 |   68.82 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | Papua                     |      2018 |   24.23 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Kepulauan Riau            |      2019 |   77.18 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | DKI Jakarta               |      2019 |   85.17 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua                     |      2019 |   26.45 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | DKI Jakarta               |      2020 |   88.08 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Banten                    |      2020 |   69.35 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | Papua                     |      2020 |   30.93 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Kepulauan Riau            |      2021 |   89.06 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | DKI Jakarta               |      2021 |   91.79 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | DI Yogyakarta             |      2021 |   84.72 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | Papua                     |      2021 |   30.58 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua                     |      2022 |   29.82 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Lampung                   |      2023 |   78.79 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | DKI Jakarta               |      2023 |   93.98 | perubahan                         | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua                     |      2023 |   33.84 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Kalimantan Utara          |      2024 |   87.16 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | Papua                     |      2024 |   72.34 | perubahan + ke samping            | patahan_wilayah      | tandai; jangan bandingkan induk sebelum dan sesudah pemekaran |
| var1447     | Papua Selatan             |      2024 |   58.01 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Tengah              |      2024 |   31.5  | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Pegunungan          |      2024 |    8.27 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Kepulauan Riau            |      2025 |   96.64 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1447     | Papua                     |      2025 |   75.43 | ke samping                        | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Selatan             |      2025 |   59.14 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Tengah              |      2025 |   35.18 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Pegunungan          |      2025 |   18.67 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | DKI Jakarta               |      2015 |   80.01 | ke samping                        | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | DI Yogyakarta             |      2015 |   83.22 | ke bawah + ke samping             | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua                     |      2015 |   17.03 | ke samping                        | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | DI Yogyakarta             |      2016 |   85.43 | ke samping                        | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua                     |      2018 |   33.48 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | DI Yogyakarta             |      2019 |   97.91 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Nusa Tenggara Barat       |      2019 |   77.54 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Kalimantan Tengah         |      2019 |   80.96 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Sulawesi Barat            |      2019 |   68.06 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua                     |      2019 |   32.88 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Kepulauan Riau            |      2020 |   90.65 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Nusa Tenggara Timur       |      2020 |   58.4  | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua                     |      2020 |   39.06 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Nusa Tenggara Timur       |      2021 |   75.2  | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Maluku Utara              |      2021 |   70.33 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua                     |      2021 |   34.95 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Barat               |      2021 |   74.27 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Nusa Tenggara Timur       |      2022 |   77.3  | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Sulawesi Barat            |      2022 |   90.41 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Maluku                    |      2022 |   78.51 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Maluku Utara              |      2022 |   77.48 | ke bawah + perubahan              | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua                     |      2022 |   33.06 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Barat               |      2022 |   76.29 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Nusa Tenggara Timur       |      2023 |   79.65 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Maluku                    |      2023 |   82.8  | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Maluku Utara              |      2023 |   81.01 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua                     |      2023 |   36.81 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Barat               |      2023 |   76.93 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Nusa Tenggara Timur       |      2024 |   82.5  | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Kalimantan Utara          |      2024 |   94.81 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Maluku                    |      2024 |   83.22 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua                     |      2024 |   76.75 | ke bawah + perubahan + ke samping | patahan_wilayah      | tandai; jangan bandingkan induk sebelum dan sesudah pemekaran |
| var1451     | Papua Barat               |      2024 |   80.17 | ke bawah                          | patahan_wilayah      | tandai; jangan bandingkan induk sebelum dan sesudah pemekaran |
| var1451     | Papua Selatan             |      2024 |   56.08 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Tengah              |      2024 |   33.31 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Pegunungan          |      2024 |    9.74 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Barat Daya          |      2024 |   79.71 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Nusa Tenggara Timur       |      2025 |   86.4  | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Maluku                    |      2025 |   89.41 | perubahan                         | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua                     |      2025 |   78.79 | ke bawah + ke samping             | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Barat               |      2025 |   83.62 | ke bawah                          | outlier              | tandai, nilai tidak diubah                                    |
| var1451     | Papua Selatan             |      2025 |   57.49 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Tengah              |      2025 |   37.06 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Pegunungan          |      2025 |   15.79 | ke bawah + perubahan              | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1451     | Papua Barat Daya          |      2025 |   82.98 | ke bawah                          | perbedaan_struktural | tandai sekali per provinsi; bukan kejadian satu tahun         |
| var1447     | Papua Barat               |      2024 |   73.44 | normal                            | patahan_wilayah      | tandai; jangan bandingkan induk sebelum dan sesudah pemekaran |
| var1221     | Papua Barat               |      2024 |   68.29 | normal                            | patahan_wilayah      | tandai; jangan bandingkan induk sebelum dan sesudah pemekaran |

Outlier di sini adalah outlier statistik. Menyebutnya *outlier asli* butuh penjelasan dunia nyata (kebijakan, bencana, cakupan survei); kolom itu diisi tim saat Sprint 2 bila buktinya ditemukan.

## Duplikat dua format BPS (CSV vs JSON)

Tidak ada seri BPS dua format.

## Kunci Silver kembar: 0