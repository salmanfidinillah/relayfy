# Relayfy — AI Handover Assistant

**Blurb (8 kata):** AI handovers with sources, access controls, and accountability.

**Track:** A — The Workplace Brain. Skenario: riwayat proyek dan onboarding penerima handover.

Relayfy membantu penerima tanggung jawab memahami status proyek, keputusan, pekerjaan terbuka, dan informasi yang masih kurang. Bahan handover berasal dari dokumen, ekspor chat, dan daftar tugas. Prototipe memisahkan pencarian berbasis izin dari antarmuka AI agar sumber dibatasi sebelum diteruskan ke model.

Persona sintetis: Andi menyerahkan proyek website kepada Budi. Tanggal peluncuran berbeda di catatan awal dan chat; tugas pembayaran belum memiliki PIC/deadline; anggaran hanya tersedia bagi manajer. Data ini adalah contoh, bukan hasil wawancara atau data perusahaan nyata. Validasi masalah dengan calon pengguna masih perlu dilakukan.

Alur: identifikasi sesi → filter sumber → pencarian/analisis → kutipan, konflik, dan gap → draf handover → review pemberi → penerimaan versi oleh penerima → audit. Sistem dapat meminta klarifikasi atau mengakui tidak tahu. Perubahan bisnis memakai preview dan persetujuan operator yang terpisah dari bridge.

Implementasi: Python standard library, SQLite, API HTTP loopback, client tool, dan kontrak runtime WorkBuddy. Local engine mengekstrak bukti secara deterministik; model WorkBuddy direncanakan menyusun jawaban dari bukti melalui tool. Percakapan model belum dijalankan dalam paket pembanding ini.

Nilai yang ingin diuji: waktu mencari jawaban, ketepatan rujukan, jumlah gap ditemukan, dan ketepatan penolakan akses. Belum ada angka penghematan tervalidasi. Rencana pengukuran: minta beberapa pengguna menjawab kumpulan pertanyaan yang sama secara manual dan dengan Relayfy; acak urutan dan laporkan waktu, akurasi, ukuran sampel, serta keterbatasan.

Pembeda: briefing sesuai audiens, konflik yang terlihat, status diterima per versi, dan pembatalan akses terhadap hasil turunan. Keterbatasan: pencarian sederhana, ekstraksi task berformat, deteksi injeksi terbatas, isolasi OS belum dibuktikan, dan tidak ada dashboard web. Tidak mengklaim kesetaraan keamanan atau fitur dengan produk enterprise.
