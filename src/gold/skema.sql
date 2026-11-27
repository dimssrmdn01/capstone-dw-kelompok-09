-- Tahap 5 (tugas #22): DDL basis data Silver dan Gold Kelompok 09.
-- Dibangun ulang oleh `python pipeline.py` ke data/gold/gold.sqlite (tidak di-commit, lihat .gitignore).
-- Pemuat: src/gold/penyimpanan.py. Jumlah baris tiap tabel dicocokkan dengan Parquet-nya.
--
-- Konvensi tipe:
--   periode TEXT       format baku '2020', '2020-S1', '2020-Q3', '2020-07' (bukan INTEGER).
--   wilayah_kode INTEGER  9999 = Indonesia, provinsi = kode BPS dua digit x 100.
--   nilai REAL         NULL berarti sel kosong; tidak pernah diisi nol.
--   bendera BOOLEAN    disimpan INTEGER 0/1 dengan CHECK.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------- Bronze (dokumen)
-- Respons JSON mentah disimpan utuh sebagai dokumen, satu baris per berkas, untuk audit.
CREATE TABLE mentah_dokumen (
    _berkas_raw   TEXT    NOT NULL PRIMARY KEY,   -- jalur relatif data/raw/
    _sha256_raw   TEXT    NOT NULL CHECK (length(_sha256_raw) = 64),
    sumber        TEXT    NOT NULL,               -- bps | wdi
    snapshot      TEXT    NOT NULL,               -- YYYY-MM-DD
    ukuran_bait   INTEGER NOT NULL,
    isi           TEXT    NOT NULL CHECK (json_valid(isi))
);

-- ---------------------------------------------------------------- Silver
-- Kunci unik skema minimal starter: sumber + seri + wilayah + periode + rincian + berkas.
CREATE TABLE silver (
    sumber          TEXT    NOT NULL,
    seri_kode       TEXT    NOT NULL,
    wilayah_kode    INTEGER NOT NULL,
    nama_wilayah    TEXT    NOT NULL,
    periode         TEXT    NOT NULL,
    jenis_periode   TEXT    NOT NULL,
    rincian         TEXT    NOT NULL,
    nilai           REAL,
    satuan          TEXT    NOT NULL,
    sdg_kode        TEXT,
    batas_bawah     REAL,
    batas_atas      REAL,
    rujukan_tahun   INTEGER,
    _berkas_raw     TEXT    NOT NULL,
    _sha256_raw     TEXT    NOT NULL CHECK (length(_sha256_raw) = 64),
    PRIMARY KEY (sumber, seri_kode, wilayah_kode, periode, rincian, _berkas_raw)
);

-- ---------------------------------------------------------------- Gold
-- Satu nilai per seri x wilayah x periode (aturan #19), dengan penanda anomali.
CREATE TABLE observasi_terpilih (
    sumber            TEXT    NOT NULL,
    seri_kode         TEXT    NOT NULL,
    wilayah_kode      INTEGER NOT NULL,
    nama_wilayah      TEXT    NOT NULL,
    periode           TEXT    NOT NULL,
    jenis_periode     TEXT    NOT NULL,
    rincian           TEXT    NOT NULL,
    nilai             REAL,
    satuan            TEXT    NOT NULL,
    sdg_kode          TEXT,
    batas_bawah       REAL,
    batas_atas        REAL,
    rujukan_tahun     INTEGER,
    _berkas_raw       TEXT    NOT NULL,
    _sha256_raw       TEXT    NOT NULL,
    kategori_anomali  TEXT,
    tindakan_anomali  TEXT,
    bukti_anomali     TEXT,
    anomaly_flag      INTEGER NOT NULL CHECK (anomaly_flag IN (0, 1)),
    PRIMARY KEY (seri_kode, wilayah_kode, periode)
);

-- Grid lengkap wilayah x periode per seri; kategori menjelaskan sel kosong.
CREATE TABLE grid_kelengkapan (
    seri_kode     TEXT    NOT NULL,
    periode       TEXT    NOT NULL,
    wilayah_kode  INTEGER NOT NULL,
    nama_wilayah  TEXT    NOT NULL,
    tingkat       TEXT    NOT NULL,
    kategori      TEXT    NOT NULL,
    bukti         TEXT,
    PRIMARY KEY (seri_kode, wilayah_kode, periode)
);

-- Panel Gold panjang: provinsi x periode x indikator.
CREATE TABLE panel_provinsi (
    seri_kode         TEXT    NOT NULL,
    periode           TEXT    NOT NULL,
    wilayah_kode      INTEGER NOT NULL,
    nama_wilayah      TEXT    NOT NULL,
    tingkat           TEXT    NOT NULL,
    kategori          TEXT    NOT NULL
        CHECK (kategori IN ('terisi', 'missing', 'belum_ada', 'tidak_diterbitkan', 'batas_lama')),
    bukti             TEXT,
    nilai             REAL,
    satuan            TEXT,
    sumber            TEXT,
    anomaly_flag      INTEGER NOT NULL CHECK (anomaly_flag IN (0, 1)),
    kategori_anomali  TEXT,
    tindakan_anomali  TEXT,
    bukti_anomali     TEXT,
    rincian           TEXT,
    _berkas_raw       TEXT,
    _sha256_raw       TEXT,
    PRIMARY KEY (seri_kode, wilayah_kode, periode),
    CHECK ((kategori = 'terisi') = (nilai IS NOT NULL))
);

-- Panel Gold lebar: satu baris per provinsi x periode, satu kolom per indikator.
CREATE TABLE panel_provinsi_lebar (
    wilayah_kode  INTEGER NOT NULL,
    nama_wilayah  TEXT    NOT NULL,
    periode       TEXT    NOT NULL,
    var1221       REAL,
    var1439       REAL,
    var1447       REAL,
    var1451       REAL,
    PRIMARY KEY (wilayah_kode, periode)
);

-- Tabel nasional: seri utama (agregat Indonesia) dan pembanding WDI per periode.
CREATE TABLE nasional (
    periode       TEXT    NOT NULL,
    seri_kode     TEXT    NOT NULL,
    wilayah_kode  INTEGER NOT NULL CHECK (wilayah_kode = 9999),
    nilai         REAL    NOT NULL,
    nama_wilayah  TEXT,
    satuan        TEXT,
    sumber        TEXT,
    rincian       TEXT,
    _berkas_raw   TEXT    NOT NULL,
    _sha256_raw   TEXT    NOT NULL,
    PRIMARY KEY (seri_kode, wilayah_kode, periode)
);

-- Rekonsiliasi seri utama vs pembanding nasional (tugas #23).
CREATE TABLE rekonsiliasi_nasional (
    pasangan             TEXT NOT NULL,
    periode              TEXT NOT NULL,
    seri_utama           TEXT NOT NULL,
    nilai_utama          REAL,
    seri_pembanding      TEXT NOT NULL,
    rincian_pembanding   TEXT NOT NULL,
    nilai_pembanding     REAL,
    selisih              REAL,
    status_pasangan      TEXT NOT NULL
        CHECK (status_pasangan IN ('berpasangan', 'hanya_utama', 'hanya_pembanding')),
    kategori_selisih     TEXT
        CHECK (kategori_selisih IS NULL OR kategori_selisih IN (
            'definisi berbeda', 'metode berbeda', 'vintage berbeda',
            'cakupan berbeda', 'belum terjelaskan')),
    penjelasan           TEXT NOT NULL,
    dugaan               TEXT,
    bukti                TEXT,
    alasan_perbandingan  TEXT NOT NULL,
    PRIMARY KEY (pasangan, periode),
    CHECK ((status_pasangan = 'berpasangan') = (selisih IS NOT NULL)),
    CHECK (status_pasangan <> 'berpasangan' OR kategori_selisih IS NOT NULL)
);
