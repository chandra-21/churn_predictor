# 🚀 Panduan Deploy ke Streamlit Community Cloud (Gratis)

Setelah model dilatih di Colab dan kamu punya `churn_model.joblib` + `metadata.json`, ikuti langkah berikut untuk menjadikan web app dapat diakses publik lewat URL.

---

## Prasyarat
- Akun **GitHub** (gratis).
- Akun **Streamlit Community Cloud** → daftar di https://share.streamlit.io (login pakai GitHub).
- 5 file ini di satu folder: `app.py`, `requirements.txt`, `churn_model.joblib`, `metadata.json`, `README.md`.

---

## Langkah 1 — Buat repository GitHub
1. Buka https://github.com/new
2. Beri nama, misalnya `churn-predictor`, set **Public**, klik **Create repository**.

## Langkah 2 — Unggah file
Cara termudah lewat browser (tanpa git):
1. Di halaman repo, klik **Add file → Upload files**.
2. Seret kelima file (`app.py`, `requirements.txt`, `churn_model.joblib`, `metadata.json`, `README.md`).
3. Klik **Commit changes**.

> Alternatif via terminal:
> ```bash
> git clone https://github.com/USERNAME/churn-predictor.git
> cd churn-predictor
> # salin kelima file ke sini
> git add . && git commit -m "Add churn app" && git push
> ```

## Langkah 3 — Deploy di Streamlit Cloud
1. Buka https://share.streamlit.io → **Create app** → **Deploy from GitHub**.
2. Isi:
   - **Repository:** `USERNAME/churn-predictor`
   - **Branch:** `main`
   - **Main file path:** `app.py`
3. Klik **Deploy**. Streamlit akan membaca `requirements.txt` dan memasang dependensi (1–3 menit).
4. Selesai — kamu dapat URL publik seperti `https://churn-predictor-username.streamlit.app` yang bisa diserahkan ke dosen.

## Langkah 4 — Update di kemudian hari
Cukup commit perubahan ke GitHub; Streamlit Cloud **otomatis redeploy**.

---

## ⚠️ Troubleshooting

| Masalah | Solusi |
|---|---|
| `FileNotFoundError: churn_model.joblib` | Pastikan file model benar-benar terunggah ke repo (cek ukurannya ~600 KB, bukan 0). |
| `ModuleNotFoundError` | Tambahkan paket yang hilang ke `requirements.txt`, commit ulang. |
| Versi scikit-learn berbeda saat unpickle | Samakan versi: di `requirements.txt` pin versi yang sama dengan Colab, mis. `scikit-learn==1.5.2`. Cek versi Colab dengan `import sklearn; sklearn.__version__`. |
| App "sleeping" | App gratis tidur jika tak dipakai; buka URL-nya, akan bangun ~30 detik. |

---

## 🔄 Alternatif cepat: jalankan dari Colab (tanpa GitHub)
Untuk demo sesaat (mati saat session berakhir), di sel Colab:
```python
!pip install -q streamlit
!npm install -g localtunnel
# tulis app.py & artefak ke disk Colab lebih dulu, lalu:
!streamlit run app.py &>/content/log.txt &
!npx localtunnel --port 8501
```
Cocok untuk uji coba; untuk deliverable, **Streamlit Cloud lebih dianjurkan**.
