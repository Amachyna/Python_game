import classe
class pretre(classe):
    def __init__(self):
        super().__init__("pretre", "player life")

    def apply_bonus(self, stats):
        stats["pv"] + 5
        return stats