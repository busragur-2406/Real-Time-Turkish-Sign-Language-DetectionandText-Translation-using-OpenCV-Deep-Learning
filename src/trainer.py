import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle
import numpy as np

# 1. Verisetini Yükle
try:
    data = pd.read_csv('isaret_dili_veriseti.csv')
    print(f"Veriseti yüklendi. Toplam veri sayısı: {len(data)}")
except FileNotFoundError:
    print("HATA: 'isaret_dili_veriseti.csv' bulunamadı. Lütfen önce data_collector.py ile veri toplayın.")
    exit()

# 2. Veriyi Parçala
X = data.drop('label', axis=1) # Girdiler (koordinatlar)
y = data['label']              # Çıktılar (A, B, C...)

# 3. Eğitim ve Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True, random_state=42)

# 4. Model Eğitimi
print("Model eğitiliyor...")
model = RandomForestClassifier()
model.fit(X_train, y_train)

# 5. Test
y_pred = model.predict(X_test)
score = accuracy_score(y_test, y_pred)
print(f"Model Doğruluk Oranı: %{score * 100:.2f}")

# 6. Kayıt
with open('model.p', 'wb') as f:
    pickle.dump(model, f)
print("Model 'model.p' dosyasına kaydedildi!")