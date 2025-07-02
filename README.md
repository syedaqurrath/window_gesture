# Window Gesture

A Python application that uses your webcam and hand gestures to switch between windows on your computer.  
Powered by [MediaPipe](https://google.github.io/mediapipe/) for hand tracking and real-time gesture recognition.

---

## Features

- **Swipe right/left with your hand** to switch to the next/previous window (Alt+Tab).
- **Visual feedback**: Colored bars and borders indicate gesture readiness and triggers.
- **Toggle gesture control**: Press `g` to enable/disable gesture recognition.
- **Performance display**: See real-time FPS on the video window.
- **On-screen instructions** for easy use.

---

## Requirements

- Python 3.7+
- Webcam

### Python Packages

- `opencv-python`
- `mediapipe`
- `numpy`
- `keyboard`

Install all dependencies with:

```sh
pip install opencv-python mediapipe numpy keyboard
```

> **Note:**  
> On Windows, you must run the script as administrator for the `keyboard` library to send system hotkeys.

---

## Usage

1. **Clone the repository:**

   ```sh
   git clone https://github.com/syedaqurrath/window_gesture.git
   cd window_gesture
   ```

2. **Install dependencies:**

   ```sh
   pip install opencv-python mediapipe numpy keyboard
   ```

3. **Run the script as administrator:**

   ```sh
   python hand_detection.py
   ```

4. **How to use:**
   - Open your hand and swipe left/right in front of your webcam.
   - Watch for the colored bar (green = right, red = left) and yellow border for feedback.
   - Press `g` to toggle gesture control on/off.
   - Press `q` to quit.

---

## Troubleshooting

- If you see `ImportError: No module named ...`, make sure you installed all dependencies.
- If gestures do not switch windows, ensure you are running as administrator.
- For best results, use in a well-lit environment with a clear background.

---

## License

MIT License

---

## Author

[syedaqurrath](https://github.com/syedaqurrath)
