import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Open webcam
cap = cv2.VideoCapture(0)

# Initialize variables
last_action_time = 0
cooldown = 1  # seconds
current_gesture = ""

def get_gesture(hand_landmarks):
    global current_gesture
    lm = hand_landmarks.landmark
    thumb_tip = lm[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = lm[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    middle_tip = lm[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
    ring_tip = lm[mp_hands.HandLandmark.RING_FINGER_TIP]
    pinky_tip = lm[mp_hands.HandLandmark.PINKY_TIP]

    thumb_ip = lm[mp_hands.HandLandmark.THUMB_IP]
    index_mcp = lm[mp_hands.HandLandmark.INDEX_FINGER_MCP]
    middle_mcp = lm[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
    ring_mcp = lm[mp_hands.HandLandmark.RING_FINGER_MCP]
    pinky_mcp = lm[mp_hands.HandLandmark.PINKY_MCP]

    # 1. Pinch Gesture (Thumb + Index)
    thumb_index_dist = np.hypot(thumb_tip.x - index_tip.x, thumb_tip.y - index_tip.y)
    if thumb_index_dist < 0.05:
        current_gesture = "CLICK"
        return 'CLICK'

    # 2. Finger Gun Gesture
    if (index_tip.y < index_mcp.y and thumb_tip.x > thumb_ip.x) and \
       (middle_tip.y > middle_mcp.y and ring_tip.y > ring_mcp.y and pinky_tip.y > pinky_mcp.y):
        current_gesture = "FINGER_GUN"
        return 'FINGER_GUN'

    # 3. Ring Touch (Thumb + Ring Finger)
    thumb_ring_dist = np.hypot(thumb_tip.x - ring_tip.x, thumb_tip.y - ring_tip.y)
    if thumb_ring_dist < 0.05:
        current_gesture = "RING_TOUCH"
        return 'RING_TOUCH'

    # 4. Middle Touch (Thumb + Middle Finger)
    thumb_middle_dist = np.hypot(thumb_tip.x - middle_tip.x, thumb_tip.y - middle_tip.y)
    if thumb_middle_dist < 0.05:
        current_gesture = "MIDDLE_TOUCH"
        return 'MIDDLE_TOUCH'

    # 5. Pinky Touch (Thumb + Pinky Finger)
    thumb_pinky_dist = np.hypot(thumb_tip.x - pinky_tip.x, thumb_tip.y - pinky_tip.y)
    if thumb_pinky_dist < 0.05:
        current_gesture = "PINKY_TOUCH"
        return 'PINKY_TOUCH'

    current_gesture = ""
    return None

# Webcam loop
while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            h, w, _ = frame.shape

            # Draw green dots and landmark labels
            for id, lm in enumerate(handLms.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                cv2.putText(frame, str(id), (cx + 5, cy - 5), cv2.FONT_HERSHEY_SIMPLEX,
                            0.4, (255, 255, 255), 1, cv2.LINE_AA)

            # Detect gesture
            gesture = get_gesture(handLms)

            # Perform actions based on gesture
            if gesture == 'CLICK' and time.time() - last_action_time > cooldown:
                pyautogui.press('space')
                last_action_time = time.time()
            elif gesture == 'FINGER_GUN' and time.time() - last_action_time > cooldown:
                pyautogui.hotkey('ctrl', 'tab')
                last_action_time = time.time()
            elif gesture == 'RING_TOUCH' and time.time() - last_action_time > cooldown:
                pyautogui.press('volumedown')
                last_action_time = time.time()
            elif gesture == 'MIDDLE_TOUCH' and time.time() - last_action_time > cooldown:
                pyautogui.press('volumeup')
                last_action_time = time.time()
            elif gesture == 'PINKY_TOUCH' and time.time() - last_action_time > cooldown:
                pyautogui.press('f')  # Fullscreen toggle
                last_action_time = time.time()

    # Display current gesture
    if current_gesture:
        cv2.putText(frame, f"Gesture: {current_gesture}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                    1.0, (0, 0, 255), 2, cv2.LINE_AA)

    # Show webcam output
    cv2.imshow("Gesture Keyboard", frame)
    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()
