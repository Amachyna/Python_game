from dice import Dice
from dice import RiggedDice

if __name__ == "__main__":
    d0 = Dice(10, "blue", "wood")
    d1 = Dice(10, "blue", "wood")
    d2 = Dice(20, "green", "metal")
    d3 = Dice()

    print(d1)
    print(d3)
    print(d2)


    rd = RiggedDice(100)
    print(rd.roll())

    print(d0 == d1)

    d1.roll()