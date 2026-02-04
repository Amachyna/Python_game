from breed import breed


class Reptilian(breed):
    def __init__(self):
        super().__init__("Reptilian", "Strength bonus")

    def apply_bonus(self, stats):
        stats["strength"] += 2
        return stats