# Customer Churn Prediction

Bu proje, bir perakende şirketinin müşterilerinin **churn (terk etme)** riskini tahmin etmek için uçtan uca bir makine öğrenmesi çözümü sunar.  
Proje; veri analizi, feature engineering, modelleme, optimizasyon, pipeline oluşturma ve Streamlit arayüzü geliştirmeyi içerir.

---

## 📁 Proje Yapısı
customer-churn-prediction/
├── app/
│ └── streamlit_app.py
├── data/
│ ├── raw/
│ └── processed/
├── models/
│ └── final_churn_model.pkl
├── notebooks/
│ ├── 01_eda.ipynb
│ ├── 02_feature_engineering.ipynb
│ ├── 03_baseline_model.ipynb
│ ├── 04_model_optimization.ipynb
│ └── 05_final_pipeline.ipynb
├── environment.yml
└── README.md


---

## 📊 Veri Seti

**Customer Personality Analysis Dataset** (Kaggle)

Veri setinde müşterilere ait bilgiler:
- Demografi (Age, Income, Education, Marital_Status)
- Satın alma geçmişi (MntWines, MntMeatProducts, ...)
- Kampanya cevapları (AcceptedCmp1–5, Response)
- Ziyaret/alışveriş davranışları
- CustomerTenure (şirkete kaydolduğu süre)
- Recency (son alışverişten geçen gün)

---

## 🛠️ Feature Engineering

Projede aşağıdaki yeni özellikler üretilmiştir:

| Feature | Açıklama |
|--------|----------|
| Age | Yıl → yaş dönüşümü |
| CustomerTenure | Kayıt süresi (gün) |
| FamilySize | Kidhome + Teenhome + Parents |
| IsParent | Evde çocuk/ergen var mı? |
| TotalSpending | Tüm harcamaların toplamı |
| TotalAcceptedCmp | Tüm kampanya kabullerinin toplamı |
| CampaignSuccessRate | Başarı oranı |
| Ordinal Education | 1–5 arası eğitim seviyesi |

Ayrıca:
- Eksik veriler tamamlandı  
- Gereksiz kolonlar silindi  
- Education → Ordinal  
- Marital_Status → One-Hot  

---

## 🤖 Modelleme

### Kullanılan Modeller:
- Logistic Regression (baseline)
- Random Forest (baseline)
- **Random Forest (GridSearchCV ile optimize edilmiş)** – *final model*

### Metrikler:
- Accuracy  
- Precision  
- Recall  
- F1  
- **ROC-AUC**  

### 📈 Final Model Performansı  
(*Kendi sonuçlarına göre doldurabilirsin*)

| Metrik | Değer |
|--------|--------|
| Accuracy | … |
| F1 Score | … |
| ROC-AUC | … |

Final model: **RandomForestClassifier + Pipeline**

---

## 🧩 Pipeline

05_final_pipeline.ipynb içerisinde oluşturulan pipeline:

### 1. Preprocessing
- Numeric kolonlar → StandardScaler  
- Marital_Status → OneHotEncoder  
- Education → ordinal numeric  

### 2. Model
- GridSearchCV ile optimize edilmiş RF

### 3. Export
Pipeline `.pkl` olarak kaydedildi:
models/final_churn_model.pkl


---

## 🌐 Streamlit Web Uygulaması

`app/streamlit_app.py` içinde geliştirilmiştir.

Kullanıcı şu bilgileri girerek churn riskini tahmin eder:

- Age, Income  
- Harcama detayları (MntWines, MntFruits, vb.)  
- Kampanya cevapları (AcceptedCmp1–5, Response)  
- Recency  
- CustomerTenure  
- NumWebVisitsMonth  
- Marital_Status  

### Çalıştırmak için:
```bash
cd app
streamlit run streamlit_app.py


### Kurulum

1-) Ortam kurulumu
conda env create -f environment.yml
conda activate churn-env

2-) Notebook çalıştırma
jupyter notebook

3-) Streamlit çalıştırma
streamlit run app/streamlit_app.py

📎 Sonuç

Bu proje ile:

Müşteri churn analizi yapılmış,

Zengin feature engineering uygulanmış,

Optimize bir model eğitilmiş,

Pipeline üretim ortamına uygun hale getirilmiş,

Streamlit arayüzü ile son kullanıcıya sunulabilir bir uygulama oluşturulmuştur.




Geliştirici

Dilaver Oruç
Data Analytics / Machine Learning Engineer