import pickle
import cv2
import mediapipe as mp
import numpy as np

# 1. Modeli Yükle
try:
    with open('./model.p', 'rb') as f:
        model = pickle.load(f)
    print("Model başarıyla yüklendi.")
except FileNotFoundError:
    print("HATA: 'model.p' dosyası bulunamadı. Lütfen önce trainer.py dosyasını çalıştırın.")
    exit()

# 2. MediaPipe Ayarları
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

cap = cv2.VideoCapture(0)

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                
                data_aux = []
                x_ = []
                y_ = []

                # Koordinatları al
                for i in range(len(hand_landmarks.landmark)):
                    x = hand_landmarks.landmark[i].x
                    y = hand_landmarks.landmark[i].y
                    data_aux.append(x)
                    data_aux.append(y)
                    
                    x_.append(x)
                    y_.append(y)

                # Tahmin Yap
                # Modelimiz 2 boyutlu array beklediği için [data_aux] şeklinde veriyoruz
                prediction = model.predict([np.array(data_aux)])
                predicted_character = prediction[0]

                # Görselleştirme (Kutu ve Harf)
                x1 = int(min(x_) * w) - 10
                y1 = int(min(y_) * h) - 10
                x2 = int(max(x_) * w) + 10
                y2 = int(max(y_) * h) + 10

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)
                cv2.putText(frame, predicted_character, (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3, cv2.LINE_AA)
                cv2.putText(frame, predicted_character, (x1, y1 - 10), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 2, cv2.LINE_AA)

                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())

        cv2.imshow('Isaret Dili Cevirmeni', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()