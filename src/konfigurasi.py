# Konfigurasi indikator Kasus 09

SERI = {
    "var1439": {
        "sumber": "bps",
        "sdg": "4.2.2",
        "tingkat": "provinsi",
        "satuan": "persen",
        "katalog_satuan": "tidak_ada",
        "katalog_sdg": "4.2.2",
        "bukti_satuan": "Field unit di manifest_asal.json dan var.unit di sdg4_apk_paud.json kosong (''), namun judul resmi Angka Partisipasi Kasar (APK) Susenas BPS (SDG 4.2.2) dan catatan var.note merujuk ukuran dalam satuan persen.",
        "bukti_sdg": "Metadata sumber BPS sdg4_apk_paud.json (SDG 4.2.2).",
        "nama": "Angka Partisipasi Kasar (APK) Anak Yang Mengikuti PAUD Menurut Provinsi",
    },
    "var1451": {
        "sumber": "bps",
        "sdg": "4.4.1",
        "tingkat": "provinsi",
        "satuan": "persen",
        "katalog_satuan": "Persen",
        "katalog_sdg": "4.4.1",
        "bukti_satuan": "Kolom satuan pada CSV BPS dan var.unit pada JSON BPS mencantumkan Persen.",
        "bukti_sdg": "Metadata sumber BPS sdg4_4_4_1_a_v1451.json (SDG 4.4.1).",
        "nama": "Proporsi Remaja dan Dewasa (Usia 15-24 Tahun) dengan Keterampilan TIK Menurut Provinsi",
    },
    "var1447": {
        "sumber": "bps",
        "sdg": "4.4.1",
        "tingkat": "provinsi",
        "satuan": "persen",
        "katalog_satuan": "Persen",
        "katalog_sdg": "4.4.1",
        "bukti_satuan": "Kolom satuan pada CSV BPS dan var.unit pada JSON BPS mencantumkan Persen.",
        "bukti_sdg": "Metadata sumber BPS sdg4_4_4_1_b_v1447.json (SDG 4.4.1).",
        "nama": "Proporsi Remaja dan Dewasa (Usia 15-59 Tahun) dengan Keterampilan TIK Menurut Provinsi",
    },
    "var1221": {
        "sumber": "bps",
        "sdg": "5.b.1",
        "tingkat": "provinsi",
        "satuan": "persen",
        "katalog_satuan": "Persen",
        "katalog_sdg": "5.b.1",
        "bukti_satuan": "Kolom satuan pada CSV BPS dan var.unit pada JSON BPS mencantumkan Persen.",
        "bukti_sdg": "Metadata sumber BPS sdg5_5_b_1_v1221.json (SDG 5.b.1).",
        "nama": "Proporsi Individu yang Menguasai/Memiliki Telepon Genggam Menurut Provinsi",
    },
    "SE.PRE.ENRR": {
        "sumber": "wdi",
        "sdg": "4.2.2",
        "tingkat": "nasional",
        "satuan": "persen",
        "katalog_satuan": "% gross",
        "katalog_sdg": "4.2.2",
        "bukti_satuan": "Metadata resmi WDI (sumber2_indikator.json): School enrollment, preprimary (% gross).",
        "bukti_sdg": "Metadata WDI indikator SE.PRE.ENRR.",
        "nama": "School enrollment, preprimary (% gross)",
    },
    "IT.NET.USER.ZS": {
        "sumber": "wdi",
        "sdg": "17.8.1",
        "tingkat": "nasional",
        "satuan": "per 100 orang",
        "katalog_satuan": "% of population",
        "katalog_sdg": "17.8.1",
        "bukti_satuan": "Metadata resmi WDI (sumber46_indikator.json): Individuals using the Internet (% of population).",
        "bukti_sdg": "Metadata WDI indikator IT.NET.USER.ZS.",
        "nama": "Individuals using the Internet (% of population)",
    },
}

DERET = {
    "var1439": ["total"],
    "var1451": ["total"],
    "var1447": ["total"],
    "var1221": ["total"],
    "SE.PRE.ENRR": ["total"],
    "IT.NET.USER.ZS": ["total"],
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
    "per 100 orang": (0, 100),
}

ANOMALI = {
    "k_iqr": 1.5,
    "lompat_relatif": 0.50,
    "min_titik_samping": 5,
    "porsi_patahan": 0.50,
}

TABEL_STATIS = {}

RINCIAN_TOTAL_WHO = {"all"}

RINCIAN_NILAI = {}

RINCIAN_DIMENSI = {}

PASANGAN = [
    {
        "id": "P-01",
        "utama": "var1439",
        "pembanding": [("SE.PRE.ENRR", "total")],
        "alasan_rincian": (
            "Dipilih agregat nasional (wilayah_kode=9999, rincian=total) karena WDI hanya menyediakan "
            "data tingkat negara. SE.PRE.ENRR dipilih untuk dibandingkan dengan var1439 (APK PAUD) "
            "karena sama-sama mengukur Angka Partisipasi Kasar jenjang prasekolah dalam satuan persen "
            "(irisan tahun 2015-2018), dengan catatan beda cakupan usia (BPS 3-6 tahun vs UIS usia resmi)."
        ),
    },
    {
        "id": "P-02",
        "utama": "var1221",
        "pembanding": [("IT.NET.USER.ZS", "total")],
        "alasan_rincian": (
            "Dipilih agregat nasional (wilayah_kode=9999, rincian=total) karena WDI hanya menyediakan "
            "data tingkat negara. IT.NET.USER.ZS dipilih sebagai pembanding kontekstual bagi var1221 "
            "(kepemilikan telepon genggam) serta var1447/var1451 (keterampilan TIK) karena tidak tersedia "
            "seri kepemilikan ponsel identik di WDI dan keduanya merepresentasikan penetrasi digital nasional (irisan 2015-2024)."
        ),
    },
]

URUTAN_BERKAS = []
