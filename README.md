# 📉 Customer Churn Predictor — Demonstrasi Data Mining

Model machine learning yang memprediksi kemungkinan pelanggan telekomunikasi berhenti berlangganan (*churn*), lengkap dengan web app interaktif **Streamlit**. Proyek ini memperlihatkan alur **data mining** end-to-end: data mentah → pembersihan → pemodelan → penemuan pola tersembunyi → aplikasi siap pakai.

---

## 📌 Executive Summary

**Masalah.** Mempertahankan pelanggan jauh lebih murah daripada mengakuisisi yang baru. Pada dataset ini, **26,5%** pelanggan churn. Pertanyaan bisnis: *pelanggan mana yang akan pergi, dan apa pemicunya?*

**Pendekatan.** Satu model klasifikasi (**Gradient Boosting**) dilatih pada **7.043** record pelanggan dengan 19 atribut. Model dipilih dari dua kandidat berdasarkan skor **F1**, karena tujuannya menangkap sebanyak mungkin pelanggan berisiko tanpa terlalu banyak alarm palsu.

**Hasil.** Model menangkap **78% pelanggan yang benar-benar churn** (recall) dengan **ROC-AUC 0,84**.

**Temuan kunci (pola tersembunyi).**
1. **Jenis kontrak** — pelanggan kontrak *bulanan* jauh lebih mungkin pergi.
2. **Lama berlangganan (tenure)** — pelanggan baru paling rawan.

**Rekomendasi.** Arahkan retensi ke pelanggan **kontrak bulanan dengan tenure rendah**: tawarkan insentif kontrak jangka panjang dan perkuat onboarding.

---

## 🎯 Dataset

- **Sumber:** Telco Customer Churn (IBM), dataset publik & bersih.
- **Ukuran:** 7.043 baris × 21 kolom.
- **Target:** `Churn` (Yes/No) → biner (1 = churn).
- **Distribusi:** 73,5% bertahan, 26,5% churn (*tidak seimbang*).

---

## 🔬 Metodologi (alur Data Mining)

| Tahap | Yang dilakukan |
|------|----------------|
| **Load** | Baca data mentah dari URL publik. |
| **Clean** | `TotalCharges` (teks, 11 kosong) → numerik + imputasi; `customerID` dibuang. |
| **Split** | Train/test 80/20 *stratified* (sebelum preprocessing → anti-leakage). |
| **Pipeline** | `ColumnTransformer`: impute+scale (numerik), impute+one-hot (kategorikal). |
| **Train** | Logistic Regression (baseline) vs Gradient Boosting, `class_weight="balanced"`. |
| **Evaluate** | Accuracy, Precision, Recall, F1, ROC-AUC, confusion matrix. |
| **Explain** | *Permutation importance* → faktor pendorong churn. |
| **Persist** | Simpan `churn_model.joblib` + `metadata.json`. |

Seluruh tahap ada di notebook **`Churn_Training_Colab.ipynb`** (dirancang untuk Google Colab).

---

## 📊 Hasil (test set)

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|-------|:--------:|:---------:|:------:|:--:|:-------:|
| **Gradient Boosting** ✅ | 0,756 | 0,527 | **0,781** | **0,629** | 0,838 |
| Logistic Regression (baseline) | 0,737 | 0,503 | 0,783 | 0,613 | 0,841 |

**Confusion Matrix** — dari 374 pelanggan yang benar-benar churn, model menangkap **292 (78%)**:

|  | Prediksi: Bertahan | Prediksi: Churn |
|--|:--:|:--:|
| **Aktual: Bertahan** | 773 | 262 |
| **Aktual: Churn** | 82 | **292** |

**Faktor pendorong churn:** Contract → tenure → InternetService → TotalCharges → OnlineSecurity.

> Grafik interaktif (confusion matrix, ROC, feature importance) dapat dilihat langsung di web app, tab **Performa Model** & **Data & Proyek**.

---

## 🖥️ Web App (Streamlit)

Tiga tab: **🔮 Prediksi** (form profil → gauge probabilitas + threshold + saran retensi), **📊 Performa Model**, **📁 Data & Proyek**.

---

## 📁 Struktur Repo (untuk deploy)

```
churn-predictor/
├── Churn_Training_Colab.ipynb   # notebook training (dijalankan di Colab)
├── app.py                       # web app Streamlit
├── churn_model.joblib           # model terlatih (hasil unduhan Colab)
├── metadata.json                # skema + metrik + data grafik
├── requirements.txt             # dependensi untuk Streamlit Cloud
├── PANDUAN_DEPLOY.md            # langkah deploy GitHub → Streamlit Cloud
└── README.md
```

---

## 🚀 Cara Menjalankan

**Training (Google Colab):** upload `Churn_Training_Colab.ipynb` ke Colab, jalankan semua sel, unduh `churn_model.joblib` + `metadata.json`.

**Web app (lokal):**
```bash
pip install -r requirements.txt
streamlit run app.py
```

**Deploy publik:** ikuti `PANDUAN_DEPLOY.md` (gratis via Streamlit Community Cloud).

---

## ⚠️ Batasan & Pengembangan Lanjut

- **Precision moderat (53%)** pada kelas churn — naikkan threshold untuk kampanye berbiaya tinggi.
- **Threshold default 0,5** belum dikalibrasi ke nilai bisnis.
- **Data statis** — perlu validasi pada data terbaru & pemantauan *model drift*.
- **Pengembangan:** tuning hyperparameter, kalibrasi probabilitas, SHAP untuk penjelasan per-pelanggan.

---

*Tugas Data Mining · scikit-learn · Streamlit · Python*
