import pygame
from board import Board
from board import Piece


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 600, 600

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("PyChess")

        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.board = Board()

        self.pieces = [self.board.get_pieces(0), self.board.get_pieces(1)]
        self.mainloop()

    def mainloop(self):
        self.running = True
        self.movingPiece = False

        self.move = 0
        while self.running:
            self.curPlayer = self.move % 2
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouseclick(event)

            self.draw_display()
            self.clock.tick(self.FPS)

        pygame.quit()

    def draw_display(self):
        # Draw grid
        for rank in range(8):
            for file in range(8):
                tileColour = (207, 181, 135)
                if (rank + file) % 2:
                    tileColour = (130, 89, 53)
                pygame.draw.rect(
                    self.screen,
                    tileColour,
                    self.board.tiles[file][rank],
                )

        # Draw pieces
        isMoving = False
        for rank in range(8):
            for file in range(8):
                piece = self.board.positions[file][rank]
                if isinstance(piece, int):
                    continue
                pos = (file * 75, rank * 75)
                if piece.isMoving != False:
                    mouse_X, mouse_Y = pygame.mouse.get_pos()
                    pos = (mouse_X - 37.5, mouse_Y - 37.5)
                    isMoving = [piece.image, pos]
                    continue
                self.screen.blit(piece.image, pos)
        if isMoving != False:
            self.screen.blit(isMoving[0], isMoving[1])

        pygame.display.update()

    def handle_mouseclick(self, event):
        if event.button != 1:
            return
        for file in range(8):
            for rank in range(8):
                tile = self.board.tiles[file][rank]
                if not tile.collidepoint(event.pos):
                    continue
                if self.movingPiece:
                    for piece in self.pieces[self.curPlayer]:
                        if piece.isMoving != False:
                            break
                    oldFile, oldRank = piece.isMoving[0], piece.isMoving[1]
                    self.board.positions[oldFile][oldRank] = 0
                    self.board.positions[file][rank] = piece
                    piece.isMoving = False
                    self.movingPiece = False
                    self.move += 1
                    return
                piece = self.board.positions[file][rank]
                if isinstance(piece, int):
                    continue
                if piece.team != self.curPlayer:
                    continue
                piece.isMoving = [file, rank]
                self.movingPiece = True


def main():
    game = Game()
    print("Game Over!")


if __name__ == "__main__":
    main()
