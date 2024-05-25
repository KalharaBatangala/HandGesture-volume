import cv2
import mediapipe as mp
import pyautogui
import math
import threading

x1 = y1 = x2 = y2 = 0
webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) // 4

def distance_checker():
    global x1, y1, x2, y2
    while True:
        distance = calculate_distance(x1, y1, x2, y2)
        if distance > 35:
            pyautogui.press("VolumeUp")
        else:
            pyautogui.press("VolumeDown")


def main():
    global x1, y1, x2, y2
    distance_thread = threading.Thread(target=distance_checker, daemon=True)
    distance_thread.start()

    while True:
        _, image = webcam.read()
        frame_height, frame_width, _ = image.shape
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        output = my_hands.process(rgb_image)
        hands = output.multi_hand_landmarks
        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(image, hand)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    if id == 8:
                        cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                        x1 = x
                        y1 = y
                    if id == 4:
                        cv2.circle(img=image, center=(x, y), radius=8, color=(0, 0, 255), thickness=3)
                        x2 = x
                        y2 = y
                    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)

        cv2.imshow("Hand volume control using python", image)
        key = cv2.waitKey(10)
        if key == 27:
            break

    webcam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
