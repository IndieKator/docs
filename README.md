# Dokumentasi IndieKator

Dokumentasi teknis IndieKator menjelaskan cara Fear and Greed Index (FGI) IHSG
dihitung, diambil, disimpan, dan digunakan oleh aplikasi.

## Metodologi

- [Formula Fear and Greed Index](methodology/fear-greed-formula.md)
- [Normalisasi dan Google Trends](methodology/normalization.md)
- [Pembobotan skor](methodology/weighting.md)

## Panduan

- [Menjalankan backend](guides/setup.md)
- [Alur data dan ingest](guides/data-pipeline.md)
- [Menggunakan API FGI](guides/usage.md)

## Arsitektur

- [Gambaran sistem](architecture/overview.md)
- [Aliran data](architecture/data-flow.md)

## Handbook PDF

PDF gabungan dibangun otomatis oleh GitHub Actions ketika dokumentasi berubah.
Untuk membuatnya secara lokal, jalankan:

```powershell
uv run --with-requirements build-pipeline/requirements.txt python build-pipeline/generate_pdf.py
```

Hasil lokal berada di `output/pdf/indiekator-docs.pdf` dan tidak disimpan di
Git. Unduh artefak `indiekator-docs-pdf` dari workflow untuk hasil CI.
