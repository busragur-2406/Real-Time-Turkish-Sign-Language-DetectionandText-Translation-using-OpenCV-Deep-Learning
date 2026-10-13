import cv2
import mediapipe as mp
import csv
import os

# --- AYARLAR ---
DOSYA_ADI = 'isaret_dili_veriseti.csv'

# MediaPipe Kurulumu
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# 1. Kullanıcıdan Hangi Harfi Kaydedeceğini İste
sinif_etiketi = input("Hangi harf/sınıf için veri toplayacaksın? (Örn: A, B, Selam): ")

# 2. CSV Dosyasını Hazırla (Başlıklar yoksa ekle)
# 21 nokta var, her birinin x ve y'si var -> toplam 42 sütun + 1 label
sutunlar = []
for i in range(21):
    sutunlar.append(f'x{i}')
    sutunlar.append(f'y{i}')
sutunlar.append('label') # Son sütun etiketimiz

if not os.path.exists(DOSYA_ADI):
    with open(DOSYA_ADI, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(sutunlar)

cap = cv2.VideoCapture(0)

counter = 0 # Kaç tane veri kaydettiğimizi sayalım

with mp_hands.Hands(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
    
    print(f"\n--- '{sinif_etiketi}' İÇİN KAYIT BAŞLADI ---")
    print("Kaydetmek için 'SPACE' tuşuna, çıkmak için 'Q' tuşuna basınız.\n")

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Kamera bulunamadı.")
            continue

        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        # El tespit edildiyse
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # İskeleti çiz
                mp_drawing.draw_landmarks(
                    image, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS)
                
                # --- VERİ HAZIRLAMA ---
                # Sadece SPACE'e basıldığında buradaki veriyi alacağız
                # Ancak veriyi her karede hazır tutuyoruz
                temp_landmark_list = []
                for lm in hand_landmarks.landmark:
                    # Sadece x ve y'yi alıyoruz (z derinliğini yoksayıyoruz şimdilik)
                    temp_landmark_list.append(lm.x)
                    temp_landmark_list.append(lm.y)
                
                # Etiketi listenin sonuna ekle
                temp_landmark_list.append(sinif_etiketi)

                # Tuş Kontrolü
                k = cv2.waitKey(1)
                
                # SPACE (Boşluk) Tuşu: ASCII 32
                if k == 32: 
                    with open(DOSYA_ADI, mode='a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow(temp_landmark_list)
                    
                    counter += 1
                    print(f"Kaydedildi: {sinif_etiketi} (Toplam: {counter})")
                    
                    # Ekrana görsel geri bildirim (Yeşil yazı)
                    cv2.putText(image, f"KAYDEDILDI ({counter})", (50, 50), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Q Tuşu: Çıkış
                elif k & 0xFF == ord('q'):
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

        # Ekrana Bilgi Yazısı
        cv2.putText(image, f"Sinif: {sinif_etiketi} | Sayac: {counter}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
        cv2.putText(image, "Space: Kaydet | Q: Cikis", (10, 450), 
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow('Veri Toplayici', image)
        
        # Döngü içinde de Q ile çıkış kontrolü (el algılanmazsa çalışması için)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()