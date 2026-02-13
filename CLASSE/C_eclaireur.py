import classe
class eclaireur(classe):
    def __init__(self):
        super().__init__("eclaireur", "player life")

    def apply_bonus(self, stats):
        stats["pv"] + 5
        return stats