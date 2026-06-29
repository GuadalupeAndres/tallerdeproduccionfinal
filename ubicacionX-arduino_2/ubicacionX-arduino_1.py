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
time.sleep(2)

proximo_envio = 0

print("Enviando valores por serial. Ctrl+C para cortar.")

contador = 0
ubicacionX = 0

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
                posX = int (hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]. x * width)
                #print(X)
                contador += 1
                #print(contador)

            #---------------------------------------------------

            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks (
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
            #-----------------------------------------------------

            if posX <= 64:

                ubicacionX = 1

            if posX >= 65 and posX <= 127:

                ubicacionX = 2

            if posX >= 128 and posX <= 191:

                ubicacionX = 3

            if posX >= 192 and posX <= 255:

                ubicacionX = 4

            if posX >= 256 and posX <= 319:

                ubicacionX = 5

            if posX >= 320 and posX <= 383:

                ubicacionX = 6

            if posX >= 384 and posX <= 447:

                ubicacionX = 7

            if posX >= 448 and posX <= 511:

                ubicacionX = 8

            if posX >= 512 and posX <= 575:

                ubicacionX = 9

            if posX >= 576:

                ubicacionX = 10

            #-----------------------------------------------------

            if contador >= 15:
                try:                    
                    valor = ubicacionX
                    direccion = 1
                    contador = 0

                    # valor += direccion
        
                    print(valor)

                    if time.time() >= proximo_envio:
                        arduino.write(f"{valor}\n".encode("utf-8"))
                        proximo_envio = time.time() + PAUSA

                except KeyboardInterrupt:
                    print("\nCerrando puerto serial.")
                    arduino.close()


        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
       

cap.release()
cv2.destroyAllWindows()