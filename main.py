import pygame
import boardhelper
from board import Board
from os import path


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 600, 600
        self.colourWHite = "0,0,0"

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("PyChess")

        self.FPS = 240
        self.clock = pygame.time.Clock()

        self.board = Board()
        self.Text = boardhelper.Text()
        self.images = self.load_images()
        self.isPromoting = False

        self.mainloop()

    def mainloop(self):
        self.running = True
        self.attemptingMove = False

        self.move = 0
        while self.running == True:
            self.curPlayer = self.move % 2
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                # If pawn is on final rank, only allow keyboard input for the promotion
                if not isinstance(self.isPromoting, bool):
                    if event.type == pygame.KEYDOWN:
                        self.handle_keyboard(event)
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_mouseclick(event)
            self.draw_display()
            self.clock.tick(self.FPS)
            # break
        # Game over

        # print(self.running)   
        # while True:
        #     self.draw_display()
        # pygame.quit()

    def draw_display(self):
        # Draw grid
        for rank in range(8):
            for file in range(8):
                tileColour = (130, 89, 53)
                if (rank + file) % 2:
                    tileColour = (207, 181, 135)
                tileIndex = boardhelper.get_index(rank, file)
                pygame.draw.rect(
                    self.screen, tileColour, self.board.newTiles[tileIndex]
                )
                # Show seen squares
                # if tileIndex in self.board.seenSquares:
                #     pygame.draw.rect(
                #         self.screen,
                #         (255, 0, 0),
                #         pygame.Rect(
                #             (file) * 75,
                #             (7 - rank) * 75,
                #             75,
                #             75,
                #         ),
                #     )

                # Show tile indexes
                x, y = (file) * 75, (7 - rank) * 75
                y += 75 - 15
                self.Text.draw(self.screen, str(tileIndex), x, y)

        # Draw pieces
        isMoving = False
        for rank in range(8):
            for file in range(8):
                index = boardhelper.get_index(rank, file)

                piece = self.board.positions[index]
                if isinstance(piece, int):
                    continue
                pos = (file * 75, (7 - rank) * 75)
                if piece.isMoving:
                    mouse_X, mouse_Y = pygame.mouse.get_pos()
                    pos = (mouse_X - 37.5, mouse_Y - 37.5)
                    isMoving = [piece, pos]
                    continue
                self.screen.blit(piece.image, pos)

        # Draw tiles in moveset
        if isMoving != False:
            piece, pos = isMoving[0], isMoving[1]
            for move in piece.moves:
                target = piece.pos + move
                targetRank = 8 - boardhelper.get_index_rank(target)
                targetFile = boardhelper.get_index_file(target) - 1
                self.screen.blit(
                    self.images["move_indicator"],
                    (targetFile * 75, targetRank * 75),
                )
            # Draw moving piece last (on top of board)
            self.screen.blit(piece.image, pos)
        pygame.display.update()

    def handle_mouseclick(self, event):
        if event.button != 1:
            return

        for var in range(64):
            tile = self.board.newTiles[var]
            if not tile.collidepoint(event.pos):
                continue
            if self.attemptingMove:
                for piece in self.board.pieces[self.curPlayer]:
                    if piece.isMoving:
                        break
                if self.board.handle_move(piece, var):
                    if piece.type == "pawn" and boardhelper.get_index_rank(var) == 8:
                        self.isPromoting = piece
                    else:
                        self.handle_move()
                self.attemptingMove = False
                return
            piece = self.board.positions[var]
            if isinstance(piece, int):
                continue
            if piece.team != self.curPlayer:
                continue
            piece.moves = self.board.get_moves(piece)
            piece.isMoving = True
            self.attemptingMove = True
            return

    def handle_keyboard(self, event):
        if isinstance(self.isPromoting, bool):
            return

        pieces = {
            pygame.K_q: "queen",
            pygame.K_r: "rook",
            pygame.K_b: "bishop",
            pygame.K_k: "knight",
        }

        self.isPromoting.promote(pieces[event.key])

        self.isPromoting = False
        self.handle_move()

    def handle_move(self):
        self.move += 1
        self.board.update_seen_squares(self.curPlayer)
        if self.board.is_check(self.curPlayer ^ 1):
            if self.is_checkmate(self.curPlayer ^ 1):
                self.running = "Checkmate"
        self.board.update_pawns(self.curPlayer ^ 1)

    def is_checkmate(self, team):
        moves = []
        for piece in self.board.pieces[team]:
            moves.extend(self.board.get_moves(piece))
        if len(moves) == 0:
            return True
        return False

    def load_images(self):
        images = {
            "move_indicator": pygame.image.load(
                path.abspath(path.join(".", "images", "move_indicator.png"))
            )
        }

        for image in images:
            transformed = pygame.transform.scale(images[image], (75, 75))
            images[image] = transformed

        return images


def main():
    game = Game()
    print("Game Over!")


if __name__ == "__main__":
    main()
