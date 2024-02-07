import pygame
import boardhelper
from board import Board


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 600, 600

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("PyChess")

        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.board = Board()

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouseclick(event)
            self.draw_display()
            self.clock.tick(self.FPS)
        pygame.quit()

    def draw_display(self):
        # Draw grid
        for rank in range(8):
            for file in range(8):
                tileColour = (130, 89, 53)
                if (rank + file) % 2:
                    tileColour = (207, 181, 135)
                tileIndex = (rank * 8) + file
                pygame.draw.rect(
                    self.screen, tileColour, self.board.newTiles[tileIndex]
                )

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
                    isMoving = [piece.image, pos]
                    continue
                self.screen.blit(piece.image, pos)

        if isMoving != False:
            self.screen.blit(isMoving[0], isMoving[1])

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
                    self.move += 1
                    if self.is_checkmate(self.curPlayer ^ 1):
                        self.running = "Checkmate"
                    self.board.update_pawns(self.curPlayer ^ 1)
                self.attemptingMove = False
                return
            piece = self.board.positions[var]
            if isinstance(piece, int):
                continue
            if piece.team != self.curPlayer:
                continue
            # Get all possible moves, then remove any if they lead to king capture next move
            piece.moves = self.board.get_moves(piece, var)
            piece.isMoving = True
            self.attemptingMove = True
            return

    def is_checkmate(self, team):
        moves = []
        for piece in self.board.pieces[team]:
            moves.extend(self.board.get_moves(piece, piece.pos))
        if len(moves) == 0:
            return True
        return False


def main():
    game = Game()
    print(game.running)
    print("Game Over!")


if __name__ == "__main__":
    main()
