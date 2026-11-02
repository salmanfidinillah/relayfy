# Product sharing — catatan faktual

Dua hal berbeda dan tidak boleh dicampur:

1. **Sesi pengembangan WorkBuddy** (agent di workspace proyek) — benar-benar terjadi pada 2026-11-02 dan di bawah ini dirinci.
2. **Sesi runtime WorkBuddy** (agent di folder `workbuddy/` menjawab pengguna lewat bridge) — **belum dijalankan**. Jangan klaim sudah.

## Kontribusi nyata sesi pengembangan WorkBuddy

| Aktivitas | Tindakan aktual | Hasil / perbaikan | Bukti |
|---|---|---|---|
| Membaca paket pembanding | Membaca README, PROJECT_BRIEF, CHECKLIST, AGENTS, WORKBUDDY_CASES, 00_index, lalu `service/core.py`, `server.py`, `bridge.py`, `demo.py`, `start.py`, `approve.py`, `import_source.py`, `test_relayfy.py` | Peta risiko: kasus W03 tidak terlayani oleh retrieval kata kunci | dokumen ini, `CHECKLIST.md` |
| Menjalankan uji yang disertakan | `python tests/run_tests.py` | 28/28 lulus di laptop ini (Python 3.13.14, Windows) — bukan lagi klaim lingkungan lama | `evidence/test-results.json` |
| Menjalankan demo lokal | `python demo.py` | 19 event: ask → analyze → import → brief → review → accept → revoke terbukti jalan | `evidence/demo-transcript.json` |
| Menguji kasus W lewat bridge | `bridge.py ask` untuk W01–W06 dengan token persona asli | 5 lulus, **1 gagal**: “Apa pekerjaan terbuka?” → `unknown` | probe sebelum perbaikan |
| Memperbaiki kegagalan | Menambah routing intent deterministik (`tasks`, `missing`, `status`) di `service/core.py`; menambah test 29–32 | 32/32 lulus; W03 kini `decision=tasks` dengan `missing={pic,deadline}` | `service/core.py`, `tests/test_relayfy.py` |
| Menutup celah operasional | Menambah `session.py` (token satu persona di luar workspace) + fallback di `bridge.py` + `workbuddy/status.py` | WorkBuddy yang diluncurkan dari GUI tidak lagi bergantung pada pewarisan environment variable | output `status.py`: `bridge: OK, 1 workspace` |
| Verifikasi lapisan bridge | Menulis `tests/bridge_cases.py` dan menjalankannya | 7/7 lulus (W01–W06 + struktur W10) | `evidence/bridge-cases.json` |
| Memperbarui dokumen | CHECKLIST, README, WORKBUDDY_CASES, AGENTS, START_HERE, 01–07 submission | Status lokal vs bridge vs WorkBuddy dipisahkan eksplisit | `submission/` |

## Yang belum terjadi (jangan diklaim)

| Aktivitas | Status | Alasan |
|---|---|---|
| Percakapan runtime WorkBuddy | Belum | Perlu kamu buka `workbuddy/` sebagai workspace dan menjalankan W01–W10 |
| Persetujuan manusia (W07–W08) | Belum | `approve.py` harus dijalankan dan SETUJU diketik oleh kamu |
| Pencabutan akses (W09) | Belum | Butuh approval ACL lalu task baru |
| Video demo | Belum | Naskah siap, rekaman belum ada |
| Kredit WorkBuddy | Tidak diukur | Sesi ini tidak menampilkan angka kredit; jangan mengarang |
| Test resmi panitia | Belum | Dataset belum tersedia |

## Pembelajaran yang bisa dipertanggungjawabkan

- **Unit test bisa menutupi kegagalan nyata.** 28 tes lulus, tetapi semuanya memakai frasa yang cocok dengan kata kunci sumber. Begitu diuji dengan kalimat wajar (“Apa pekerjaan terbuka?”), sistem menjawab tidak tahu. Harness harus memakai bahasa pengguna, bukan bahasa implementasi.
- **Perbaikan harus menambah tes, bukan hanya mengubah kode.** Empat tes regresi (29–32) mengunci intent baru, termasuk memastikan intent tugas tidak membuka sumber terbatas.
- **Pemisahan folder bukan isolasi.** `session.py` membuat demo lebih mudah, tetapi agent dengan shell pada akun OS yang sama masih bisa memanggilnya. Ini keterbatasan yang harus diucapkan di video, bukan disembunyikan.
- **Persetujuan manusia harus berada di luar jalur agent.** Bridge tidak punya endpoint approve; ini keputusan desain yang murah dan langsung terlihat di demo.
- **Kejujuran status menaikkan kredibilitas.** Menandai “belum diuji” pada percakapan WorkBuddy lebih kuat daripada klaim yang tidak bisa dibuktikan saat juri bertanya.

## Kalimat siap pakai untuk formulir

> Kami memakai WorkBuddy sebagai pasangan pengembangan: membaca seluruh paket pembanding, menjalankan ulang 28 tes yang disertakan, menemukan satu kegagalan nyata pada pertanyaan “Apa pekerjaan terbuka?”, lalu memperbaikinya dengan routing intent deterministik dan empat tes regresi. WorkBuddy juga menemukan hambatan operasional — aplikasi GUI tidak mewarisi environment variable — sehingga kami menambahkan mekanisme token satu-persona di luar workspace. Setelah perbaikan: 32/32 tes inti dan 7/7 kasus bridge lulus. Sesi runtime WorkBuddy belum kami klaim karena belum dijalankan.
