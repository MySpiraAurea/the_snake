"""the_snake
Модуль представляет собой реализацию игры The snake.
Предпологается, что этот модуль будет запускаться напрямую.
Основной цикл модуля реализован в функции main().

Классы:
GameObject - родительский для всех игровых объектов.
Snake - дочерний класс реализующий игровой объект змейка.
Apple - дочерний класс реализующий игровой объект яблоко.

Функции:
handle_keys - отслеживает действий пользователя.
Случайный выбор направления при новом старте в методе reset
класса Snake.
"""

from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Словарь для управления движением
MOVEMENT_KEYS = {
    (pygame.K_UP, LEFT): UP,
    (pygame.K_UP, RIGHT): UP,
    (pygame.K_DOWN, LEFT): DOWN,
    (pygame.K_DOWN, RIGHT): DOWN,
    (pygame.K_RIGHT, UP): RIGHT,
    (pygame.K_RIGHT, DOWN): RIGHT,
    (pygame.K_LEFT, UP): LEFT,
    (pygame.K_LEFT, DOWN): LEFT,
}


# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(snake):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            new_direction = MOVEMENT_KEYS.get(
                (event.key, snake.direction),
                snake.direction
            )
            TURN_KEYS = set(event_key for event_key, _ in MOVEMENT_KEYS)
            if event.key in TURN_KEYS:
                snake.direction = new_direction


class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self) -> None:
        self.position = SCREEN_CENTER
        self.body_color = None

    """Метод-заглушка отрисовки объекта.
    Конкретная реализация описывается в дочернем классе.
    """
    def draw(self):
        """Метод-заглушка отрисовки объекта.
        Конкретная реализация описывается в дочернем классе.
        """

    def draw_cell(self, position, color=None):
        """Метод отвечает за отрисовку одной клетки игрового поля"""
        position = position or self.position
        color = color or self.body_color
        rect = pygame.Rect(
            position,
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс игровых объектов Яблоко."""

    def __init__(self, ):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = SCREEN_CENTER

    def randomize_position(self, occupied_positions):
        """Метод задает случайное положение яблока на игровом поле."""
        while self.position in occupied_positions:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """
        Метод переопределяет функцию базового класса GameObject.
        Метод отвечает за отрисовку яблока на игровом поле.
        """
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс игровых объектов Змейка."""

    def __init__(self):
        super().__init__()
        self.reset()

    def update_direction(self, next_direction=None):
        """Метод переопределяет атрибут self.direction класса Snake."""
        self.direction = next_direction

    def move(self):
        """
        Метод отвечает за отображение движения объекта Snake по игровому полю.
        Добавляеткортеж с координатами новой клетки в начало списка.
        Удаляет кортеж с координатами последней клетки из списка.
        """
        x, y = self.get_head_position()
        current_x, current_y = self.direction
        new_head_position = (
            (x + current_x * GRID_SIZE) % SCREEN_WIDTH,
            (y + current_y * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        """Метод сбрасывает игру в изначальное состояние в случае поражения."""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None
        self.body_color = SNAKE_COLOR
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Метод отвечает за отрисовку объекта Snake на игровом поле."""
    # Отрисовка головы змейки
        self.draw_cell(self.get_head_position(), SNAKE_COLOR)

    # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Метод возвращает координату головы объекта Snake."""
        return self.positions[0]


def main():
    """Выполняется если the_snake запущен напрямую."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = Apple()
            apple.randomize_position(snake.positions)
        if snake.positions[0] in snake.positions[4:]:
            snake.reset()
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
