from pygame import image
from pygame import transform
from os import path


class Piece:
    def __init__(self, type, team):
        self.type = type
        self.team = team

        self.image = image.load(path.abspath(f".\\images\\white_{type}.png"))
        if team == 1:
            self.image = image.load(path.abspath(f".\\images\\black_{type}.png"))
        self.image = transform.scale(self.image, (75, 75))

        self.isMoving = False

    # Get every possible move for the piece, excluding special cases like castling or en passant
    def get_moveset(self):
        moveset = []
        if self.type == "rook" or self.type == "queen":
            for move in range(1, 8):
                moveset.extend([1 * move, -1 * move, 8 * move, -8 * move])
        # Not using elif so queen can use moves of both rook and bishop
        if self.type == "bishop" or self.type == "queen":
            for move in range(1, 8):
                moveset.extend([9 * move, -9 * move, 7 * move, -7 * move])
        elif self.type == "pawn":
            moveset.extend([7, 8, 9])
        elif self.type == "knight":
            moveset.extend([-10, -17, -6, -15, 6, 15, 10, 17])
        elif self.type == "king":
            moveset.extend([1, -1, 8, -8, 7, 9, -7, -9])

        if self.team == 1:
            moveset = [n * -1 for n in moveset]
        return moveset
