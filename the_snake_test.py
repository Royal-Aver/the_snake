import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption('Змейка')


class Snake:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.direction = 'right'

    def move(self):
        if self.direction == 'right':
            self.x += 1
        elif self.direction == 'left':
            self.x -= 1
        elif self.direction == 'up':
            self.y -= 1
        elif self.direction == 'down':
            self.y += 1

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.x * 20, self.y * 20, 20, 20))


snake = Snake()


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    snake.draw(screen)
    snake.move()
    pygame.display.update()

pygame.quit()