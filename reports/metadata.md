# Metadata seri: nama, satuan, kode SDG

Dihasilkan `python pipeline.py` dari berkas mentah dan `src/konfigurasi.py`. Tabel lengkap ada di `docs/seri.csv`. Bila katalog dan berkas mentah berbeda, berkas mentah yang dipakai dan koreksinya dicatat di `log-keputusan.csv`.

## Nama di berkas mentah dan nama baku

| seri_kode      | nama_di_berkas   | nama_baku                                                                              |
|:---------------|:-----------------|:---------------------------------------------------------------------------------------|
| var1439        |                  | Angka Partisipasi Kasar (APK) Anak Yang Mengikuti PAUD Menurut Provinsi                |
| var1451        |                  | Proporsi Remaja dan Dewasa (Usia 15-24 Tahun) dengan Keterampilan TIK Menurut Provinsi |
| var1447        |                  | Proporsi Remaja dan Dewasa (Usia 15-59 Tahun) dengan Keterampilan TIK Menurut Provinsi |
| var1221        |                  | Proporsi Individu yang Menguasai/Memiliki Telepon Genggam Menurut Provinsi             |
| SE.PRE.ENRR    |                  | School enrollment, preprimary (% gross)                                                |
| IT.NET.USER.ZS |                  | Individuals using the Internet (% of population)                                       |

## Satuan dan kode SDG

| seri_kode      | katalog_satuan   | satuan        | bukti_satuan                                                                                                                                                                                                      | katalog_sdg   | sdg_kode   |
|:---------------|:-----------------|:--------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--------------|:-----------|
| var1439        | tidak_ada        | persen        | Field unit di manifest_asal.json dan var.unit di sdg4_apk_paud.json kosong (''), namun judul resmi Angka Partisipasi Kasar (APK) Susenas BPS (SDG 4.2.2) dan catatan var.note merujuk ukuran dalam satuan persen. | 4.2.2         | 4.2.2      |
| var1451        | Persen           | persen        | Kolom satuan pada CSV BPS dan var.unit pada JSON BPS mencantumkan Persen.                                                                                                                                         | 4.4.1         | 4.4.1      |
| var1447        | Persen           | persen        | Kolom satuan pada CSV BPS dan var.unit pada JSON BPS mencantumkan Persen.                                                                                                                                         | 4.4.1         | 4.4.1      |
| var1221        | Persen           | persen        | Kolom satuan pada CSV BPS dan var.unit pada JSON BPS mencantumkan Persen.                                                                                                                                         | 5.b.1         | 5.b.1      |
| SE.PRE.ENRR    | % gross          | persen        | Metadata resmi WDI (sumber2_indikator.json): School enrollment, preprimary (% gross).                                                                                                                             | 4.2.2         | 4.2.2      |
| IT.NET.USER.ZS | % of population  | per 100 orang | Metadata resmi WDI (sumber46_indikator.json): Individuals using the Internet (% of population).                                                                                                                   | 17.8.1        | 17.8.1     |

## Koreksi katalog

Tidak ada.

## Catatan BPS (var.note)

Tidak ada seri BPS.

## Metadata WDI yang muncul di lebih dari satu berkas

Tidak ada.

## Judul dengan spasi di awal/akhir

Tidak ada.