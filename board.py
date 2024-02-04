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
        self.pieces = [[], []]
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

            offset = team * 48
            for piece in range(16):
                self.pieces[team].append(self.positions[piece + offset])

        for n in range(2):
            pieces = []
            for piece in self.pieces[n]:
                pieces.append(piece.type)
            print(pieces)
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
        if not moveOffset in piece.moves:
            return False
        if isinstance(self.positions[new_pos], Piece):
            self.pieces[piece.team ^ 1].remove(self.positions[new_pos])
        elif piece.type == "pawn" and moveOffset in [7, -7, 9, -9]:
            if piece.team == 0:
                offset = moveOffset - 8
            else:
                offset = moveOffset + 8
            self.pieces[piece.team ^ 1].remove(self.positions[old_pos + offset])
            self.positions[old_pos + offset] = 0
        piece.moveCount += 1

        self.positions[old_pos] = 0
        self.positions[new_pos] = piece

        # Handle Castling
        if piece.type == "king":
            if new_pos == 2 or new_pos == 58:
                teamOffset = new_pos - 2
                rookOffset = 3
            elif new_pos == 6 or new_pos == 62 and piece.type == "king":
                teamOffset = new_pos + 1
                rookOffset = -2
            else:
                return True
            rook = self.positions[teamOffset]
            rook.moveCount += 1
            self.positions[teamOffset] = 0
            self.positions[teamOffset + rookOffset] = rook

        if piece.type == "pawn" and moveOffset in [16, -16]:
            piece.doublePush = True
        return True

    def get_moves(self, piece, position):
        moveset = []
        if piece.type == "rook" or piece.type == "queen":
            moveset.extend(self.get_sliding_moves("rook", piece.team, position))
        # Not using elif so queen can use moves of both rook and bishop
        if piece.type == "bishop" or piece.type == "queen":
            moveset.extend(self.get_sliding_moves("bishop", piece.team, position))
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

            if piece.moveCount == 0:
                moveset.append(16)
            if piece.team == 1:
                moveset = [n * -1 for n in moveset]

            moveset.extend(self.can_en_passant(position, piece.team))

        elif piece.type == "knight":
            for move in [-10, -17, -6, -15, 6, 15, 10, 17]:
                # Handle cases where piece jumps across screen
                current_file = boardhelper.get_index_file(position)
                target_file = boardhelper.get_index_file(position + move)
                difference = target_file - current_file
                if difference in [1, 2, -1, -2]:
                    moveset.append(move)
        elif piece.type == "king":
            moveset.extend([1, -1, 8, -8, 7, 9, -7, -9])
            canCastle = self.can_castle(piece.team)
            if canCastle != False:
                moveset.extend(canCastle)

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

    def get_sliding_moves(self, piece, team, position):
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

    def can_en_passant(self, position, team):
        moves = []
        for move in range(7, 10, 2):
            target_position = position + move if team == 0 else position - move
            if isinstance(self.positions[target_position], Piece):
                continue
            offset = move - 8
            if team == 1:
                offset = offset * -1
            if isinstance(self.positions[position + offset], int):
                continue
            possiblePawn = self.positions[position + offset]
            if possiblePawn.team == team:
                continue
            if possiblePawn.type == "pawn" and possiblePawn.doublePush == True:
                moves.append(move)
        if team == 1:
            moves = [-item for item in moves]
        return moves

    def can_castle(self, team):
        kingSquare = 4 + (team * 56)
        if isinstance(self.positions[kingSquare], int):
            return False
        if self.positions[kingSquare].moveCount != 0:
            return False

        moves = []
        for side in range(2):
            rookSquare = (7 * side) + (team * 56)
            if isinstance(self.positions[rookSquare], int):
                continue
            piece = self.positions[rookSquare]
            if piece.type != "rook":
                continue
            if piece.moveCount != 0:
                continue
            clear = 0
            for move in range(1, 4 - side):
                position = rookSquare + move
                if side == 1:
                    position = rookSquare - move
                if isinstance(self.positions[position], Piece):
                    break
                clear += 1
            if clear == 3 - side:
                if side == 0:
                    moves.append(-2)
                else:
                    moves.append(2)

        return moves

    # Updates pawns to prevent en passant
    def update_pawns(self, team):
        for piece in self.pieces[team]:
            if piece.type != "pawn":
                continue
            if piece.moveCount > 1:
                continue
            if piece.doublePush == True:
                piece.doublePush = False
