import classe
class mage(classe):
    def __init__(self):
        super().__init__("mage", "attaque magique", "defense magique")

    def apply_bonus(self, stats):
        stats["Magic def", "Magic atk"] + 1.5
        return stats