"""
hand_tracker.py
Tracks both hands. Returns:
  - 8 fingertip positions (4 fingers x 2 hands, NO thumbs)
  - 2 thumb tip positions (one per hand)
"""

import cv2
import mediapipe as mp

# Only the 4 fingers — thumbs are used as the play trigger
FINGER_IDS = [8, 12, 16, 20]   # index, middle, ring, pinky

# Left hand finger words (index→pinky)
LEFT_WORDS  = ["Work It", "Make It", "Do It", "Makes Us"]
# Right hand finger words (index→pinky)
RIGHT_WORDS = ["Harder", "Better", "Faster", "Stronger"]

THUMB_ID = 4


class HandTracker:
    def __init__(self):
        _mp          = mp.solutions.hands
        self._hands  = _mp.Hands(
            max_num_hands            = 2,
            min_detection_confidence = 0.75,
            min_tracking_confidence  = 0.65,
        )

    def get_data(self, frame):
        """
        Returns:
          fingers : list of { 'word', 'x', 'y' }
          thumbs  : list of { 'x', 'y' }
        """
        h, w = frame.shape[:2]
        rgb  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        res  = self._hands.process(rgb)

        fingers, thumbs = [], []

        if not res.multi_hand_landmarks:
            return fingers, thumbs

        for hand_lm, hand_info in zip(res.multi_hand_landmarks,
                                       res.multi_handedness):
            label    = hand_info.classification[0].label  # "Left" or "Right"
            lm       = hand_lm.landmark

            # Mirrored feed: MediaPipe "Left" = user's right hand on screen
            word_map = LEFT_WORDS if label == "Right" else RIGHT_WORDS

            # 4 finger tips
            for i, tip_id in enumerate(FINGER_IDS):
                cx = int(lm[tip_id].x * w)
                cy = int(lm[tip_id].y * h)
                fingers.append({"word": word_map[i], "x": cx, "y": cy})

            # Thumb tip
            tx = int(lm[THUMB_ID].x * w)
            ty = int(lm[THUMB_ID].y * h)
            thumbs.append({"x": tx, "y": ty})

        return fingers, thumbs

    def close(self):
        self._hands.close()
