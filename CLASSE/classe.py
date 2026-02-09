from dice import Dice


class classe:
    def __init__(self, name_classe, bonus_classe):
        self._name_classe = name_classe
        self._bonus_classe = bonus_classe

    def name_breed(self):
        return f"ma classe est {self._name_classe}, mon bonus est {self._bonus_classe}"
    
    def bonus_classe(self, bonus_classe):
        pass