# Relayfy — comparison prototype

AI Handover Assistant untuk Challenge A. Paket ini dibuat di ChatGPT/Codex sebagai pembanding, belum pernah dijalankan di WorkBuddy. Tidak ada push, deployment, atau submission.

## Yang dapat dijalankan sekarang

Layanan Python lokal + SQLite, client tool untuk WorkBuddy, dataset sintetis, draf brief ekstraktif, pencarian kutipan, tugas, pemeriksaan PIC/deadline, konflik field, persetujuan operator, versi, audit, dan pengujian otomatis. Semua tanpa paket pip tambahan atau API key model.

**AI bahasa alami berasal dari WorkBuddy ketika pengguna menjalankannya.** Mode lokal adalah pemrosesan bukti deterministik, bukan LLM. Pengujian lokal tidak membuktikan kualitas jawaban model.

## Windows: mulai dalam 5 langkah

Gunakan Python 3.10 atau lebih baru. Contoh mengasumsikan ZIP diekstrak sehingga foldernya `D:\Relayfy\relayfy`; sesuaikan dengan lokasi Anda.

1. Buka PowerShell operator di folder proyek. Jalankan:

```powershell
python start.py
```

Biarkan terminal ini terbuka. Layanan hanya mendengarkan `127.0.0.1:8765`. Data demo dan token dibuat satu kali di `$HOME\.relayfy-local`, di luar folder kerja agent. Restart memakai data yang sama. Untuk demo bersih gunakan `python start.py --state D:\RelayfyDemoBaru` dan berikan `--state` yang sama saat approve.

2. Buka PowerShell kedua (operator). Atur token **satu persona** untuk proses yang akan menjalankan WorkBuddy:

```powershell
$relayfyKeys = Get-Content "$HOME\.relayfy-local\operator-keys.json" | ConvertFrom-Json
$env:RELAYFY_TOKEN = $relayfyKeys.budi
python workbuddy/bridge.py workspaces
python workbuddy/bridge.py ask --file examples/query.json
```

Output harus berupa workspace dan kutipan dari layanan. Jangan membagikan token, screenshot keys, atau file database.

3. Jalankan aplikasi WorkBuddy dari terminal kedua agar mewarisi variabel lingkungan. Tutup instance WorkBuddy lama dulu; jalankan executable WorkBuddy yang benar pada laptop Anda. Buka **hanya folder `workbuddy/`** sebagai workspace. Path executable tergantung instalasi dan tidak diasumsikan di paket ini. Jika WorkBuddy tidak mewarisi variabel, tool akan memberi error eksplisit; konfigurasikan env untuk proses tool sesuai fasilitas aplikasi. Jangan menaruh seluruh keys di workspace.

4. Tempel prompt pada `workbuddy/START_HERE.md`. Pastikan terlihat pemanggilan `bridge.py`, bukan hanya respons berdasarkan ingatan. Gunakan Default Permissions, bukan Full Access.

5. Jalankan kasus pada `tests/WORKBUDDY_CASES.md`. Bukti dan screenshot tahap ini masih perlu Anda kumpulkan.

**Batas isolasi penting:** folder terpisah bukan sandbox. Pada OS user yang sama, agent yang punya akses shell luas mungkin dapat membaca state atau menjalankan approve.py. Proteksi yang diuji adalah API; untuk isolasi kuat, jalankan service/operator pada akun OS/container terpisah dengan filesystem tidak bisa dibaca agent. Gunakan hanya data sintetis sampai isolasi dan runtime WorkBuddy diuji. Pencabutan izin tidak dapat menarik kembali informasi yang sudah tampil atau berada dalam konteks LLM; wajib task baru setelah pergantian persona/izin.

## Demo satu perintah tanpa WorkBuddy

```powershell
python demo.py
```

Menjalankan server sementara, client bridge HTTP, import task CSV, analisis, review/accept, dan pencabutan akses pada database sementara. Menulis `evidence/demo-transcript.json`. Persetujuan disimulasikan oleh test harness (bukan bukti persetujuan manusia). Tidak mengubah database demo permanen.

## Import manual

Pemberi Andi memiliki izin import di workspace demo. Operator memasang token Andi pada proses client untuk sesi pemberi baru.

```powershell
python import_source.py examples/tasks.csv --kind tasks --title "Tugas tambahan" --users andi,budi --output draft-import.json
python workbuddy/bridge.py plan --file draft-import.json
```

Baca preview. Di terminal operator (bukan chat agent), setujui ID plan yang ditampilkan:

```powershell
python approve.py ID_PLAN
```

Program menampilkan detail lalu meminta mengetik `SETUJU`. Plan lama/duplikat ditolak. TXT/MD/chat diterima sebagai teks; CSV/JSON tasks menggunakan kolom title,status,pic,deadline,blocker,dependency. Teks bebas dapat dicari/dikutip, tetapi ekstraksi task otomatis lokal memerlukan format task tersebut. Model WorkBuddy dapat membantu menyiapkan draf ekstraksi untuk diperiksa manusia.

## Review dan accept

Dengan token Andi, panggil `brief` menggunakan `{"workspace":"demo","audience":"budi"}`. Catat ID brief. Buat `plan` review dengan payload berikut, lalu approve melalui terminal operator:

```json
{"workspace":"demo","action":"review","payload":{"brief":"ID_BRIEF"}}
```

Pada sesi baru dengan token Budi, baca `get_brief`, lalu buat plan `accept` atau `clarify`:

```json
{"workspace":"demo","action":"accept","payload":{"brief":"ID_BRIEF"}}
```

```json
{"workspace":"demo","action":"clarify","payload":{"brief":"ID_BRIEF","question":"Siapa PIC integrasi pembayaran?"}}
```

Manusia tetap dapat menerima dengan masalah terbuka setelah meninjau; status Accepted berarti serah terima versi tersebut diterima, bukan semua tugas selesai.

## API/tool contract

Semua request POST JSON ke `/api/OP`, header Authorization Bearer token. Body default workspace `demo`.

| OP | Input tambahan | Hasil |
|---|---|---|
| workspaces | — | Workspace milik pengguna |
| create | name, receiver | Workspace baru; pengguna penerima harus sudah terdaftar |
| sources | — | Metadata sumber yang diizinkan |
| cite | citation | Potongan sumber atau respons kosong seragam |
| ask | question | Kutipan relevan, konflik, revision |
| analyze | — | Bukti, tasks, missing, conflicts |
| brief | audience opsional | Draf bersumber untuk audiens |
| get_brief | id | Brief jika izin dan revision masih berlaku |
| plan | action, payload | Preview menunggu operator |
| audit | — | Aktivitas sendiri pada revision terkini |

Aksi plan: import, acl, review, accept, clarify. ACL payload `{"source":"chat","users":["andi"]}` mencabut akses pengguna lain. Layanan menyimpan audit historis privat, tetapi menyembunyikan entri pengguna yang lebih lama setelah revision berubah. Identitas baru di luar tiga akun demo memerlukan administrasi layanan; belum ada UI pendaftaran.

## Testing

```powershell
python tests/run_tests.py
```

Lihat `submission/03_test_results.md`. Pengujian resmi, model WorkBuddy, Windows aktual, rekaman video, dan pengukuran manfaat belum dilakukan di lingkungan pembuat paket. Linux/Python dan bridge HTTP sudah diuji di sini.

## Keterbatasan dan keputusan scope

- Tidak ada UI web/deployment: opsional sesuai prioritas pengguna dan handbook.
- Search token/alias sederhana; tidak ada embedding, pemahaman semantik lokal, atau model inferensi lokal.
- Konflik hanya dikenali pada baris `Field: nilai`; resolusi otoritas diserahkan kepada manusia.
- Missing checker lokal hanya PIC/deadline tugas terbuka; blocker/dependency tampil, penalaran kelengkapan luas perlu model dan evaluasi.
- Regex injeksi hanya mengarantina pola yang dikenal; bukan detektor universal. Tool tetap tidak memiliki aksi kirim email/publish.
- Audit mencatat hasil tool; respons bahasa alami WorkBuddy perlu ekspor percakapan sebagai bukti terpisah.
- Operator bertindak sebagai pemberi persetujuan pada demo. Produksi memerlukan autentikasi manusia dan otorisasi approval yang lebih kuat.
- SQLite lokal single-user demo; bukan sistem multi-tenant produksi.
- Dataset resmi belum diperoleh. Semua bahan demo fiktif.

Baca `CHECKLIST.md`, kemudian `submission/00_index.md`. Tidak ada tautan publik atau bukti submit yang dibuat.
