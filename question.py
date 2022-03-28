import pandas as pd


class DB():
    def __init__(self, file):
        self.questions = []
        self.df = pd.read_excel(file)
        self.make_questions()

    def make_questions(self):
        for index, row in self.df.iterrows():
            question = Question(
                number=row["№"],
                right_answer=row[1],
                image=f'assets/{row["№"]}.png',
                text=row[2],
                answers=row[3:]
            )
            self.questions.append(question)


class Question:
    def __init__(
        self,
        number=0,
        right_answer=0,
        text="",
        image="assets/01.png",
        answers=["варианты ответа не созданы"]
    ):
        self.number = number
        self.right_answer = right_answer
        self.text = text
        self.image = image
        self.answers = answers


class Session():
    def __init__(
        self,
        questions=[],
        first_name="Имя не указано",
        last_name="Фамилия не указана",
        time_start="00:00:00",
        time_stop="00:00:60",
        right_answers=0,
        wrong_answers=0
    ):
        pass
