# Metadata seri: nama, satuan, kode SDG

Dihasilkan `python pipeline.py` dari berkas mentah dan `src/konfigurasi.py`. Tabel lengkap ada di `docs/seri.csv`. Bila katalog dan berkas mentah berbeda, berkas mentah yang dipakai dan koreksinya dicatat di `log-keputusan.csv`.

## Nama di berkas mentah dan nama baku

| seri_kode   | nama_di_berkas   | nama_baku                                                            |
|:------------|:-----------------|:---------------------------------------------------------------------|
| var1439     |                  | Angka Partisipasi Kasar PAUD usia 3-6 tahun                          |
| var1451     |                  | Proporsi keterampilan TIK usia 15-24 tahun                           |
| var1447     |                  | Proporsi keterampilan TIK usia 15-59 tahun                           |
| var1221     |                  | Proporsi individu usia 5 tahun ke atas yang memiliki telepon genggam |

## Satuan dan kode SDG

| seri_kode   | katalog_satuan   | satuan           | bukti_satuan                                         | katalog_sdg   | sdg_kode   |
|:------------|:-----------------|:-----------------|:-----------------------------------------------------|:--------------|:-----------|
| var1439     | Tidak tercantum  | tidak_dinyatakan | Kolom satuan pada CSV BPS tidak mencantumkan satuan. | 4.2.2         | 4.2.2      |
| var1451     | Persen           | persen           | Kolom satuan pada CSV BPS mencantumkan Persen.       | 4.4.1         | 4.4.1      |
| var1447     | Persen           | persen           | Kolom satuan pada CSV BPS mencantumkan Persen.       | 4.4.1         | 4.4.1      |
| var1221     | Persen           | persen           | Kolom satuan pada CSV BPS mencantumkan Persen.       | 5.b.1         | 5.b.1      |

## Koreksi katalog

Tidak ada.

## Catatan BPS (var.note)

Tidak ada seri BPS.

## Metadata WDI yang muncul di lebih dari satu berkas

Tidak ada.

## Judul dengan spasi di awal/akhir

Tidak ada.