import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 600, 600

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("PyChess")

        self.FPS = 60
        self.clock = pygame.time.Clock()

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
        for column in range(8):
            for row in range(8):
                tileColour = (207, 181, 135)
                if (column + row) % 2:
                    tileColour = (130, 89, 53)
                pygame.draw.rect(
                    self.screen,
                    tileColour,
                    pygame.Rect(75 * row, 75 * column, 75, 75),
                )

        pygame.display.update()


def main():
    game = Game()
    print("Game Over!")


if __name__ == "__main__":
    main()
