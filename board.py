import pygame
import boardhelper
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

    # Get every possible move for the piece, excluding special cases like castling or en passant
    def get_moves(self, piece, position):
        moveset = []
        if piece.type == "rook" or piece.type == "queen":
            moveset.extend(self.handle_sliding_moves("rook", piece.team, position))
        # Not using elif so queen can use moves of both rook and bishop
        if piece.type == "bishop" or piece.type == "queen":
            moveset.extend(self.handle_sliding_moves("bishop", piece.team, position))
        elif piece.type == "pawn":
            for move in range(7, 10):
                offset = move
                if piece.team == 1:
                    offset = offset * -1
                if isinstance(self.positions[position + offset], Piece):
                    if move == 8:
                        continue
                    elif self.positions[position + offset].team != piece.team:
                        moveset.append(move)
                if move == 8:
                    moveset.append(move)
            if piece.team == 1:
                moveset = [n * -1 for n in moveset]
        elif piece.type == "knight":
            for move in [-10, -17, -6, -15, 6, 15, 10, 17]:
                current_file = boardhelper.get_index_file(position)
                target_file = boardhelper.get_index_file(position + move)
                difference = target_file - current_file
                if difference in [1, 2, -1, -2]:
                    moveset.append(move)
        elif piece.type == "king":
            moveset.extend([1, -1, 8, -8, 7, 9, -7, -9])

        moves = []
        for move in moveset:
            target = position + move
            if target < 0 or target > 63:
                continue
            target = self.positions[target]
            if isinstance(target, Piece):
                if target.team == piece.team:
                    continue
            moves.append(move)
        return moves

    def handle_sliding_moves(self, piece, team, position):
        moves = []
        if piece == "rook":
            moveOffset = [1, -1, 8, -8]
        elif piece == "bishop":
            moveOffset = [7, 9, -7, -9]

        blockedDirs = []
        for count in range(1, 8):
            for dir in range(4):
                if dir in blockedDirs:
                    continue
                move = moveOffset[dir] * count
                target = position + move
                if target < 0 or target > 63:
                    blockedDirs.append(dir)
                    continue

                # Handle cases where piece jumps across screen
                currentRank = boardhelper.get_index_rank(position)
                targetRank = boardhelper.get_index_rank(target)
                if piece == "rook" and dir < 2 and currentRank != targetRank:
                    blockedDirs.append(dir)
                    continue
                if piece == "bishop" and dir < 2 and currentRank + count != targetRank:
                    blockedDirs.append(dir)
                    continue
                elif (
                    piece == "bishop" and dir > 1 and currentRank - count != targetRank
                ):
                    blockedDirs.append(dir)
                    continue

                if isinstance(self.positions[target], Piece):
                    if self.positions[target].team != team:
                        moves.append(move)
                    blockedDirs.append(dir)
                    continue
                moves.append(move)
        return moves

    def handle_move(self, piece, new_pos):
        old_pos = piece.isMoving
        piece.isMoving = False
        moveOffset = new_pos - old_pos
        if not moveOffset in piece.moves:
            return False

        self.positions[old_pos] = 0
        self.positions[new_pos] = piece
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
