# Product sharing — draf faktual

Relayfy dibangun di ChatGPT/Codex dengan mempertahankan core Python/SQLite. Versi MVP ini menyiapkan WorkBuddy sebagai runtime agent, melalui antrean job web, CLI dan MCP. **Belum ada penggunaan aplikasi atau kredit WorkBuddy aktual yang dapat diklaim pada pembuatan paket ini.**

Rencana kontribusi WorkBuddy yang dapat dibuktikan: mengambil bukti berizin melalui next, menyusun jawaban/brief dengan model dalam WorkBuddy, lalu mengirim hasil melalui finish. Backend melakukan validasi dan UI menampilkan hasilnya. Ini peran runtime yang nyata setelah dijalankan, berbeda dari klaim WorkBuddy menulis seluruh kode. Pengujian CLI/MCP dengan jawaban fixture hanya membuktikan protokol berjalan.

| Aktivitas | Status saat paket dibuat | Bukti yang harus diisi pengguna | Kredit awal / akhir |
|---|---|---|---|
| Menjalankan next untuk brief penerima | belum diuji di aplikasi WorkBuddy | ekspor percakapan/tool next; sumber berizin | belum diukur |
| Menyusun brief dan finish | belum diuji di aplikasi WorkBuddy | keluaran model, tool finish Done, draf web | belum diukur |
| Menjawab pertanyaan Maya | belum diuji di aplikasi WorkBuddy | next/finish dan kutipan hasil web | belum diukur |
| Menangani konflik/unknown/injeksi | kode/fixture diuji; model aktual menunggu | percakapan dan hasil aktual, termasuk kegagalan | belum diukur |
| Akses berubah: task dan pairing baru | backend diuji; perilaku WorkBuddy menunggu | penolakan tool lama dan proses ulang | belum diukur |

Pembelajaran yang benar-benar terjadi: otorisasi harus mendahului retrieval; sumber yang berubah juga membatalkan history, brief dan job. Draf harus privat sampai review/share. Key worker memerlukan batas tujuan agar brief penerima tidak memakai konteks pertanyaan privat pemberi. Lease mencegah hasil terlambat atau replay. Audit dan perubahan hasil perlu transaksi yang sama. UI harus menunjukkan Pending/Failed secara jujur ketika agent belum menyelesaikan pekerjaan.

Uji browser membuktikan draf tidak terlihat penerima, klarifikasi diterima pemberi, acceptance tercatat, dan revokasi mengosongkan history/brief lama. CSV dengan koma dalam judul berhasil diimpor. Workspace baru dan input teks juga diuji; label peran sidebar diperbaiki agar mengikuti giver/receiver workspace, bukan badge profil global. Pemeriksaan menemukan label Catatan generik dapat menimbulkan konflik palsu; data demo diperjelas menjadi Arti penerimaan. Ini mengingatkan bahwa parser field belum memahami otoritas atau makna sumber.

Isi tabel dari bukti aktual setelah menjalankan WorkBuddy. Template ada di `../evidence/workbuddy-record-template.md`. Laporkan prompt, tools, kegagalan, perbaikan dan kredit apa adanya. Jangan mengarang angka penghematan, screenshot atau penggunaan WorkBuddy.
