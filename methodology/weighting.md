# Pembobotan Skor

FGI V2 memberikan bobot **60%** untuk momentum harga dan **40%** untuk minat
pencarian. Harga menjadi sinyal utama; pencarian publik berperan sebagai
konfirmasi arah pasar.

## Price Score

Price Score memakai jarak harga dari MA-125. Jarak positif menaikkan skor dan
jarak negatif menurunkannya. Pembagian dengan 6 membuat jarak sekitar 6% dari
MA-125 mencapai ujung skala sebelum nilai dibatasi.

$$
P_t = \operatorname{clip}\left(50 + \frac{D_t}{6} \times 50, 0, 100\right)
$$

## Search Score

Search Score membaca rata-rata Trends mengikuti arah harga. Saat harga di atas
MA-125, minat tinggi menaikkan skor. Saat harga di bawah MA-125, minat tinggi
menurunkannya dan mencerminkan kekhawatiran pasar.

$$
S_t = \operatorname{clip}\left(50 + (G_t - 50) \times \operatorname{sign}(D_t), 0, 100\right)
$$

`clip(x, 0, 100)` menjaga setiap komponen tetap pada skala 0-100. Nilai akhir
dibulatkan dua angka desimal sebelum disimpan dan dipetakan ke zona FGI.
