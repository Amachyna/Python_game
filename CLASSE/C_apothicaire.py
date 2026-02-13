import classe
class apothicaire(classe):
    def __init__(self):
        super().__init__("apothicaire", "player life")

    def apply_bonus(self, stats):
        stats["pv"] + 5
        return stats