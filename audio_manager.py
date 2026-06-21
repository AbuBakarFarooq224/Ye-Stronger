"""
audio_manager.py .
Loads .wav files from assets/ and plays them on demand.
Falls back to a synthetic sine-wave tone if a file is missing.
"""

import os
import numpy as np
import pygame


class AudioManager:

    WORD_FILES = {
        "Work It":  "work_it.wav",
        "Make It":  "make_it.wav",
        "Do It":    "do_it.wav",
        "Makes Us": "makes_us.wav",
        "Harder":   "harder.wav",
        "Better":   "better.wav",
        "Faster":   "faster.wav",
        "Stronger": "stronger.wav",
    }

    FALLBACK_FREQS = {
        "Work It":  294,
        "Make It":  330,
        "Do It":    349,
        "Makes Us": 392,
        "Harder":   440,
        "Better":   494,
        "Faster":   523,
        "Stronger": 587,
    }

    def __init__(self, assets_dir="assets"):
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        self._sounds = {}
        self._load_all(assets_dir)

    def _make_tone(self, freq, duration=0.25, volume=0.5):
        sr  = 22050
        n   = int(sr * duration)
        t   = np.linspace(0, duration, n, False)
        wav = np.sin(2 * np.pi * freq * t)
        wav = (wav * np.linspace(1, 0, n) * volume * 32767).astype(np.int16)
        return pygame.sndarray.make_sound(np.column_stack([wav, wav]))

    def _load_all(self, assets_dir):
        for word, fname in self.WORD_FILES.items():
            path = os.path.join(assets_dir, fname)
            if os.path.exists(path):
                try:
                    self._sounds[word] = pygame.mixer.Sound(path)
                    print(f"  ✅  loaded  {fname}")
                    continue
                except Exception as e:
                    print(f"  ⚠️   failed  {fname}: {e}")
            freq = self.FALLBACK_FREQS.get(word, 440)
            self._sounds[word] = self._make_tone(freq)
            print(f"  🎵  tone    {word}  ({freq} Hz)")

    def play(self, word):
        s = self._sounds.get(word)
        if s:
            s.play()

    def stop_all(self):
        pygame.mixer.stop()
