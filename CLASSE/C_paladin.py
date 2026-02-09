import classe
class paladin(classe):
    def __init__(self):
        super().__init__("paladin", "defense")

    def apply_bonus(self, stats):
        stats["def"] + 3
        return stats