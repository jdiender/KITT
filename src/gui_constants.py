# Constants
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

FIELD_WIDTH = WINDOW_WIDTH if WINDOW_WIDTH < WINDOW_HEIGHT else WINDOW_HEIGHT
FIELD_HEIGHT = FIELD_WIDTH

SCALE = 0.5
FIELD_WIDTH *= SCALE
FIELD_HEIGHT *= SCALE

FIELD_X_OFFSET = WINDOW_WIDTH/2.0-FIELD_WIDTH/2.0
FIELD_Y_OFFSET = WINDOW_HEIGHT/2.0-FIELD_HEIGHT/2.0

# Position container
from pygame import Vector2
from dataclasses import dataclass

@dataclass
class Position:
    pos: Vector2

    dx: float = FIELD_X_OFFSET
    dy: float = FIELD_Y_OFFSET + FIELD_HEIGHT

    def __init__(self, x: float, y: float):
        self.pos = Vector2(self.dx + FIELD_WIDTH*x/4.8,
                           self.dy - FIELD_HEIGHT*y/4.8)

    def update(self, x: float, y: float):
        self.pos = Vector2(self.dx + FIELD_WIDTH*x/4.8,
                           self.dy - FIELD_HEIGHT*y/4.8)

    def get(self) -> Vector2:
        return self.pos
