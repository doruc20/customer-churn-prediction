import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# -------------------------------------------------
# Model yolu (proje kökünden models/final_churn_model.pkl)
# -------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "final_churn_model.pkl")


@st.cache_resource
def load_model():
    model = joblib.load(MODEL_PATH)
    return model


model = load_model()

# -------------------------------------------------
# Streamlit Arayüzü
# -------------------------------------------------
st.title("Customer Churn Prediction App")

st.markdown(
    """
Bu uygulama, bir perakende şirketinin müşterilerinin **churn (terk etme)** riskini tahmin eder.

> **Churn Tanımı:**  
> Veri setinde gerçek churn etiketi bulunmadığı için, churn Recency üzerinden davranışsal bir eşik ile tanımlanmıştır:
> - **Churn = 1** → Recency > 40 (uzun süredir alışveriş yapmayan müşteri)
> - **Churn = 0** → Recency ≤ 40  
>
> Model Recency'den türetilen bu churn etiketi ile eğitilmiş, ancak **Recency girdi feature'ı olarak kullanılmamaktadır** (data leakage engellenmiştir).
"""
)

st.sidebar.header("Müşteri Özelliklerini Girin")

# -------------------------------------------------
# Demografik Özellikler
# -------------------------------------------------
age = st.sidebar.slider("Yaş (Age)", min_value=18, max_value=90, value=35)
income = st.sidebar.number_input(
    "Yıllık Gelir (Income)", min_value=0, max_value=300000, value=50000, step=1000
)

education_label = st.sidebar.selectbox(
    "Eğitim Seviyesi (Education)",
    options=["Basic", "2n Cycle", "Graduation", "Master", "PhD"],
    index=2,
)
education_map = {
    "Basic": 1,
    "2n Cycle": 2,
    "Graduation": 3,
    "Master": 4,
    "PhD": 5,
}
education_value = education_map[education_label]

marital_status = st.sidebar.selectbox(
    "Medeni Durum (Marital_Status)",
    options=["Married", "Single", "Together", "Divorced", "Widow"],
    index=0,
)

# -------------------------------------------------
# Aile Yapısı
# -------------------------------------------------
kidhome = st.sidebar.slider(
    "Evdeki Çocuk Sayısı (Kidhome)", min_value=0, max_value=5, value=0
)
teenhome = st.sidebar.slider(
    "Evdeki Genç Sayısı (Teenhome)", min_value=0, max_value=5, value=0
)
parents_count = st.sidebar.slider(
    "Evde Yetişkin Sayısı (Ebeveyn vb.)", min_value=1, max_value=4, value=2
)

family_size = parents_count + kidhome + teenhome
is_parent = int(kidhome + teenhome > 0)

# -------------------------------------------------
# Müşteri Zaman Bilgisi
# -------------------------------------------------
customer_tenure = st.sidebar.slider(
    "Müşterinin Şirkette Kalma Süresi (CustomerTenure - gün)",
    min_value=0,
    max_value=4000,
    value=1000,
)

# -------------------------------------------------
# Harcama Bilgileri (Mnt* kolonları)
# -------------------------------------------------
st.sidebar.subheader("Son 2 Yıldaki Harcamalar (Mnt*)")

mnt_wines = st.sidebar.number_input(
    "Şarap Harcaması (MntWines)", min_value=0, max_value=20000, value=500, step=10
)
mnt_fruits = st.sidebar.number_input(
    "Meyve Harcaması (MntFruits)", min_value=0, max_value=20000, value=50, step=10
)
mnt_meat = st.sidebar.number_input(
    "Et Harcaması (MntMeatProducts)", min_value=0, max_value=20000, value=300, step=10
)
mnt_fish = st.sidebar.number_input(
    "Balık Harcaması (MntFishProducts)", min_value=0, max_value=20000, value=100, step=10
)
mnt_sweet = st.sidebar.number_input(
    "Tatlı Harcaması (MntSweetProducts)", min_value=0, max_value=20000, value=50, step=10
)
mnt_gold = st.sidebar.number_input(
    "Altın Ürün Harcaması (MntGoldProds)", min_value=0, max_value=20000, value=100, step=10
)

total_spending = (
    mnt_wines
    + mnt_fruits
    + mnt_meat
    + mnt_fish
    + mnt_sweet
    + mnt_gold
)

# -------------------------------------------------
# Alışveriş ve Ziyaret Sayıları
# -------------------------------------------------
st.sidebar.subheader("Alışveriş ve Ziyaret Davranışları")

num_deals = st.sidebar.number_input(
    "İndirimli Alışveriş Sayısı (NumDealsPurchases)",
    min_value=0,
    max_value=100,
    value=0,
    step=1,
)
num_web_pur = st.sidebar.number_input(
    "Web Alışveriş Sayısı (NumWebPurchases)",
    min_value=0,
    max_value=100,
    value=3,
    step=1,
)
num_catalog_pur = st.sidebar.number_input(
    "Katalog Alışveriş Sayısı (NumCatalogPurchases)",
    min_value=0,
    max_value=100,
    value=2,
    step=1,
)
num_store_pur = st.sidebar.number_input(
    "Mağaza Alışveriş Sayısı (NumStorePurchases)",
    min_value=0,
    max_value=100,
    value=5,
    step=1,
)
num_web_visits = st.sidebar.slider(
    "Aylık Web Ziyaret Sayısı (NumWebVisitsMonth)",
    min_value=0,
    max_value=30,
    value=5,
)

purchase_activity = (
    num_web_visits + num_web_pur + num_catalog_pur + num_store_pur
)

# -------------------------------------------------
# Kampanya Tepkileri (AcceptedCmp* + Response)
# -------------------------------------------------
st.sidebar.subheader("Kampanya Tepkileri")

accepted_cmp1 = st.sidebar.selectbox("AcceptedCmp1", options=[0, 1], index=0)
accepted_cmp2 = st.sidebar.selectbox("AcceptedCmp2", options=[0, 1], index=0)
accepted_cmp3 = st.sidebar.selectbox("AcceptedCmp3", options=[0, 1], index=0)
accepted_cmp4 = st.sidebar.selectbox("AcceptedCmp4", options=[0, 1], index=0)
accepted_cmp5 = st.sidebar.selectbox("AcceptedCmp5", options=[0, 1], index=0)
response = st.sidebar.selectbox("Son Kampanya Yanıtı (Response)", options=[0, 1], index=0)

total_accepted_cmp = (
    accepted_cmp1
    + accepted_cmp2
    + accepted_cmp3
    + accepted_cmp4
    + accepted_cmp5
    + response
)
campaign_success_rate = total_accepted_cmp / 6.0

complain = st.sidebar.selectbox(
    "Son 2 Yılda Şikayet Var mı? (Complain)", options=[0, 1], index=0
)

# -------------------------------------------------
# FE: Türetilmiş Özellikler
# -------------------------------------------------
clv = total_spending / (customer_tenure + 1)
spending_to_income = total_spending / (income + 1)

high_value_threshold = 2000  # örnek eşik
high_value = int(total_spending >= high_value_threshold)

# -------------------------------------------------
# Modelin beklediği kolonlara uygun DataFrame
# (Eğitimde kullanılan X kolonları ile uyumlu olmalı)
# -------------------------------------------------
input_data = {
    # Ham numeric & davranışsal feature'lar
    "Age": age,
    "Income": income,
    "CustomerTenure": customer_tenure,
    "FamilySize": family_size,
    "Kidhome": kidhome,
    "Teenhome": teenhome,
    "MntWines": mnt_wines,
    "MntFruits": mnt_fruits,
    "MntMeatProducts": mnt_meat,
    "MntFishProducts": mnt_fish,
    "MntSweetProducts": mnt_sweet,
    "MntGoldProds": mnt_gold,
    "NumDealsPurchases": num_deals,
    "NumWebPurchases": num_web_pur,
    "NumCatalogPurchases": num_catalog_pur,
    "NumStorePurchases": num_store_pur,
    "NumWebVisitsMonth": num_web_visits,
    "AcceptedCmp1": accepted_cmp1,
    "AcceptedCmp2": accepted_cmp2,
    "AcceptedCmp3": accepted_cmp3,
    "AcceptedCmp4": accepted_cmp4,
    "AcceptedCmp5": accepted_cmp5,
    "Response": response,
    "Complain": complain,
    "TotalSpending": total_spending,
    "TotalAcceptedCmp": total_accepted_cmp,
    "CampaignSuccessRate": campaign_success_rate,

    # FE feature'lar
    "CLV": clv,
    "SpendingToIncome": spending_to_income,
    "HighValue": high_value,
    "PurchaseActivity": purchase_activity,
    "IsParent": is_parent,

    # Diğer
    "Education": education_value,
    "Marital_Status": marital_status,
}

input_df = pd.DataFrame([input_data])

st.subheader("Girilen Müşteri Özeti")
st.write(input_df)

# -------------------------------------------------
# Tahmin
# -------------------------------------------------
if st.button("Churn Riskini Tahmin Et"):
    prob = model.predict_proba(input_df)[0, 1]
    pred = model.predict(input_df)[0]  # 0.5 threshold

    st.subheader("Tahmin Sonucu")
    st.write(f"Churn olasılığı: **%{prob * 100:.2f}**")

    if pred == 1:
        st.error(
            "Bu müşteri **YÜKSEK churn riski** taşıyor "
            "(modelin sınıflandırmasına göre Churn = 1)."
        )
    else:
        st.success(
            "Bu müşteri **düşük churn riski** taşıyor "
            "(modelin sınıflandırmasına göre Churn = 0)."
        )

    st.markdown(
        """
**Yorum:**  
Bu tahmin, müşterinin harcama düzeyi, gelir, aile yapısı, kampanya tepkisi,
alışveriş ve ziyaret davranışları gibi bilgilerden üretilen feature'lar
üzerinden eğitilmiş RF pipeline modeline dayanmaktadır.
"""
    )
