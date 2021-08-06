from typing import List, Tuple, Dict
from utils.view import View


class Form(View):

    def __init__(self, title: str, choices: List[Tuple[str, str]]):
        content = '\n'.join([f'Option {i} : {choice}' for i, (choice, path) in enumerate(choices, start=1)])
        super().__init__(title, content)
        self.choices = choices

    def show(self):
        super().show()
        choice = int(input("Choose an option: "))
        return self.choices[choice-1][1]
