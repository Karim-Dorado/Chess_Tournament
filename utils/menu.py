from typing import List, Tuple
from utils.view import View


class Menu(View):

    def __init__(self, title: str, choices: List[Tuple[str, any]]):
        content = '\n'.join([f'Option {i} : {choice}' for i, (choice, path) in enumerate(choices, start=1)])
        super().__init__(title, content)
        self.choices = choices

    def show(self):
        super().show()
        check = True
        while check is True:
            try:
                choice = int(input("Choose an option: "))
                if choice > len(self.choices) or choice == 0:
                    raise ValueError
                check = False
            except ValueError:
                print("Invalid choice")
        return self.choices[choice-1][1]
