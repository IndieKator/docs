# Menjalankan Backend

Backend IndieKator membutuhkan Python 3.12+, proyek Supabase, dan API key
Sectors.app. Dari repository backend, siapkan konfigurasi lalu sinkronkan
dependensi.

```powershell
Copy-Item .env.example .env
uv sync
uv run uvicorn app.main:app --reload --port 8000
```

Isi `.env` dengan `SECTORS_API_KEY`, `SUPABASE_URL`,
`SUPABASE_SERVICE_ROLE_KEY`, dan `ADMIN_SECRET`. Service-role key hanya untuk
server; jangan masukkan ke frontend atau dokumentasi contoh.

Setelah migrasi database diterapkan, jalankan ingest awal:

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/admin/ingest -H "X-Admin-Secret: YOUR_SECRET"
```

Endpoint FGI dapat memicu refresh sendiri saat snapshot berusia lebih dari 24
jam, tetapi ingest awal tetap dibutuhkan agar data tersedia.
