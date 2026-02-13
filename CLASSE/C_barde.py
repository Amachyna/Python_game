import classe
class barde(classe):
    def __init__(self):
        super().__init__("barde", "player life")

    def apply_bonus(self, stats):
        stats["pv"] + 3
        return stats