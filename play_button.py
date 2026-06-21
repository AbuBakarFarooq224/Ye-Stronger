"""
play_button.py 
Fixed play button in the centre of the screen.
Collision: checks if thumb tip is inside the button rectangle.
"""

import cv2
import numpy as np


class PlayButton:
    W = 100
    H =  60

    def __init__(self, frame_w, frame_h):
        self.cx = frame_w // 2
        self.cy = frame_h // 2

    def contains(self, px, py):
        """True if point (px,py) is inside the button."""
        return (abs(px - self.cx) < self.W // 2 and
                abs(py - self.cy) < self.H // 2)

    def draw(self, frame, hovered=False):
        x1 = self.cx - self.W // 2
        y1 = self.cy - self.H // 2
        x2 = self.cx + self.W // 2
        y2 = self.cy + self.H // 2

        fill   = (0, 180, 60)  if hovered else (40, 40, 40)
        border = (0, 255, 100) if hovered else (180, 180, 180)

        cv2.rectangle(frame, (x1, y1), (x2, y2), fill,   -1)
        cv2.rectangle(frame, (x1, y1), (x2, y2), border,  2)

        # ▶ triangle
        tri = np.array([
            [self.cx - 14, self.cy - 16],
            [self.cx - 14, self.cy + 16],
            [self.cx + 18, self.cy],
        ], dtype=np.int32)
        cv2.fillPoly(frame, [tri], (255, 255, 255))
