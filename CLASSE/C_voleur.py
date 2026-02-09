import classe
class voleur(classe):
    def __init__(self):
        super().__init__("voleur", "Critical chance")

    def apply_bonus(self, stats):
        stats["crit"] + 0.40
        return stats