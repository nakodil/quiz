"""Главный модуль приложения."""

# TODO: время вышло, масштабирование виджетов, кнопка перед началом теста

from __future__ import annotations

import pygame

import config
from scene import InstructionsScene


class App:
    """Игра."""

    def __init__(self, fixed_resolution: tuple[int, int] | None = None) -> None:
        """Конструктор класса."""
        pygame.init()

        # Фиксированный размер экрана
        if fixed_resolution is None:
            info = pygame.display.Info()
            self.screen_w = info.current_w
            self.screen_h = info.current_h
            self.screen = pygame.display.set_mode(
                (self.screen_w, self.screen_h),
                pygame.FULLSCREEN,
            )
        # Полноэкранный режим
        else:
            self.screen_w = fixed_resolution[0]
            self.screen_h = fixed_resolution[1]
            self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))

        pygame.display.set_caption(config.APP_NAME)

        self.font_size = int(min(self.screen_w, self.screen_h) * 0.025)
        self.is_run = False
        self.scene = None

    def main_loop(self) -> None:
        """Главный цикл игры."""
        self.scene = InstructionsScene(self)
        self.is_run = True
        while self.is_run:
            events = pygame.event.get()
            self.scene.handle_events(events)
            self.scene.update()
            self.scene.render()
        pygame.quit()


if __name__ == "__main__":
    app = App()
    app.main_loop()
