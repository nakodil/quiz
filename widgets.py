"""Модуль виджетов."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pygame

import config


class TextWidget(pygame.sprite.Sprite):
    """Экранный виджет с текстом."""

    def __init__(
            self,
            sprite_group: pygame.sprite.Group,
            coords: tuple[int, int],
            font_size: int,
            font_path: Path,
            font_color: tuple[int, int, int],
            text: str | int = "",
            align: str = "center",
    ) -> None:
        """Конструктор класса."""
        self.sprite_group = sprite_group
        self.coords = coords
        self.font_size = font_size
        self.font_path = font_path
        self.font_color = font_color
        self.text = text
        self.align = align

        self.font = pygame.font.Font(
            self.font_path,
            self.font_size,
        )
        self.image = None
        self.rect = None
        super().__init__(self.sprite_group)
        self.sprite_group.add(self)
        self.update()

    def update(self) -> None:
        """Перерисовывает изображение текста."""
        self.image = self.font.render(
            str(self.text),
            True,
            self.font_color,
        )

        rect_kwargs = (
            {"topleft": self.coords} if self.align == "topleft" else
            {"topright": self.coords} if self.align == "topright" else
            {"center": self.coords}
        )
        self.rect = self.image.get_rect(**rect_kwargs)

class Timer(TextWidget):
    """Таймер с обратным отсчетом."""

    def __init__(
            self,
            sprite_group: pygame.sprite.Group,
            coords: tuple[int, int],
            font_size: int,
            align: str = "center",
    ) -> None:
        """Конструктор класса."""
        self.color_critical = config.TIMER_CRITICAL_COLOR
        self.time_initial = None
        self.time_current = None
        self.time_critical = None
        self.time_stop = None
        self.is_ticking = False
        font_path = config.FONT_MONO
        font_color = config.TIMER_COLOR
        super().__init__(
            sprite_group, coords, font_size, font_path, font_color, align=align,
        )

    def start(self) -> None:
        """Запуск обратного отсчета."""
        self.time_initial = config.TIME_MAX_SEC
        self.time_current = self.time_initial
        self.time_critical = 60.0
        self.time_stop = 0.0
        self.is_ticking = True

    def tick(self) -> None:
        """Таймер тикает 10 раз в секунду."""
        if not self.is_ticking:
            return
        self.time_current = round(self.time_current - 0.1, 1)

        if self.time_current <= self.time_critical:
            self.font_color = config.TIMER_CRITICAL_COLOR

        if self.time_current <= self.time_stop:
            self.is_ticking = False

    def update(self) -> None:
        """Обновляет изображение."""
        if not self.is_ticking:
            return
        if self.time_current < self.time_critical:
            self.color = self.color_critical
        minutes, seconds = divmod(int(self.time_current), 60)
        self.text = f"{minutes:02}:{seconds:02}"
        super().update()


class Button(TextWidget):
    """Кнопка с текстом и действием."""

    def __init__(
        self,
        sprite_group: pygame.sprite.Group,
        coords: tuple[int, int],
        font_size: int,
        callback: Callable,
        min_width: int,
        text: int | str = "",
    ) -> None:
        """Конструктор класса."""
        self.font_size = font_size
        self.callback = callback
        self.min_width = min_width
        self.text = text
        self.bg_color = config.BUTTON_BG_COLOR
        self.padding = self.font_size // 2
        self.font_path = config.FONT_REGULAR
        self.font_color = config.BUTTON_TEXT_COLOR
        super().__init__(
            sprite_group,
            coords,
            self.font_size,
            self.font_path,
            self.font_color,
            text=self.text,
        )

    def handle_click(self, mouse_pos: tuple[int, int]) -> None:
        """Обработка нажатия."""
        if self.rect.collidepoint(mouse_pos):
            self.callback()

    def update(self) -> None:
        """Обновляет изображение кнопки (например, при изменении текста)."""
        text_surface = self.font.render(self.text, True, self.font_color)
        text_rect = text_surface.get_rect(center=(0, 0))
        width = text_rect.width + 4 * self.padding
        height = text_rect.height + self.padding

        # Ширина кнопок не меньше минимальной
        width = max(self.min_width, width)

        # Фон кнопки
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(
            self.image,
            self.bg_color,
            (0, 0, width, height),
        )
        self.image.blit(
            text_surface,
            (width // 2 - text_rect.width // 2, height // 2 - text_rect.height // 2),
        )
        self.rect = self.image.get_rect(center=self.coords)


class Image(pygame.sprite.Sprite):
    """Виджет для отображения изображения с масштабированием."""

    def __init__(
        self,
        group: pygame.sprite.Group,
        image_name: str,
        top: int,
        bottom: int,
        center_x: int,
    ) -> None:
        """Конструктор класса."""
        super().__init__(group)

        self.image_name = image_name
        self.top = top
        self.bottom = bottom
        self.center_x = center_x

        self.load_and_scale_image()
        group.add(self)

    def load_and_scale_image(self) -> None:
        """Загружает изображение, ресайзит его пропорционально."""
        # Загружаем оригинальное изображение
        original = pygame.image.load(config.IMG_DIR / self.image_name).convert_alpha()
        orig_w, orig_h = original.get_size()

        # Вычисляем высоту, доступную под изображение
        available_height = self.bottom - self.top

        # Вычисляем новую ширину пропорционально
        scale_factor = available_height / orig_h
        new_w = int(orig_w * scale_factor)
        new_h = int(orig_h * scale_factor)

        self.image = pygame.transform.smoothscale(original, (new_w, new_h))
        self.rect = self.image.get_rect()
        self.rect.top = self.top
        self.rect.centerx = self.center_x
