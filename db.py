import pandas as pd


class TEST():
    def __init__(self, file):
        self.questions = []
        self.df = pd.read_excel(file)

        self.df = self.df.dropna(how='all').dropna(how='all', axis=1)

        self.make_questions()

    def make_questions(self):
        for index, row in self.df.iterrows():
            # игнорируем пустые ответы №4, иначе pd запишет туда NaN
            # нужно ли игнорировать пустой текст вопроса?
            if isinstance(row[6], str):
                ans = row[3:7]
            else:
                ans = row[3:6]

            question = Question(
                number=row["№"],
                right_answer=row[1],
                image=f'assets/{row["№"]}.png',
                text=row[2],
                answers=ans
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
