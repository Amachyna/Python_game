import random
from dice import Dice


class Combat:
    """Système de combat tour par tour"""
    
    def __init__(self, personnage, monstre):
        self.personnage = personnage
        self.monstre = monstre
        self.de20 = Dice(20)
        self.tour = 0
        self.en_cours = True
    
    def commencer(self):
        """Démarre le combat"""
        print(f"\n{'⚔️ '*25}")
        print(f"⚔️  COMBAT COMMENCE !")
        print(f"{'⚔️ '*25}\n")
        print(f"{self.personnage.prenom} {self.personnage.nom} VS {self.monstre.nom}")
        
        self.afficher_stats_combat()
        
        # Boucle principale du combat
        while self.en_cours:
            self.tour += 1
            print(f"\n{'─'*60}")
            print(f"🎲 TOUR {self.tour}")
            print(f"{'─'*60}")
            
            # Tour du joueur
            if not self.tour_joueur():
                break
            
            # Vérifier si le monstre est vaincu
            if not self.monstre.is_alive():
                self.victoire()
                break
            
            # Tour du monstre (si le monstre peut attaquer)
            if hasattr(self.monstre, 'peut_attaquer') and not self.monstre.peut_attaquer:
                print(f"\n💤 {self.monstre.nom} ne fait rien... (C'est un mannequin d'entraînement)")
            else:
                self.tour_monstre()
            
            # Vérifier si le joueur est vaincu
            if self.personnage.stats.pv <= 0:
                self.defaite()
                break
    
    def tour_joueur(self):
        """Gère le tour du joueur"""
        print(f"\n⚔️  C'est votre tour, {self.personnage.prenom} !")
        
        # Demander l'action
        while True:
            action = input("Que voulez-vous faire ? (1: Attaquer | 2: Fuir) : ").strip()
            
            if action == "1":
                self.attaque_joueur()
                return True
            elif action == "2":
                print(f"\n🏃 Vous prenez la fuite !")
                self.en_cours = False
                return False
            else:
                print("❌ Choix invalide. Tapez 1 pour attaquer ou 2 pour fuir.")
    
    def attaque_joueur(self):
        """Le joueur attaque le monstre"""
        # Lancer le dé de 20
        jet = self.de20.roll()
        print(f"\n🎲 Vous lancez le dé... Résultat : {jet}")
        
        # Déterminer le type d'attaque
        if jet == 20:
            # Critique réussi
            degats_base = self.personnage.stats.attaque * 2
            print(f"💥 COUP CRITIQUE ! Dégâts doublés !")
        elif jet == 1:
            # Échec critique
            degats_base = 0
            print(f"💢 ÉCHEC CRITIQUE ! Vous ratez complètement votre attaque !")
        else:
            # Attaque normale - Les dégâts augmentent avec le jet
            # Formule : attaque * (0.5 + (jet/20) * 0.5)
            # Jet de 2 = 55% des dégâts, Jet de 19 = 97.5% des dégâts
            multiplicateur = 0.5 + (jet / 20) * 0.5
            degats_base = int(self.personnage.stats.attaque * multiplicateur)
            
            if jet >= 15:
                print(f"✨ Belle frappe ! (Jet: {jet}/20)")
            elif jet >= 10:
                print(f"👍 Coup correct. (Jet: {jet}/20)")
            else:
                print(f"😐 Coup faible... (Jet: {jet}/20)")
        
        # Appliquer les dégâts
        if degats_base > 0:
            degats_infliges = self.monstre.take_damage(degats_base)
            print(f"⚔️  Vous infligez {degats_infliges} dégâts à {self.monstre.nom} !")
        else:
            print(f"⚔️  Aucun dégât infligé...")
        
        # Afficher les stats après l'attaque
        self.monstre.afficher_stats()
    
    def tour_monstre(self):
        """Le monstre attaque le joueur (pour les futurs monstres)"""
        print(f"\n🔴 C'est au tour de {self.monstre.nom} !")
        # À implémenter pour les monstres qui attaquent
        pass
    
    def afficher_stats_combat(self):
        """Affiche les stats des deux combattants"""
        print(f"\n{'='*60}")
        
        # Stats du joueur
        barre_vie_joueur = self._creer_barre_vie(self.personnage.stats.pv, self.personnage.stats.pv_max)
        print(f"👤 {self.personnage.prenom} {self.personnage.nom}")
        print(f"   {barre_vie_joueur} {self.personnage.stats.pv}/{self.personnage.stats.pv_max} PV")
        print(f"   ⚔️  ATK: {self.personnage.stats.attaque} | 🛡️  DEF: {self.personnage.stats.defense}")
        
        # Stats du monstre
        self.monstre.afficher_stats()
        
        print(f"{'='*60}")
    
    def _creer_barre_vie(self, pv, pv_max):
        """Crée une barre de vie visuelle"""
        longueur_barre = 20
        if pv_max == 0:
            pourcentage = 0
        else:
            pourcentage = pv / pv_max
        blocs_pleins = int(pourcentage * longueur_barre)
        blocs_vides = longueur_barre - blocs_pleins
        
        return f"[{'█' * blocs_pleins}{'░' * blocs_vides}]"
    
    def victoire(self):
        """Le joueur a gagné"""
        print(f"\n{'🏆'*30}")
        print(f"🏆 VICTOIRE !")
        print(f"{'🏆'*30}")
        print(f"\n{self.personnage.prenom} a vaincu {self.monstre.nom} !")
        print(f"Combat terminé en {self.tour} tours.\n")
        self.en_cours = False
    
    def defaite(self):
        """Le joueur a perdu"""
        print(f"\n{'💀'*30}")
        print(f"💀 DÉFAITE...")
        print(f"{'💀'*30}")
        print(f"\n{self.personnage.prenom} a été vaincu par {self.monstre.nom}...")
        print(f"Combat terminé en {self.tour} tours.\n")
        self.en_cours = False