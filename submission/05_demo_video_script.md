# Urutan rekaman demo — 7 menit 20 detik

**BELUM DIREKAM.** Gunakan aplikasi WorkBuddy aktual untuk bagian AI dan rekam pemanggilan tools. Jangan memakai fixture sebagai hasil AI nyata. Bahasa narasi Indonesia disarankan agar lancar; periksa ketentuan bahasa panitia sebelum final.

## Sebelum merekam

Jalankan `MULAI_DI_SINI.md`. Server dan WorkBuddy pada laptop yang sama; siapkan Python. Buat state demo baru tanpa menghapus sesi lama (`--state ./sesi-rekaman`). Tutup notifikasi pribadi. Pastikan file koneksi dan token tidak tampil. Catat kredit WorkBuddy sebelum/sesudah. Uji satu job nyata terlebih dahulu; simpan hasilnya di template evidence. Jangan merekam seolah berhasil bila agent belum menyelesaikan job.

| Waktu | Tampilan dan ucapan | Hasil yang seharusnya terlihat |
|---|---|---|
| 00:00–00:35 | Landing: “Orangnya berganti, konteks pekerjaannya jangan hilang.” Kenalkan Relayfy dan data sintetis. | Identitas Relayfy, bukan klaim dukungan resmi penyelenggara. |
| 00:35–01:10 | Pilih Andi. Dashboard → sumber → pekerjaan → kelengkapan. | 6 sumber Andi, 3 tugas terbuka, PIC/deadline pembayaran kosong, konflik 7/9 November pada state awal. |
| 01:10–01:45 | Diagram singkat: sesi/ACL → antrean → tools WorkBuddy → validasi → review manusia. | Batas akses di server; model tidak menyetujui bisnis. |
| 01:45–02:55 | Andi → susun brief dengan agent. Pair tujuan brief tanpa menampilkan file. WorkBuddy task baru menjalankan prompt satu job. Tunjukkan next, bukti dan finish. | Job Done aktual; draf bersumber di web. Buka satu kutipan. Jangan menyebut selesai jika masih Pending/Failed. |
| 02:55–03:35 | Tinjau & bagikan. Berhenti pada preview, jelaskan persetujuan, lalu operator konfirmasi. | Tidak dibagikan sebelum konfirmasi. |
| 03:35–04:40 | Maya, task/pairing baru tujuan pertanyaan. Chat: “Mengapa peluncuran tertunda?” Jalankan satu job di WorkBuddy. | Jawaban aktual mengutip foto produk; kutipan dapat dibuka. “Kapan jadwal peluncuran?” menampilkan konflik jika sempat diuji. |
| 04:40–05:15 | Maya: “Anggaran Kenari?” dan “Anggaran Unicorn?” | Respons belum diketahui yang sama, tanpa menyinggung keberadaan sumber privat. Jelaskan klaim peran di chat tidak memberi izin. |
| 05:15–06:15 | Maya minta klarifikasi PIC → preview/konfirmasi. Andi melihat pertanyaan, meninjau ulang. Maya menerima versi. | Klarifikasi tercatat, status diterima; tugas terbuka tetap ada. |
| 06:15–06:50 | Andi cabut akses chat untuk Maya. Maya buka chat/workspace kembali. | Revisi baru; history dan brief lama tidak dipakai. Tool lama ditolak; task/pairing baru diperlukan. |
| 06:50–07:20 | Activity Log, hasil tes, kontribusi aktual WorkBuddy dan batas. | 79 tes lokal, fixture transport dibedakan dari job WorkBuddy yang baru direkam; manfaat belum diukur. |

Jika waktu terlalu panjang, tunjukkan klarifikasi atau satu konflik yang sudah disiapkan, jangan mempercepat hingga kutipan/gerbang persetujuan tidak terlihat. Total akhir harus 5–8 menit sesuai acuan tersedia. Periksa audio, teks kutipan, izin tautan video dan durasi sebelum publikasi yang diotorisasi.

Bahan: dataset otomatis Karsa, `examples/import-tasks.csv`, `relayfy-agent/START_HERE.md`, `evidence/workbuddy-record-template.md`. Skenario penolakan/unknown dan preview persetujuan tersedia. Video dan tautan tetap belum selesai sampai benar-benar direkam/diunggah; tidak ada upload yang dilakukan oleh pembuat paket.
