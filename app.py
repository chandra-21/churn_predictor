"""
app.py — Web app Streamlit untuk prediksi Customer Churn.

Hanya butuh dua artefak dari Colab: churn_model.joblib & metadata.json.
Semua grafik digambar dari metadata (tanpa file gambar terpisah).

Jalankan lokal:  streamlit run app.py
Deploy gratis :  share.streamlit.io (lihat PANDUAN_DEPLOY.md)
"""
from __future__ import annotations
import json
from pathlib import Path

import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Customer Churn Predictor",
                   page_icon="📉", layout="wide")

ROOT = Path(__file__).resolve().parent


def _find(name: str) -> Path:
    """Cari artefak di root repo atau folder models/."""
    for p in (ROOT / name, ROOT / "models" / name):
        if p.exists():
            return p
    raise FileNotFoundError(f"{name} tidak ditemukan. Latih model dulu via notebook Colab.")


@st.cache_resource
def load_artifacts():
    model = joblib.load(_find("churn_model.joblib"))
    meta = json.loads(_find("metadata.json").read_text())
    return model, meta


model, meta = load_artifacts()
schema = meta["schema"]

LABELS = {
    "gender": "Jenis Kelamin", "SeniorCitizen": "Lansia (Senior)",
    "Partner": "Punya Pasangan", "Dependents": "Punya Tanggungan",
    "tenure": "Lama Berlangganan (bulan)", "PhoneService": "Layanan Telepon",
    "MultipleLines": "Banyak Saluran", "InternetService": "Layanan Internet",
    "OnlineSecurity": "Keamanan Online", "OnlineBackup": "Backup Online",
    "DeviceProtection": "Proteksi Perangkat", "TechSupport": "Dukungan Teknis",
    "StreamingTV": "Streaming TV", "StreamingMovies": "Streaming Film",
    "Contract": "Jenis Kontrak", "PaperlessBilling": "Tagihan Tanpa Kertas",
    "PaymentMethod": "Metode Pembayaran", "MonthlyCharges": "Tagihan Bulanan ($)",
    "TotalCharges": "Total Tagihan ($)",
}
lab = lambda c: LABELS.get(c, c)

st.title("📉 Customer Churn Predictor")
st.caption("Demonstrasi Data Mining — memprediksi kemungkinan pelanggan "
           "berhenti berlangganan beserta faktor pendorongnya.")

tab_predict, tab_perf, tab_data = st.tabs(
    ["🔮 Prediksi", "📊 Performa Model", "📁 Data & Proyek"])

# ====================== TAB 1 — PREDIKSI ======================
with tab_predict:
    st.subheader("Masukkan profil pelanggan")
    inputs: dict = {}
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("**👤 Profil**")
        for c in ["gender", "SeniorCitizen", "Partner", "Dependents"]:
            inputs[c] = st.selectbox(lab(c), schema["categorical"][c], key=c)
        t = schema["numeric"]["tenure"]
        inputs["tenure"] = st.slider(lab("tenure"), int(t["min"]), int(t["max"]),
                                     int(t["median"]))
    with c2:
        st.markdown("**🌐 Layanan**")
        for c in ["PhoneService", "MultipleLines", "InternetService",
                  "OnlineSecurity", "OnlineBackup", "DeviceProtection",
                  "TechSupport", "StreamingTV", "StreamingMovies"]:
            inputs[c] = st.selectbox(lab(c), schema["categorical"][c], key=c)
    with c3:
        st.markdown("**📄 Kontrak & Tagihan**")
        for c in ["Contract", "PaperlessBilling", "PaymentMethod"]:
            inputs[c] = st.selectbox(lab(c), schema["categorical"][c], key=c)
        for c in ["MonthlyCharges", "TotalCharges"]:
            n = schema["numeric"][c]
            inputs[c] = st.slider(lab(c), float(n["min"]), float(n["max"]),
                                  float(n["median"]))

    st.divider()
    left, right = st.columns([1, 2])
    with left:
        threshold = st.slider("Ambang batas (threshold) churn", 0.10, 0.90, 0.50, 0.05,
                              help="Probabilitas di atas ambang ditandai berisiko churn.")
        go_btn = st.button("🔮 Prediksi", type="primary", use_container_width=True)

    if go_btn:
        X = pd.DataFrame([inputs])[schema["feature_order"]]
        proba = float(model.predict_proba(X)[0, 1])
        is_churn = proba >= threshold
        with right:
            g = go.Figure(go.Indicator(
                mode="gauge+number", value=proba * 100,
                number={"suffix": "%", "font": {"size": 40}},
                title={"text": "Probabilitas Churn"},
                gauge={"axis": {"range": [0, 100]},
                       "bar": {"color": "#dc2626" if is_churn else "#16a34a"},
                       "steps": [{"range": [0, 30], "color": "#dcfce7"},
                                 {"range": [30, 60], "color": "#fef9c3"},
                                 {"range": [60, 100], "color": "#fee2e2"}],
                       "threshold": {"line": {"color": "black", "width": 3},
                                     "value": threshold * 100}}))
            g.update_layout(height=280, margin=dict(t=50, b=10))
            st.plotly_chart(g, use_container_width=True)
        if is_churn:
            st.error(f"⚠️ **BERISIKO CHURN** — probabilitas {proba:.1%} "
                     f"(≥ ambang {threshold:.0%}). Pertimbangkan tindakan retensi.")
        else:
            st.success(f"✅ **CENDERUNG BERTAHAN** — probabilitas churn {proba:.1%} "
                       f"(< ambang {threshold:.0%}).")
        tips = []
        if inputs["Contract"] == "Month-to-month":
            tips.append("Tawarkan insentif pindah ke kontrak 1–2 tahun (driver churn #1).")
        if inputs["tenure"] <= 12:
            tips.append("Pelanggan baru rawan pergi — perkuat onboarding & dukungan awal.")
        if inputs["OnlineSecurity"] == "No" and inputs["InternetService"] != "No":
            tips.append("Tawarkan layanan Keamanan Online / Dukungan Teknis.")
        if tips:
            st.markdown("**💡 Saran retensi:**")
            for t in tips:
                st.markdown(f"- {t}")

# ====================== TAB 2 — PERFORMA ======================
with tab_perf:
    st.subheader(f"Model terpilih: {meta['best_model']}")
    lb = pd.DataFrame(meta["leaderboard"]).set_index("model")
    best = lb.loc[meta["best_model"]]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Accuracy", f"{best['accuracy']:.1%}")
    m2.metric("Recall (Churn)", f"{best['recall']:.1%}",
              help="Persentase pelanggan churn yang berhasil ditangkap.")
    m3.metric("Precision (Churn)", f"{best['precision']:.1%}")
    m4.metric("ROC-AUC", f"{best['roc_auc']:.3f}")

    st.markdown("**Perbandingan model**")
    st.dataframe(lb.style.format("{:.4f}").highlight_max(axis=0, color="#dcfce7"),
                 use_container_width=True)

    gc1, gc2 = st.columns(2)
    with gc1:
        st.markdown("**Confusion Matrix**")
        cm = meta["confusion_matrix"]
        z = [[cm[1][1], cm[1][0]], [cm[0][1], cm[0][0]]]  # tata ulang utk heatmap
        fig = go.Figure(go.Heatmap(
            z=z, x=["Prediksi Churn", "Prediksi Bertahan"],
            y=["Aktual Churn", "Aktual Bertahan"], colorscale="Blues",
            text=z, texttemplate="%{text}", showscale=False))
        fig.update_layout(height=320, margin=dict(t=20, b=10))
        st.plotly_chart(fig, use_container_width=True)
    with gc2:
        st.markdown("**Kurva ROC**")
        roc = meta["roc"]
        fig = go.Figure()
        fig.add_scatter(x=roc["fpr"], y=roc["tpr"], mode="lines",
                        name=f"ROC (AUC={roc['auc']:.3f})", line=dict(color="#2563eb", width=3))
        fig.add_scatter(x=[0, 1], y=[0, 1], mode="lines",
                        line=dict(dash="dash", color="gray"), showlegend=False)
        fig.update_layout(height=320, margin=dict(t=20, b=10),
                          xaxis_title="False Positive Rate", yaxis_title="True Positive Rate",
                          legend=dict(x=0.4, y=0.1))
        st.plotly_chart(fig, use_container_width=True)

# ====================== TAB 3 — DATA & PROYEK ======================
with tab_data:
    st.subheader("Tentang dataset")
    d1, d2, d3 = st.columns(3)
    d1.metric("Jumlah pelanggan", f"{meta['n_rows']:,}")
    d2.metric("Tingkat churn", f"{meta['churn_rate']:.1%}")
    d3.metric("Jumlah fitur", len(schema["feature_order"]))
    st.markdown(
        "Dataset **Telco Customer Churn** (IBM): profil demografi, layanan, "
        "jenis kontrak, dan tagihan pelanggan perusahaan telekomunikasi. "
        "Target: apakah pelanggan berhenti berlangganan (*churn*).")

    st.divider()
    st.subheader("Faktor pendorong churn (pola tersembunyi)")
    imp = pd.DataFrame(meta["top_features"]).sort_values("importance")
    fig = go.Figure(go.Bar(x=imp["importance"], y=imp["feature"],
                           orientation="h", marker_color="#2563eb"))
    fig.update_layout(height=380, margin=dict(t=10, b=10),
                      xaxis_title="Penurunan ROC-AUC saat fitur diacak")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(
        "Diukur via *permutation importance*. **Jenis kontrak** dan **lama "
        "berlangganan** adalah penentu terkuat — pelanggan kontrak bulanan "
        "dengan masa langganan pendek paling rawan pergi.")

st.caption("Tugas Data Mining · Streamlit + scikit-learn")
