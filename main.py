"""
    TODO:
        Фрейм приветствия
        Фрейм финиша
        Экспорт сессии в csv или xlsx
"""

import tkinter as tk
from db import TEST
import sys
import datetime
import pyglet


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.attributes('-fullscreen', True)
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        # шрифты
        pyglet.font.add_file("assets/PTSans-Regular.ttf")
        self.font = ("PTSans-Regular", 18)
        # фрейм вопроса
        self.question_frame = tk.Frame(self, pady=20)
        self.question_frame.place(relx=.5, rely=0, anchor="n")
        # фрейм вариантов ответа
        self.answers_frame = tk.Frame(self.question_frame)
        self.answers_frame.grid(column=0, row=2)
        # текст вопроса
        self.question_text = tk.Label(
            self.question_frame,
            width=1260,
            anchor="center"
        )
        # выход
        self.bind("<Escape>", self.close)
        # показать первый вопрос

    def close(self, keypress):
        sys.exit()

    def show_question(self, question):
        # пустой текст в базе - NaN типа float
        if isinstance(question.text, str):
            self.question_text.config(text=question.text, font=self.font)
            self.question_text.grid(column=0, row=1, pady=20)
        else:
            self.question_text.grid_forget()

        self.img = tk.PhotoImage(file=question.image)
        self.canvas = tk.Canvas(
            self.question_frame,
            width=self.img.width(),
            height=self.img.height()
        )
        self.canvas.grid(column=0, row=0)
        self.canvas.create_image(0, 0, anchor='nw', image=self.img)
        answer_idx = 0
        for answer in question.answers:
            button = tk.Button(
                self.answers_frame,
                font=self.font,
                text=question.answers[answer_idx],
                command=lambda idx=answer_idx + 1: self.check_answer(idx)
            )
            button.grid(column=0, row=answer_idx, pady=10)
            answer_idx += 1

    def check_answer(self, answer_idx):
        # удаление виджетов - в метод
        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        if self.questions[self.current_question_idx].right_answer == answer_idx:
            print("Верно!")
            self.right_answers += 1
        else:
            print("Ошибка!")
            self.wrong_answers += 1

        self.next_question()

    def next_question(self):
        if self.current_question_idx >= len(self.questions) - 1:
            print("вопросы кончились")
            for widget in self.question_frame.winfo_children():
                widget.destroy()
            self.write_results()
        else:
            self.current_question_idx += 1
            self.show_question(db.questions[self.current_question_idx])

    def write_results(self):
        self.time_finished = datetime.datetime.now()
        self.time_total = self.time_finished - self.time_started
        print("Прошло времени", self.time_total)
        print("Правильных ответов:", self.right_answers)
        print("Ошибок:", self.wrong_answers)

    def start_test(self, db):
        self.time_started = datetime.datetime.now()
        self.questions = db.questions
        self.right_answers = 0
        self.wrong_answers = 0
        self.current_question_idx = 0
        self.show_question(db.questions[self.current_question_idx])


if __name__ == "__main__":
    db = TEST("assets/db.xlsx")
    app = App()
    app.start_test(db)
    app.mainloop()
