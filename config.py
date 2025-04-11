"""Конфигурация."""

import os
import sys
from pathlib import Path

import pygame

APP_NAME = "Знатоки ПДД 2025"

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "img"
FONT_DIR = ASSETS_DIR / "font"
RESULTS_FILE = BASE_DIR.parent / "результаты.xlsx"

# Шрифты
FONT_BOLD = FONT_DIR / "Roboto-Bold.ttf"
FONT_REGULAR = FONT_DIR / "Roboto-Regular.ttf"
FONT_MONO = FONT_DIR / "FiraMono-Bold.ttf"

# Базовые цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Цвета оформления
BG_COLOR = BLACK
BUTTON_TEXT_COLOR = BLACK
BUTTON_BG_COLOR = WHITE
TIMER_CRITICAL_COLOR = RED
TEXT_WIDGET_FONT_COLOR = WHITE
TIMER_COLOR = WHITE
TITLE_COLOR = WHITE

# Клавиши
QUIT_KEY = (pygame.K_q, pygame.KMOD_CTRL)
NEXT_SESSION_KEY = (pygame.K_n, pygame.KMOD_CTRL)

# Тексты
WELCOME_TEXT = "Знатоки ПДД 2025"
TIME_IS_UP_TEXT = "Время вышло!"
QUIZ_COMPLETED_TEXT = "Тест окончен. Большое спасибо за участие:)"
STUDENT_INSTRUCTION_TEXT_START = "Подождите, пока ведущий запишет участников команды и нажмите ENTER"
STUDENT_INSTRUCTION_TEXT_FINISH = "Дождитесь других участников вашей команды и идите к следующей станции."
HOST_INSTRUCTIONS_TEXT = [
    "Если до начала теста открыт файл результаты.xlsx, результат не сохранится",
    "Записывайте имя, фамилию и школу каждого участника в таблицу список.xlsx",
    "Укажите в начале списка номер компьютера",
    "Когда участник закончит тест, нажмите одновременно Ctrl и N",
    "Когда ВСЕ участники пройдут тест нажмите одновременно Ctrl и Q для выхода",
    "После выхода появится файл результаты.xlsx",
    "Добавьте в его имя результаты.xlsx номер компьютера, например, результаты_1.xlsx",
    "Добавьте в имя список.xlsx номер компьютера, например, список_1.xlsx",
    "У вас должны быть 2 файла для каждого компьютера: результаты_N.xlsx и список_N.xlsx",
    "Для выхода из программы в любой момент теста нажмите одновременно Ctrl и Q",
]

# Настройка сессии теста
TIME_MAX_SEC = 600.0  # 10 минут
PUNISH_FACTOR = 3  # множитель штрафных баллов
