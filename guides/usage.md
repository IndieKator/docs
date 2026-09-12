# Menggunakan API FGI

Gunakan `GET /api/fgi` untuk membaca FGI terbaru dan riwayat sekitar enam
bulan. Endpoint tidak memerlukan kredensial browser.

```bash
curl http://127.0.0.1:8000/api/fgi
```

Respons memiliki bentuk berikut:

```json
{
  "current": {"date": "2026-09-06", "value": 56.85, "sentiment": "Greed"},
  "history": [{"date": "2026-03-15", "value": 51.2}],
  "updated_at": "2026-09-13T00:00:00+00:00",
  "is_stale": false
}
```

Gunakan `current.value` dan `history` untuk chart. Tampilkan status lama bila
`is_stale` bernilai `true`; data masih dapat dipakai tetapi refresh terakhir
gagal. HTTP 503 dengan `FGI data unavailable` berarti belum ada snapshot yang
bisa ditampilkan.

Endpoint `/api/sentiment/*` adalah implementasi V1 lama dan tetap tersedia
untuk kompatibilitas. Gunakan `/api/fgi` untuk fitur FGI V2 baru.
