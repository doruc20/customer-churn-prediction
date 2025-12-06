# 🛒 Customer Churn Prediction  
Müşterilerin alışveriş davranışlarına dayalı olarak **churn (terk etme)** olasılığını tahmin eden bir makine öğrenimi projesidir.  
Proje, veri analizi → feature engineering → modelleme → pipeline → Streamlit arayüzü adımlarını kapsar.

---

## 📌 1. Proje Amacı
Bu çalışma, bir perakende şirketindeki müşterilerin **churn riskini** tahmin etmeyi amaçlar.  
Orijinal veri setinde gerçek churn etiketi bulunmadığı için, davranışsal olarak türetilmiş bir churn tanımı oluşturulmuştur.

Bu model sayesinde işletme:
- Riskli müşterileri erken tespit edebilir,
- Kampanya stratejilerini daha doğru hedefleyebilir,
- Müşteri kaybını azaltabilir.

---

## 📌 2. Veri Seti
Kullanılan veri seti:  
**Marketing Campaign Dataset** (UCI / Kaggle)  
Müşterilere ait demografik bilgiler, harcama tutarları, ziyaret davranışları ve kampanya etkileşimlerini içerir.

### Önemli Değişken Grupları:
- **Demografik:** Age, Income, Education, Marital_Status, Kidhome, Teenhome  
- **Harcama Değerleri:** MntWines, MntMeatProducts, MntGoldProds vb.  
- **Davranışsal:** NumWebVisitsMonth, NumStorePurchases vb.  
- **Kampanya Tepkileri:** AcceptedCmp1–5, Response  
- **Zaman Bilgisi:** Dt_Customer

---

## 📌 3. Churn Tanımımız (Çok Önemli)
Veri setinde gerçek churn etiketi olmadığından, churn davranış temelli olarak tanımlanmıştır.

### ✔ **Churn = 1 → Recency > 40**  
### ✔ **Churn = 0 → Recency ≤ 40**

Bu, sektörde yaygın kullanılan “inactivity-based churn” yaklaşımıdır.

**NOT:**  
Modeli eğitirken Recency kullanılmamıştır → *data leakage engellenmiştir.*

---

## 📌 4. Veri Temizleme İşlemleri
EDA sırasında tespit edilen problemler düzeltilmiştir:

- Eksik tarih formatları düzeltilip datetime’a çevrildi  
- Age, Income, harcama değişkenleri uç değer (outlier) kontrolleri yapıldı  
- Categorical değişkenlerde yanlış sınıf birleştirmeleri düzeltildi  
- Gereksiz değişkenler çıkarıldı  
  - `Z_CostContact`, `Z_Revenue`, `ID`  
- Recency modeli leak etmemesi için veri setinden çıkarıldı

---

## 📌 5. Feature Engineering
Model performansını artırmak için yeni anlamlı değişkenler türetildi:

### 🔧 Türetilmiş Değişkenler
| Feature | Açıklama |
|--------|----------|
| **TotalSpending** | Tüm harcama kolonlarının toplamı |
| **TotalAcceptedCmp** | Kampanya kabul sayısı |
| **CustomerTenure** | Müşterinin şirkette kaç gündür bulunduğu |
| **CLV** | Yaşam boyu değer = TotalSpending / Tenure |
| **SpendingToIncome** | Harcama / gelir oranı |
| **HighValue** | Değerli müşteri bayrağı (Toplam harcamaya göre) |
| **PurchaseActivity** | Web + mağaza + katalog toplam etkileşim |
| **IsParent** | Evde çocuk/teen olup olmadığı |

### 🔧 Encoding
- **Education** → *Ordinal Encoding* (Basic → PhD)  
- **Marital_Status** → *One-Hot Encoding*  
- Tüm numeric değişkenler → *StandardScaler*  

---

## 📌 6. Modelleme Yaklaşımı
Model bir **Sklearn Pipeline** içinde eğitildi:

1. Preprocessing  
2. Feature engineering  
3. Encoding & Scaling  
4. RandomForestClassifier  

### Neden Random Forest?
- Karmaşık veri yapılarında başarı oranı yüksek  
- Outlier ve non-linear ilişkilerde dayanıklı  
- Aşırı öğrenmeye karşı güçlü

---

## 📌 7. Threshold Optimization
Varsayılan olarak modeller **0.50** kesim değeri ile sınıflandırır.  
Fakat churn türü problemlerde bu kesim genellikle churn sınıfını bastırır.

Bu nedenle ROC eğrisi üzerinden **en uygun threshold** test edilmiştir.  
Yaptığımız churn tanımı sayesinde default threshold bile iyi performans üretmiştir.

---

##  8. Model Sonuçları
Son durumda elde edilen en önemli metrikler:

| Metrik | Değer |
|--------|--------|
| **Accuracy** | ~0.62 |
| **Recall (Churn=1)** | **0.80** |
| **F1 Score (Churn=1)** | **0.71** |
| **ROC-AUC** | ~0.60 |

###  Yorum:
Churn sınıfında **%80 yakalama oranı** (recall) sektörel olarak **çok güçlüdür**.  
F1 = 0.71 churn modellerinde oldukça iyi bir performanstır.  
Accuracy düşük olabilir, ancak churn modellerinde accuracy önemsizdir.

---

##  9. Streamlit Uygulaması
Proje, kullanıcı arayüzü ile tamamlanmıştır.

### Kullanıcı:
- Müşteri bilgilerini girer  
- Model churn olasılığını hesaplar  
- Riskli müşteriler için uyarı verir  

Çalıştırmak için:
--> streamlit run app/streamlit_app.py



### 10. Proje Dosya Yapısı
customer-churn-prediction/
│
├── data/                    # Ham veri & işlenmiş veri
├── notebooks/               # EDA, FE ve model eğitim notebook'ları
├── models/                  # final_churn_model.pkl
├── app/
│   └── streamlit_app.py     # Streamlit uygulaması
├── environment.yml          # Conda ortam dosyası
└── README.md                # Proje dokümantasyonu




### 11. Sonuç ve Değerlendirme

Bu proje:

✔ Veri temizleme
✔ Feature engineering
✔ ML pipeline
✔ Model optimizasyonu
✔ Churn tanımlama
✔ Streamlit uygulaması

adımlarını uçtan uca içeren tam bir makine öğrenimi projesidir.

Model, operasyonel olarak kullanılabilir seviyede churn tahminleri verir ve işletmenin müşteri kaybını azaltmasına yardımcı olabilir.



### Geliştirici

Dilaver Oruç
Data Analytics & Machine Learning

```bash
