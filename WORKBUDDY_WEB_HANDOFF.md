# Handoff runtime Relayfy ke WorkBuddy

Versi 0.3 memakai **web + antrean job + runtime WorkBuddy** sebagai jalur demo utama. Kode dibuat di ChatGPT/Codex. Jangan mengklaim kontribusi WorkBuddy sebelum tools benar-benar dijalankan.

1. Operator menjalankan server dari `MULAI_DI_SINI.md`.
2. Di web, operator memilih profil dan tujuan, menyimpan koneksi terbatas di `relayfy-agent/`.
3. WorkBuddy membuka hanya `relayfy-agent/`, membaca `AGENTS.md` dan `START_HERE.md`, lalu memproses satu job melalui client CLI atau MCP. Tidak perlu mengubah kode.
4. Bukti → susunan hasil model WorkBuddy → validator server → jawaban/draf. Persetujuan tetap melalui sesi manusia di web.
5. Simpan output tools dan percakapan aktual, kegagalan dan kredit sebelum/sesudah pada template evidence. Tidak ada angka kredit yang dapat diklaim dari pengerjaan paket ini.

Buka task baru dan pairing ulang ketika profil, revisi atau tujuan berubah. Backend membatalkan key/lease lama, tetapi tidak dapat menghapus konteks model. Shell pada OS yang sama bukan sandbox; gunakan hanya data sintetis sampai isolasi tersedia.

`workbuddy/bridge.py` dan README_LEGACY.md adalah pembanding lama pada database terpisah. Untuk demo baru gunakan **relayfy-agent/client.py**, bukan bridge legacy. Adapter API website tetap tersedia opsional, tidak memakai kredit aplikasi WorkBuddy.
