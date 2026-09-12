# Alur Data dan Ingest

FGI V2 mengambil harga IHSG dari Sectors.app dan tiga seri Google Trends.
Permintaan harga dipecah menjadi blok maksimal 89 hari untuk mengikuti batas
penyedia data. Tanggal menggunakan UTC agar tidak meminta hari perdagangan di
masa depan.

Data harga dihitung MA-125, diubah menjadi titik mingguan, lalu digabungkan
dengan minggu Google Trends yang tersedia pada semua keyword. Sistem menghitung
Price Score, Search Score, FGI, dan zona sebelum meng-upsert hasil ke tabel
`fgi_snapshots` dengan kunci `week_date`.

Snapshot menyimpan input dan hasil antara: `close_price`, `ma_125`,
`distance_pct`, tiga kolom `trend_*`, `trends_mean`, `price_score`,
`search_score`, dan `fgi`. Ini memungkinkan audit perhitungan tanpa mengambil
ulang data eksternal.

Jika Google Trends atau Sectors.app gagal saat refresh, endpoint tetap
mengembalikan snapshot lama bila tersedia dengan `is_stale: true`. Tanpa
snapshot, endpoint mengembalikan HTTP 503.
