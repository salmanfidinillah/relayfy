# Mulai di sini — Relayfy MVP

**Tujuan:** web Relayfy ditampilkan di browser; agent benar-benar mengerjakan permintaan melalui WorkBuddy di laptop yang sama. Tidak perlu deploy untuk mencoba paket ini.

## Pilih cara membuka proyek

Klon repositori untuk langsung menjalankan web. Untuk mencoba impor Skill di WorkBuddy, buat arsip dengan `python scripts/package.py --workbuddy-skill --output ../Relayfy_MVP_WorkBuddy.zip`, lalu ikuti langkah berikut.

1. Di WorkBuddy Desktop, buka **Experts · Skills · Connectors → Skills → Add Skill → Upload Skill**, lalu pilih `Relayfy_MVP_WorkBuddy.zip`. Paket menyertakan `SKILL.md` di akar arsip. Aktifkan Skill **relayfy** setelah impor berhasil.
2. Ekstrak ZIP yang sama ke satu folder lokal. Folder utama berisi `START_RELAYFY.bat` dan `relayfy-agent`. Landing terbaru sudah tergabung.
3. Jalankan web dan buat file koneksi sesuai langkah di bawah. Pada task WorkBuddy, pilih **Open Local Folder** dan arahkan ke `relayfy-agent`. Aktifkan Skill relayfy dan kirim **Proses satu pekerjaan Relayfy yang sudah saya kirim dari web.**

Jika impor Skill belum tersedia di aplikasi, buka `relayfy-agent` sebagai folder lokal dan pakai prompt siap tempel di `relayfy-agent/START_HERE.md`. Kedua cara memakai client dan antrean yang sama. Pemeriksaan impor pada WorkBuddy Desktop dilakukan saat mencoba di laptop.

## 1. Buka web

1. Buka folder proyek yang berisi `START_RELAYFY.bat`.
2. Pastikan Python 3.10+ tersedia. Windows: klik `START_RELAYFY.bat`; terminal alternatif `py -3 run_demo.py`. macOS/Linux: `python3 run_demo.py`.
3. Buka `http://127.0.0.1:8765/`. Jangan ganti menjadi localhost. Pilih **Andi Pratama**.
4. Data Karsa tersedia otomatis: 6 sumber untuk Andi, 5 untuk Maya, 4 tugas (3 terbuka), 2 gap dan 1 konflik tanggal pada dataset awal baru. Satu sumber berisi instruksi tersisip sebagai bahan uji. Semua sintetis.

Terminal harus tetap terbuka. Tidak perlu menjalankan build untuk memakai web. Port terpakai? Tutup server Relayfy lama atau jalankan `python3 run_demo.py --port 8770 --origin http://127.0.0.1:8770`, lalu buka origin tersebut. Jangan menghapus database untuk memperbaiki port.

## 2. Coba alur tanpa model dahulu

Andi → Workspace → **Lihat ringkasan bukti**. Buka kutipan, lihat Pekerjaan/Kelengkapan. Ini ekstraktif, bukan keluaran AI. **Tinjau & bagikan versi** menampilkan pratinjau; konfirmasi diperlukan sebelum penerima membacanya. Ganti profil ke Maya → Review → minta klarifikasi atau terima versi siap. Klik Ganti profil melakukan logout sesi saat ini.

Di Chat, mode **Bukti sumber · tanpa AI** memberi kutipan langsung. Pertanyaan `Anggaran Kenari?` dari Maya menghasilkan `Informasi belum tersedia untuk pertanyaan ini.` tanpa menyiratkan sumber terbatas. Jangan menyebut hasil ekstraktif sebagai AI pada demo.

## 3. Jalankan agent dengan WorkBuddy

1. Pilih Andi → Workspace → **Susun brief dengan agent**. Ini membuat job menunggu.
2. **Hubungkan WorkBuddy** → tujuan **Susun brief untuk penerima** → siapkan/unduh file koneksi. Simpan bernama `relayfy-connection.json` di `relayfy-agent/`.
3. Buka **folder `relayfy-agent` saja** di WorkBuddy. Buat **task baru**. Baca `START_HERE.md`, tempel prompt satu job dari sana. Tidak perlu menyuruh WorkBuddy membuat ulang aplikasinya.
4. Pastikan WorkBuddy menjalankan `client.py next`, membaca bukti, lalu `client.py finish`. Status harus Done. Website polling sekitar tiga detik; draf bersumber akan muncul. Tinjau dan bagikan lewat UI.
5. Untuk percakapan Maya: ganti profil ke Maya di web, pairing tujuan pertanyaan akun ini, ganti file koneksi, buat task WorkBuddy baru. Ajukan `Mengapa peluncuran tertunda?`, jalankan prompt satu job lagi.
6. Untuk pertanyaan berikutnya pada profil/workspace/revisi/tujuan yang sama, prompt satu job dapat dipakai lagi pada task yang sama. Setelah izin/sumber/tujuan/profil berubah, task baru dan pairing ulang wajib dilakukan.

Jangan merekam file koneksi, token, .env, atau data pribadi. File koneksi berumur empat jam dan pairing ulang membatalkan token lama. Tool tidak dapat menerima handover atau mengubah akses; keputusan tetap di web.

**Hasil yang diharapkan, belum bukti WorkBuddy nyata:** brief memuat sumber yang diizinkan penerima; jawaban penundaan mengutip foto produk; konflik 7/9 November dijelaskan tanpa menetapkan tanggal final; PIC/deadline pembayaran tetap belum diketahui. Jika WorkBuddy belum menjalankan tools, web tetap menunggu. Batalkan antrean melalui UI bila perlu.

## 4. Bila koneksi gagal

| Gejala | Langkah |
|---|---|
| Python tidak ditemukan | Gunakan interpreter yang terpasang: `py -3`, `python` atau `python3`. Instal Python dari sumber resmi jika belum ada. |
| File koneksi belum ada | Simpan hasil unduhan tepat di folder `relayfy-agent`, nama `relayfy-connection.json`, bukan `.json.json`. |
| Server tidak terjangkau | Biarkan terminal server terbuka; web dan WorkBuddy harus pada laptop yang sama. Jangan memakai URL preview cloud. |
| Tidak ada antrean | Ajukan pertanyaan / susun brief di web; cek tujuan koneksi sesuai ask/brief dan profil benar. |
| Akses/revisi berubah | Hentikan task lama, buat task baru, pairing ulang, ajukan permintaan baru. |
| Kutipan tidak valid | WorkBuddy harus menyalin citation dan seluruh text evidence persis ke quote; perbaiki satu kali atau laporkan fail. |
| UI diam setelah klik | Periksa pesan error, muat ulang. Jangan mengganti hasil dengan jawaban contoh. |

CLI adalah pilihan awal. MCP tersedia opsional: panduan di `relayfy-agent/START_HERE.md`. Konfigurasi MCP yang disiapkan belum diverifikasi pada versi aplikasi WorkBuddy milikmu.

## 5. Yang sudah dan belum

Sudah: web lokal, penyimpanan SQLite, alur handover, kontrol server, antrean, CLI/MCP, 79 tes otomatis, uji browser dua profil dan build. Respons tes model adalah fixture yang diberi label.

Belum: eksekusi pada aplikasi WorkBuddy aktual, kualitas model aktual, kasus/dataset resmi, video, deploy dan pengiriman. Naskah dan bahan tersedia di `submission/`. Isi `evidence/workbuddy-record-template.md` setelah menjalankan demo; jangan menandainya selesai lebih awal.

Data disimpan di `~/.relayfy-mvp/`; restart memakai data yang sama. Untuk demo baru tanpa menghapus sesi sebelumnya: jalankan `python3 run_demo.py --state ./sesi-demo-baru`. Folder yang berisi database atau koneksi jangan dikirim ke repo.
