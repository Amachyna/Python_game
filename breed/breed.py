from dice import Dice


class breed:
    def __init__(self, name_breed, bonus_breed):
        self._name_breed = name_breed
        self._bonus_breed = bonus_breed

    def name_breed(self):
        return f"My breed is {self._name_breed}, my bonus is {self._bonus_breed}"
    
    def bonus_breed(self, bonus_breed):
        pass

if __name__ == "__main__":
    d2 = Dice(2, "blue", "wood")
    d4 = Dice(4, "blue", "wood")
    d6 = Dice(6, "green", "metal")
    d8 = Dice(8, "red", "obsidian")
    d10 = Dice(10, "violet", "bob")
    d12 = Dice(12, "green", "plastic")
    d20 = Dice(20, "blue", "platic")

