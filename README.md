#  Gesture Controlled Media Player

Control your media player using just your fingers and a webcam — no need to touch your keyboard or mouse!

This project lets you play/pause, adjust volume, toggle fullscreen, and even switch tabs by making simple hand gestures in front of your webcam. It uses **MediaPipe** to track your hand, **OpenCV** to process the video, and **PyAutoGUI** to simulate keyboard shortcuts.

---

##  What Can It Do?

Here are the gestures you can use:

| Gesture               | Action             |
|-----------------------|--------------------|
| Thumb + Index         | Play/Pause         |
| Thumb + Middle        | Volume Up          |
| Thumb + Ring          | Volume Down        |
| Thumb + Pinky         | Toggle Fullscreen  |
| Finger Gun            | Switch Tab         |

All gestures are tracked live using your webcam, and the app gives visual feedback by showing which points it's tracking and which gesture you're making.

---

## 🛠 How to Set It Up

###  Requirements
- Python 3.7 or newer
- Webcam
- The following Python libraries:
  - `opencv-python`
  - `mediapipe`
  - `pyautogui`
  - `numpy`

Install them using:

```bash
**pip install opencv-python mediapipe pyautogui numpy
▶ Run the App
bash
Copy
Edit
python gesture_control.py
Make sure your webcam is on and you have good lighting. Then start making gestures!
* Why I Built This
Sometimes it's nice to control videos or presentations without needing to touch your laptop — especially during talks, workouts, or while cooking. This project makes it possible using only your hands and some computer vision magic.
**
