# Checklist Relayfy MVP — 4 November 2026

Target terbaru: web lokal dengan desain gelap seperti referensi; serta alur agent melalui WorkBuddy. Pengujian aplikasi WorkBuddy, deployment, dan pengiriman submission masih menunggu.

| Pekerjaan | Status | Bukti dan batas |
|---|---|---|
| Inspeksi fondasi dan baseline | selesai | Core Python/SQLite dipertahankan; baseline 59 tes |
| Perhalusan landing editorial | selesai | Pratinjau tab, keyboard, kutipan, FAQ, dark/light, CTA; evidence/landing-polish.md |
| Landing, profil foto, Dashboard dan sidebar | selesai | web/; foto/identitas sintetis, visual diperiksa browser desktop |
| Workspace, Chat, Sumber, Task, Gaps, Review, Log | selesai | UI terhubung API nyata; tanpa respons AI hardcoded |
| Mode profil lokal + sesi server | selesai | 4 profil; demo ditolak produksi; akun sungguhan tetap tersedia |
| Auth / membership / ACL sebelum retrieval | selesai | Scrypt, cookie, origin/CSRF; test lintas akun dan nonanggota |
| Import teks/chat/TXT/MD/CSV/JSON | selesai | Paste dan file chooser CSV diuji; semua format file belum diuji via browser |
| Kutipan, tugas, gap dan konflik | selesai | Parser terstruktur/kata; otoritas konflik tidak ditebak |
| Draf privat dan human review/share | selesai | Browser membuktikan draf tidak terlihat penerima sebelum dibagikan |
| Klarifikasi dan accept versi | selesai | Browser dua profil; preview/konfirmasi; tugas terbuka tetap ada |
| Antrean WorkBuddy + scoped pairing | selesai | Key akun/workspace/revisi/tujuan, lease/expiry, cancel/fail/replay |
| CLI HTTP + MCP stdio empat tools | selesai | Subprocess nyata dalam tes, jawaban fixture berlabel |
| Revokasi sumber dan hasil turunan | selesai | Kode + browser; history/brief/job/plan lama ditolak |
| Hasil/job/audit atomik | selesai | Kegagalan audit membatalkan penyimpanan hasil dan approval |
| Test utama 79/79 | selesai | evidence/test-results.json; 20 tes runtime agent ditambahkan |
| Build aset | selesai | dist/build-manifest.json; source tetap buildless |
| Gunicorn restart/session 10/10 | selesai | evidence/production-smoke.json; loopback, bukan deploy/volume hosting |
| Uji browser desktop dua profil | selesai | evidence/browser-mvp.md; klik approval dilakukan otomasi QA |
| Quickstart dan prompt satu job | selesai | MULAI_DI_SINI.md; relayfy-agent/START_HERE.md |
| Deskripsi, accountability satu halaman, diagram | selesai | submission/; PDF/SVG dirender dan diperiksa |
| Naskah video 5–8 menit | selesai | submission/05_demo_video_script.md; bukan video jadi |
| Product sharing dan draf form | selesai | Draf faktual; kontribusi WorkBuddy aktual belum terisi |
| Paket clean ZIP / uji hasil ekstraksi | selesai | 79 tes dari ekstraksi, manifest/secret check, demo HTTP/restart/backup; evidence/artifact-checks.json |
| Aplikasi/model WorkBuddy aktual | terhambat | Tidak tersedia pada lingkungan pembuat; jalankan di laptop operator |
| Provider API opsional nyata | terhambat | Key/model belum tersedia; tidak diperlukan untuk jalur WorkBuddy lokal |
| Dataset dan test case resmi | terhambat | Belum tersedia; pengujian lokal sintetis |
| Windows launcher / mobile fisik | belum dikerjakan | Disiapkan, belum diuji pada perangkat tersebut |
| Docker image / volume hosting / redeploy | belum dikerjakan | Docker tidak tersedia; deployment tidak diotorisasi |
| Video dan formulir | belum dikerjakan | Repositori sumber tersedia di GitHub |

Folder agent bukan sandbox OS. Task baru dan pairing ulang wajib saat konteks akses berubah. Server dapat menolak hasil lama tetapi tidak dapat menghapus ingatan model atau informasi yang sudah dilihat. Kebenaran semantik tetap memerlukan review. Tidak ada klaim penghematan waktu atau kredit WorkBuddy yang belum diukur.
