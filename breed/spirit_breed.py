from breed import breed

class Spirit(breed):
    def __init__(self):
        super().__init__("Spirit", "Elemental power")

    def apply_bonus(self, stats):
        stats["elemental"] += 3
        return stats