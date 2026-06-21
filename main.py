"""
main.py — Gesture Controlled Music Mixer .
- 8 words on 8 fingers (no thumbs)
- Play button follows each thumb
- When thumb (play button) touches any finger tip → play that finger's word
"""

import cv2
import math
import time
from hand_tracker  import HandTracker
from finger_label  import FingerLabel
from audio_manager import AudioManager
import numpy as np


BUTTON_W, BUTTON_H = 80, 46
THUMB_ID = 4


def draw_thumb_button(frame, tx, ty, hovered=False):
    """Draw play button centred on thumb tip."""
    x1 = tx - BUTTON_W // 2
    y1 = ty - BUTTON_H // 2
    x2 = tx + BUTTON_W // 2
    y2 = ty + BUTTON_H // 2

    fill   = (0, 180, 60)  if hovered else (40, 40, 40)
    border = (0, 255, 100) if hovered else (180, 180, 180)

    cv2.rectangle(frame, (x1, y1), (x2, y2), fill,   -1)
    cv2.rectangle(frame, (x1, y1), (x2, y2), border,  2)

    tri = np.array([
        [tx - 10, ty - 12],
        [tx - 10, ty + 12],
        [tx + 14, ty],
    ], dtype=np.int32)
    cv2.fillPoly(frame, [tri], (255, 255, 255))


def thumb_hits_finger(tx, ty, fx, fy, thresh=50):
    """True if thumb button overlaps a fingertip."""
    return math.hypot(tx - fx, ty - fy) < thresh


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌  Cannot open webcam"); return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,  720)

    tracker = HandTracker()
    label   = FingerLabel()
    audio   = AudioManager(assets_dir="assets")

    # Track which (thumb_idx, word) pairs are currently touching
    # prevents continuous replay while contact is maintained
    touching = set()

    active_word = ""
    prev_time   = time.time()

    print("\n✅  Move thumb play button onto a finger to trigger | Q to quit\n")

    while True:
        ok, frame = cap.read()
        if not ok: break

        frame = cv2.flip(frame, 1)
        fingers, thumbs = tracker.get_data(frame)

        active_labels  = set()
        currently_touch = set()

        # ── For each thumb, check collision with every finger ─────────────────
        for ti, thumb in enumerate(thumbs):
            tx, ty   = thumb["x"], thumb["y"]
            hovered  = False

            for f in fingers:
                fx, fy = f["x"], f["y"]
                key    = (ti, f["word"])

                if thumb_hits_finger(tx, ty, fx, fy):
                    hovered = True
                    currently_touch.add(key)
                    active_labels.add(f["word"])

                    # Play only on fresh contact
                    if key not in touching:
                        audio.play(f["word"])
                        active_word = f["word"]

            draw_thumb_button(frame, tx, ty, hovered)

        # Keys no longer touching → remove so they can retrigger
        touching = currently_touch

        # ── Draw finger labels ────────────────────────────────────────────────
        for f in fingers:
            label.draw(frame,
                       word   = f["word"],
                       cx     = f["x"],
                       cy     = f["y"],
                       active = f["word"] in active_labels)

        # ── UI ────────────────────────────────────────────────────────────────
        now       = time.time()
        fps       = 1.0 / (now - prev_time + 1e-9)
        prev_time = now

        cv2.putText(frame, f"FPS: {fps:.0f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)

        if active_word:
            fw = frame.shape[1]
            cv2.putText(frame, active_word.upper(),
                        (fw // 2 - 100, 50),
                        cv2.FONT_HERSHEY_DUPLEX, 1.1, (0, 200, 255), 2, cv2.LINE_AA)

        cv2.imshow("Gesture Music Mixer", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    tracker.close()
    audio.stop_all()


if __name__ == "__main__":
    main()
