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


class TrainingDummy(Monstre):
    """Mannequin d'entraînement - Ne riposte pas"""
    
    def __init__(self):
        super().__init__("Training Dummy", 30, 0)
        self.peut_attaquer = False  # Le mannequin n'attaque jamais
    
    def description(self):
        return f"{self.nom} | HP: {self.pv}/{self.pv_max} | 🎯 Cible d'entraînement"