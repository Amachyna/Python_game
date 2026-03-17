class Breed:
    def __init__(self, name_breed, bonus_type):
        self.name_breed = name_breed
        self.bonus_type = bonus_type

    def description(self):
        return f"Breed: {self.name_breed} | Bonus: {self.bonus_type}"

    def apply_bonus(self, stats):
        # Generic method — overridden in subclasses
        return stats


class Feline(Breed):
    def __init__(self):
        super().__init__("Feline", "Critical chance")

    def apply_bonus(self, stats):
        stats["crit"] += 0.15
        return stats


class Human(Breed):
    def __init__(self):
        super().__init__("Human", "Weapon bonus")

    def apply_bonus(self, stats):
        stats["attack"] += 1
        return stats


class Panda(Breed):
    def __init__(self):
        super().__init__("Panda", "Defense bonus")

    def apply_bonus(self, stats):
        stats["defense"] += 2
        return stats


class Reptilian(Breed):
    def __init__(self):
        super().__init__("Reptilian", "Strength bonus")

    def apply_bonus(self, stats):
        stats["strength"] += 2
        return stats


class Spirit(Breed):
    def __init__(self):
        super().__init__("Spirit", "Elemental power")

    def apply_bonus(self, stats):
        stats["elemental"] += 3
        return stats