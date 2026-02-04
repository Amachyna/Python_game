
import random


class Dice:
    def __init__(self, f=6, c="red", m="plastic"):
        self.faces = f
        self.color = c
        self.material = m

    def __str__(self):
        return f"This a {self.color} {self.material} with {self.faces} faces"

    def __eq__(self, another_dice):
        return self.faces == another_dice.faces and self.color == another_dice.color and self.material == another_dice.material

    def roll(self):
        """This method should return a random number..."""
        return random.randint(1, self.faces)


if __name__ == "__main__":
    d2 = Dice(2, "golden", "coin")
    d4 = Dice(4, "blue", "wood")
    d6 = Dice(6, "green", "metal")
    d8 = Dice(8, "red", "obsidian")
    d10 = Dice(10, "violet", "bob")
    d12 = Dice(12, "green", "plastic")
    d20 = Dice(20, "blue", "platic")


