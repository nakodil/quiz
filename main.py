import tkinter as tk
from db import TEST
import sys
import datetime
import pyglet


class App(tk.Tk):
    def __init__(self, db, results_file):
        super().__init__()
        self.db = db
        self.results_file = results_file
        self.questions = self.db.questions
        self.attributes('-fullscreen', True)
        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()
        # шрифты
        pyglet.font.add_file("assets/PTSans-Regular.ttf")
        self.font_button = ("PTSans-Regular", 16)
        self.font_question = ("PTSans-Regular", 18)
        # выход
        self.bind("<Escape>", self.close)

    def close(self, keypress):
        sys.exit()

    def show_question(self, question):
        # пустой текст в базе - NaN типа float
        if isinstance(question.text, str):
            self.question_text.config(
                text=question.text,
                font=self.font_question
            )
            self.question_text.grid(column=0, row=1, pady=10)
        else:
            self.question_text.grid_forget()

        self.img = tk.PhotoImage(file=question.image).subsample(2)
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
                font=self.font_button,
                text=question.answers[answer_idx],
                command=lambda idx=answer_idx + 1: self.check_answer(idx)
            )
            button.grid(column=0, row=answer_idx, pady=5)
            answer_idx += 1

    def check_answer(self, answer_idx):
        # удаление виджетов - в метод
        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        if self.questions[self.current_question_idx].right_answer == answer_idx:
            self.right_answers += 1
        else:
            self.wrong_answers += 1

        self.next_question()

    def next_question(self):
        if self.current_question_idx >= len(self.questions) - 1:
            self.finish_screen()
        else:
            self.current_question_idx += 1
            self.show_question(db.questions[self.current_question_idx])

    def start_screen(self):
        self.start_frame = tk.Frame(self)
        self.start_frame.place(relx=.5, rely=.5, anchor="c")
        self.start_button = tk.Button(
            self.start_frame,
            font=self.font_button,
            text="начать тест",
            command=self.start_test
        )
        self.start_button.grid(column=0, row=0)
        # фрейм вопроса
        self.question_frame = tk.Frame(self, pady=10)
        self.question_frame.place(relx=.5, rely=0, anchor="n")
        # текст вопроса
        self.question_text = tk.Label(
            self.question_frame,
            width=self.width,
            anchor="center"
        )
        # фрейм вариантов ответа
        self.answers_frame = tk.Frame(self.question_frame)
        self.answers_frame.grid(column=0, row=2)

    def start_test(self):
        self.start_frame.destroy()
        self.time_started = datetime.datetime.now()
        self.right_answers = 0
        self.wrong_answers = 0
        self.current_question_idx = 0
        self.show_question(self.questions[self.current_question_idx])

    def finish_screen(self):
        self.time_finished = datetime.datetime.now()
        self.time_total = self.time_finished - self.time_started
        self.question_frame.destroy()
        self.answers_frame.destroy()
        self.finish_frame = tk.Frame(self)
        self.finish_frame.place(relx=.5, rely=.5, anchor="c")
        self.finish_text = tk.Label(
            self.finish_frame,
            font=self.font_question,
            text="Спасибо что прошли тест!\nОтправляйтесь к следующей станции!",
            width=self.width,
            anchor="center"
        )
        self.finish_text.grid(column=0, row=0)
        self.db.write_user_results(
            results_file=self.results_file,
            time_total=self.time_total,
            wrong_answers=self.wrong_answers
        )
        self.after(3000, self.finish_frame.destroy)
        self.after(3001, self.start_screen)


if __name__ == "__main__":
    db = TEST("assets/db.xlsx")
    results_file = "результаты.xlsx"
    app = App(db, results_file)
    app.start_screen()
    app.mainloop()
