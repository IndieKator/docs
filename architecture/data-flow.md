# Aliran Data

```text
React -> GET /api/fgi -> FastAPI
                         |
                         +-- snapshot segar -> Supabase -> respons
                         |
                         +-- snapshot kosong/kedaluwarsa -> FGI ingestion
                                                        |
                    Sectors.app + Google Trends -> FGI engine
                                                        |
                          fgi_snapshots <- upsert hasil mingguan
                                                        |
                                              respons current + history
```

FastAPI menilai snapshot kedaluwarsa setelah 24 jam. Refresh dilindungi lock
dalam proses agar beberapa request lokal tidak menjalankan ingest yang sama
bersamaan. Bila refresh gagal dan snapshot lama ada, respons memakai data lama
dengan `is_stale: true`.

Engine meminta 18 bulan input untuk pemanasan MA-125, tetapi route hanya
memilih 183 hari terakhir sebagai history untuk frontend. Nilai mingguan
diurutkan naik berdasarkan tanggal agar langsung cocok untuk chart.
