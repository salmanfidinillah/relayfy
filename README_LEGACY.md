# Relayfy — comparison prototype

AI Handover Assistant untuk Challenge A. Paket ini dibuat di ChatGPT/Codex sebagai pembanding, lalu dijalankan dan diperbaiki di laptop pengguna (Windows, Python 3.13.14). Percakapan WorkBuddy yang sebenarnya belum dijalankan. Catatan ini mendokumentasikan prototipe CLI. Untuk demo web saat ini, lihat [README.md](README.md).

## Status verifikasi di laptop ini (2026-11-02)

| Lapisan | Hasil | Bukti |
|---|---|---|
| Uji otomatis inti (deterministik) | **33/33 lulus** | [laporan saat itu](https://github.com/salmanfidinillah/relayfy/blob/1da097e/evidence/test-results.json) |
| Demo lokal end-to-end (HTTP + bridge, approval disimulasikan) | **21 event** | `evidence/demo-transcript.json` |
| Kasus bridge W01–W06 + struktur W10 | **7/7 lulus** | `evidence/bridge-cases.json` |
| Percakapan WorkBuddy (W01–W10) | **belum dijalankan** | `tests/WORKBUDDY_CASES.md` |
| Dataset/test resmi panitia | belum tersedia | — |

Perbaikan yang dilakukan saat menjalankan ulang: pertanyaan seperti “Apa pekerjaan terbuka?” dulu dijawab `unknown` karena pencarian hanya berbasis kata kunci. Sekarang ada routing intent deterministik (`tasks`, `missing`, `status`) sehingga tugas dan kekurangan PIC/deadline bisa dijawab tanpa menebak. Regresi ditambahkan sebagai test 29–32.

## Yang dapat dijalankan sekarang

Layanan Python lokal + SQLite, client tool untuk WorkBuddy, dataset sintetis, draf brief ekstraktif, pencarian kutipan, tugas, pemeriksaan PIC/deadline, konflik field, persetujuan operator, versi, audit, dan pengujian otomatis. Semua tanpa paket pip tambahan atau API key model.

**AI bahasa alami berasal dari WorkBuddy ketika pengguna menjalankannya.** Mode lokal adalah pemrosesan bukti deterministik, bukan LLM. Pengujian lokal tidak membuktikan kualitas jawaban model.

## Windows: mulai dalam 4 langkah

Gunakan Python 3.10 atau lebih baru dan jalankan perintah dari folder repositori.

1. **Terminal operator #1** — jalankan layanan dan biarkan terbuka:

```powershell
python start.py
```

Layanan hanya mendengarkan `127.0.0.1:8765`. Data demo dan token dibuat satu kali di `$HOME\.relayfy-local`, di luar folder kerja agent. Restart memakai data yang sama. Untuk demo bersih: `python start.py --state D:\RelayfyDemoBaru` (pakai `--state` yang sama saat approve).

2. **Terminal operator #2** — pilih persona runtime (satu persona per task):

```powershell
python session.py --persona budi
python workbuddy/status.py
```

`session.py` hanya menulis **satu** token ke `$HOME\.relayfy-local\active-token`, bukan seluruh key. Ini membuat WorkBuddy yang diluncurkan dari GUI tetap bisa memanggil bridge tanpa mengatur environment variable.

3. **WorkBuddy** — buka **hanya folder `workbuddy/`** sebagai workspace, tempel prompt dari `workbuddy/START_HERE.md`, dan gunakan Default Permissions (bukan Full Access). Alternatif tanpa GUI: dari terminal yang sudah menjalankan `session.py`, panggil `python workbuddy/bridge.py ask --file workbuddy/requests/01_ask_delay.json`.

4. Jalankan kasus pada `tests/WORKBUDDY_CASES.md`. Bukti dan screenshot tahap ini masih perlu Anda kumpulkan.

**Batas isolasi penting:** folder terpisah bukan sandbox. Pada OS user yang sama, agent yang punya akses shell luas mungkin dapat membaca state, menjalankan `session.py`, atau `approve.py`. Proteksi yang diuji adalah API; untuk isolasi kuat, jalankan service/operator pada akun OS/container terpisah. Gunakan hanya data sintetis sampai isolasi dan runtime WorkBuddy diuji. Pencabutan izin tidak dapat menarik kembali informasi yang sudah tampil atau berada dalam konteks LLM; wajib task baru setelah pergantian persona/izin.

## Catatan lingkungan (ditemukan saat verifikasi di laptop ini)

- **Proxy**: laptop ini menyalakan `HTTP_PROXY`/`HTTPS_PROXY`. `bridge.py` sekarang memakai `ProxyHandler({})` agar trafik loopback tidak pernah lewat proxy; tanpa itu, request ke `127.0.0.1` bisa gagal dengan pesan `upstream connect failed`.
- **Path state harus sama persis** di `start.py`, `session.py`, dan `approve.py`. Di Git Bash, gunakan path Windows (`C:/Users/.../relayfy-fresh`), bukan `/tmp/...`, karena variabel environment tidak ikut dikonversi.
- **Stabilitas HTTP**: server kini membaca body request sebelum menolak. Sebelumnya, menolak dengan body yang belum dibaca membuat Windows me-reset koneksi sehingga tes sesekali gagal `RemoteDisconnected`. Sesudah perbaikan, 33/33 lulus pada 10 kali eksekusi berturut-turut; regresi dikunci di `test_33`.
- **Uji state baru** (port 8799, state kosong) sudah dilakukan: seeding, `session.py`, `status.py`, `ask`, `plan`, dan penolakan `approve.py` saat input bukan `SETUJU` semuanya berjalan; sumber tidak berubah setelah penolakan.

## Demo satu perintah tanpa WorkBuddy

```powershell
python demo.py
```

Menjalankan server sementara, client bridge HTTP, import task CSV, analisis, review/accept, dan pencabutan akses pada database sementara. Menulis `evidence/demo-transcript.json` (21 event). Persetujuan disimulasikan oleh test harness (bukan bukti persetujuan manusia). Tidak mengubah database demo permanen.

## Import manual

Pemberi Andi memiliki izin import di workspace demo.

```powershell
python import_source.py examples/tasks.csv --kind tasks --title "Tugas tambahan" --users andi,budi --output draft-import.json
python workbuddy/bridge.py plan --file draft-import.json
```

Baca preview. Di terminal operator (bukan chat agent), setujui ID plan yang ditampilkan:

```powershell
python approve.py ID_PLAN
```

Program menampilkan detail lalu meminta mengetik `SETUJU`. Plan lama/duplikat ditolak. TXT/MD/chat diterima sebagai teks; CSV/JSON tasks menggunakan kolom title,status,pic,deadline,blocker,dependency. Teks bebas dapat dicari/dikutip, tetapi ekstraksi task otomatis lokal memerlukan format task tersebut.

## Review dan accept

Dengan persona Andi, panggil `brief` memakai `workbuddy/requests/09_brief.json`. Catat ID brief. Buat plan review dengan `11_plan_review.json` (ganti ID), lalu approve melalui terminal operator. Pada sesi baru dengan persona Budi, baca `get_brief` (`10_get_brief.json`), lalu buat plan `accept` (`12_plan_accept.json`) atau `clarify` (`13_plan_clarify.json`).

Manusia tetap dapat menerima dengan masalah terbuka setelah meninjau; status Accepted berarti serah terima versi tersebut diterima, bukan semua tugas selesai.

## API/tool contract

Semua request POST JSON ke `/api/OP`, header Authorization Bearer token. Body default workspace `demo`.

| OP | Input tambahan | Hasil |
|---|---|---|
| workspaces | — | Workspace milik pengguna |
| create | name, receiver | Workspace baru; pengguna penerima harus sudah terdaftar |
| sources | — | Metadata sumber yang diizinkan |
| cite | citation | Potongan sumber atau respons kosong seragam |
| ask | question | `decision` = `evidence` / `tasks` / `missing` / `unknown`, plus kutipan, konflik, warnings |
| analyze | — | Bukti, tasks, missing, conflicts |
| brief | audience opsional | Draf bersumber untuk audiens |
| get_brief | id | Brief jika izin dan revision masih berlaku |
| plan | action, payload | Preview menunggu operator |
| audit | — | Aktivitas sendiri pada revision terkini |

Aksi plan: import, acl, review, accept, clarify. ACL payload `{"source":"chat","users":["andi"]}` mencabut akses pengguna lain. Layanan menyimpan audit historis privat, tetapi menyembunyikan entri pengguna yang lebih lama setelah revision berubah. Identitas baru di luar tiga akun demo memerlukan administrasi layanan; belum ada UI pendaftaran.

### Routing intent `ask` (deterministik)

| Pola pertanyaan | `decision` | Isi |
|---|---|---|
| tugas, pekerjaan, PIC, deadline, hambatan, blocker | `tasks` | `tasks` + `missing` (PIC/deadline kosong) |
| klarifikasi, belum lengkap, kelengkapan | `missing` | `missing` + tugas terkait |
| status, posisi, terakhir, ringkasan | `evidence` | baris fakta bersumber + konflik |
| lainnya | `evidence` / `unknown` | kutipan skor kata kunci |

Ini bukan pencarian semantik: pertanyaan yang tidak memuat kata kunci maupun pola intent tetap dijawab `unknown` dengan sengaja.

## Testing

```powershell
python -m unittest discover -s tests -p test_relayfy.py
python tests/bridge_cases.py  # 7 kasus bridge ke layanan yang sedang berjalan
```

Lihat `submission/03_test_results.md`. Pengujian resmi, model WorkBuddy, rekaman video, dan pengukuran manfaat belum dilakukan.

## Keterbatasan dan keputusan scope

- Tidak ada UI web/deployment: opsional sesuai prioritas pengguna dan handbook.
- Search token/alias + intent regex; tidak ada embedding atau pemahaman semantik.
- Konflik hanya dikenali pada baris `Field: nilai`; resolusi otoritas diserahkan kepada manusia.
- Missing checker lokal hanya PIC/deadline tugas terbuka; penalaran kelengkapan luas perlu model.
- Regex injeksi hanya mengarantina pola yang dikenal; bukan detektor universal.
- Audit mencatat hasil tool; respons bahasa alami WorkBuddy perlu ekspor percakapan sebagai bukti terpisah.
- `session.py` dan `approve.py` adalah alat operator; keduanya berada di luar workspace runtime, tetapi bukan sandbox.
- Operator bertindak sebagai pemberi persetujuan pada demo. Produksi memerlukan autentikasi manusia dan otorisasi approval yang lebih kuat.
- SQLite lokal single-user demo; bukan sistem multi-tenant produksi.
- Dataset resmi belum diperoleh. Semua bahan demo fiktif.

Baca [checklist](CHECKLIST.md) dan [indeks bahan penilaian](submission/00_index.md).
