import pygame
import matplotlib.pyplot as plt

pygame.init()

screen = pygame.display.set_mode((1000, 640), pygame.RESIZABLE)
pygame.display.set_caption("Dynamic Layout")

WHITE = (238, 238, 238)
BLACK = (34, 40, 49)
GRAY = (237, 233, 230)
DARK = (57, 62, 70)

values = [30, 20, 50]
labels = ["A", "B", "C"]

plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.savefig("chart.png")
plt.close()


def layout(width, heigth):
    top_bar_height = int(height * 0.15) # this is to make the GUI dynamic, to ensure that the solution works on every device
    side_bar_width = int(width * 0.25)
    top_bar = pygame.Rect(0, 0, width, top_bar_height)
    side_bar = pygame.Rect(width-side_bar_width, top_bar_height, side_bar_width, height - top_bar_height)


    return top_bar, side_bar

running = True
chart_img = pygame.image.load("chart.png").convert_alpha()
while running:
    width = screen.get_size()[0]
    height = screen.get_size()[1]
    print(width, height)
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    top_bar = layout(width, height)[0]
    side_bar = layout(width, height)[1]
    pygame.draw.rect(screen, BLACK, top_bar)
    pygame.draw.rect(screen, GRAY, side_bar)

    img_w, img_h = chart_img.get_size()


    max_w = side_bar.width
    max_h = side_bar.height 

    scale = min(max_w / img_w, max_h / img_h)
    new_w = int(img_w * scale)
    print(new_w)
    new_h = int(img_h * scale)
    
    chart_scaled = pygame.transform.smoothscale(chart_img, (new_w, new_h))
    x = side_bar.x + (side_bar.width - new_w) // 2
    y = side_bar.y + (side_bar.height - new_h) // 2

    screen.blit(chart_scaled, (x, y))


    pygame.display.flip()
