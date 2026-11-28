# Penyimpanan SQL — hasil pemuatan terakhir

Dibuat otomatis oleh `src/gold/penyimpanan.py` saat `python pipeline.py` dijalankan.
Basis data: `data/gold/gold.sqlite` (tidak di-commit); DDL: `src/gold/skema.sql`.

| Tabel | Kunci primer | Baris SQL | Baris Parquet | Cocok |
|---|---|---:|---:|---|
| `silver` | sumber, seri_kode, wilayah_kode, periode, rincian, _berkas_raw | 1,653 | 1,653 | ya |
| `observasi_terpilih` | seri_kode, wilayah_kode, periode | 1,653 | 1,653 | ya |
| `panel_provinsi` | seri_kode, wilayah_kode, periode | 1,672 | 1,672 | ya |
| `panel_provinsi_lebar` | wilayah_kode, periode | 418 | 418 | ya |
| `grid_kelengkapan` | seri_kode, wilayah_kode, periode | 1,716 | 1,716 | ya |
| `nasional` | seri_kode, wilayah_kode, periode | 125 | 125 | ya |
| `rekonsiliasi_nasional` | pasangan, periode | 89 | 89 | ya |
| `mentah_dokumen` | _berkas_raw | 12 | — | — |
