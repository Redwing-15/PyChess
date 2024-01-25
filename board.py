import pygame
from piece import Piece


class Board:
    def __init__(self):
        # Create board tiles
        self.positions = [0] * 64
        self.newTiles = []

        for file in range(8):
            for rank in range(8):
                self.newTiles.append(pygame.Rect((rank) * 75, (7 - file) * 75, 75, 75))

        # Create pieces
        for pos in range(8):
            self.positions[pos + 8] = Piece("pawn", 0)
            self.positions[pos + 48] = Piece("pawn", 1)

        for team in range(2):
            offset = team * 56

            self.positions[0 + offset] = Piece("rook", team)
            self.positions[1 + offset] = Piece("knight", team)
            self.positions[2 + offset] = Piece("bishop", team)
            self.positions[3 + offset] = Piece("queen", team)
            self.positions[4 + offset] = Piece("king", team)
            self.positions[5 + offset] = Piece("bishop", team)
            self.positions[6 + offset] = Piece("knight", team)
            self.positions[7 + offset] = Piece("rook", team)

        # Code for displaying board
        # temp = []
        # for item in self.positions:
        #     if isinstance(item, int):
        #         temp.append(0)
        #         continue
        #     temp.append(f"{item.type}, {item.team}")
        # print(temp)

    def move_piece(self, piece, pos):
        self.positions[piece.isMoving] = 0
        self.positions[pos] = piece
        piece.isMoving = False

    def get_pieces(self, team):
        pieces = [0] * 16
        for entry in range(16):
            for value in range(64):
                piece = self.positions[value]
                if isinstance(piece, int):
                    continue
                if piece.team != team:
                    continue
                if piece in pieces:
                    continue
                pieces[entry] = piece
        return pieces
