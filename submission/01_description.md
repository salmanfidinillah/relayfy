# Relayfy — AI Handover Assistant

**Blurb (9 kata):** AI handovers with sources, access controls, and human approval.

**Challenge A — The Workplace Brain.** Skenario project history dan perpindahan tanggung jawab.

Saat tanggung jawab berpindah, orang baru perlu memahami keputusan yang sudah diambil, pekerjaan yang masih terbuka dan alasan di baliknya. Konteks itu sering berada di dokumen, percakapan dan daftar tugas yang terpisah. Relayfy menyatukannya menjadi handover yang dapat ditanyakan, diperiksa sumbernya, lalu diterima sebagai versi yang jelas. Masalah ini adalah hipotesis produk; belum divalidasi melalui wawancara atau pengukuran di perusahaan.

Pengguna utama adalah pemberi pekerjaan, penerima dan anggota proyek. Dalam skenario sintetis Karsa, Andi menyerahkan proyek kepada Maya. Brief menunjukkan tujuan, keputusan, pekerjaan, hambatan dan informasi kosong. Chat membantu Maya menanyakan alasan penundaan dan memeriksa kutipannya. Konflik jadwal dari dua sumber tetap ditampilkan untuk diklarifikasi, bukan ditebak sebagai tanggal final.

MVP web menampilkan Dashboard, Workspace, Ask Relayfy, daftar sumber/tugas, pemeriksaan kelengkapan, Review dan Activity Log. Pengguna dapat memasukkan teks, ekspor chat serta tugas terstruktur manual. Draf disusun berdasarkan sumber yang diizinkan bagi penerima dan pemberi, tetap privat sebelum ditinjau. Penerimaan berlaku pada versi tertentu; pembaruan sumber atau izin memerlukan peninjauan ulang.

Arsitektur mempertahankan Python WSGI, SQLite dan HTML/CSS/JavaScript. Jalur AI utama adalah **antrean web → tool WorkBuddy → model dalam WorkBuddy → validator server → hasil web**. WorkBuddy menjadi runtime penalaran melalui client CLI Python atau empat tools MCP stdio. Website tidak memakai kredit WorkBuddy sebagai API publik. Adapter API model backend juga tersedia sebagai pilihan terpisah.

Otorisasi berada di kode. Identitas berasal dari sesi server, membership dan ACL diperiksa sebelum retrieval. Key worker dibatasi akun/workspace/revisi/tujuan; setiap klaim memerlukan ID dan kutipan persis dari bukti job. Lease, versi dan akses diperiksa kembali saat hasil diterima. Worker tidak dapat menjalankan approval. Import, audiens, review/share, klarifikasi dan accept melewati preview, konfirmasi aktor serta transaksi dengan audit. Pilihan profil foto adalah simulasi identitas khusus demo lokal dan dilarang pada konfigurasi produksi.

Prompt berfungsi menjaga fokus penalaran: bukti dianggap data, instruksi tersisip diabaikan, identitas dari server tidak dapat diganti lewat chat, dan bukti yang tidak memadai menghasilkan unknown atau klarifikasi. Prompt tidak menggantikan batas akses. Struktur JSON dan kutipan dapat divalidasi, sedangkan kebenaran semantik masih membutuhkan review. Ketika konteks akses berubah, operator wajib membuka task WorkBuddy baru; server tidak dapat menghapus ingatan model atau menutup akses shell OS secara otomatis.

Manfaat yang ingin diuji adalah waktu memahami proyek, ketepatan jawaban bersumber dan penemuan informasi kurang sebelum tanggung jawab diterima. Belum ada angka penghematan. Evaluasi selanjutnya membandingkan pertanyaan manual dan Relayfy pada dataset yang sama dengan urutan acak, waktu, akurasi dan kegagalan yang dilaporkan apa adanya.

Bukti lokal: 79 tes kode, 10 pemeriksaan runtime produksi, serta uji browser dua profil dengan import CSV, draf privat, kutipan, klarifikasi, review, accept, antrean dan revokasi. Jawaban model pada tes transport adalah fixture, bukan inferensi aktual. Aplikasi/model WorkBuddy, dataset resmi, video dan deploy belum diuji/dilakukan. Batas MVP mencakup retrieval kata, task terstruktur, konflik field tanpa penentuan otoritas otomatis dan autentikasi tanpa verifikasi email/SSO/MFA.
