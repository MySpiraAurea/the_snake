from typing import Optional
import pygame
from random import randint


pygame.init()
SNAKE_COLOR = (0, 255, 0)
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
MENU_WIDTH, MENU_HEIGHT = 200, 200
TITLE_MENU_WIDTH, TITLE_MENU_HEIGHT = MENU_WIDTH, 50
MENU_FONT_SIZE = 35
TITLE_FONT_SIZE = 60
MAIN_MENU_COLOR = (200, 200, 200)
MENU_BORDER_COLOR = (25, 25, 25)
MIDDLE_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
SLOW_SPEED = 10
KEY_ENTER = 13
NOISE_SIZE = 5
NOISE_STRENGTH = 4
BOARD_BACKGROUND_COLOR = (181, 130, 81)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
main_menu = pygame.Surface((MENU_WIDTH, MENU_HEIGHT))
main_menu_rect = main_menu.get_rect(center=MIDDLE_SCREEN)
title_menu = pygame.Surface((TITLE_MENU_WIDTH, TITLE_MENU_HEIGHT))
title_menu_rect = main_menu.get_rect(
    center=(SCREEN_WIDTH // 2, main_menu_rect.y + TITLE_MENU_HEIGHT)
)
background_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
"""Создаем объект текст."""
background_surface.fill(BOARD_BACKGROUND_COLOR)
screen.blit(background_surface, (0, 0))
menu_font = pygame.font.Font(None, MENU_FONT_SIZE)
title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
game_caption = pygame.display.set_caption
game_caption('Змейка')


class GameManager():
    """Класс для управления общей логикой игры."""

    def __init__(self) -> None:
        """Инициализирует экземпляр класса
        и базовые атрибуты.
        """
        self.reset: bool = False
        self.new_game: bool = True
        self.__game_is_run: bool = False
        self.__slow_count: int = 0
        self.__snake_length: int = 1
        self.__snake_speed: float = 0
        self.__start_time: Optional[float] = None
        self.__eaten_apples: int = 0
        self.__reset_count: int = 0
        self.__status_menu: bool = True
        self.__menu_value: int = 0
        self.__menu_sections: list = [
            'Новая игра',
            'Продолжить',
            'Рейтинги',
            'Выход'
        ]

    def is_run(self) -> bool:
        """Возвращяет {True} если игра включена и {False} если нет."""
        return self.__game_is_run

    def switch_on(self) -> None:
        """Переключатель игры в положение - включено."""
        self.__game_is_run = True

    def switch_off(self) -> None:
        """Переключатель игры в положение - выключено."""
        self.__game_is_run = False

    def menu_is_open(self) -> bool:
        """Отображает статус меню (активно / не активно)."""
        return self.__status_menu

    def close_menu(self) -> None:
        """Закрывает меню."""
        self.__status_menu = False

    def open_menu(self) -> None:
        """Открывает меню."""
        self.__status_menu = True

    def menu_up(self) -> None:
        """Передвижение по меню вверх."""
        self.__menu_value -= 1 if self.__menu_value > 0 else 0

    def menu_down(self) -> None:
        """Передвижение по меню вниз."""
        x = len(self.__menu_sections) - 1
        if self.__menu_value < x:
            self.__menu_value += 1
        else:
            self.__menu_value = x

    def menu_title(self) -> str:
        """Возвращает название выбранного пункта меню."""
        return self.__menu_sections[self.__menu_value]

    def get_menu_step(self) -> int:
        """Возвращает расстояние между пунктами меню исходя из размеров
        высоты меню, заданных константой {MENU_HEIGHT}, и их количества.
        """
        return (MENU_HEIGHT // (len(self.__menu_sections) + 1))

    def get_menu_list(self) -> list:
        """Возвращает списо из пунктов меню."""
        return self.__menu_sections

    def slow_mode(self, how_slow: int = SLOW_SPEED) -> bool:
        """Возвращает {False} пока действует замедление для выбранного
        блока кода, и {True} в момент когда код должен быть выполнен.
        Работает по принципу пропуска кадров, количество пропущенных
        кадров по умолчанию = {SLOW_SPEED}. Чем больше значение
        тем сильнее замедление.
        """
        self.__slow_count += 1
        if self.__slow_count > how_slow:
            self.__slow_count = 0

        return self.__slow_count == how_slow

    def update_snake_speed(self, end_time: float) -> None:
        """Обновляет скорость движения змейки."""
        if self.__start_time:
            self.__snake_speed = round(60 / (end_time - self.__start_time))

        self.__start_time = end_time

    def update_eaten_apples(self) -> None:
        """Обновляет количество съеденных яблок."""
        self.__eaten_apples += 1

    def update_count_of_resets(self) -> None:
        """Обновляет количество врезаний в препятствие."""
        self.__reset_count += 1

    def update_snake_length(self, length: int) -> None:
        """Обновляет значение длины зъмейки."""
        self.__snake_length = length

    def reset_info(self) -> None:
        """Сбрасывает информаци о текущей игре."""
        self.__snake_length = 1
        self.__eaten_apples = 0
        self.__reset_count = 0

    def info(self) -> str:
        """Выводит информацию об игре."""
        info = (
            f'Длина змейки: {self.__snake_length} || '
            f'Яблок съедено: {self.__eaten_apples} || '
            f'Врезаний: {self.__reset_count} || '
            f'Скорость {self.__snake_speed} клеток в минуту!'
        )
        return info

    def over(self) -> None:
        """Реализует логику при проигрыше"""
        pass


game = GameManager()


def handle_keys_menu() -> None:
    """Отслеживает нажатые клавиши для управления в меню."""
    keys = pygame.key.get_pressed()

    if keys[KEY_ENTER] and game.menu_title() == 'Новая игра':
        if game.new_game:
            game.new_game = False
        else:
            game.reset = True
        game.close_menu()
    elif (keys[KEY_ENTER] and game.menu_title() == 'Продолжить'
          and not game.new_game):
        game.close_menu()
    elif keys[KEY_ENTER] and game.menu_title() == 'Выход':
        game.switch_off()
        game.close_menu()

    if game.slow_mode(1):
        if keys[pygame.K_UP]:
            game.menu_up()
        elif keys[pygame.K_DOWN]:
            game.menu_down()


def quit_game() -> None:
    """Завершает игру."""
    pygame.quit()
    raise SystemExit


def quit_pressed() -> bool:
    """Реализует логику нажатия на клавишу ESCAPE."""
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            if game.new_game:
                game.switch_off()
            else:
                return True

    return False


def draw_menu():
    """Отрисовывает главное меню."""
    title_menu.fill('Black')
    text = title_font.render('Змейка', True, 'White')
    txt_x, txt_y = TITLE_MENU_WIDTH // 2, TITLE_MENU_HEIGHT // 2
    text_rect = text.get_rect(center=(txt_x, txt_y))
    title_menu.blit(text, text_rect)

    main_menu.fill(MAIN_MENU_COLOR)
    rect = (0, 0, MENU_WIDTH, MENU_HEIGHT)
    step = game.get_menu_step()

    pygame.draw.rect(main_menu, MENU_BORDER_COLOR, rect, 4)
    y_tmp = step

    for item in game.get_menu_list():
        if item == 'Продолжить' and game.new_game:
            text = menu_font.render(item, True, 'DarkGray')
        else:
            text = menu_font.render(item, True, 'Black')

        text_rect = text.get_rect(center=(MENU_WIDTH // 2, y_tmp))
        main_menu.blit(text, text_rect)

        if game.menu_title() == item:
            text_rect.inflate_ip(MENU_FONT_SIZE // 2, MENU_FONT_SIZE // 2)
            pygame.draw.rect(main_menu, SNAKE_COLOR, text_rect, 5)

        y_tmp += step

    screen.blit(main_menu, main_menu_rect)
    screen.blit(title_menu, title_menu_rect)


def draw_texture_on_background() -> None:
    """Рисует текстуру на поверхности."""
    color = BOARD_BACKGROUND_COLOR
    noise = NOISE_STRENGTH
    for pos_x in range(0, SCREEN_WIDTH, NOISE_SIZE):
        for pos_y in range(0, SCREEN_HEIGHT, NOISE_SIZE):
            pygame.draw.rect(
                background_surface,
                [randint(color[index] - noise, color[index] + noise)
                 for index in range(3)],
                (pos_x, pos_y, NOISE_SIZE, NOISE_SIZE)
            )
