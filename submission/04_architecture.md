# Arsitektur dan trust boundaries

Lihat 04_architecture.svg. WorkBuddy memegang satu token pengguna melalui environment proses atau file sesi satu-persona di direktori operator (`session.py` menulis `active-token`, bukan seluruh key). Bridge hanya dapat memanggil endpoint API. API memeriksa token, membership, ACL, dan versi sebelum mengembalikan kutipan. SQLite dan keys berada di direktori operator. Operator memeriksa plan dan mengonfirmasi melalui approve.py.

Agent memilih tool dan menyusun jawaban; service menghasilkan bukti deterministik dan mengendalikan mutasi. Loop LLM belum diuji. Tidak ada API publik WorkBuddy yang diasumsikan.

Verifikasi laptop ini: 32/32 tes inti, 7/7 kasus bridge (W01–W06 + struktur W10), demo 21 event. Percakapan WorkBuddy belum dijalankan sehingga kualitas jawaban model belum dinilai.

Trade-off: Python tanpa dependency memudahkan demo lokal tetapi retrieval masih sederhana (kata kunci + intent regex). Revision workspace global lebih konservatif: perubahan sumber apa pun membatalkan semua brief lama. Log historis privat tetap tersimpan; pengguna hanya melihat revision aktif agar tidak membuka isi yang dicabut.

Batas keamanan yang diuji adalah HTTP API. Folder berbeda bukan isolasi filesystem; `session.py` dan `approve.py` berada di luar workspace runtime tetapi tetap dapat dipanggil bila agent punya shell pada akun OS yang sama. Penggunaan nyata membutuhkan akun OS/container terpisah, pengelolaan token, autentikasi approver, serta evaluasi konteks model setelah perubahan izin.
