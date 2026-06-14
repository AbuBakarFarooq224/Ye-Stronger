# Gesture Controlled Ye's Stronger

A real-time AR music interface built with Python and OpenCV. Each finger on both hands carries a word label from Ye's *Stronger*. Touch a finger with your thumb (the play button) to trigger that word's audio clip.

---

## Demo

> Both thumbs act as floating play buttons. Move your thumb to touch any fingertip and the assigned word plays its audio clip.

---

## Project Structure

```
├── main.py              # Main app loop
├── hand_tracker.py      # MediaPipe hand tracking
├── finger_label.py      # Draws word boxes on fingertips
├── play_button.py       # Play button UI (unused in v4, logic in main)
├── audio_manager.py     # Loads and plays audio clips
├── requirements.txt     # Python dependencies
│
└── assets/              # Audio clips (you provide these)
    ├── work_it.wav
    ├── make_it.wav
    ├── do_it.wav
    ├── makes_us.wav
    ├── harder.wav
    ├── better.wav
    ├── faster.wav
    └── stronger.wav
```

---

## Installation

Make a Separate Folder in your PC and name it whatever you want, then open powershell and run this command 

```bash
cd WHATEVER_YOU_NAMED
```

After that run this command, you need to have git installed before.

```bash
git clone https://github.com/AbuBakarFarooq224/Ye-Stronger.git
```

**2. Install dependencies**

```bash
pip install opencv-python mediapipe==0.10.9 numpy pygame
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```
Press **Q** to quit.

> If the webcam doesn't open, edit line 8 of `main.py` and change `VideoCapture(0)` to `VideoCapture(1)`.

---


## Adding Audio

Chopped *Stronger* by Ye into 8 short `.wav` clips and place them in the `assets/` folder with these exact filenames:

| File | Word |
|------|------|
| `work_it.wav` | Work It |
| `make_it.wav` | Make It |
| `do_it.wav` | Do It |
| `makes_us.wav` | Makes Us |
| `harder.wav` | Harder |
| `better.wav` | Better |
| `faster.wav` | Faster |
| `stronger.wav` | Stronger |


## How It Works

### Hand Tracking
MediaPipe detects 21 landmarks per hand. The app uses:
- **Landmarks 8, 12, 16, 20** — index, middle, ring, pinky fingertips → word labels
- **Landmark 4** — thumb tip → play button

### Word Mapping

| Hand | Finger | Word |
|------|--------|------|
| Left | Index  | Work It |
| Left | Middle | Make It |
| Left | Ring   | Do It |
| Left | Pinky  | Makes Us |
| Right | Index | Harder |
| Right | Middle | Better |
| Right | Ring  | Faster |
| Right | Pinky | Stronger |

### Collision Detection
Each frame, the Euclidean distance between the thumb tip and every fingertip is calculated:

```
distance = √((thumb_x - finger_x)² + (thumb_y - finger_y)²)
```

If `distance < 50px` → contact detected → audio plays.

### No Repeat Playback
A `touching` set tracks active contacts. Audio only fires on the **first frame** of contact. The finger must leave and re-enter before it triggers again.

---

## Dependencies

| Library | Purpose |
|---------|---------|
| `opencv-python` | Webcam feed and drawing |
| `mediapipe==0.10.9` | Hand landmark detection |
| `numpy` | Array operations |
| `pygame` | Audio playback |

---


## Built With

- Python 3.11
- OpenCV
- MediaPipe
- Pygame
- NumPy

---

