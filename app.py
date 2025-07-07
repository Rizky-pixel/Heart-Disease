import streamlit as st
import pandas as pd
import joblib

# Load model
model = joblib.load('rfheart_model.pkl')

st.title("Prediksi Penyakit Jantung")
st.markdown("Masukkan data pasien untuk memprediksi risiko penyakit jantung.")

# Input fitur
age = st.number_input("Umur", 20, 100, 50)
sex = st.selectbox("Jenis Kelamin", [0, 1], format_func=lambda x: "Perempuan" if x == 0 else "Laki-laki")
chest_pain_type = st.slider("Tipe Nyeri Dada (0-3)", 0, 3, 1)
bp = st.number_input("Tekanan Darah (BP)", 80, 200, 120)
cholesterol = st.number_input("Kolesterol", 100, 400, 200)
fbs_over_120 = st.selectbox(
    "Gula Darah Lebih dari 120 mg/dl?",
    [0, 1],
    format_func=lambda x: "Tidak (>120 mg/dl)" if x == 0 else "Ya (≤120 mg/dl)"
)
ekg_results = st.selectbox(
    "Hasil EKG",
    [0, 1, 2],
    format_func=lambda x: {
        0: "Normal (0)",
        1: "Memiliki kelainan gelombang ST-T (1)",
        2: "Menunjukkan kemungkinan atau pasti hipertrofi ventrikel kiri (2)"
    }[x]
)
max_hr = st.number_input("Detak Jantung Maksimum", 60, 250, 150)
exercise_angina = st.selectbox("Apakah mengalami angina saat olahraga?", [0, 1],
    format_func=lambda x: "Tidak" if x == 0 else "Ya")
st_depression = st.number_input("ST Depression", 0.0, 6.0, 1.0)
slope_of_st = st.selectbox("Kemiringan Segmen ST", [0, 1, 2], format_func=lambda x: {
    0: "Menurun (Downsloping)",
    1: "Datar (Flat)",
    2: "Menanjak (Upsloping)"
}[x])
number_of_vessels_fluro = st.selectbox("Jumlah Pembuluh Terlihat", [0, 1, 2, 3])
thallium = st.selectbox(
    "Hasil Tes Thallium",
    [3, 6, 7],
    format_func=lambda x: {
        3: "Normal (3)",
        6: "Fixed Defect (6)",
        7: "Reversible Defect (7)"
    }[x]
)

# Masukkan ke DataFrame
input_data = pd.DataFrame([[age, sex, chest_pain_type, bp, cholesterol,
                            fbs_over_120, ekg_results, max_hr, exercise_angina,
                            st_depression, slope_of_st, number_of_vessels_fluro, thallium]],
                          columns=['age', 'sex', 'chest_pain_type', 'bp', 'cholesterol',
                                   'fbs_over_120', 'ekg_results', 'max_hr', 'exercise_angina',
                                   'st_depression', 'slope_of_st', 'number_of_vessels_fluro', 'thallium'])

# Prediksi
if st.button("Prediksi"):
    pred = model.predict(input_data)[0]
    if pred == 1:
        st.error("❗ Pasien Berisiko Mengalami Penyakit Jantung!")
        st.markdown("""
        <div style='font-size:18px; color:#b22222;'>
        <b>Penjelasan:</b><br>
        Berdasarkan data yang dimasukkan, pasien <b>memiliki risiko tinggi</b> terkena penyakit jantung.<br><br>
        <b>Saran:</b>
        <ul>
            <li>Konsultasikan segera ke dokter spesialis jantung.</li>
            <li>Perbaiki pola makan dan gaya hidup sehat.</li>
            <li>Rutin berolahraga dan hindari stres berlebih.</li>
            <li>Kontrol tekanan darah, gula darah, dan kolesterol secara berkala.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/616/616494.png", width=80, caption="Jaga kesehatan jantung Anda!")
    else:
        st.success("✅ Pasien Tidak Berisiko Penyakit Jantung.")
        st.markdown("""
        <div style='font-size:18px; color:#228B22;'>
        <b>Penjelasan:</b><br>
        Berdasarkan data yang dimasukkan, pasien <b>tidak menunjukkan risiko signifikan</b> penyakit jantung.<br><br>
        <b>Tetap Jaga Kesehatan:</b>
        <ul>
            <li>Pertahankan pola hidup sehat dan aktif.</li>
            <li>Periksa kesehatan secara rutin.</li>
            <li>Hindari rokok dan konsumsi makanan tinggi lemak.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/1484/1484849.png", width=80, caption="Pertahankan gaya hidup sehat!")