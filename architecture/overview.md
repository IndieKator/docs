# Gambaran Sistem

IndieKator terdiri dari frontend yang menampilkan chart, FastAPI sebagai API
dan engine perhitungan, layanan eksternal untuk harga serta Trends, dan
Supabase PostgreSQL untuk snapshot.

| Komponen | Tanggung jawab |
| --- | --- |
| Frontend React | Meminta `/api/fgi` dan menampilkan nilai serta riwayat enam bulan |
| FastAPI | Memeriksa kesegaran snapshot, menjalankan refresh, dan mengirim kontrak API |
| FGI engine | Menghitung MA-125, score harga/pencarian, FGI, dan zona |
| Sectors.app | Menyediakan harga IHSG harian |
| Google Trends | Menyediakan tiga sinyal minat pencarian Indonesia |
| Supabase | Menyimpan snapshot FGI yang dapat ditelusuri |

Route handler tetap tipis: pengambilan data dan transformasi berada di service,
sedangkan schema respons menjaga bentuk kontrak API.
