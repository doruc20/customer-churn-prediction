## 🔗 Demo

Projenin canlı halini buradan deneyebilirsiniz:  
https://kullanici-adi-customer-churn-prediction.streamlit.app



# 🛒 Customer Churn Prediction  
Bu proje, bir perakende şirketindeki müşterilerin **churn (müşteri kaybı)** olasılığını tahmin etmek için geliştirilmiş uçtan uca bir makine öğrenimi uygulamasıdır.  
Proje, veri keşfi (EDA), feature engineering, model geliştirme, değerlendirme ve Streamlit arayüzü ile tamamlanmıştır.

---

## Proje Kapsamı  
Bu çalışma, **Zero2End Machine Learning Bootcamp** final projesi kapsamında geliştirilmiştir.  
Amaç, gerçek bir iş senaryosuna benzeyen churn tahmini problemini, veri işleme aşamalarından modellemesine ve basit bir uygulamaya kadar uçtan uca çözmektir.

---

## 1️⃣ Proje Amacı  
Perakende sektöründe müşterilerin bir kısmı zaman içinde platformdan uzaklaşarak alışverişi bırakır.  
Bu müşteri kaybını (churn) doğru tahmin etmek:

- Satış departmanına erken müdahale imkânı tanır  
- Kampanya maliyetini düşürür  
- Müşteri bağlılığını artırır  

Bu projede amaç, müşterinin geçmiş davranışları üzerinden **churn riskini tahmin edebilen bir model** geliştirmektir.

---

## 2️⃣ Veri Seti  
Kullanılan veri seti: **Marketing Campaign Dataset**  
Müşterilerin:

- Demografik bilgilerini  
- Harcama alışkanlıklarını  
- Kampanya geri dönüşlerini  
- Dijital davranışlarını  

içerir.

---

## 2.1 Veri Seti Kolon Açıklamaları

### 🔹 Demografik Bilgiler
| Kolon | Açıklama |
|-------|----------|
| **ID** | Müşteri kimlik numarası |
| **Year_Birth** | Müşterinin doğum yılı |
| **Education** | Eğitim seviyesi |
| **Marital_Status** | Medeni durum |
| **Income** | Yıllık gelir |
| **Kidhome** | Evdeki küçük çocuk sayısı |
| **Teenhome** | Evdeki genç sayısı |

### 🔹 Müşteri Zaman Bilgisi
| Kolon | Açıklama |
|-------|----------|
| **Dt_Customer** | Müşterinin şirkete katıldığı tarih |
| **Recency** | Son alışverişten bu yana geçen gün |

### 🔹 Harcama Bilgileri
| Kolon | Açıklama |
|-------|----------|
| **MntWines** | Şarap harcaması |
| **MntFruits** | Meyve harcaması |
| **MntMeatProducts** | Et ürünleri harcaması |
| **MntFishProducts** | Balık harcaması |
| **MntSweetProducts** | Tatlı harcaması |
| **MntGoldProds** | Altın/değerli ürün harcaması |

### 🔹 Davranış
| Kolon | Açıklama |
|-------|----------|
| **NumDealsPurchases** | İndirimli alışveriş sayısı |
| **NumWebPurchases** | Web siparişi sayısı |
| **NumCatalogPurchases** | Katalog siparişi |
| **NumStorePurchases** | Mağaza alışverişi |
| **NumWebVisitsMonth** | Web ziyaret sayısı |

### 🔹 Kampanya Etkileşimleri
| Kolon | Açıklama |
|-------|----------|
| **AcceptedCmp1–5** | Kampanya kabul bilgisi |
| **Response** | Son kampanyaya dönüş |
| **Complain** | Son 2 yılda şikayet var mı? |

---

## 3️⃣ Problem Tanımı ve Baseline

### ✔ Problem  
Veri setinde gerçek churn etiketi bulunmadığı için, churn davranışı **müşteri etkileşim azalmasına göre tanımlanmıştır**.

### ✔ Baseline  
Basit RF/LogReg modelleri ile temel feature'larla yapılan analiz sonucu:

- **Baseline Recall (Churn=1): ~0.30**  
- **Baseline F1 (Churn=1): ~0.35**

Bu seviyeler iyileştirme için referans olarak kullanılmıştır.

---

## 4️⃣ Churn Tanımı  

Veri setinde gerçek churn olmadığı için davranışsal bir tanım geliştirilmiştir:

- **Churn = 1 → Recency > 40**  
- **Churn = 0 → Recency ≤ 40**

⚠ Not: Recency **modelde feature olarak kullanılmamıştır** (data leakage engellendi).

---

## 5️⃣ Veri Temizleme  

- Eksik tarih formatları düzeltildi  
- Outlier kontrolleri yapıldı (özellikle Income & harcama kolonları)  
- Gereksiz kolonlar silindi: `ID`, `Z_CostContact`, `Z_Revenue`  
- Kategorik değişken sınıfları birleştirildi  
- Recency leak olmaması için modelde kullanılmadı  

---

## 6️⃣ Validasyon Şeması & Ön İşleme Stratejisi

**Validasyon:**

- %80 / %20 train-test split  
- Random split (çünkü zaman bağımlı veri değil)  
- Hedef: genel performansı ölçmek

**Ön İşleme:**

- Education → ordinal encoding (1–5)  
- Marital_Status → one-hot encoding  
- Tüm sayısal kolonlar → StandardScaler  
- Pipeline içinde otomatik uygulanacak şekilde düzenlendi  

---

## 7️⃣ Feature Engineering  

Oluşturulan yeni değişkenler:

| Feature | Açıklama |
|--------|----------|
| **TotalSpending** | Tüm harcamaların toplamı |
| **CustomerTenure** | Müşterinin şirkette kalma süresi |
| **TotalAcceptedCmp** | Kabul edilen kampanya sayısı |
| **CampaignSuccessRate** | Kampanya başarı oranı |
| **CLV** | Yaşam boyu değer |
| **SpendingToIncome** | Harcama / gelir oranı |
| **PurchaseActivity** | Tüm alışveriş & ziyaret aktivitesi |
| **HighValue** | Üst segment müşteri bayrağı |
| **IsParent** | Evde çocuk/genç var mı |

---

## 8️⃣ Modelleme  
Model **Sklearn Pipeline** ile geliştirilmiştir:

- Preprocessing  
- Feature Engineering  
- Encoding & Scaling  
- **RandomForestClassifier**

Pipeline → eğitim → değerlendirme → kaydetme (.pkl)

---

## 9️⃣ Model Sonuçları  

| Metrik | Değer |
|--------|--------|
| **Accuracy** | ~0.62 |
| **Recall (Churn=1)** | **0.80** |
| **F1 Score (Churn=1)** | **0.71** |
| **ROC-AUC** | ~0.60 |

### 🧠 Yorum  
Churn modellerinde accuracy yanlı bir metrik olabilir.  
Burada kritik olan Recall ve F1 skorudur:

- **Recall 0.80** → churn edenlerin %80’i doğru yakalanıyor  
- **F1 0.71** → dengeli bir doğruluk-performans uyumu  

Bu sonuçlar, bir churn modeli için oldukça başarılıdır.

---

## 🔟 Final Model vs Baseline & Business Uyumu

### Baseline → Final farkı:
| Metrik | Baseline | Final |
|--------|----------|--------|
| Recall (1) | ~0.30 | **0.80** |
| F1 (1) | ~0.35 | **0.71** |

Performans artışı; yeni feature’lar, churn tanımının düzenlenmesi ve sadeleştirilmiş feature seti sayesinde elde edilmiştir.

### Business Uyumu  
Gerçek şirketlerde churn modellerinde amaç:

✔ Churn eden müşteriyi *kaçırmamak*  
→ Bu nedenle **Recall > Accuracy**

Model bu iş gereksinimiyle uyumludur.

---

## 1️⃣1️⃣ Streamlit Uygulaması  

Müşteri bilgileri girilerek anlık churn riski tahmini yapılabilir.

Çalıştırmak için:

```bash
streamlit run app/streamlit_app.py
