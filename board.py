import pygame
from piece import Piece


class Board:
    def __init__(self):
        # Create board tiles
        self.positions = []
        self.tiles = []
        for file in range(8):
            self.positions.append([])
            self.tiles.append([])
            for rank in range(8):
                self.positions[file].append(0)
                self.tiles[file].append(pygame.Rect(file * 75, rank * 75, 75, 75))

        # Create pieces
        for n in range(2):
            if n == 0:
                pawnRank = 6
                pieceRank = 7
            else:
                pawnRank = 1
                pieceRank = 0

            for i in range(8):
                self.positions[i][pawnRank] = Piece("pawn", n)
            self.positions[0][pieceRank] = Piece("rook", n)
            self.positions[1][pieceRank] = Piece("knight", n)
            self.positions[2][pieceRank] = Piece("bishop", n)
            self.positions[3][pieceRank] = Piece("queen", n)
            self.positions[4][pieceRank] = Piece("king", n)
            self.positions[5][pieceRank] = Piece("bishop", n)
            self.positions[6][pieceRank] = Piece("knight", n)
            self.positions[7][pieceRank] = Piece("rook", n)

    def get_pieces(self, team):
        pieces = [0] * 16
        for entry in range(16):
            for rank in range(8):
                for file in range(8):
                    piece = self.positions[rank][file]
                    if isinstance(piece, int):
                        continue
                    if piece.team != team:
                        continue
                    if piece in pieces:
                        continue
                    pieces[entry] = piece
        return pieces
