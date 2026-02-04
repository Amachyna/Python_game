from breed import breed

class Feline(breed):
    def __init__(self):
        super().__init__("Feline", "Critical chance")

    def apply_bonus(self, stats):
        stats["crit"] += 0.15
        return stats

