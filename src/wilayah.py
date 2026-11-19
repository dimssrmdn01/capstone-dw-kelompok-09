"""Pemetaan kode wilayah BPS ke susunan 38 provinsi tahun 2025."""

INDONESIA = 9999

# Kode BPS: kode provinsi dua digit dikali 100.
# Nilai kedua adalah tahun mulai provinsi tersedia sebagai wilayah tersendiri.
PROVINSI = {
    1100: ("Aceh", 2015),
    1200: ("Sumatera Utara", 2015),
    1300: ("Sumatera Barat", 2015),
    1400: ("Riau", 2015),
    1500: ("Jambi", 2015),
    1600: ("Sumatera Selatan", 2015),
    1700: ("Bengkulu", 2015),
    1800: ("Lampung", 2015),
    1900: ("Kepulauan Bangka Belitung", 2015),
    2100: ("Kepulauan Riau", 2015),
    3100: ("DKI Jakarta", 2015),
    3200: ("Jawa Barat", 2015),
    3300: ("Jawa Tengah", 2015),
    3400: ("DI Yogyakarta", 2015),
    3500: ("Jawa Timur", 2015),
    3600: ("Banten", 2015),
    5100: ("Bali", 2015),
    5200: ("Nusa Tenggara Barat", 2015),
    5300: ("Nusa Tenggara Timur", 2015),
    6100: ("Kalimantan Barat", 2015),
    6200: ("Kalimantan Tengah", 2015),
    6300: ("Kalimantan Selatan", 2015),
    6400: ("Kalimantan Timur", 2015),
    6500: ("Kalimantan Utara", 2012),
    7100: ("Sulawesi Utara", 2015),
    7200: ("Sulawesi Tengah", 2015),
    7300: ("Sulawesi Selatan", 2015),
    7400: ("Sulawesi Tenggara", 2015),
    7500: ("Gorontalo", 2015),
    7600: ("Sulawesi Barat", 2015),
    8100: ("Maluku", 2015),
    8200: ("Maluku Utara", 2015),
    9100: ("Papua", 2015),
    9200: ("Papua Barat", 2015),
    9300: ("Papua Selatan", 2022),
    9400: ("Papua Tengah", 2022),
    9500: ("Papua Pegunungan", 2022),
    9600: ("Papua Barat Daya", 2022),
}
NAMA = {kode: nama for kode, (nama, _) in PROVINSI.items()}
NAMA[INDONESIA] = "Indonesia"

# Hubungan induk hanya dipakai untuk mengenali batas wilayah historis.
INDUK = {
    6500: 6400,
    9200: 9100,
    9300: 9100,
    9400: 9100,
    9500: 9100,
    9600: 9200,
}


def _tahun(periode):
    """Ambil tahun dari label periode, misalnya 2020 atau 2020-S1."""
    try:
        return int(str(periode)[:4])
    except (TypeError, ValueError):
        return 0


def sudah_ada(kode, periode):
    """Periksa apakah provinsi sudah terbentuk pada periode tersebut."""
    if kode == INDONESIA:
        return True

    if kode not in PROVINSI:
        return False

    return _tahun(periode) >= PROVINSI[kode][1]


def dari_nama(nama):
    """Cari kode provinsi berdasarkan nama."""
    nama = str(nama).strip().casefold()

    for kode, label in NAMA.items():
        if label.casefold() == nama:
            return kode

    return None


def dari_negara(sumber, kode):
    """Konversi kode negara dari sumber eksternal."""
    kode = str(kode).strip().upper()

    if kode in {"ID", "IDN", "INDONESIA"}:
        return INDONESIA

    return None


def dari_kemendagri(kode):
    """Konversi kode wilayah Kemendagri ke kode BPS."""
    kode = str(kode).strip()

    # Belum ada pemetaan lintas-kode yang diverifikasi.
    return None