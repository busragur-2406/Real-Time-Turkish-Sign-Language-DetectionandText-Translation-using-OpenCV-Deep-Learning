import cv2
import mediapipe as mp

# MediaPipe çizim ve el algılama modüllerini çağırıyoruz
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Kamerayı başlat
cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    min_detection_confidence=0.5, # Algılama hassasiyeti
    min_tracking_confidence=0.5) as hands:
    
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Kamera bulunamadı.")
            continue

        # Görüntüyü yatay çevir (ayna etkisi) ve BGR'den RGB'ye dönüştür
        image = cv2.flip(image, 1)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # MediaPipe ile elleri tara
        results = hands.process(image_rgb)

        # Çizim için tekrar BGR'ye dönüştür
        image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

        # Eğer el tespit edildiyse
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Eklemleri çiz
                mp_drawing.draw_landmarks(
                    image, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS)
                
                # Örnek: Baş parmağın ucunun koordinatlarını yazdıralım (Landmark 4)
                # print(hand_landmarks.landmark[4]) 

        cv2.imshow('Isaret Dili Algilama - Test', image)

        # 'q' tuşuna basınca çık
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()