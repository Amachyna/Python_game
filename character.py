from dice import Dice

class Character:
    def __init__(self, name, max_hp, attack_v, defense_v, dice, breed: Dice):
        self._name = name
        self._max_hp = max_hp
        self._hp = max_hp
        self._attack_value = attack_v
        self._defense_value = defense_v
        self._dice = dice
        self._breed = breed

    # Ex 1 → Créer la méthode __str__ pour print correctement un personnage

    def __str__(self):
        return f"Hi ! My name is {self._name}. I am a {self._breed}, Attack: {self._attack_value}/Defense: {self._defense_value}"

    def is_alive(self):
        return self._hp > 0

    def show_healthbar(self):
        print(
            f"[{self._hp * "♥"}{(self._max_hp - self._hp) * " "}] {self._hp}/{self._max_hp}hp")

    def decrease_hp(self, amount):
        self._hp = max(0, self._hp - amount)
        self.show_healthbar()

    def compute_damages(self, roll, target):
        return self._attack_value + roll

    def attack(self, target):
        roll = self._dice.roll()
        if (self.is_alive()):
            damages = self.compute_damages(roll, target)
            print(
                f"{self._name} attack {target._name} for {damages} damages.({self._attack_value} att + {roll} on the dice)")
            target.defend(damages)

    def compute_wounds(self, damages, roll):
        return damages - self._defense_value - roll

    def defend(self, damages):
        roll = self._dice.roll()
        wounds = self.compute_wounds(damages, roll)
        print(f"{self._name} lost {wounds} hp. ({damages} dmg - {self._defense_value} def - {roll} on the diceself._dice.roll() )")
        self.decrease_hp(wounds)