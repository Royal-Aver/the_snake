"""Модуль игра Змейка."""

from random import choice, randint
import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption(
    'Змейка.'
    ' Для выхода нажмите клавишу ESC')

clock = pygame.time.Clock()


class GameObject():
    """Родительский класс для всех объектов на игровом поле."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Иницилизатор класса GameObject."""
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, описывающий яблоко и действия с ним."""

    def __init__(self, occupied_cells=None):
        """Иницилизатор класса Apple."""
        super().__init__(body_color=APPLE_COLOR)
        if occupied_cells is None:
            occupied_cells = []
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells):
        """Устанавливает случайное положение яблока на игровом поле."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_cells:
                break

    def draw(self):
        """Метод draw класса Apple."""
        super().draw()


class Snake(GameObject):
    """Класс, описывающий змейку и действия с ней."""

    def __init__(self):
        """Иницилизатор класса Snake."""
        super().__init__()
        self.reset()
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки."""
        head_x, head_y = self.get_head_position()
        x, y = self.direction
        new_head = ((
            head_x + x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + y * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, new_head)

        self.last = self.positions[-1]

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Отрисовка змейки."""
        head_rect = pygame.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Позиция головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))


def handle_keys(game_object):
    """Обработка нажатий клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE):
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция."""
    pygame.init()

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        handle_keys(snake)
        clock.tick(SPEED)

        if apple.position in snake.positions:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill((BOARD_BACKGROUND_COLOR))
            apple.randomize_position(snake.positions)

        snake.move()
        snake.update_direction()

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
