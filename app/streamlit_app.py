import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Model yolunu ayarla
MODEL_PATH = "C:/Users/dilav/Desktop/customer-churn-prediction/models/final_churn_model.pkl"

@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    return model

model = load_model()

st.title("Customer Churn Prediction App")
st.write("Bu uygulama, bir müşterinin churn (kaybedilme) riskini tahmin eder.")

st.sidebar.header("Müşteri Özelliklerini Girin")

# --- Temel demografik ve davranışsal özellikler ---
age = st.sidebar.slider("Yaş (Age)", min_value=18, max_value=90, value=35)
income = st.sidebar.number_input("Gelir (Income)", min_value=0, max_value=300000, value=50000, step=1000)
recency = st.sidebar.slider("Son Alışverişten Bu Yana Gün (Recency)", min_value=0, max_value=120, value=30)

kidhome = st.sidebar.slider("Evdeki Çocuk Sayısı (Kidhome)", min_value=0, max_value=5, value=1)
teenhome = st.sidebar.slider("Evdeki Genç Sayısı (Teenhome)", min_value=0, max_value=5, value=0)
family_size = kidhome + teenhome + 2  # Anne + baba varsayıyoruz

customer_tenure = st.sidebar.slider("Müşteri Yaşı (CustomerTenure - gün)", min_value=0, max_value=4000, value=1000)
num_web_visits = st.sidebar.slider("Aylık Web Ziyaret Sayısı (NumWebVisitsMonth)", min_value=0, max_value=20, value=5)

# Evde çocuk var mı?
is_parent = int(kidhome + teenhome > 0)

# --- Harcama (Mnt*) kolonları ---
st.sidebar.subheader("Son 2 Yıldaki Harcamalar")
mnt_wines = st.sidebar.number_input("Şarap Harcaması (MntWines)", min_value=0, max_value=20000, value=0, step=10)
mnt_fruits = st.sidebar.number_input("Meyve Harcaması (MntFruits)", min_value=0, max_value=20000, value=0, step=10)
mnt_meat = st.sidebar.number_input("Et Harcaması (MntMeatProducts)", min_value=0, max_value=20000, value=0, step=10)
mnt_fish = st.sidebar.number_input("Balık Harcaması (MntFishProducts)", min_value=0, max_value=20000, value=0, step=10)
mnt_sweet = st.sidebar.number_input("Tatlı Harcaması (MntSweetProducts)", min_value=0, max_value=20000, value=0, step=10)
mnt_gold = st.sidebar.number_input("Altın Ürün Harcaması (MntGoldProds)", min_value=0, max_value=20000, value=0, step=10)

total_spending = mnt_wines + mnt_fruits + mnt_meat + mnt_fish + mnt_sweet + mnt_gold

# --- Satın alma davranışları ---
st.sidebar.subheader("Alışveriş Sayıları")
num_deals = st.sidebar.number_input("İndirimli Alışveriş Sayısı (NumDealsPurchases)", min_value=0, max_value=100, value=0, step=1)
num_web_pur = st.sidebar.number_input("Web Alışveriş Sayısı (NumWebPurchases)", min_value=0, max_value=100, value=0, step=1)
num_catalog_pur = st.sidebar.number_input("Katalog Alışveriş Sayısı (NumCatalogPurchases)", min_value=0, max_value=100, value=0, step=1)
num_store_pur = st.sidebar.number_input("Mağaza Alışveriş Sayısı (NumStorePurchases)", min_value=0, max_value=100, value=0, step=1)

# --- Kampanya tepkileri ---
st.sidebar.subheader("Kampanya Tepkileri (0 veya 1)")
accepted_cmp1 = st.sidebar.selectbox("AcceptedCmp1", options=[0, 1], index=0)
accepted_cmp2 = st.sidebar.selectbox("AcceptedCmp2", options=[0, 1], index=0)
accepted_cmp3 = st.sidebar.selectbox("AcceptedCmp3", options=[0, 1], index=0)
accepted_cmp4 = st.sidebar.selectbox("AcceptedCmp4", options=[0, 1], index=0)
accepted_cmp5 = st.sidebar.selectbox("AcceptedCmp5", options=[0, 1], index=0)
response = st.sidebar.selectbox("Son Kampanya Yanıtı (Response)", options=[0, 1], index=0)

total_accepted_cmp = accepted_cmp1 + accepted_cmp2 + accepted_cmp3 + accepted_cmp4 + accepted_cmp5 + response
campaign_success_rate = total_accepted_cmp / 6.0

# Şikayet (Complain)
complain = st.sidebar.selectbox("Son 2 Yılda Şikayet Var mı? (Complain)", options=[0, 1], index=0)

# Medeni durum
marital_status = st.sidebar.selectbox(
    "Medeni Durum (Marital_Status)",
    options=["Married", "Single", "Together", "Divorced", "Widow"]
)

# Eğitim: şimdilik Graduation (3) varsayalım
education_value = 3  # Graduation

# --- Modelin beklediği tüm kolonlarla DataFrame oluştur ---
input_data = {
    # Ana feature'lar
    "Age": age,
    "Income": income,
    "Recency": recency,
    "FamilySize": family_size,
    "TotalSpending": total_spending,
    "CustomerTenure": customer_tenure,
    "Kidhome": kidhome,
    "Teenhome": teenhome,
    "NumWebVisitsMonth": num_web_visits,

    # Harcama kolonları
    "MntWines": mnt_wines,
    "MntFruits": mnt_fruits,
    "MntMeatProducts": mnt_meat,
    "MntFishProducts": mnt_fish,
    "MntSweetProducts": mnt_sweet,
    "MntGoldProds": mnt_gold,

    # Satın alma kolonları
    "NumDealsPurchases": num_deals,
    "NumWebPurchases": num_web_pur,
    "NumCatalogPurchases": num_catalog_pur,
    "NumStorePurchases": num_store_pur,

    # Kampanya kolonları
    "AcceptedCmp1": accepted_cmp1,
    "AcceptedCmp2": accepted_cmp2,
    "AcceptedCmp3": accepted_cmp3,
    "AcceptedCmp4": accepted_cmp4,
    "AcceptedCmp5": accepted_cmp5,
    "Response": response,
    "TotalAcceptedCmp": total_accepted_cmp,
    "CampaignSuccessRate": campaign_success_rate,

    # Diğer
    "Complain": complain,
    "IsParent": is_parent,
    "Education": education_value,
    "Marital_Status": marital_status,
}

input_df = pd.DataFrame([input_data])


st.subheader("Girilen Müşteri Özeti")
st.write(input_df)

if st.button("Churn Riskini Tahmin Et"):
    # Model pipeline zaten içinde preprocessing yapıyor
    pred_prob = model.predict_proba(input_df)[:, 1][0]
    pred_class = model.predict(input_df)[0]

    st.subheader("Tahmin Sonucu")
    st.write(f"Churn olasılığı: **%{pred_prob * 100:.2f}**")

    if pred_class == 1:
        st.error("Bu müşteri **YÜKSEK churn riski** taşıyor.")
    else:
        st.success("Bu müşteri **düşük churn riski** taşıyor.")
