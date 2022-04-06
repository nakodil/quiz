import tkinter as tk
from db import TEST
import sys
import datetime
import pyglet


class App(tk.Tk):
    def __init__(self, results_file):
        super().__init__()
        self.results_file = results_file
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

    def set_option(self, num):
        self.db = TEST(file=f"assets/{num}/db.xlsx", option=num)
        self.questions = self.db.questions
        self.start_screen()

    def options_screen(self):
        self.options_frame = tk.Frame(self)
        self.options_frame.place(relx=.5, rely=.5, anchor="c")

        # DRY!
        self.option_1 = tk.Button(
            self.options_frame,
            font=self.font_button,
            text=f"вариант 1",
            command=lambda: self.set_option(1)
        ).pack()
        self.option_2 = tk.Button(
            self.options_frame,
            font=self.font_button,
            text=f"вариант 2",
            command=lambda: self.set_option(2)
        ).pack()
        self.option_3 = tk.Button(
            self.options_frame,
            font=self.font_button,
            text=f"вариант 3",
            command=lambda: self.set_option(3)
        ).pack()
        self.option_4 = tk.Button(
            self.options_frame,
            font=self.font_button,
            text=f"вариант 4",
            command=lambda: self.set_option(4)
        ).pack()

    def show_question(self, question):
        self.question_number.config(
            text=f"Вопрос {self.current_question_idx + 1} из {len(self.questions)}"
        )
        # пустой текст в базе - NaN типа float
        if isinstance(question.text, str):
            self.question_text.config(text=question.text)
        else:
            self.question_text.config(text="")
        self.img = tk.PhotoImage(file=question.image)
        self.canvas = tk.Canvas(
            self.question_frame,
            width=self.img.width(),
            height=self.img.height()
        )
        self.canvas.grid(column=0, row=1, columnspan=2)
        self.canvas.create_image(0, 0, anchor='nw', image=self.img)
        answer_idx = 0
        for answer in question.answers:
            button = tk.Button(
                self.answers_frame,
                font=self.font_button,
                text=question.answers[answer_idx],
                command=lambda idx=answer_idx + 1: self.check_answer(idx)
            )
            button.grid(column=1, row=answer_idx, pady=5)
            answer_idx += 1

    def check_answer(self, answer_idx):
        for widget in self.answers_frame.winfo_children():
            widget.destroy()

        if self.questions[self.current_question_idx].right_answer == answer_idx:
            self.right_answers += 1
        else:
            self.wrong_answers += 1

        self.next_question()

    def next_question(self):
        if self.current_question_idx >= len(self.questions) - 1:
            self.finish_screen("Спасибо что прошли тест!\nОтправляйтесь к следующей станции!")
        else:
            self.current_question_idx += 1
            self.show_question(self.db.questions[self.current_question_idx])

    def update_clock(self):
        self.time -= 1
        if self.time <= 0:
            self.finish_screen(
                "Время вышло!\nОтправляйтесь к следующей станции!"
            )
            return None
        self.question_time.configure(text=f"осталось {self.time} секунд")
        self.question_frame.after(1000, self.update_clock)

    def start_screen(self):
        self.options_frame.destroy()
        self.start_frame = tk.Frame(self)
        self.start_frame.place(relx=.5, rely=.5, anchor="c")
        self.start_button = tk.Button(
            self.start_frame,
            font=self.font_button,
            text="начать тест",
            command=self.start_test
        )
        self.start_button.grid(column=0, row=0)

    def start_test(self):
        self.start_frame.destroy()
        self.time_started = datetime.datetime.now()
        self.right_answers = 0
        self.wrong_answers = 0
        self.current_question_idx = 0
        self.time = 600  # хардкод!

        # фрейм вопроса
        self.question_frame = tk.Frame(self, pady=10)
        self.question_frame.place(relx=.5, rely=0, anchor="n")

        # номер вопроса из всех
        self.question_number = tk.Label(
            self.question_frame,
            font=self.font_button,
            anchor="w"
        )
        self.question_number.grid(column=0, row=0)

        # время
        self.question_time = tk.Label(
            self.question_frame,
            font=self.font_button,
            anchor="e"
        )
        self.question_time.grid(column=1, row=0)

        # текст вопроса
        self.question_text = tk.Label(
            self.question_frame,
            font=self.font_question,
            anchor="center",
            text="текст вопроса"
        )
        self.question_text.grid(column=0, row=2, pady=10, columnspan=2)

        # фрейм вариантов ответа
        self.answers_frame = tk.Frame(self.question_frame)
        self.answers_frame.grid(column=0, row=3, columnspan=2)

        # старт
        self.show_question(self.questions[self.current_question_idx])
        self.update_clock()

    def finish_screen(self, message):
        self.time_finished = datetime.datetime.now()
        self.time_total = self.time_finished - self.time_started
        self.question_frame.destroy()
        self.answers_frame.destroy()
        self.finish_frame = tk.Frame(self)
        self.finish_frame.place(relx=.5, rely=.5, anchor="c")
        self.finish_text = tk.Label(
            self.finish_frame,
            font=self.font_question,
            text=message,
            width=self.width,
            anchor="center"
        )
        self.finish_text.grid(column=0, row=0)
        self.db.write_user_results(
            results_file=self.results_file,
            time_total=self.time_total,
            wrong_answers=self.wrong_answers,
            right_answers=self.right_answers
        )
        self.after(3000, self.finish_frame.destroy)
        self.after(3001, self.start_screen)


if __name__ == "__main__":
    results_file = "результаты.xlsx"
    app = App(results_file)
    app.options_screen()
    app.mainloop()
