class TrainingDummy:
    def __init__(self):
        self.name = "Training Dummy"
        self.hp = 30
        self.max_hp = 30
        self.defense = 0

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

    def description(self):
        return f"{self.name} | HP: {self.hp}/{self.max_hp}"
    