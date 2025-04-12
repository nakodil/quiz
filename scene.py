"""Модуль сцены."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame

import config
from test_session import Test
from widgets import Button, Image, TextWidget, Timer

if TYPE_CHECKING:
    from main import App

TIMER_EVENT = pygame.USEREVENT + 1


class Scene(ABC):
    """Базовая сцена."""

    @abstractmethod
    def __init__(self, app: App) -> None:
        """Конструктор класса."""
        self.app = app
        self.screen = app.screen
        self.sprites = pygame.sprite.Group()
        self.width = self.app.screen_w
        self.height = self.app.screen_h
        self.font_size = app.font_size

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Сбор событий, клавиши."""
        for event in events:
            if event.type == pygame.QUIT:
                self.app.is_run = False
            if event.type == pygame.KEYDOWN:
                key, mod = config.QUIT_KEY
                if event.key == key and (event.mod & mod):
                    self.app.is_run = False

    def render(self) -> None:
        """Отрисовка."""
        self.sprites.draw(self.screen)
        pygame.display.flip()

    def update(self) -> None:
        """Обновление спрайтов."""
        self.sprites.update()


class ErrorScene(Scene):
    """Сцена ошибки."""

    def __init__(self, app: App, text: str) -> None:
        """Конструктор класса сцены ошибки."""
        super().__init__(app)
        title = "Ошибка!"
        TextWidget(
            self.sprites,
            (self.width // 2, self.height // 10),
            int(self.font_size * 1.5),
            config.FONT_BOLD,
            config.ERROR_COLOR,
            text=title,
        )

        TextWidget(
            self.sprites,
            (self.width // 2, self.height // 2),
            int(self.font_size),
            config.FONT_REGULAR,
            config.TEXT_COLOR,
            text=text,
        )

        position_y = self.height // 2 + self.font_size * 2

        TextWidget(
            self.sprites,
            (self.width // 2, position_y),
            int(self.font_size),
            config.FONT_REGULAR,
            config.TEXT_COLOR,
            text=config.EXIT_INSTRUCTION_TEXT,
        )


class InstructionsScene(Scene):
    """Инструкции для ведущего - показывается один раз при запуске программы."""

    def __init__(self, app: App) -> None:
        """Конструктор класса сцены инструкций для ведущего."""
        super().__init__(app)

        # Отступ от верхней границы экрана
        position_y = self.height // 10

        # Заголовок
        title = "Памятка ведущему"
        TextWidget(
            self.sprites,
            (self.width // 2, position_y),
            int(self.font_size * 1.5),
            config.FONT_BOLD,
            config.TITLE_COLOR,
            text=title,
        )
        position_y += self.font_size * 3

        # Текст инструкции для ведущего
        for num, text in enumerate(config.HOST_INSTRUCTIONS_TEXT, 1):
            text_line = f"{num}. {text}."
            self.text = TextWidget(
                self.sprites,
                (self.width // 2, position_y),
                self.font_size,
                config.FONT_BOLD,
                config.TEXT_COLOR,
                text=text_line,
            )
            position_y += self.font_size * 2

        # Клавиша для продолжения
        position_y = int(self.height * 0.9)
        title = "Нажмите ENTER"
        self.text = TextWidget(
            self.sprites,
            (self.width // 2, position_y),
            int(self.font_size * 1.5),
            config.FONT_BOLD,
            config.TITLE_COLOR,
            text=title,
        )

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Сбор событий сцены."""
        super().handle_events(events)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.app.scene = SplashScene(self.app)


class SplashScene(Scene):
    """Инструкции для тестируемого - показывается до каждой тестовой сессии."""

    def __init__(self, app: App) -> None:
        """Конструктор класса."""
        super().__init__(app)

        # Заголовок
        TextWidget(
            self.sprites,
            (self.width // 2, self.height // 2),
            self.font_size * 2,
            config.FONT_BOLD,
            config.TITLE_COLOR,
            text=config.WELCOME_TEXT,
        )

        # Текст
        TextWidget(
            self.sprites,
            (self.width // 2, self.height // 2 + self.font_size * 3),
            self.font_size,
            config.FONT_REGULAR,
            config.TEXT_WIDGET_FONT_COLOR,
            text=config.STUDENT_INSTRUCTION_TEXT_START,
        )

        # Кнопка старта тестовой сессии
        Button(
            self.sprites,
            (self.width // 2, int(self.height * 0.9)),
            self.font_size,
            None,
            self.width // 3,
            text="Начать тест",
        )

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Сбор событий сцены."""
        super().handle_events(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for sprite in self.sprites:
                    if isinstance(sprite, Button):
                        self.app.scene = TestScene(self.app)


class TestEndScene(Scene):
    """Сцена после окончания теста."""

    def __init__(self, app: App, test_status: str) -> None:
        """Конструктор класса заставки окончания теста."""
        super().__init__(app)
        title = f"{test_status.capitalize()}. {config.QUIZ_COMPLETED_TEXT}"
        TextWidget(
            self.sprites,
            (self.width // 2, self.height // 2),
            self.font_size * 2,
            config.FONT_BOLD,
            config.TITLE_COLOR,
            text=title,
        )
        TextWidget(
            self.sprites,
            (self.width // 2, self.height // 2 + self.font_size * 3),
            self.font_size,
            config.FONT_REGULAR,
            config.TEXT_WIDGET_FONT_COLOR,
            text=config.STUDENT_INSTRUCTION_TEXT_FINISH,
        )

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Сбор событий сцены."""
        super().handle_events(events)
        for event in events:
            key, mod = config.NEXT_SESSION_KEY
            if event.type == pygame.KEYDOWN and event.key == key and (event.mod & mod):
                self.app.scene = SplashScene(self.app)


class TestScene(Scene):
    """Сцена теста."""

    def __init__(self, app: App) -> None:
        """Конструктор класса сцены теста."""
        super().__init__(app)

        # Разметка виджетов
        center_x = self.width // 2
        widget_y = int(self.height * 0.01)

        # Таймер
        self.timer = Timer(
            self.sprites,
            (int(self.width * 0.98), widget_y),
            self.font_size,
            align="topright",
        )
        pygame.time.set_timer(TIMER_EVENT, 100)

        # Запуск сессии теста
        self.test = Test(self.timer)
        self.test.load_question()

        # Номер вопроса / количество оставшихся
        self.question_order = TextWidget(
            self.sprites,
            (int(self.width * 0.02), widget_y),
            self.font_size,
            config.FONT_MONO,
            config.TEXT_WIDGET_FONT_COLOR,
            align="topleft",
        )

        widget_y += self.question_order.rect.height

        # FIXME костыли - вычисляем высоту с учетом высоты всех кнопок
        image_top = widget_y
        button_height = self.font_size * 2
        padding = self.font_size
        buttons_total_height = len(self.test.options) * (button_height + padding) - padding
        image_bottom = self.height - buttons_total_height - self.font_size  # небольшой отступ от низа
        image_bottom -= self.font_size
        self.image = Image(
            self.sprites,
            self.test.image_name,
            image_top,
            image_bottom,
            center_x,
        )
        widget_y += self.image.rect.height + self.font_size

        # Текст вопроса
        self.question_text = TextWidget(
            self.sprites,
            (center_x, widget_y),
            self.font_size,
            config.FONT_BOLD,
            config.TEXT_WIDGET_FONT_COLOR,
        )
        widget_y += self.question_text.rect.height + self.font_size

        self.update_widgets(widget_y)
        self.timer.start()

    def update_widgets(self, buttons_start_y: int) -> None:
        """Обновляет текст и изображения во всех виджетах."""
        text = f"{self.test.question_idx + 1} из {len(self.test.questions)}"
        self.question_order.text = text
        self.image.image_name = self.test.current_question["image"]
        self.image.load_and_scale_image()
        self.question_text.text = self.test.current_question["text"]
        self.make_options_buttons(buttons_start_y)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        """Сбор событий сцены."""
        super().handle_events(events)
        for event in events:
            if event.type == TIMER_EVENT:
                self.timer.tick()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for sprite in self.sprites:
                    if isinstance(sprite, Button):
                        sprite.handle_click(event.pos)

    def update(self) -> None:
        """Обновление."""
        super().update()
        # Если время истекло, завершить тестовую сессию
        if self.timer.time_current <= self.timer.time_stop:
            test_staus = "время вышло"
            self.test.finish(test_staus)
            self.app.scene = TestEndScene(self.app, test_staus)

    def make_options_buttons(self, start_y: int) -> None:
        """Создает кликабельные кнопки."""
        # Удаляем старые кнопки
        for sprite in self.sprites:
            if isinstance(sprite, Button):
                sprite.kill()

        for idx, option in enumerate(self.test.options):
            def callback(opt: int = idx) -> None:
                """Коллбек по клику кнопки."""
                self.test.check_answer(opt)

                # Кончились вопросы - тест пройден
                if self.test.is_finished:
                    test_status = "Тест окончен"
                    self.app.scene = TestEndScene(self.app, test_status)

                self.update_widgets(start_y)

            Button(
                self.sprites,
                (self.width // 2, int(start_y + idx * self.font_size * 2.3)),
                self.font_size,
                callback,
                self.width // 3,
                text=option,
            )

