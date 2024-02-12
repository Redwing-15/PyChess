import pygame


def get_index_rank(index):
    return (index // 8) + 1


def get_index_file(index):
    return (index % 8) + 1


def get_index(rank, file):
    return (rank * 8) + file


class Text:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, surface, text, x, y):
        img = self.font.render(text, True, (0, 0, 0))
        surface.blit(img, (x, y))
