import time
import serial
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap= cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

PUERTO = "COM3"

BAUDIOS = 9600
PAUSA = 0.001


arduino = serial.Serial(PUERTO, BAUDIOS)
time.sleep(1)

proximo_envio = 0

print("Enviando valores por serial. Ctrl+C para cortar.")


with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,) as hands:

    while True:
        ret, frame = cap.read()
        if ret == False:
            break

        height, width, _ = frame.shape
        frame = cv2.flip(frame,1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(frame_rgb)

        #print("Handedness:", results.multi_handedness)


        if results.multi_hand_landmarks is not None:

            for hand_landmarks in results.multi_hand_landmarks:
                posX = int (hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]. x * width)
                #print(X)
                
            #---------------------------------------------------

            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks (
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
            #-----------------------------------------------------
            

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

try:
    valor = posX
    direccion = 1
    while True:
        valor += direccion
        #if valor >= 200:
        #    direccion = 1
        #elif valor <= 199:
        #    direccion = -1
        
        print(valor)

        if time.time() >= proximo_envio:
            arduino.write(f"{valor}\n".encode("utf-8"))
            proximo_envio = time.time() + PAUSA

except KeyboardInterrupt:
    print("\nCerrando puerto serial.")
    arduino.close()

cap.release()
cv2.destroyAllWindows()


