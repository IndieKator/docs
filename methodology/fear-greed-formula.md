# Formula Fear and Greed Index

IndieKator mempertahankan dua versi indeks. V1 adalah sentiment lama di
`/api/sentiment/*`. V2 adalah FGI mingguan di `/api/fgi` dan menjadi sumber
chart aplikasi.

## Formula V1

V1 memakai Google Trends keyword `ihsg`, dinormalisasi pada data yang sedang
di-ingest. Harga hanya menentukan arah terhadap MA-125.

| Simbol | Arti |
| --- | --- |
| $GT_t$ | Nilai Google Trends `ihsg` pada tanggal $t$ |
| $N_t$ | Trends yang telah dinormalisasi ke 0-100 |
| $A_t$ | $1$ saat harga di atas MA-125, atau $-1$ saat harga sama/di bawah MA-125 |

$$
FGI^{V1}_t = 50 + A_t \times \frac{N_t}{2}
$$

Contoh snapshot V1: $Close=6.599{,}943$, $MA125=6.702{,}1175$, dan $N=0$.
Karena harga berada di bawah MA-125, $A=-1$, sehingga:

$$
FGI^{V1} = 50 + (-1) \times \frac{0}{2} = 50{,}00
$$

Hasilnya **Neutral**. Nilai $N=0$ berasal dari normalisasi seluruh seri pada
ingest tersebut; lihat [normalisasi V1](normalization.md#v1-min-max-pada-satu-ingest).

## Formula V2

V2 menggabungkan momentum harga dengan minat pencarian publik. Data dihitung
per minggu setelah harga harian memiliki MA-125.

| Simbol | Arti |
| --- | --- |
| $G_t$ | Rata-rata tiga nilai Google Trends |
| $D_t$ | Jarak harga penutupan dari MA-125, dalam persen |
| $P_t$ | Price Score, 0-100 |
| $S_t$ | Search Score, 0-100 |

$$
D_t = \frac{Close_t - MA125_t}{MA125_t} \times 100
$$

$$
P_t = \operatorname{clip}\left(50 + \frac{D_t}{6} \times 50, 0, 100\right)
$$

$$
S_t = \operatorname{clip}\left(50 + (G_t - 50) \times \operatorname{sign}(D_t), 0, 100\right)
$$

$$
FGI^{V2}_t = 0{,}60 \times P_t + 0{,}40 \times S_t
$$

## Contoh hitung V2

**Diketahui** pada minggu 6 September 2026: harga penutupan 6.636,48,
MA-125 6.662,47, dan Trends `15`, `23`, `46`.

$$
G = \frac{15 + 23 + 46}{3} = 28
$$

$$
D = \frac{6.636{,}48 - 6.662{,}47}{6.662{,}47} \times 100 = -0{,}39\%
$$

$$
P = 50 + \frac{-0{,}39}{6} \times 50 = 46{,}75
$$

Karena harga di bawah MA-125, $\operatorname{sign}(D)=-1$.

$$
S = 50 + (28 - 50) \times (-1) = 72
$$

$$
FGI^{V2} = 0{,}60(46{,}75) + 0{,}40(72) = 56{,}85
$$

Hasilnya **Greed**. Zona: Extreme Fear $\le25$, Fear $\le45$, Neutral
$\le55$, Greed $\le75$, lalu Extreme Greed.

Setiap snapshot menyimpan harga, MA-125, tiga input Trends, kedua skor, dan
FGI di `fgi_snapshots`, sehingga hasil dapat ditelusuri ulang.
