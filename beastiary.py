class Monstre:
    """Classe de base pour tous les monstres"""
    
    def __init__(self, nom, pv, defense):
        self.nom = nom
        self.pv_max = pv
        self.pv = pv
        self.defense = defense
    
    def is_alive(self):
        """Vérifie si le monstre est vivant"""
        return self.pv > 0
    
    def take_damage(self, damage):
        """Le monstre subit des dégâts"""
        actual_damage = max(0, damage - self.defense)
        self.pv = max(0, self.pv - actual_damage)
        return actual_damage
    
    def afficher_stats(self):
        """Affiche les statistiques du monstre"""
        barre_vie = self._creer_barre_vie()
        print(f"\n🎯 {self.nom}")
        print(f"   {barre_vie} {self.pv}/{self.pv_max} PV")
        print(f"   🛡️  DEF: {self.defense}")
    
    def _creer_barre_vie(self):
        """Crée une barre de vie visuelle"""
        longueur_barre = 20
        if self.pv_max == 0:
            pourcentage = 0
        else:
            pourcentage = self.pv / self.pv_max
        blocs_pleins = int(pourcentage * longueur_barre)
        blocs_vides = longueur_barre - blocs_pleins
        
        return f"[{'█' * blocs_pleins}{'░' * blocs_vides}]"
    
    def description(self):
        """Retourne une description du monstre"""
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
        damage_dealt = target.take_damage(self.attack)
        return damage_dealt

    def description(self):
        return f"{self.name} | HP: {self.hp}/{self.max_hp} | ATK: {self.attack} | DEF: {self.defense}"


class TrainingDummy(Monstre):
    """Mannequin d'entraînement - Ne riposte pas"""
    
    def __init__(self):
        super().__init__("Training Dummy", 30, 0)
        self.peut_attaquer = False  # Le mannequin n'attaque jamais
    
    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🎯 Cible d'entraînement"
    
class Goblin(Monstre):
    """Goblin - Un monstre basique avec une attaque modérée"""
    
    def __init__(self):
        super().__init__("Goblin", 20, 5)
        self.attaque = 5  # Dégâts de base du Goblin
        self.peut_defendre = True  # Le Goblin peut se défendre

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"

class loup(Monstre):
    """Loup - Un monstre rapide avec une attaque plus élevée"""
    
    def __init__(self):
        super().__init__("Loup", 25, 3)
        self.attaque = 7  # Dégâts de base du Loup
        self.peut_defendre = True  # Le Loup peut se défendre

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"
    
class kobold(Monstre):
    """Kobold - Un monstre avec une défense élevée mais une attaque plus faible"""
    
    def __init__(self):
        super().__init__("Kobold", 15, 8)
        self.attaque = 4  # Dégâts de base du Kobold
        self.peut_defendre = True  # Le Kobold peut se défendre

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"

class skeleton(Monstre):
    """Squelette - Un monstre avec une attaque modérée et une défense faible"""
    
    def __init__(self):
        super().__init__("Squelette", 10, 2)
        self.attaque = 6  # Dégâts de base du Squelette
        self.peut_defendre = True  # Le Squelette peut se défendre

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"
    
class Slime(Monstre):
    """Slime - Un monstre avec une défense faible mais une attaque modérée"""
    
    def __init__(self):
        super().__init__("Slime", 12, 1)
        self.attaque = 5  # Dégâts de base du Slime
        self.peut_defendre = True  # Le Slime peut se défendre

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"
    

class GoblinBoss(Boss):
    def __init__(self):
        super().__init__(
            name="Goblin",
            hp=50,
            attack=5,
            defense=2,
            reward={"xp": 100, "gold": 30}
        )