# Normalisasi dan Google Trends

## V1: min-max pada satu ingest

V1 mengambil keyword `ihsg` lalu menormalkan seluruh seri yang diterima pada
satu kali ingest.

$$
N_t = 100 \times \frac{GT_t - \min(GT)}{\max(GT) - \min(GT)}
$$

Jika seluruh nilai sama, sistem memakai $N_t=50$. Karena minimum dan maksimum
bergantung pada data saat ingest, nilai Trends mentah saja tidak cukup untuk
menghitung ulang V1.

## V2: tiga seri yang disejajarkan

V2 tidak memakai normalisasi min-max lintas keyword. Google Trends dipanggil
terpisah untuk `ihsg`, `idx composite`, dan `indeks harga saham gabungan`.
Setiap query memakai `hl=id-ID`, `geo=ID`, serta rentang tanggal yang sama.
Nilai `isPartial` dibuang; hanya minggu yang ada pada ketiga seri digunakan.

$$
G_t = \frac{K_{1,t} + K_{2,t} + K_{3,t}}{3}
$$

Google Trends memberi skala 0-100 untuk masing-masing query. Rata-rata $G_t$
menjadi sinyal minat pencarian pada minggu tersebut, bukan klaim volume
pencarian absolut.

## Rentang perhitungan

Ingest meminta 18 bulan harga IHSG dan Google Trends. Harga harian memakai
MA-125 lalu di-resample ke penutupan minggu terakhir (`W-SUN`), kemudian
digabungkan dengan Trends pada minggu yang sama. Periode panjang ini memberi
data pemanasan untuk MA-125; API `/api/fgi` hanya menampilkan sekitar enam
bulan riwayat terbaru.
