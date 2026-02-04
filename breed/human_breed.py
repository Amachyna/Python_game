from breed import breed

class Human(breed):
    def __init__(self):
        super().__init__("Human", "Weapon bonus")

    def apply_bonus(self, stats):
        stats["attack"] += 1
        return stats