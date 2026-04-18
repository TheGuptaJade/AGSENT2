import pygame

pygame.init()

screen = pygame.display.set_mode((1001, 640), pygame.RESIZABLE)
pygame.display.set_caption("Dynamic Layout")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK = (100, 100, 100)

running = True
while running:
    width, height = screen.get_size()
    print(width, height)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
