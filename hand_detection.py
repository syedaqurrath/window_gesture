import cv2
import mediapipe as mp
import time
import numpy as np
from collections import deque
import keyboard

# ---------------------- CONFIGURATION ----------------------
MAX_NUM_HANDS = 1
GESTURE_COOLDOWN = 1  # seconds
SWIPE_THRESHOLD = 80  # pixels
SWIPE_SPEED = 0.5     # pixels/ms
BUFFER_SIZE = 7       # For smoothing finger position

# ---------------------- INITIALIZATION ----------------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

FINGER_TIPS = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
FINGER_PIPS = [6, 10, 14, 18]  # Corresponding PIP joints


def is_hand_open(landmarks):
    """Return True if all four fingers (except thumb) are open."""
    open_fingers = 0
    for tip, pip in zip(FINGER_TIPS, FINGER_PIPS):
        if landmarks[tip].y < landmarks[pip].y:
            open_fingers += 1
    return open_fingers >= 3  # At least 3 fingers extended


def main():
    """Main loop for hand gesture detection and window switching."""
    cap = cv2.VideoCapture(0)
    hands = mp_hands.Hands(max_num_hands=MAX_NUM_HANDS)
    prev_x = 0
    prev_time = time.time()
    last_gesture_time = 0
    finger_x_buffer = deque(maxlen=BUFFER_SIZE)
    finger_time_buffer = deque(maxlen=BUFFER_SIZE)
    gesture_enabled = True
    swipe_ready = False
    swipe_direction = None
    trigger_visual = False
    trigger_visual_time = 0

    while True:
        success, img = cap.read()
        if not success:
            print("[ERROR] Failed to read from webcam.")
            break

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)
        img_height, img_width = img.shape[:2]
        now = time.time()
        swipe_ready = False
        swipe_direction = None

        if results.multi_hand_landmarks:
            for hand_landmark in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_landmark, mp_hands.HAND_CONNECTIONS)

                # Get index finger x position
                x = hand_landmark.landmark[8].x
                finger_x = int(x * img_width)
                finger_x_buffer.append(finger_x)
                finger_time_buffer.append(now)

                # Use smoothed x position
                if len(finger_x_buffer) == BUFFER_SIZE:
                    smoothed_x = int(np.mean(finger_x_buffer))
                    dx = finger_x_buffer[-1] - finger_x_buffer[0]
                    dt = finger_time_buffer[-1] - finger_time_buffer[0]
                    speed = abs(dx) / (dt * 1000) if dt > 0 else 0  # pixels/ms

                    # Check if hand is open
                    if is_hand_open(hand_landmark.landmark):
                        # Visual feedback for swipe readiness
                        if abs(dx) > SWIPE_THRESHOLD and speed > SWIPE_SPEED:
                            swipe_ready = True
                            swipe_direction = 'right' if dx > 0 else 'left'

                        # Gesture detection and trigger
                        if prev_x != 0 and gesture_enabled and (now - last_gesture_time > GESTURE_COOLDOWN):
                            if swipe_ready:
                                if swipe_direction == 'right':
                                    print("➡️ Swiped Right — Next Window")
                                    switch_window(next=True)
                                    last_gesture_time = now
                                    trigger_visual = True
                                    trigger_visual_time = now
                                elif swipe_direction == 'left':
                                    print("⬅️ Swiped Left — Previous Window")
                                    switch_window(next=False)
                                    last_gesture_time = now
                                    trigger_visual = True
                                    trigger_visual_time = now
                    prev_x = smoothed_x
                else:
                    prev_x = finger_x
        else:
            finger_x_buffer.clear()
            finger_time_buffer.clear()
            prev_x = 0

        # FPS calculation
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if curr_time != prev_time else 0
        prev_time = curr_time
        cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        status_text = 'Gesture: ON' if gesture_enabled else 'Gesture: OFF'
        cv2.putText(img, status_text, (10, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

        # On-screen instructions
        cv2.putText(img, 'Swipe hand (open) left/right to switch windows', (10, img_height-40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
        cv2.putText(img, 'Press G to toggle gesture, Q to quit', (10, img_height-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        # Visual feedback for swipe readiness
        if swipe_ready and gesture_enabled:
            color = (0,255,0) if swipe_direction == 'right' else (0,0,255)
            cv2.rectangle(img, (0,0), (img_width, 10), color, -1)
        # Visual feedback for trigger
        if trigger_visual and (now - trigger_visual_time < 0.3):
            cv2.rectangle(img, (0,0), (img_width, img_height), (0,255,255), 10)
        else:
            trigger_visual = False

        cv2.imshow("Gesture Control", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('g'):
            gesture_enabled = not gesture_enabled
            print(f"Gesture control {'enabled' if gesture_enabled else 'disabled'}.")

    cap.release()
    cv2.destroyAllWindows()

def switch_window(next=True):
    """Switch to the next or previous window using Alt+Tab."""
    if next:
        keyboard.press_and_release('alt+tab')
    else:
        keyboard.press('alt')
        keyboard.press('shift')
        keyboard.press_and_release('tab')
        keyboard.release('shift')
        keyboard.release('alt')

if __name__ == "__main__":
    main()
