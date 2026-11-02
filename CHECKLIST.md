# Checklist implementasi dan submission

Diperbarui: 2026-11-02 (laptop pengguna, Windows, Python 3.13.14). Status hanya diisi dari eksekusi nyata.

Legenda: **Selesai** (terbukti di laptop ini) · **Sebagian** (ada bukti, cakupan terbatas) · **Terhambat** (butuh pihak lain) · **Belum** (belum dikerjakan).

| Item | Status | Bukti / keterbatasan |
|---|---|---|
| Brief/handbook/playbook diperiksa | Selesai | PROJECT_BRIEF.md, submission/08_sources.md |
| Struktur proyek & Python diperiksa | Selesai | Python 3.13.14, hanya stdlib; 31→37 file |
| Uji otomatis inti | Selesai | 32/32 lulus — `evidence/test-results.json` |
| Demo lokal end-to-end | Selesai | 21 event — `evidence/demo-transcript.json` (approval disimulasikan harness) |
| Koneksi bridge nyata (HTTP client) | Selesai | 7/7 kasus W — `evidence/bridge-cases.json` |
| Workspace dan sumber manual | Selesai | `service/core.py`, `import_source.py` |
| Hak akses sebelum retrieval | Selesai pada API | Test 01–06, W04; filesystem WorkBuddy belum terisolasi |
| Brief dan tasks | Selesai ekstraktif | Format TASK terstruktur; generasi bahasa alami belum diuji |
| Tanya jawab bersumber | Sebagian | Retrieval kata + intent tugas/status; kualitas model WorkBuddy belum diuji |
| Kelengkapan | Sebagian | PIC/deadline tugas terbuka; pemeriksaan lebih luas perlu model |
| Konflik | Selesai field terstruktur | Eskalasi manusia; tidak otomatis mengesahkan sumber |
| Review/accept/clarify/versi | Selesai | `plan` + `approve.py`; approval manusia |
| Audit | Selesai hasil tool | Ekspor percakapan WorkBuddy masih diperlukan |
| Perbaikan temuan W03 | Selesai | "Apa pekerjaan terbuka?" dulu `unknown` → kini `decision=tasks` + `missing`; regresi test_29–32 |
| Sesi runtime tanpa env var | Selesai | `session.py` + fallback `active-token`; diuji lewat `workbuddy/status.py` |
| Trafik loopback tanpa proxy | Selesai | `bridge.py` memakai `ProxyHandler({})`; laptop ini menyalakan `HTTP_PROXY` |
| Guard `approve.py` | Selesai | Input selain `SETUJU` ditolak; jumlah sumber tidak berubah |
| Uji state baru (port 8799) | Selesai | Seeding → session → ask → plan → penolakan approve berjalan |
| Percakapan aktual WorkBuddy | Belum | Perlu kamu buka `workbuddy/` sebagai workspace (W01–W06) |
| Persetujuan manusia W07–W08 | Belum | Perlu `approve.py` + ketik SETUJU sendiri |
| Pencabutan akses W09 | Belum | Perlu approval ACL lalu task baru |
| Isolasi filesystem agent | Belum | Butuh akun OS/container terpisah sebelum data nyata |
| Dataset/test resmi | Terhambat | Belum diberikan panitia; semua data sintetis |
| UI/deploy | Belum | Sengaja ditunda; prioritas pada workflow WorkBuddy |
| Deskripsi/akuntabilitas/arsitektur | Selesai draf | `submission/` |
| Video demo | Belum | Naskah siap, belum direkam |
| Product sharing | Sebagian | Draf jujur; kontribusi WorkBuddy aktual belum ada |
| Repo publik | Belum | Kamu minta tidak push |
| Form submission | Belum | Draf berdasarkan handbook; form terbaru belum diperiksa |
| Kredit WorkBuddy | Belum diukur | Tidak ada akun WorkBuddy dipakai di sesi ini |

Status paket: **siap didemokan secara lokal dan lewat bridge**; percakapan WorkBuddy serta seluruh bukti submission (screenshot, video, repo) masih menunggu tindakan manusia.
