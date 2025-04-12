"""Главный модуль приложения."""

# FIXME: длинный текст вопроса может вый ти за прдлы экрана
# TODO: переделать лейаут: изображение должно занимать % от высоты экрана и подстраивать под нее ширину

from __future__ import annotations

import pygame

import config
import results
from scene import ErrorScene, InstructionsScene


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
        self.background_image = self.get_background_image()
        self.is_run = False
        self.scene = None

    def main_loop(self) -> None:
        """Главный цикл игры."""
        if not results.is_results_writable():
            error_text = config.RESULTS_UNWRITABLE_ERROR
            self.scene = ErrorScene(self, error_text )
        else:
            self.scene = InstructionsScene(self)
        self.is_run = True
        while self.is_run:
            events = pygame.event.get()
            self.scene.handle_events(events)
            self.scene.update()
            self.screen.blit(self.background_image, (0, 0))
            self.scene.render()
        pygame.quit()

    def get_background_image(self) -> pygame.Surface:
        """Возвращает масштабированное на весь экран изображение.

        Загружает изображение, масштабирует, обрезает при необходимости
        и возвращает его поверхность.
        """
        image = pygame.image.load(config.BG_IMAGE).convert()
        original_width, original_height = image.get_size()

        # Вычисляем пропорцию изображения и его размеры
        scale_factor = max(
            self.screen_w / original_width,
            self.screen_h / original_height,
        )
        scaled_width = int(original_width * scale_factor)
        scaled_height = int(original_height * scale_factor)

        # Масштабируем изображение
        scaled_image = pygame.transform.smoothscale(
            image,
            (scaled_width, scaled_height),
        )

        # Вычисляем координаты верхнего левого угла под обрез
        x = (scaled_width - self.screen_w) // 2
        y = (scaled_height - self.screen_h) // 2

        return scaled_image.subsurface((x, y, self.screen_w, self.screen_h)).copy()

if __name__ == "__main__":
    app = App()
    app.main_loop()
