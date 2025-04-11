"""Модуль теста."""

import config
from questions import QUESTIONS
from results import save_results
from widgets import Timer


class Test:
    """Сессия теста."""

    def __init__(self, timer: Timer) -> None:
        """Конструктор класса."""
        self.timer = timer
        self.questions = QUESTIONS
        self.question_idx = 0
        self.student_name = ""
        self.student_school = ""
        self.right_answers = 0
        self.wrong_answers = 0
        self.time_taken = 0
        self.punish_score = 0
        self.status = "тест не пройден"
        self.is_finished = False

    def finish(self, status: str) -> None:
        """Завершение сессии: кончились вопросы или время. Запись результата."""
        self.status = status
        self.is_finished = True
        self.punish_score = self.wrong_answers * config.PUNISH_FACTOR
        self.time_taken = self.timer.time_initial - self.timer.time_current
        save_results(self)

    def load_question(self) -> None:
        """Загружает вопрос: изображение, текст, варианты ответов, ответ."""
        self.current_question = self.questions[self.question_idx]
        self.image_name = self.current_question["image"]
        self.text = self.current_question["text"]
        self.options = self.current_question["options"]
        self.answer_idx = self.current_question["answer_idx"]

    def check_answer(self, answer_idx: int) -> None:
        """Проверяет полученный ответ."""
        if answer_idx == self.answer_idx:
            self.right_answers += 1
        else:
            self.wrong_answers += 1

        self.question_idx += 1
        if self.question_idx < len(self.questions):
            self.load_question()
        else:
            self.finish("тест пройден")
