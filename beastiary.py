class Monstre:
    def __init__(self, nom, pv, defense, reward=None):
        self.nom = nom
        self.pv_max = pv
        self.pv = pv
        self.defense = defense
        self.reward = reward if reward is not None else {"xp": 0, "gold": 0}

    def is_alive(self):
        return self.pv > 0

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.pv = max(0, self.pv - actual_damage)
        return actual_damage

    def get_reward(self):
        """Retourne la récompense si le monstre est mort"""
        if not self.is_alive():
            return self.reward
        return None

    def afficher_stats(self):
        barre_vie = self._creer_barre_vie()
        print(f"\n🎯 {self.nom}")
        print(f"   {barre_vie} {self.pv}/{self.pv_max} PV")
        print(f"   🛡️  DEF: {self.defense}")

    def _creer_barre_vie(self):
        longueur_barre = 20
        pourcentage = self.pv / self.pv_max if self.pv_max > 0 else 0
        blocs_pleins = int(pourcentage * longueur_barre)
        blocs_vides = longueur_barre - blocs_pleins
        return f"[{'█' * blocs_pleins}{'░' * blocs_vides}]"

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max}"

    def __str__(self):
        return f"{self.nom} (PV: {self.pv}/{self.pv_max})"


class Boss:
    def __init__(self, name, hp, attack, defense, reward):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.reward = reward

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return actual_damage

    def attack_target(self, target):
        return target.take_damage(self.attack)

    def get_reward(self):
        """Retourne la récompense si le boss est mort"""
        if not self.is_alive():
            return self.reward
        return None

    def description(self):
        return f"{self.name} | HP: {self.hp}/{self.max_hp} | ATK: {self.attack} | DEF: {self.defense}"


class TrainingDummy(Monstre):
    def __init__(self):
        super().__init__("Training Dummy", 30, 0, reward={"xp": 0, "gold": 0})
        self.peut_attaquer = False

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🎯 Cible d'entraînement"


class Goblin(Monstre):
    def __init__(self):
        super().__init__("Goblin", 20, 5, reward={"xp": 20, "gold": 5})
        self.attaque = 5
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"


class loup(Monstre):
    def __init__(self):
        super().__init__("Loup", 25, 3, reward={"xp": 25, "gold": 8})
        self.attaque = 7
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"


class kobold(Monstre):
    def __init__(self):
        super().__init__("Kobold", 15, 8, reward={"xp": 18, "gold": 6})
        self.attaque = 4
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"


class skeleton(Monstre):
    def __init__(self):
        super().__init__("Squelette", 10, 2, reward={"xp": 15, "gold": 4})
        self.attaque = 6
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"


class Slime(Monstre):
    def __init__(self):
        super().__init__("Slime", 12, 1, reward={"xp": 10, "gold": 3})
        self.attaque = 5
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"


class rat(Monstre):
    def __init__(self):
        super().__init__("Rat", 8, 1, reward={"xp": 8, "gold": 2})
        self.attaque = 3
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"


class ratgéant(Monstre):
    def __init__(self):
        super().__init__("Rat Géant", 15, 2, reward={"xp": 15, "gold": 5})
        self.attaque = 5
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"


class chauve_souris(Monstre):
    def __init__(self):
        super().__init__("Chauve-souris", 7, 1, reward={"xp": 7, "gold": 2})
        self.attaque = 4
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"


class GoblinBoss(Boss):
    def __init__(self):
        super().__init__(
            name="Goblin Boss",
            hp=60,
            attack=8,
            defense=2,
            reward={"xp": 100, "gold": 30}
        )


class ratempereur(Boss):
    def __init__(self):
        super().__init__(
            name="Rat Empereur",
            hp=40,
            attack=6,
            defense=3,
            reward={"xp": 70, "gold": 15}
        )

