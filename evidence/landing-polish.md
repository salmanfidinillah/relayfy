# Landing polish — 4 November 2026

Permintaan pengguna: landing lebih mandiri dari referensi, lebih rapi dan tidak terasa seperti template AI. Lingkup: renderHome dan helper pratinjau di web/app.js, CSS baru dengan prefix lp-, serta meta description. Backend, autentikasi, izin, penyimpanan dan runtime WorkBuddy tidak diubah.

Desain: hero tipografi serif dengan komposisi terpusat, palet arang/ivory/terracotta, panel handover seperti lembar dokumen, daftar manfaat editorial, alur kerja, FAQ dan footer. Foto hero besar serta geometri berwarna pada versi sebelumnya diganti pratinjau isi produk. Foto sintetis kecil hanya untuk ilustrasi perpindahan Andi ke Maya. Contoh tidak mengklaim keluaran AI aktual, angka manfaat atau pelanggan.

Validasi aktual pada Chrome cloud desktop 1363×940:

| Pemeriksaan | Hasil |
|---|---|
| Syntax JavaScript dan build aset | Lulus |
| Bagian app.js di luar fungsi home/helper | Dibandingkan sebelum/sesudah, identik |
| Tiga tab pratinjau | Brief, pekerjaan, sumber berubah sesuai pilihan |
| Keyboard tab | ArrowDown ke sumber dan Home ke brief berhasil; aria-selected sesuai |
| Kutipan contoh | Dialog menampilkan judul, baris, versi dan kutipan sintetis |
| FAQ | Buka/tutup; penjelasan keterbatasan agent tersedia |
| Tema gelap dan terang | Diperiksa visual; tidak ada overflow horizontal desktop |
| CTA pengguna belum masuk | Masuk ke pemilih profil demo, lalu Dashboard Andi berhasil |
| CTA pengguna aktif | Mengarah ke Dashboard akun aktif |
| Pratinjau dan scroll | Jelajahi contohnya mengarahkan ke panel produk |
| Layout viewport kecil | Media query tersedia; belum diuji viewport/perangkat mobile aktual |

Catatan QA: klik tab pertama yang dibatch saat smooth scroll berjalan belum mengubah panel; setelah memeriksa state dan mengklik pada posisi stabil, tab berfungsi. Teks kecil panel dokumen ditingkatkan kontrasnya. Tidak menambah tes unit untuk perubahan presentasi yang bisa dibalik. Laporan 79 tes backend sebelumnya tetap tersimpan dengan timestamp aslinya; bukan klaim tes tersebut dijalankan ulang untuk perubahan ini.

Tidak ada pemanggilan model, penggunaan aplikasi WorkBuddy aktual, push, deploy atau publikasi. Screenshot pratinjau dalam percakapan bukan bukti penggunaan WorkBuddy. Lihat browser-mvp.md untuk pemeriksaan fungsi handover sebelumnya.
