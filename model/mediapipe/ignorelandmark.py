# https://github.com/google/mediapipe/issues/3454
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
handConnection = [(5, 9), (10, 11), (5, 6), (15, 16), (13, 17), (18, 19),
            (6, 7), (0, 17), (9, 10), (0, 5), (14, 15),
            (11, 12), (19, 20), (9, 13), (17, 18), (13, 14), (7, 8)]

cap = cv2.VideoCapture(0)

def main():
    hands = mp_hands.Hands(
        min_detection_confidence=0.7, min_tracking_confidence=0.7)
    hand_landmark_drawing_spec = mp_drawing.DrawingSpec(thickness=5, circle_radius=5)
    hand_connection_drawing_spec = mp_drawing.DrawingSpec(thickness=10, circle_radius=10)

    while cap.isOpened():
        ret, image = cap.read()
        image = cv2.flip(image, 1)
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results_hand = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results_hand.multi_hand_landmarks:
            for hand_landmarks in results_hand.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=hand_landmarks,
                    connections=handConnection,
                    landmark_drawing_spec=hand_landmark_drawing_spec,
                    connection_drawing_spec=hand_connection_drawing_spec)

        keypress = cv2.waitKey(1)
        if keypress == ord('c'):
            break
        cv2.imshow("Img", image)

    hands.close()
    cap.release()

main()