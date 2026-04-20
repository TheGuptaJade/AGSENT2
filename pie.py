import pygame
import math
import matplotlib.pyplot as plt
values = [30, 20, 50]
labels = ["A", "B", "C"]

plt.pie(values, labels=labels, autopct='%1.1f%%')
plt.savefig("chart.png")
plt.close()

pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

# Data
values = [30, 20, 50]
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

total = sum(values)
center = (300, 300)
radius = 150

def draw_pie(surface, values, colors, center, radius):
    start_angle = 0

    for i, value in enumerate(values):
        proportion = value / total
        end_angle = start_angle + proportion * 2 * math.pi

        points = [center]

        # create arc points
        steps = 50  # higher = smoother
        for step in range(steps + 1):
            angle = start_angle + (end_angle - start_angle) * step / steps
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            points.append((x, y))

        pygame.draw.polygon(surface, colors[i], points)

        start_angle = end_angle

running = True
while running:
    screen.fill((255, 255, 255))

    draw_pie(screen, values, colors, center, radius)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()