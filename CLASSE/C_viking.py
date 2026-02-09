import classe
class viking(classe):
    def __init__(self):
        super().__init__("viking", "attaque")

    def apply_bonus(self, stats):
        stats["atk"] + 3
        return stats