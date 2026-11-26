# Kelengkapan panel provinsi dan kategori sel kosong

Dihasilkan `python pipeline.py` (`src/silver/grid.py`). Grid = 38 provinsi susunan 2025 x periode yang diterbitkan seri itu. Persen dari 38 menghitung semua sel; persen dari seharusnya hanya menghitung sel yang provinsinya sudah ada dan tidak dinyatakan tidak terbit oleh penerbit.

## Persen sel terisi per seri per periode

| seri_kode   |   periode |   sel |   terisi |   seharusnya_ada |   persen_dari_38 |   persen_dari_seharusnya |
|:------------|----------:|------:|---------:|-----------------:|-----------------:|-------------------------:|
| var1221     |      2015 |    38 |       34 |               34 |             89.5 |                      100 |
| var1221     |      2016 |    38 |       34 |               34 |             89.5 |                      100 |
| var1221     |      2017 |    38 |       34 |               34 |             89.5 |                      100 |
| var1221     |      2018 |    38 |       34 |               34 |             89.5 |                      100 |
| var1221     |      2019 |    38 |       34 |               34 |             89.5 |                      100 |
| var1221     |      2020 |    38 |       34 |               34 |             89.5 |                      100 |
| var1221     |      2021 |    38 |       34 |               34 |             89.5 |                      100 |
| var1221     |      2022 |    38 |       34 |               34 |             89.5 |                      100 |
| var1221     |      2023 |    38 |       34 |               34 |             89.5 |                      100 |
| var1221     |      2024 |    38 |       38 |               38 |            100   |                      100 |
| var1221     |      2025 |    38 |       38 |               38 |            100   |                      100 |
| var1439     |      2015 |    38 |       34 |               34 |             89.5 |                      100 |
| var1439     |      2016 |    38 |       34 |               34 |             89.5 |                      100 |
| var1439     |      2017 |    38 |       34 |               34 |             89.5 |                      100 |
| var1439     |      2018 |    38 |       34 |               34 |             89.5 |                      100 |
| var1439     |      2019 |    38 |       34 |               34 |             89.5 |                      100 |
| var1439     |      2020 |    38 |       34 |               34 |             89.5 |                      100 |
| var1439     |      2021 |    38 |       34 |               34 |             89.5 |                      100 |
| var1439     |      2022 |    38 |       34 |               34 |             89.5 |                      100 |
| var1439     |      2023 |    38 |       34 |               34 |             89.5 |                      100 |
| var1439     |      2024 |    38 |       38 |               38 |            100   |                      100 |
| var1439     |      2025 |    38 |       38 |               38 |            100   |                      100 |
| var1447     |      2015 |    38 |       34 |               34 |             89.5 |                      100 |
| var1447     |      2016 |    38 |       34 |               34 |             89.5 |                      100 |
| var1447     |      2017 |    38 |       34 |               34 |             89.5 |                      100 |
| var1447     |      2018 |    38 |       34 |               34 |             89.5 |                      100 |
| var1447     |      2019 |    38 |       34 |               34 |             89.5 |                      100 |
| var1447     |      2020 |    38 |       34 |               34 |             89.5 |                      100 |
| var1447     |      2021 |    38 |       34 |               34 |             89.5 |                      100 |
| var1447     |      2022 |    38 |       34 |               34 |             89.5 |                      100 |
| var1447     |      2023 |    38 |       34 |               34 |             89.5 |                      100 |
| var1447     |      2024 |    38 |       38 |               38 |            100   |                      100 |
| var1447     |      2025 |    38 |       38 |               38 |            100   |                      100 |
| var1451     |      2015 |    38 |       34 |               34 |             89.5 |                      100 |
| var1451     |      2016 |    38 |       34 |               34 |             89.5 |                      100 |
| var1451     |      2017 |    38 |       34 |               34 |             89.5 |                      100 |
| var1451     |      2018 |    38 |       34 |               34 |             89.5 |                      100 |
| var1451     |      2019 |    38 |       34 |               34 |             89.5 |                      100 |
| var1451     |      2020 |    38 |       34 |               34 |             89.5 |                      100 |
| var1451     |      2021 |    38 |       34 |               34 |             89.5 |                      100 |
| var1451     |      2022 |    38 |       34 |               34 |             89.5 |                      100 |
| var1451     |      2023 |    38 |       34 |               34 |             89.5 |                      100 |
| var1451     |      2024 |    38 |       38 |               38 |            100   |                      100 |
| var1451     |      2025 |    38 |       38 |               38 |            100   |                      100 |

## Jumlah sel per kategori (provinsi)

| seri_kode   |   batas_lama |   belum_ada |   terisi |
|:------------|-------------:|------------:|---------:|
| var1221     |            8 |          28 |      382 |
| var1439     |            8 |          28 |      382 |
| var1447     |            8 |          28 |      382 |
| var1451     |            8 |          28 |      382 |

## Baris Indonesia

| seri_kode   |   periode | kategori   | bukti   |
|:------------|----------:|:-----------|:--------|
| var1439     |      2015 | terisi     |         |
| var1439     |      2016 | terisi     |         |
| var1439     |      2017 | terisi     |         |
| var1439     |      2018 | terisi     |         |
| var1439     |      2019 | terisi     |         |
| var1439     |      2020 | terisi     |         |
| var1439     |      2021 | terisi     |         |
| var1439     |      2022 | terisi     |         |
| var1439     |      2023 | terisi     |         |
| var1439     |      2024 | terisi     |         |
| var1439     |      2025 | terisi     |         |
| var1451     |      2015 | terisi     |         |
| var1451     |      2016 | terisi     |         |
| var1451     |      2017 | terisi     |         |
| var1451     |      2018 | terisi     |         |
| var1451     |      2019 | terisi     |         |
| var1451     |      2020 | terisi     |         |
| var1451     |      2021 | terisi     |         |
| var1451     |      2022 | terisi     |         |
| var1451     |      2023 | terisi     |         |
| var1451     |      2024 | terisi     |         |
| var1451     |      2025 | terisi     |         |
| var1447     |      2015 | terisi     |         |
| var1447     |      2016 | terisi     |         |
| var1447     |      2017 | terisi     |         |
| var1447     |      2018 | terisi     |         |
| var1447     |      2019 | terisi     |         |
| var1447     |      2020 | terisi     |         |
| var1447     |      2021 | terisi     |         |
| var1447     |      2022 | terisi     |         |
| var1447     |      2023 | terisi     |         |
| var1447     |      2024 | terisi     |         |
| var1447     |      2025 | terisi     |         |
| var1221     |      2015 | terisi     |         |
| var1221     |      2016 | terisi     |         |
| var1221     |      2017 | terisi     |         |
| var1221     |      2018 | terisi     |         |
| var1221     |      2019 | terisi     |         |
| var1221     |      2020 | terisi     |         |
| var1221     |      2021 | terisi     |         |
| var1221     |      2022 | terisi     |         |
| var1221     |      2023 | terisi     |         |
| var1221     |      2024 | terisi     |         |
| var1221     |      2025 | terisi     |         |

## Batas pemakaian panel

| seri_kode   | tingkat   |   periode_pertama |   periode_terakhir |   jumlah_periode |
|:------------|:----------|------------------:|-------------------:|-----------------:|
| var1221     | nasional  |              2015 |               2025 |               11 |
| var1221     | provinsi  |              2015 |               2025 |               11 |
| var1439     | nasional  |              2015 |               2025 |               11 |
| var1439     | provinsi  |              2015 |               2025 |               11 |
| var1447     | nasional  |              2015 |               2025 |               11 |
| var1447     | provinsi  |              2015 |               2025 |               11 |
| var1451     | nasional  |              2015 |               2025 |               11 |
| var1451     | provinsi  |              2015 |               2025 |               11 |

Provinsi yang belum ada pada sebagian periode panel: Papua Barat Daya, Papua Pegunungan, Papua Selatan, Papua Tengah.

Tahun sesudah periode terakhir di luar jangkauan panel; panel tidak menggambarkan keadaan tahun itu. Tahun di antara dua periode survei tidak termasuk grid dan tidak diisi di Silver.

Daftar semua sel kosong beserta buktinya: `reports/grid-sel-kosong.csv`.

