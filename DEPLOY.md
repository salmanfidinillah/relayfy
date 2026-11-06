# Menyiapkan deployment Relayfy (opsional setelah demo)

Untuk target terbaru demo lokal melalui WorkBuddy, gunakan `MULAI_DI_SINI.md` dan `run_demo.py`. Jalur ini tidak memerlukan deployment atau key API website. Bagian di bawah mempertahankan panduan **web dengan backend API**. Worker WorkBuddy dibatasi loopback; host publik tidak otomatis dapat memakai client pada laptop tanpa rancangan worker/transport terisolasi tambahan. Jangan membuka endpoint worker ke internet.

Produksi harus memakai `RELAYFY_DEMO=false` dan `RELAYFY_AI_BACKEND=api`. Peluncur `run_demo.py` khusus lokal, bukan server produksi.

Belum ada deployment atau layanan yang dibeli. Target: satu container Python + satu volume SQLite permanen. UI buildless disajikan dari origin yang sama. Tidak cocok untuk serverless berfilesystem sementara atau beberapa replica yang memakai SQLite terpisah.

## Lokal (Windows / macOS / Linux)

Python 3.10+ (disarankan 3.12). Tidak perlu npm atau pip untuk server development.

```powershell
Copy-Item .env.example .env
python web_start.py
```

macOS/Linux: `cp .env.example .env`, lalu `python3 web_start.py`.
Buka **http://127.0.0.1:8765/**; jangan campur `localhost` dengan `127.0.0.1` karena origin harus sama. Default data: `~/.relayfy-web/relayfy.sqlite`, terpisah dari database persona legacy. Skema dibuat otomatis tanpa menghapus data lama. Jangan menjalankan server legacy terhadap database web.

Daftar dua akun dari UI. Masuk sebagai pemberi → Dashboard → Handover baru → email penerima → Sumber → Tambah sumber → tinjau preview → konfirmasi. Susun ringkasan bukti (tanpa AI) atau brief AI jika model sudah dikonfigurasi. Pemberi meninjau & membagikan. Keluar, masuk sebagai penerima → periksa kutipan → terima atau minta klarifikasi.

`examples/web_demo.md` memuat bahan sintetis dan urutan demo. Tidak ada akun/password produksi bawaan.

## Mengaktifkan AI secara lokal

Edit `.env` pada editor lokal. Jangan menempelkan secret ke chat, browser, Git, atau screenshot.

- `OPENAI_API_KEY`: key proyek dari penyedia API OpenAI atau penyedia kompatibel yang dipercaya.
- `OPENAI_MODEL`: ID model yang tersedia pada akun, mendukung Chat Completions dan JSON mode. Tidak diasumsikan setiap model kompatibel.
- `OPENAI_BASE_URL`: default `https://api.openai.com/v1`. Adapter menambahkan `/chat/completions`.
- `MODEL_TIMEOUT_SECONDS`: default 35.

Restart server setelah perubahan. Badge menunjukkan konfigurasi tersedia, **bukan** bukti koneksi provider berhasil. Verifikasi dengan pertanyaan bersumber dan brief AI; buka kutipannya. API key salah, model tak tersedia, timeout, JSON buruk, atau kutipan tidak valid menghasilkan error eksplisit. Tidak ada fallback AI palsu. Kuota ChatGPT Plus dan kredit aplikasi WorkBuddy tidak dipakai sebagai API website.

Data yang dikirim ke provider: pertanyaan, bukti yang diizinkan untuk tujuan tersebut, dan maksimal empat turn akun/workspace/revisi yang sama. Brief memakai audiens penerima dan juga harus boleh dibaca pemberi. Pencabutan izin berlaku pada request berikutnya, dan hasil model yang masih berjalan dibuang jika revisi berubah. Data yang sebelumnya terkirim ke provider tidak dapat ditarik kembali.

## Build & validasi produksi

Dari root proyek, dengan Node.js dan Python tersedia:

```sh
python3 tests/run_tests.py
python3 scripts/build.py
python3 -m pip install -r requirements.txt
python3 -m gunicorn --config gunicorn.conf.py service.wsgi:application
```

Build menyalin aset ke `dist/`, memeriksa sintaks Python/JavaScript dan menghasilkan SHA256 manifest. Tidak ada bundler atau server Node pada runtime. Gunicorn digunakan di Linux/container; Windows development memakai `web_start.py`.

## Docker (belum menjalankan deployment)

```sh
docker build -t relayfy:local .
docker volume create relayfy-data
docker run --rm -p 8000:8000 --mount source=relayfy-data,target=/data --env-file .env.production relayfy:local
```

Contoh `.env.production` privat:

```dotenv
RELAYFY_ENV=production
RELAYFY_DEMO=false
RELAYFY_AI_BACKEND=api
PUBLIC_ORIGIN=https://relayfy.example.com
RELAYFY_DB_PATH=/data/relayfy.sqlite
PERSISTENT_STORAGE_CONFIRMED=true
ALLOW_REGISTRATION=true
OPENAI_API_KEY=ISI_DI_SECRET_MANAGER_HOSTING
OPENAI_MODEL=MODEL_YANG_TERSEDIA
OPENAI_BASE_URL=https://api.openai.com/v1
```

Container harus berada di belakang HTTPS reverse proxy. Untuk uji Docker lokal lewat HTTP, gunakan `RELAYFY_ENV=development` dan `PUBLIC_ORIGIN=http://127.0.0.1:8000`; jangan memakai konfigurasi itu pada internet. Pastikan volume dapat ditulis UID 10001. Jika host memasang volume sebagai root, atur kepemilikan mount melalui fasilitas host sebelum menjalankan app.

## Pilihan hosting: Render Docker Web Service + persistent disk

Ini pilihan yang mempertahankan stack. Dokumentasi resmi: https://render.com/docs/disks dan https://render.com/docs/docker (diperiksa 2 November 2026). Persistent disk tersedia pada layanan berbayar; jangan mengaktifkan pembelian sebelum persetujuan pemilik. VPS + volume Docker juga memungkinkan.

Setelah pengguna memutuskan publikasi:

1. Gunakan source yang sudah ditinjau; Dockerfile di root folder `relayfy`.
2. Buat satu Docker Web Service; konfigurasi satu instance.
3. Pasang disk permanen ke `/data`, pastikan izin tulis UID 10001.
4. Atur env seperti di atas melalui secret manager, khususnya domain HTTPS yang sebenarnya. Jangan menyimpan `.env.production` ke repo.
5. Health path `/healthz`; Gunicorn membaca `PORT` dari host.
6. Daftarkan dua akun, uji izin dan sesi; selanjutnya pertimbangkan `ALLOW_REGISTRATION=false`. Pada MVP belum ada undangan admin, reset password, atau verifikasi email.
7. Uji restart dan redeploy menggunakan **disk yang sama**. Pastikan akun, sumber dan handover tidak hilang.
8. Buat backup privat di luar host, uji restore pada lingkungan terpisah, jalankan smoke test provider nyata. Baru evaluasi penggunaan data nyata.

`PERSISTENT_STORAGE_CONFIRMED=true` adalah pernyataan operator, bukan detektor volume. Server menolak startup produksi jika env/path belum disiapkan, tetapi operator tetap harus memverifikasi mount. Disk tidak tersedia saat image build; skema dibuat saat runtime. Jangan memakai SQLite pada share NFS atau autoscaling multi-instance.

## Backup dan pemulihan

```sh
python3 scripts/backup.py /data/relayfy.sqlite /data/backups/relayfy-YYYYMMDD.sqlite
```

Salin hasil ke penyimpanan privat luar host. Backup memuat data dan sesi sensitif; batasi akses. Restore: hentikan server, buat backup database saat ini, salin file backup ke path database, hapus file WAL/SHM yang terkait dengan database lama **setelah server berhenti**, pastikan kepemilikan benar, lalu start dan verifikasi. Jangan menggabungkan file WAL lama dengan database hasil restore. Session lama dapat dihapus melalui SQLite oleh operator sebelum restart jika diperlukan.

## Batasan sebelum penggunaan perusahaan

- MVP single instance, SQLite + scrypt, tanpa SSO/MFA, reset password, atau verifikasi email. Orang dapat memakai alamat email orang lain saat pendaftaran; verifikasi identitas di luar aplikasi diperlukan sebelum memakai data sensitif.
- Retrieval kata/alias; task harus CSV/JSON atau TASK terstruktur. Konflik otomatis hanya field `Nama: nilai`; gap terstruktur PIC/deadline. Tidak ada embeddings atau OCR.
- Model output divalidasi JSON, ID kutipan dan kutipan persis. Kebenaran semantik setiap klaim tetap perlu review manusia; deteksi injeksi regex terbatas. Model tidak memiliki tool mutasi.
- Log UI hanya aktivitas sendiri pada revisi aktif. Audit lama tersimpan privat, bukan log immutable/tamper-proof. Operator database dapat membaca data.
- Belum ada kebijakan retensi/penghapusan mandiri, quota penyimpanan per organisasi, atau pengujian beban/penetrasi independen.
- Rate limit auth konservatif per remote IP. Di belakang proxy semua pengunjung dapat berbagi IP; jangan percaya `X-Forwarded-For` sembarangan untuk menghilangkan batas ini.
- Browser dapat menampilkan kutipan yang telah dibuka hingga polling sekitar 3 detik/refresh; setiap request server memeriksa akses segera. Informasi yang sudah dilihat tidak bisa dihapus dari ingatan manusia.
- Dataset resmi, kualitas provider nyata, WorkBuddy aktual dan deployment nyata masih memerlukan verifikasi terpisah.
