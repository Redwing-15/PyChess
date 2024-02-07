from pygame import image
from pygame import transform
from os import path


class Piece:
    def __init__(self, type, team, position):
        self.type = type
        self.team = team

        self.image = image.load(path.abspath(f".\\images\\white_{type}.png"))
        if team == 1:
            self.image = image.load(path.abspath(f".\\images\\black_{type}.png"))
        self.image = transform.scale(self.image, (75, 75))

        self.pos = position
        self.moves = []
        self.moveCount = 0

        if type == "pawn":
            self.doublePush = False

        self.isMoving = False
