import pygame
from piece import Piece
from math import ceil


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

    def handle_move(self, piece, new_pos):
        old_pos = piece.isMoving
        piece.isMoving = False
        moveOffset = new_pos - old_pos
        moveset = piece.get_moveset()
        if not moveOffset in moveset:
            return False
        if len(moveset) > 8:
            if piece.type == "rook" or piece.type == "bishop":
                if not self.handle_sliding_moves(
                    piece.type, piece.team, old_pos, new_pos
                ):
                    return False
            elif piece.type == "queen":
                movesets = ["rook", "bishop"]
                for move in range(2):
                    print(move)
                    if not self.handle_sliding_moves(
                        movesets[move], piece.team, old_pos, new_pos
                    ):
                        return False
        # elif isinstance(self.positions[new_pos], Piece):
        #     if self.positions[new_pos].team == piece.team:
        #         return False
        self.positions[old_pos] = 0
        self.positions[new_pos] = piece
        return True

    def handle_sliding_moves(self, piece, team, old_pos, new_pos):
        moveset = []
        if piece == "rook":
            moveOffset = [1, -1, 8, -8]
        elif piece == "bishop":
            moveOffset = [7, 9, -7, -9]
        elif piece == "queen":
            print("cba to continue with this method")
        blockedDirs = []
        for count in range(1, 8):
            for dir in range(4):
                if dir in blockedDirs:
                    continue
                move = moveOffset[dir] * count
                target = old_pos + move
                if target < 0 or target > 63:
                    blockedDirs.append(dir)
                    continue

                # Handle cases where piece jumps across screen
                currentRank = ceil((old_pos + 1) / 8)
                targetRank = ceil((target + 1) / 8)
                if piece == "rook" and dir < 2 and currentRank != targetRank:
                    blockedDirs.append(dir)
                    continue

                if piece == "bishop" and dir < 2 and currentRank + count != targetRank:
                    print(count, currentRank + count, targetRank)
                    blockedDirs.append(dir)
                    continue
                elif (
                    piece == "bishop" and dir > 1 and currentRank - count != targetRank
                ):
                    print(count, currentRank + count, targetRank)
                    blockedDirs.append(dir)
                    continue
                # print(move)
                if isinstance(self.positions[target], Piece):
                    if self.positions[target].team != team:
                        moveset.append(move)
                    blockedDirs.append(dir)
                    continue
                moveset.append(move)
        print(moveset)
        if not (new_pos - old_pos) in moveset:
            return False
        return True

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
