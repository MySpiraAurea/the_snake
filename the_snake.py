"""the_snake
Модуль представляет собой реализацию игры The snake.
Предпологается, что этот модуль будет запускаться напрямую.
Основной цикл модуля реализован в функции main().

Классы:
GameObject - родительский для всех игровых объектов.
Snake - дочерний класс реализующий игровой объект змейка.
Apple - дочерний класс реализующий игровой объект яблоко.
Stone - дочерний класс, реализующий игровой объект камень

Функции:
handle_keys - отслеживает действий пользователя.
Случайный выбор направления при новом старте в методе reset
класса Snake.
"""
import game
from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

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

STONE_COLOR = (128, 128, 128)

# Скорость движения змейки:
SPEED = 10


# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
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


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс игровых объектов."""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    """Метод-заглушка отрисовки объекта.
    Конкретная реализация описывается в дочернем классе.
    """
    def draw(self):
        """Метод-заглушка отрисовки объекта.
        Конкретная реализация описывается в дочернем классе.
        """
        pass


class Apple(GameObject):
    """Класс игровых объектов Яблоко."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = Apple.randomize_position(self)

    def randomize_position(self):
        """Метод задает случайное положение яблока на игровом поле."""
        position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        return position

    def draw(self):
        """
        Метод переопределяет функцию базового класса GameObject.
        Метод отвечает за отрисовку яблока на игровом поле.
        """
        pygame.draw.circle(
            screen,
            self.body_color,
            (
                self.position[0] + 10,
                self.position[1] + 10
            ),
            GRID_SIZE // 2 - 1,
            10
        )


class Snake(GameObject):
    """Класс игровых объектов Змейка."""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.body_color = SNAKE_COLOR

    def update_direction(self):
        """Метод переопределяет атрибут self.direction класса Snake."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Метод отвечает за отображение движения объекта Snake по игровому полю.
        Добавляеткортеж с координатами новой клетки в начало списка.
        Удаляет кортеж с координатами последней клетки из списка.
        """
        head_position = self.get_head_position()
        new_head_position = (
            (head_position[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head_position[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        while len(self.positions) > (self.length):
            self.last = self.positions.pop()

    def reset(self):
        """Метод сбрасывает игру в изначальное состояние в случае поражения."""
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Метод отвечает за отрисовку объекта Snake на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
        if self.last:
            color = game.BOARD_BACKGROUND_COLOR
            noise = game.NOISE_STRENGTH
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(
                screen,
                [randint(color[index] - noise, color[index] + noise)
                    for index in range(3)],
                last_rect
            )

    def get_head_position(self):
        """Метод возвращает координату головы объекта Snake."""
        return self.positions[0]


class Stone(Apple):
    """Класс игровых объектов камень"""

    def __init__(self):
        super().__init__()
        self.body_color = STONE_COLOR
        self.positions = [self.randomize_position()]

    def draw(self):
        """
        Метод переопределяет функцию базового класса GameObject.
        Метод отвечает за отрисовку яблока на игровом поле.
        """
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def add_stone(self):
        """Метод добавляет камень на игровое поле"""
        new_stone_position = self.randomize_position()
        self.positions.append(new_stone_position)
#        self.positions.append(self.randomize_position())

    def reset(self):
        """Метод сбрасывает игру в изначальное состояние в случае поражения."""
        self.positions.clear()
        self.positions.append(self.randomize_position())


def main():
    """Выполняется если the_snake запущен напрямую."""
    # Инициализация PyGame:
#    pygame.init()
    game.draw_texture_on_background()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    stone = Stone()
    game.game.switch_on()

    while game.game.is_run():
        screen.blit(game.background_surface, (0, 0))
        apple.draw()
        snake.draw()
        stone.draw()
        handle_keys(snake)
        if game.game.menu_is_open():
            game.game_caption('Змейка || Основное меню')
            if game.quit_pressed():
                game.game.close_menu()

            game.draw_menu()
            game.handle_keys_menu()
            if game.game.reset:
                snake.reset()
                stone.reset()
                game.reset = False
        else:
            if game.quit_pressed():
                game.game.open_menu()
            snake.update_direction()
            snake.move()
            if snake.positions[0] == apple.position:
                snake.length += 1
                while apple.position in snake.positions:
                    apple.position = Apple.randomize_position(apple)
                while apple.position in stone.positions:
                    apple.position = Apple.randomize_position(apple)
                apple.draw()
                stone.add_stone()
                while stone.positions[-1] in snake.positions:
                    stone.positions[-1] = Stone.randomize_position(apple)
                while stone.positions[-1] == apple.position:
                    stone.positions[-1] = Stone.randomize_position(apple)
                stone.draw()
            if snake.positions[0] in snake.positions[1:]:
                snake.reset()
                stone.reset()
            if snake.positions[0] in stone.positions:
                snake.reset()
                stone.reset()
        clock.tick(SPEED)
        pygame.display.update()        # Тут опишите основную логику игры.
        # ...
    game.quit_game()

 
if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#           elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#           elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
