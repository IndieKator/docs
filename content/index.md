# Dokumentasi IndieKator

Selamat datang di dokumentasi teknis **IndieKator**. Situs ini menjelaskan
bagaimana Fear and Greed Index (FGI) IHSG dihitung, bagaimana data diproses,
dan bagaimana frontend menggunakan hasilnya.

## Mulai dari sini

<div class="landing-grid" markdown>

<a class="landing-card" href="methodology/fear-greed-formula/">
<span class="eyebrow">METODOLOGI</span>
<strong>Memahami FGI</strong>
<span>Pelajari formula V1 dan V2, zona sentimen, serta contoh perhitungan aktual.</span>
</a>

<a class="landing-card" href="guides/usage/">
<span class="eyebrow">PANDUAN</span>
<strong>Menggunakan API</strong>
<span>Lihat kontrak endpoint FGI, riwayat chart, dan penanganan data stale.</span>
</a>

<a class="landing-card" href="architecture/overview/">
<span class="eyebrow">ARSITEKTUR</span>
<strong>Melihat alur sistem</strong>
<span>Telusuri perjalanan data dari Sectors.app dan Google Trends sampai React.</span>
</a>

</div>

## Peta dokumentasi

| Bagian | Isi |
| --- | --- |
| Metodologi | Formula, normalisasi Google Trends, dan alasan bobot 60/40 |
| Panduan | Menjalankan backend, proses ingest, dan memakai endpoint FGI |
| Arsitektur | Komponen utama dan aliran data mingguan |

Dokumentasi diperbarui bersama perubahan implementasi backend agar formula dan
perilaku API tetap dapat ditelusuri.
