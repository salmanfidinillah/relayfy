# Relayfy — Accountability Sheet

**Lingkup:** prototipe lokal, data sintetis, Challenge A.

| Area | Kebijakan dan implementasi |
|---|---|
| Identitas | Token per pengguna dari operator (env atau file sesi di luar workspace); klaim peran dalam chat tidak dipercaya API. |
| Akses | Membership workspace dan ACL sumber diperiksa sebelum pencarian; kutipan dan brief diperiksa ulang. |
| Otonom | Membaca sumber berizin, mengambil kutipan, mendeteksi konflik field, menandai PIC/deadline kosong, membuat draf, mencatat hasil tool. |
| Persetujuan | Import, perubahan ACL, review, klarifikasi tercatat, dan accept memakai plan dengan preview, revision, dan persetujuan terminal operator. |
| Larangan | Tidak mengirim email, memublikasikan data, mengarang sumber, mengganti identitas berdasarkan chat, atau melewati persetujuan. Bridge tidak memiliki endpoint approve. |
| Ketidakpastian | Bukti kosong memakai respons generik. Konflik tidak diselesaikan hanya dari tanggal terbaru. |
| Rekam | Timestamp, identitas, query/tool, sumber/versi, hasil, dan approval tersimpan SQLite. Audit pengguna dibatasi pemilik dan revision aktif. |
| Perubahan akses | Revision meningkat; plan/brief lama ditolak dan audit lama disembunyikan dari tampilan pengguna. |
| Batas aktual | Agent bershell pada akun OS sama mungkin dapat melewati batas filesystem, menjalankan `session.py`, atau `approve.py`. Isolasi kuat memerlukan akun/container terpisah. Model tidak dapat “melupakan” data yang sudah dilihat; task baru diperlukan setelah perubahan persona/izin. |
| Status uji | 33/33 tes inti, 7/7 kasus bridge, demo 21 event (approval disimulasikan). Percakapan WorkBuddy, test resmi, dan isolasi OS belum diuji. |

**Pemilik evaluasi:** Salman Fidinillah. **Sumber data:** sintetis. **Produksi:** belum siap. Bukti respons bahasa alami harus ditambahkan dari sesi WorkBuddy; audit tool tidak menggantikannya.
