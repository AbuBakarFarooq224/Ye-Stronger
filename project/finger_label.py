"""
finger_label.py
Draws a green bounding box label anchored to a fingertip position.
"""

import cv2


class FingerLabel:
    W       = 90    # box width
    H       = 30    # box height
    PADDING = 6

    COLOR_NORMAL = (0, 255, 0)       # green
    COLOR_ACTIVE = (0, 200, 255)     # cyan-yellow when triggered

    def draw(self, frame, word, cx, cy, active=False):
        """
        Draw label box centred just above the fingertip at (cx, cy).
        active=True highlights the box when audio is triggered.
        """
        color = self.COLOR_ACTIVE if active else self.COLOR_NORMAL

        x1 = cx - self.W // 2
        y1 = cy - self.H - 10     # sit above the fingertip dot
        x2 = x1 + self.W
        y2 = y1 + self.H

        # Dark fill so text is readable over any background
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), -1)
        # Coloured border
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Dot on the actual fingertip
        cv2.circle(frame, (cx, cy), 6, color, -1)

        # Centred text
        font  = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.45
        thick = 1
        (tw, th), _ = cv2.getTextSize(word, font, scale, thick)
        tx = x1 + (self.W - tw) // 2
        ty = y1 + (self.H + th) // 2
        cv2.putText(frame, word, (tx, ty),
                    font, scale, color, thick, cv2.LINE_AA)
