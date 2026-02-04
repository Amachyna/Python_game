from breed import breed


class Panda(breed):
    def __init__(self):
        super().__init__("Panda", "Defense bonus")

    def apply_bonus(self, stats):
        stats["defense"] += 2
        return stats