# Arsitektur dan trust boundaries

Lihat 04_architecture.svg. WorkBuddy memegang satu token pengguna melalui lingkungan proses. Bridge hanya dapat memanggil endpoint API. API memeriksa token, membership, ACL, dan versi sebelum mengembalikan kutipan. SQLite dan keys berada di direktori operator. Operator memeriksa plan dan mengonfirmasi melalui approve.py.

Agent memilih tool dan menyusun jawaban; service menghasilkan bukti deterministik dan mengendalikan mutasi. Loop LLM belum diuji. Tidak ada API publik WorkBuddy yang diasumsikan.

Trade-off: Python tanpa dependency memudahkan demo lokal tetapi retrieval masih sederhana. Revision workspace global lebih konservatif: perubahan sumber apa pun membatalkan semua brief lama. Log historis privat tetap tersimpan; pengguna hanya melihat revision aktif agar tidak membuka isi yang dicabut.

Batas keamanan yang diuji adalah HTTP API. Folder berbeda bukan isolasi filesystem. Penggunaan nyata membutuhkan akun OS/container terpisah, pengelolaan token, autentikasi approver, serta evaluasi konteks model setelah perubahan izin. UI/helper tidak boleh menyediakan token semua persona kepada agent.
