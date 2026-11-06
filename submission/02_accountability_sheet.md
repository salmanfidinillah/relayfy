# Relayfy — Accountability Sheet

**Pemilik:** Salman Fidinillah · **Lingkup:** MVP web + runtime WorkBuddy, Challenge A, data sintetis.

| Area | Perilaku aktual |
|---|---|
| Identitas | Sesi server dan password scrypt; chat tidak mengubah peran. Profil foto adalah simulasi khusus demo lokal, dilarang di produksi. Produksi: Secure/HttpOnly, origin dan CSRF; belum verifikasi email/SSO/MFA. |
| Akses | Membership/ACL sebelum retrieval; browser dan worker hanya menerima bukti berizin. Brief mengikuti akses penerima dan pemberi. Key worker terikat akun, workspace, revisi, tujuan dan masa berlaku. |
| Otonom | Retrieval, task/gap terstruktur, konflik field dan draf privat. WorkBuddy mengisi job via CLI/MCP. Kutipan/lease/revisi divalidasi; tool agent tidak bisa menyetujui tindakan bisnis. |
| Persetujuan | Import/audiens, review/share, klarifikasi dan accept melalui preview serta konfirmasi UI. Actor/revisi/status/brief terbaru diperiksa lagi. Mutasi dan audit approval satu transaksi. |
| Ketidakpastian | Tanpa bukti: belum diketahui tanpa menyiratkan sumber privat. Konflik: tampilkan dua rujukan dan minta klarifikasi. PIC/deadline kosong tidak ditebak. Kutipan valid belum menjamin makna klaim benar. |
| Rekam | Query, sumber, versi, job, hasil, approval dan tindakan di SQLite. UI audit hanya aktivitas sendiri pada revisi aktif. Token tidak dicetak ke log; audit bukan immutable. |
| Revokasi | Request berikut mengikuti ACL baru; history/brief/job/lease/plan lama ditolak. UI polling sekitar 3 detik. Task dan pairing baru wajib; ingatan model/data yang sudah dilihat tidak bisa dihapus server. |
| Batas agent | Evidence adalah data, bukan instruksi. Tidak mengirim email, membeli layanan atau memublikasikan otomatis. Folder agent bukan sandbox OS; data nyata memerlukan isolasi filesystem dan evaluasi. |
| Bukti aktual | 79 tes, 10 smoke checks, browser dua profil. CLI HTTP/MCP stdio memakai fixture berlabel; aplikasi/model WorkBuddy, provider API nyata, dataset resmi, Docker, video dan deploy belum diverifikasi. Tidak ada klaim penghematan. |

**Sebelum data nyata:** verifikasi identitas, kualitas model, isolasi agent, HTTPS, volume/backup dan evaluasi independen. Demo dan persetujuan klik otomatis pada pengujian bukan persetujuan pengguna bisnis nyata.
