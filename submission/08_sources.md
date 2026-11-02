# Acuan dan interpretasi

- Tencent Cloud Hackathon Indonesia 2026 Handbook.pdf, bagian 3, 6, 7, 10: Challenge A, test, submission, kriteria penjurian. Materi disediakan pengguna dan telah dibaca dalam percakapan.
- workbuddy-adopter-brainstorm-2026-10-29-v7.pdf, halaman 9–16: workflow folder WorkBuddy; deadline diperbarui 7 November 2026 (jam penutupan belum dipastikan).
- Relayfy_Project_Brief.md: versi produk yang disepakati pengguna; salinan ada di PROJECT_BRIEF.md.
- percakapan-sesi-2026-10-29.md.pdf: contoh Rukun, bukan aturan resmi atau bukti pengujian Relayfy. Klaim teknis di contoh tidak otomatis benar untuk versi aplikasi pengguna.
- WorkBuddy Permission Modes: https://www.codebuddy.ai/docs/workbuddy/From-Beginner-to-Expert-Guide/Function-Description/Permission-Modes — dokumentasi resmi yang diperiksa 1 November 2026. Default Permissions adalah guardrail, tidak dianggap jaminan isolasi database.

Penyesuaian brief: UI empat halaman ditunda; file instruksi dibaca eksplisit tanpa mengklaim skill terpasang otomatis; backend lokal ekstraktif dan orkestrasi AI WorkBuddy dibedakan; review/accept tetap ada. Paket ini tidak memuat dokumen sumber berhak cipta atau dataset resmi yang belum tersedia.

## Catatan eksekusi ulang (2026-11-02)

Seluruh pengujian lokal dijalankan ulang di laptop pengguna: Windows, Python 3.13.14, tanpa paket pip tambahan. Hasil 28 tes dari lingkungan pembuat paket direproduksi, lalu ditambah empat tes regresi setelah perbaikan intent routing (total 32). Kasus bridge W01–W06 dijalankan lewat HTTP dengan token persona asli. Yang **belum** diverifikasi: percakapan WorkBuddy, persetujuan manusia pada W07–W08, pencabutan akses W09, isolasi filesystem W10, dataset resmi, dan seluruh bukti submission (screenshot, video, repo).

