# Acuan dan interpretasi

- Tencent Cloud Hackathon Indonesia 2026 Handbook.pdf, bagian 3, 6, 7, 10: Challenge A, test, submission, kriteria penjurian. Materi disediakan pengguna dan telah dibaca dalam percakapan.
- workbuddy-adopter-brainstorm-2026-10-29-v7.pdf, halaman 9–16: workflow folder WorkBuddy; deadline diperbarui 7 November 2026 (jam penutupan belum dipastikan).
- Relayfy_Project_Brief.md: versi produk yang disepakati pengguna; salinan ada di PROJECT_BRIEF.md.
- percakapan-sesi-2026-10-29.md.pdf: contoh Rukun, bukan aturan resmi atau bukti pengujian Relayfy. Klaim teknis di contoh tidak otomatis benar untuk versi aplikasi pengguna.
- WorkBuddy Permission Modes: https://www.codebuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Permission-Modes — dokumentasi resmi yang diperiksa 1 November 2026. Default Permissions adalah guardrail, tidak dianggap jaminan isolasi database.

Penyesuaian brief pada versi pembanding awal (digantikan pembaruan web di bawah): UI empat halaman saat itu ditunda; file instruksi dibaca eksplisit tanpa mengklaim skill terpasang otomatis; backend lokal ekstraktif dan orkestrasi AI WorkBuddy dibedakan; review/accept tetap ada. Paket ini tidak memuat dokumen sumber berhak cipta atau dataset resmi yang belum tersedia.

Pembaruan 2 November 2026: handbook bagian Challenge A dan submission dibaca ulang dari dokumen yang disediakan. Web empat halaman kini dikerjakan atas instruksi terbaru pengguna; ini menggantikan penundaan UI pada versi pembanding. Approval terminal tetap hanya di mode legacy; web memakai sesi/preview UI. Bukti WorkBuddy belum ada dan tidak digantikan oleh website.

Dokumentasi teknis resmi yang diperiksa untuk keputusan implementasi:
- https://render.com/docs/disks — filesystem default ephemeral, disk permanen diperlukan; disk melekat pada layanan berbayar.
- https://render.com/docs/docker — hosting container; tidak ada layanan yang dibuat.
- https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create — kontrak Chat Completions dan JSON response format.
- https://pypi.org/project/gunicorn/26.2.0/ dan https://gunicorn.org/2026-news/ — versi runtime yang diinstal dan diuji lokal.

Tidak ada dataset resmi yang diunduh, akun WorkBuddy yang digunakan, atau formulir yang dikirim pada pengerjaan web ini. Acuan handbook tidak boleh diartikan seluruh kasus resmi telah lulus; resolusi konflik otomatis berdasarkan otoritas belum tersedia pada parser MVP.


Pembaruan 4 November 2026: instruksi pengguna kini memprioritaskan MVP lokal berdesain seperti referensi dan runtime WorkBuddy. Jalur web + antrean CLI/MCP ditambahkan, core dan adapter API dipertahankan. Tidak perlu key API website untuk jalur runtime WorkBuddy. Artefak versi lama dan bukti legacy tidak dianggap hasil aplikasi WorkBuddy aktual.

Dokumentasi resmi yang diperiksa untuk sambungan baru:
- https://www.workbuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Skills — aktivasi skill harus dibedakan dari sekadar ada file instruksi. AGENTS.md dibaca eksplisit; tidak mengklaim skill telah terpasang.
- https://open.workbuddy.cn/en/docs/connector — connector CLI/MCP stdio, command/args dan wrapper mcpServers. Konfigurasi aplikasi aktual belum diuji; CLI disediakan sebagai jalur awal.
- https://modelcontextprotocol.io/specification/2025-03-26/basic/transports — stdio JSON-RPC per baris, tanpa log nonprotokol di stdout. Implementasi lokal diuji subprocess, bukan sertifikasi kompatibilitas seluruh MCP client.

Foto profil sintetis dibuat menggunakan ImageGen selama pembangunan ini; bukan foto pegawai nyata. Desain mengambil arah visual gelap/komposisi referensi pengguna tanpa memakai nama atau identitas Nohalu/SafeDesk. Tidak mengklaim dukungan penyelenggara.
