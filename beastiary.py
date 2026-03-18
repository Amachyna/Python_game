class Monstre:
    """Classe de base pour tous les monstres"""
    
    def __init__(self, nom, pv, attaque, defense, attaque_magique=0, defense_magique=0, vitesse=3, xp=0, gold=0):
        self.nom = nom
        self.pv_max = pv
        self.pv = pv
        self.attaque = attaque
        self.defense = defense
        self.attaque_magique = attaque_magique
        self.defense_magique = defense_magique
        self.vitesse = vitesse
        self.reward = {"xp": xp, "gold": gold}
    
    def is_alive(self):
        """Vérifie si le monstre est vivant"""
        return self.pv > 0
    
    def take_damage(self, damage, magique=False):
        """Le monstre subit des dégâts physiques ou magiques (minimum 1)"""
        resistance = self.defense_magique if magique else self.defense
        actual_damage = max(1, damage - resistance)
        self.pv = max(0, self.pv - actual_damage)
        return actual_damage
    
    def afficher_stats(self):
        """Affiche les statistiques du monstre"""
        barre_vie = self._creer_barre_vie()
        print(f"\n🎯 {self.nom}")
        print(f"   {barre_vie} {self.pv}/{self.pv_max} PV")
        print(f"   ⚔️  ATK: {self.attaque} | 🛡️  DEF: {self.defense} | ✨ ATK MAG: {self.attaque_magique} | 🔮 DEF MAG: {self.defense_magique} | 💨 VIT: {self.vitesse}")
    
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
    def __init__(self, name, hp, attack, defense, reward, attaque_magique=0, defense_magique=0, vitesse=3):
        self.nom = name
        self.pv = hp
        self.pv_max = hp
        self.attaque = attack
        self.defense = defense
        self.reward = reward
        self.attaque_magique = attaque_magique
        self.defense_magique = defense_magique
        self.vitesse = vitesse

    def is_alive(self):
        return self.pv > 0

    def take_damage(self, damage, magique=False):
        """Le boss subit des dégâts physiques ou magiques (minimum 1)"""
        resistance = self.defense_magique if magique else self.defense
        actual_damage = max(1, damage - resistance)
        self.pv = max(0, self.pv - actual_damage)
        return actual_damage

    def attack_target(self, target):
        damage_dealt = target.take_damage(self.attaque)
        return damage_dealt

    def afficher_stats(self):
        """Affiche les statistiques du boss (compatible avec Combat)"""
        barre_vie = self._creer_barre_vie()
        print(f"\n👑 {self.nom} (BOSS)")
        print(f"   {barre_vie} {self.pv}/{self.pv_max} PV")
        print(f"   ⚔️  ATK: {self.attaque} | 🛡️  DEF: {self.defense} | ✨ ATK MAG: {self.attaque_magique} | 🔮 DEF MAG: {self.defense_magique} | 💨 VIT: {self.vitesse}")

    def _creer_barre_vie(self):
        longueur_barre = 20
        pourcentage = self.pv / self.pv_max if self.pv_max > 0 else 0
        blocs_pleins = int(pourcentage * longueur_barre)
        blocs_vides = longueur_barre - blocs_pleins
        return f"[{chr(9608) * blocs_pleins}{chr(9617) * blocs_vides}]"

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | ATK: {self.attaque} | DEF: {self.defense}"


class TrainingDummy(Monstre):
    """Mannequin d'entraînement - Ne riposte pas"""
    
    def __init__(self):
        super().__init__("Training Dummy", 30, 0, 0)
        self.peut_attaquer = False  # Le mannequin n'attaque jamais
    
    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🎯 Cible d'entraînement"
    
class Goblin(Monstre):
    """Goblin - Un monstre basique avec une attaque modérée"""
    
    def __init__(self):
        super().__init__("Goblin", 18, 16, 4, vitesse=4, xp=15, gold=5)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"

class loup(Monstre):
    """Loup - Un monstre rapide avec une attaque plus élevée"""
    
    def __init__(self):
        super().__init__("Loup", 20, 15, 3, defense_magique=0, vitesse=9, xp=20, gold=7)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"
    
class kobold(Monstre):
    """Kobold - Un monstre avec une défense élevée mais une attaque plus faible"""
    
    def __init__(self):
        super().__init__("Kobold", 22, 7, 14, defense_magique=1, vitesse=2, xp=18, gold=6)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"

class skeleton(Monstre):
    """Squelette - Un monstre avec une attaque modérée et une défense faible"""
    
    def __init__(self):
        super().__init__("Squelette", 12, 4, 1, attaque_magique=16, defense_magique=6, vitesse=5, xp=20, gold=8)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"
    
class Slime(Monstre):
    """Slime - Un monstre avec une défense faible mais une attaque modérée"""
    
    def __init__(self):
        super().__init__("Slime", 28, 6, 2, attaque_magique=0, defense_magique=10, vitesse=2, xp=10, gold=3)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"
    
class rat(Monstre):
    """Rat - Un monstre rapide avec une attaque faible"""
    
    def __init__(self):
        super().__init__("Rat", 10, 8, 1, vitesse=8, xp=8, gold=2)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"
    
class ratgéant(Monstre):
    """Rat Géant - Un monstre rapide avec une attaque plus élevée que le Rat normal"""
    
    def __init__(self):
        super().__init__("Rat Géant", 30, 8, 8, vitesse=2, xp=12, gold=4)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"
    
class chauve_souris(Monstre):
    """Chauve-souris - Un monstre rapide avec une attaque faible mais une grande agilité"""
    
    def __init__(self):
        super().__init__("Chauve-souris", 6, 7, 0, vitesse=12, xp=8, gold=2)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🗡️ Attaque: {self.attaque} | 🛡️ Défense: {self.defense}"
    

class GoblinBoss(Boss):
    def __init__(self):
        super().__init__(
            name="Goblin",
            hp=60,
            attack=16,
            defense=2,
            reward={"xp": 100, "gold": 30}
        )

class ratempereur(Boss):
    def __init__(self):
        super().__init__(
            name="Rat Empereur",
            hp=60,
            attack=10,
            defense=8,
            attaque_magique=10,
            defense_magique=8,
            vitesse=8,
            reward={"xp": 70, "gold": 15}
        )

# ─── Monstres de la Forêt ────────────────────────────────────────────────────

class loup_alpha(Monstre):
    """Loup Alpha - Plus grand et plus féroce que le loup ordinaire"""
    def __init__(self):
        super().__init__("Loup Alpha", 45, 22, 6, vitesse=10, xp=30, gold=10)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | ATK: {self.attaque} | DEF: {self.defense}"


class araignee_geante(Monstre):
    """Araignée Géante - Empoisonne ses proies avec des attaques magiques"""
    def __init__(self):
        super().__init__("Araignée Géante", 35, 15, 5, attaque_magique=14, defense_magique=4, vitesse=7, xp=28, gold=9)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | ATK: {self.attaque} | ATK MAG: {self.attaque_magique}"


class goblin_archer(Monstre):
    """Goblin Archer - Attaque à distance, rapide mais fragile"""
    def __init__(self):
        super().__init__("Goblin Archer", 30, 18, 3, vitesse=9, xp=25, gold=8)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | ATK: {self.attaque} | DEF: {self.defense}"


class ent(Monstre):
    """Ent - Arbre animé, très résistant physiquement et magiquement"""
    def __init__(self):
        super().__init__("Ent", 80, 14, 12, defense_magique=8, vitesse=2, xp=40, gold=15)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | ATK: {self.attaque} | DEF: {self.defense}"


class esprit_foret(Monstre):
    """Esprit de la Forêt - Entité magique, très puissant magiquement"""
    def __init__(self):
        super().__init__("Esprit de la Forêt", 30, 5, 2, attaque_magique=22, defense_magique=12, vitesse=8, xp=35, gold=12)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | ATK MAG: {self.attaque_magique} | DEF MAG: {self.defense_magique}"


class sanglier_enrage(Monstre):
    """Sanglier Enragé - Charge brutale, ATK physique très élevée"""
    def __init__(self):
        super().__init__("Sanglier Enragé", 55, 25, 8, vitesse=6, xp=32, gold=11)
        self.peut_defendre = True

    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | ATK: {self.attaque} | DEF: {self.defense}"


# ─── Boss de la Forêt ────────────────────────────────────────────────────────

class gobelin_sergant(Boss):
    """Gobelin Sergant - Boss de la ville menacée, salle 20"""
    def __init__(self):
        super().__init__(
            name="Gobelin Sergant",
            hp=120,
            attack=18,
            defense=10,
            attaque_magique=8,
            defense_magique=6,
            vitesse=7,
            reward={"xp": 150, "gold": 50}
        )


class roi_gobelin(Boss):
    """Roi Gobelin - Boss final de la forêt, salle 30"""
    def __init__(self):
        super().__init__(
            name="Roi Gobelin",
            hp=200,
            attack=22,
            defense=14,
            attaque_magique=18,
            defense_magique=12,
            vitesse=8,
            reward={"xp": 300, "gold": 100}
        )