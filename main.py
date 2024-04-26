import tkinter as tk
import random
from quiestions import questions
from datetime import datetime

blue_dark = '#569cd6'
blue_light = '#9cdcfe'
black = '#1f1f1f'
yellow_dark = '#ffd700'
yellow_light = '#dcdcaa'
orange = '#ce9178'
purple = '#da70d6'
green = '#4ec9b0'

paddings = {
    'pady': 50,
    'padx': 30
}


class App:
    def __init__(self, questions_shuffle=False, options_shuffle=False) -> None:
        self.window = tk.Tk()
        self.window.attributes('-fullscreen', True)
        self.window.update()
        self.width = self.window.winfo_width()
        self.height = self.window.winfo_height()
        self.window.config(padx=0, pady=0, bg=black)

        self.window.bind('<Escape>', lambda _: self.window.destroy())

        self.font_size = int(min((self.width, self.height)) * 0.03)
        self.font_name = 'Consolas'
        self.font_color = 'black'
        self.window.option_add('*font', (self.font_name, self.font_size))

        self.top_frame = tk.Frame(self.window, bg=black)
        self.top_frame.place(relx=0.5, rely=0.5, anchor="c")

        self.questions_shuffle = questions_shuffle
        self.options_shuffle = options_shuffle
        self.correct = None
        self.incorrect = None
        self.question_idx = None
        self.start_time = None
        self.start()

        self.window.mainloop()

    def start(self) -> None:
        self.correct = 0
        self.incorrect = 0
        self.question_idx = 0
        if self.questions_shuffle:
            random.shuffle(questions)
        self.start_time = datetime.now()
        self.show_question()

    def clear(self) -> None:
        [widget.destroy() for widget in self.top_frame.winfo_children()]

    def show_question(self) -> None:
        self.clear()
        question = questions[self.question_idx]
        if self.options_shuffle:
            random.shuffle(question['ответы'])

        tk.Label(
            self.top_frame,
            text=f'вопрос {self.question_idx + 1} из {len(questions)}',
            bg=black,
            fg=yellow_light
        ).pack(**paddings)
        tk.Label(
            self.top_frame, text=question['вопрос'], bg=black, fg=yellow_light,
        ).pack(**paddings)

        options_frame = tk.Frame(self.top_frame, bg=black)
        options_frame.pack(expand=True, fill='x')
        for idx, option in enumerate(question['ответы']):
            button = tk.Button(
                options_frame,
                text=option,
                command=lambda arg=option: self.on_button(arg),
                bg=black,
                fg=blue_dark,
                width=10
            )
            button.pack(side='left', **paddings)

    def on_button(self, option: str) -> None:
        question = questions[self.question_idx]
        if option == question['ответ']:
            self.correct += 1
        else:
            self.incorrect += 1

        self.question_idx += 1
        if self.question_idx == len(questions):
            self.show_result()
        else:
            self.show_question()

    def show_result(self) -> None:
        self.clear()
        time_delta = datetime.now() - self.start_time
        time = time_delta
        tk.Label(
            self.top_frame,
            bg=black,
            fg=yellow_light,
            text=f'время: {time}'
        ).pack(**paddings)
        tk.Label(
            self.top_frame,
            bg=black,
            fg=green,
            text=f'верно: {self.correct}'
        ).pack()
        tk.Label(
            self.top_frame,
            bg=black,
            fg=purple,
            text=f'ошибки: {self.incorrect}'
        ).pack()
        tk.Button(
            self.top_frame,
            text='заново',
            bg=black,
            fg=blue_dark,
            command=self.start
        ).pack(**paddings)


App(questions_shuffle=True, options_shuffle=True)
