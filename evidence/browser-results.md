# Pengujian browser aktual — 2 November 2026 (WIB)

Lingkungan: cloud Chrome, preview lokal terisolasi `terminal.local`, data dan akun fiktif (Andi QA / Budi QA, domain example.test). Interaksi melalui UI nyata. Persetujuan diklik oleh otomasi pengujian; ini **bukan** bukti persetujuan manusia pengguna dan bukan sesi WorkBuddy. Tidak ada inferensi model nyata.

| Skenario | Hasil yang diamati | Status |
|---|---|---|
| Daftar dan login dua akun | Dashboard menampilkan identitas akun yang sesuai; logout lalu login akun lain | Lulus |
| Dashboard kosong → buat workspace | Penerima harus sudah mendaftar; workspace tampil dan bisa dibuka | Lulus |
| Tambah dokumen, chat, tugas manual | Form → preview detail/audiens → konfirmasi → jumlah sumber/revisi berubah | Lulus |
| Sumber privat | Pemberi melihat empat sumber; penerima melihat tiga; brief penerima tidak berisi anggaran privat | Lulus |
| Gap dan konflik | Dua tugas (satu terbuka), PIC/deadline kosong, dua tanggal peluncuran dan permintaan klarifikasi | Lulus |
| Buka kutipan | Dialog menampilkan judul, ID/baris, versi dan teks sumber yang diizinkan | Lulus |
| Susun brief tanpa API key | Pesan “Model AI belum dikonfigurasi…”; tidak membuat brief AI palsu | Lulus |
| Ringkasan bukti | Diberi label tanpa AI; bisa direview/dibagikan | Lulus |
| Review oleh pemberi | Dialog konfirmasi sebelum berbagi, status “Siap diterima”; penerima melihat versi | Lulus |
| Klarifikasi | Penerima mengirim pertanyaan melalui konfirmasi; pemberi melihat teks pertanyaan dan status | Lulus setelah perbaikan |
| Accept oleh penerima | Dialog konfirmasi; status “Diterima”; catatan tugas terbuka tetap ada | Lulus |
| Activity Log | Riwayat sendiri, termasuk permintaan persetujuan dan tindakan, tampil | Lulus |
| Ask tanpa kredensial | Halaman percakapan terbuka; query menampilkan error konfigurasi tanpa jawaban/history palsu | Lulus |
| Revokasi sumber | Pemberi mencabut akses melalui preview dan konfirmasi; penerima melihat Sumber (0), Pekerjaan (0), Draf revisi baru | Lulus |
| Brief/log setelah revokasi | Penerima melihat “Menunggu handover dari pemberi” dan “Belum ada aktivitas pada revisi ini” | Lulus |

Kegagalan yang ditemukan dan ditangani:

1. Preview launcher menambahkan `--strictPort`; development runner semula menolak argumen itu. Runner kini menerimanya, preview berhasil.
2. Locator pengujian label jenis sumber tidak cocok dengan nama aksesibel select. Pengujian dilanjutkan memakai selector form yang spesifik; UI tetap bisa memilih jenis.
3. Klarifikasi awal hanya tercatat pada log penerima sehingga pemberi belum dapat melihat pertanyaan. Ditambahkan tabel klarifikasi dan panel pada workspace, dibatasi revisi dan pihak handover. Uji ulang memperlihatkan “Siapa PIC pengganti pembayaran?” di akun pemberi.
4. Restart daemon preview membuat lingkungan sementara baru; akun/bahan preview disiapkan ulang. Ini keterbatasan preview, bukan bukti persistensi hosting. Persistensi aplikasi diuji terpisah dengan restart Gunicorn dan path database yang sama (production-smoke.json).

Belum diuji lewat browser: model/provider nyata, hasil AI dengan API key, upload file melalui file chooser, viewport mobile/perangkat fisik, concurrency multi-tab setelah idle panjang, runtime WorkBuddy, serta hosting publik. Parser unggah dan CSS responsif tersedia pada source, tetapi jangan menganggap tabel ini sebagai bukti semua format/perangkat diuji.

Tes lintas pengguna nonanggota, stale/replay approval, draf baru pada revisi yang sama, ACL berubah saat model berjalan, provider error, JSON/kutipan palsu, dan rollback audit diuji otomatis pada test_web.py. Fixture adalah simulasi. Screenshot pemeriksaan digunakan internal; paket screenshot test resmi masih menunggu dataset dan WorkBuddy aktual.
