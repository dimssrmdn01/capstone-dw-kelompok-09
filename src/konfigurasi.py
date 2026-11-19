# Konfigurasi indikator Kasus 09

SERI = {
    "var1439": {
        "sumber": "bps",
        "sdg": "4.2.2",
        "tingkat": "provinsi",
        "satuan": "tidak_dinyatakan",
        "katalog_satuan": "Tidak tercantum",
        "katalog_sdg": "4.2.2",
        "bukti_satuan": "Kolom satuan pada CSV BPS tidak mencantumkan satuan.",
        "bukti_sdg": "Pemetaan indikator PAUD pada konfigurasi Kasus 09; perlu verifikasi dokumen definisi.",
        "nama": "Angka Partisipasi Kasar PAUD usia 3-6 tahun",
    },
    "var1451": {
        "sumber": "bps",
        "sdg": "4.4.1",
        "tingkat": "provinsi",
        "satuan": "persen",
        "katalog_satuan": "Persen",
        "katalog_sdg": "4.4.1",
        "bukti_satuan": "Kolom satuan pada CSV BPS mencantumkan Persen.",
        "bukti_sdg": "Pemetaan indikator TIK usia 15-24 tahun pada konfigurasi Kasus 09; perlu verifikasi dokumen definisi.",
        "nama": "Proporsi keterampilan TIK usia 15-24 tahun",
    },
    "var1447": {
        "sumber": "bps",
        "sdg": "4.4.1",
        "tingkat": "provinsi",
        "satuan": "persen",
        "katalog_satuan": "Persen",
        "katalog_sdg": "4.4.1",
        "bukti_satuan": "Kolom satuan pada CSV BPS mencantumkan Persen.",
        "bukti_sdg": "Pemetaan indikator TIK usia 15-59 tahun pada konfigurasi Kasus 09; perlu verifikasi dokumen definisi.",
        "nama": "Proporsi keterampilan TIK usia 15-59 tahun",
    },
    "var1221": {
        "sumber": "bps",
        "sdg": "5.b.1",
        "tingkat": "provinsi",
        "satuan": "persen",
        "katalog_satuan": "Persen",
        "katalog_sdg": "5.b.1",
        "bukti_satuan": "Kolom satuan pada CSV BPS mencantumkan Persen.",
        "bukti_sdg": "Pemetaan indikator kepemilikan telepon genggam pada konfigurasi Kasus 09; perlu verifikasi dokumen definisi.",
        "nama": "Proporsi individu usia 5 tahun ke atas yang memiliki telepon genggam",
    },
}
# Semua indikator BPS memiliki satu rincian utama.
DERET = {
    "var1439": ["total"],
    "var1451": ["total"],
    "var1447": ["total"],
    "var1221": ["total"],
}

FORMAT_BPS = "csv"

RINCIAN_TOTAL_BPS = {
    "tidak ada",
    "jumlah",
    "total",
}

RINCIAN_BPS = {}

RUJUKAN_TAHUN = {}

TIDAK_TERBIT = {}

RENTANG = {
    "persen": (0, 100),
}

ANOMALI = {
    "lompat_relatif": 0.50,
    "porsi_patahan": 0.50,
    "min_provinsi_patahan": 3,
}

TABEL_STATIS = {}

RINCIAN_TOTAL_WHO = {"all"}

RINCIAN_NILAI = {}

RINCIAN_DIMENSI = {}

PASANGAN = []

URUTAN_BERKAS = []