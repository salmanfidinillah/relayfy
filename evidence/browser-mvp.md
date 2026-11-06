# Pengujian browser aktual MVP — 4 November 2026 (WIB)

Lingkungan: Chrome cloud desktop, 1363×940, preview lokal terisolasi. Aplikasi web benar-benar disajikan oleh WSGI dan dioperasikan melalui UI. Data/profil Karsa sintetis. Approval diklik oleh otomasi QA, bukan persetujuan manusia bisnis. WorkBuddy/model aktual tidak dijalankan. Tidak ada deployment.

| Skenario | Pengamatan nyata | Hasil |
|---|---|---|
| Workspace baru | Maya membuat workspace baru dengan Andi sebagai penerima; kosong 0 sumber; menyusun brief ditolak dengan pesan tambahkan sumber | lulus |
| Import teks manual | Workspace baru menerima dokumen melalui preview/konfirmasi; 1 sumber, 2 anggota, revisi 2 | lulus |
| Label peran aktif | Maya yang menjadi pemberi pada workspace baru ditampilkan sebagai Pemberi handover, mengikuti workspace | lulus setelah perbaikan |
| Landing dan profil | Hero gelap, geometri oranye, profil foto fiktif, empat pilihan profil; tautan berfungsi | lulus |
| Sesi Andi/Maya | Pilihan profil memberi sesi server; Ganti profil logout; nama dan peran UI sesuai | lulus |
| Dashboard berizin | Awal baru: Andi 6 sumber, Maya 5; 3 pekerjaan terbuka | lulus |
| Ringkasan bukti | Pemberi menyusun draf ekstraktif berlabel Kutipan tanpa AI | lulus |
| Draf privat | Beralih ke Maya sebelum review/share: Menunggu handover dari pemberi | lulus |
| Review/share | Preview aktor, revisi, brief; konfirmasi baru mengubah status Siap diterima | lulus |
| Klarifikasi | Maya mengirim pertanyaan PIC pengganti; Andi melihat teks pertanyaan pada Review | lulus |
| Accept | Setelah peninjauan ulang, Maya mengonfirmasi; status Diterima; tugas terbuka tetap ada | lulus |
| Audit | Aktivitas sendiri dan permintaan/tindakan persetujuan tampil | lulus |
| Chat bukti | Alasan penundaan mengutip foto produk; label bukan sintesis model; konflik tanggal tampil | lulus |
| Buka kutipan | Dialog sumber menunjukkan karsa-chat:2, versi, tanggal dan teks | lulus |
| Pertanyaan terbatas | Maya: Anggaran Kenari? → Informasi belum tersedia untuk pertanyaan ini. Tidak menyebut sumber privat | lulus |
| Antrean nyata | Mode WorkBuddy: pertanyaan PIC pembayaran menghasilkan Pending, menunggu tool; bukan jawaban palsu | lulus |
| Pairing dan cancel | UI membuat konfigurasi tanpa menampilkan token; tombol unduh tersedia; cancel menghapus antrean aktif | lulus untuk UI; file unduhan tidak diuji |
| Revokasi | Andi mencabut akses chat Maya melalui preview/konfirmasi → revisi 2; sumber Maya 5→4 | lulus |
| Turunan setelah revokasi | Chat Maya kembali kosong; brief yang sebelumnya diterima tidak lagi ditampilkan | lulus |
| Upload CSV | File chooser import-tasks.csv; judul berkoma menjadi satu task; preview/konfirmasi; kedua task muncul di tabel | lulus |
| Data demo diperbaiki | Pada restart preview versi final: 2 gap PIC/deadline + 1 konflik tanggal; tidak ada konflik Catatan palsu | lulus |
| Pilihan mode dipertahankan | Setelah kirim, Bukti sumber · tanpa AI tetap terpilih | lulus setelah perbaikan |

Temuan dan penanganan:

1. Mode jawaban semula kembali ke WorkBuddy setelah kirim. State mode disimpan, syntax check dan browser ulang membuktikan tetap pada mode bukti.
2. Field Catatan generik dari dua dokumen demo menimbulkan konflik yang tidak bermakna. Salah satu label diperjelas menjadi Arti penerimaan; dataset baru memperlihatkan 3 temuan, bukan 4. Parser konflik tetap terbatas field, belum semantik.
3. Beberapa locator harness memakai judul/label tebakan dan gagal menemukan elemen. Disesuaikan berdasarkan accessibility tree; tindakan berhasil. Ini bukan bukti error aplikasi.
4. Restart preview membuat filesystem/container sementara baru dan membatalkan sesi sebelumnya. Dataset baru disiapkan otomatis. Persistensi aplikasi di path yang sama diuji terpisah lewat Gunicorn restart; jangan memakai preview sebagai bukti volume hosting.
5. Label profil sidebar semula memakai badge demo global. Pada workspace baru Maya adalah pemberi, tetapi badge menyebut penerima. Label diganti mengikuti giver/receiver workspace aktif; reload browser membuktikan Pemberi handover.
6. Log browser memuat error chrome-extension saat mengirim metadata ke extension. Error berasal dari URL chrome-extension, bukan server aplikasi; tidak dianggap bukti semua console bersih.

Batas: viewport mobile/perangkat fisik, Windows launcher, unduhan koneksi, MCP UI WorkBuddy, aplikasi/model WorkBuddy, provider API nyata, semua format upload, concurrent tab jangka panjang, dataset resmi dan hosting belum diuji browser. CLI HTTP/MCP protocol, fail/lease/replay, forged quote, stale acceptance dan rollback audit diuji otomatis dengan fixture, bukan model nyata.

Tampilan home dan chat ditangkap untuk inspeksi/pratinjau percakapan ini; tidak menjadi screenshot test resmi atau bukti WorkBuddy. Rekaman video belum dibuat. Catatan versi sebelumnya tersimpan di browser-results.md dengan tanggal dan lingkupnya sendiri.


Pembaruan landing setelah pengujian MVP awal: desain hero/pratinjau diganti. Hasil pemeriksaan presentasi terbaru berada di landing-polish.md. Catatan awal di atas tetap merupakan riwayat uji versi sebelumnya.
