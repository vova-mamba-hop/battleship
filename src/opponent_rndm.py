import random

class rndm:
    def __init__(self):
        self.name = 'Random'
        self.dscr = 'Opponent takes random shots and does not retain memory of previous moves'

    def move(self):
        index = random.randint(0,99)
        return index