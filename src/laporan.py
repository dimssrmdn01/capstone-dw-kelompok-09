"""Fungsi pendukung untuk laporan dan metrik pipeline."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GAMBAR = ROOT / "reports" / "gambar"
REPORTS = ROOT / "reports"
RESULTS = ROOT / "results"

def _siapkan():
    REPORTS.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)

def tulis(nama, isi):
    """Simpan laporan teks ke folder reports."""
    _siapkan()
    (REPORTS / nama).write_text(str(isi), encoding="utf-8")

def tabel_md(data):
    """Ubah DataFrame menjadi tabel Markdown."""
    if data is None or data.empty:
        return "_Tidak ada data._"
    return data.to_markdown(index=False)

def catat(**metrik):
    """Perbarui metrik pipeline pada berkas sementara."""
    _siapkan()
    path = RESULTS / "metrik-sementara.json"

    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            data = {}
    else:
        data = {}

    data.update(metrik)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )