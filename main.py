import pygame
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
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

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
                if type(self.board.positions[file][rank]) == int:
                    continue
                self.screen.blit(
                    self.board.positions[file][rank].image, (file * 75, rank * 75)
                )

        pygame.display.update()


def main():
    game = Game()
    print("Game Over!")


if __name__ == "__main__":
    main()
