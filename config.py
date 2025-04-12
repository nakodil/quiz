"""Конфигурация."""

from pathlib import Path

import pygame

APP_NAME = "Знатоки ПДД 2025"

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"
FONT_DIR = ASSETS_DIR / "font"
RESULTS_FILE = BASE_DIR.parent / "результаты.xlsx"
BG_IMAGE = IMG_DIR / "bg.jpg"

# Настройка сессии теста
TIME_MAX_SEC = 600.0  # 10 минут
PUNISH_FACTOR = 3  # множитель штрафных баллов

# Шрифты
FONT_BOLD = FONT_DIR / "Roboto-Bold.ttf"
FONT_REGULAR = FONT_DIR / "Roboto-Regular.ttf"
FONT_MONO = FONT_DIR / "FiraMono-Bold.ttf"

# Базовые цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Цвета оформления
ERROR_COLOR = RED
BG_COLOR = BLACK
BUTTON_TEXT_COLOR = BLACK
BUTTON_BG_COLOR = WHITE
TIMER_CRITICAL_COLOR = RED
TEXT_WIDGET_FONT_COLOR = WHITE
TIMER_COLOR = WHITE
TITLE_COLOR = WHITE
TEXT_COLOR = WHITE

# Клавиши
QUIT_KEY = (pygame.K_q, pygame.KMOD_CTRL)
NEXT_SESSION_KEY = (pygame.K_n, pygame.KMOD_CTRL)

# Тексты
EXIT_INSTRUCTION_TEXT = "Нажите Ctrl + Q чтобы выйти из программы."
RESULTS_UNWRITABLE_ERROR = "Открыт файл результаты.xlsx. Выйдите из программы, закройте этот файл и запустите программу заново."
WELCOME_TEXT = "Знатоки ПДД 2025"
TIME_IS_UP_TEXT = "Время вышло!"
QUIZ_COMPLETED_TEXT = "Большое спасибо за участие:)"
STUDENT_INSTRUCTION_TEXT_START = f"Дождитесь команды ведущего и нажмите кнопку «Начать тест‎». У вас будет {round(TIME_MAX_SEC // 60)} минут. Удачи;)‎"
STUDENT_INSTRUCTION_TEXT_FINISH = "Дождитесь других участников вашей команды и идите к следующей станции."
HOST_INSTRUCTIONS_TEXT = [
    "Скопируйте файл список.xlsx на компьютер ведущего",
    "Записывайте в список.xlsx школу команды и ее состав: имя и фамилию каждого участника",
    "Когда команда закончит тест, нажмите одновременно Ctrl и N на компьютере каждого участника",
    "Когда ВСЕ команды пройдут тест, нажмите одновременно Ctrl и Q для выхода",
    "После выхода появится файл результаты.xlsx",
    "Добавьте в имя файла результаты.xlsx номер компьютера, например, результаты_1.xlsx",
    "Для выхода из программы в любой момент теста нажмите одновременно Ctrl и Q",
]
