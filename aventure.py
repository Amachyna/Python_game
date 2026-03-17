class Salle:
    """Classe représentant une salle dans l'aventure"""
    
    def __init__(self, numero):
        self.numero = numero
    
    def afficher(self):
        """Affiche la salle actuelle"""
        print(f"\n{'='*50}")
        print(f"🚪 SALLE {self.numero}/10")
        print(f"{'='*50}")
        print(f"Vous êtes dans la salle numéro {self.numero}.")
    
    def __str__(self):
        return f"Salle {self.numero}"


class Aventure:
    """Classe pour gérer l'aventure du joueur"""
    
    def __init__(self, personnage):
        self.personnage = personnage
        self.salle_actuelle = 0
        self.nombre_salles_total = 10
        self.en_cours = False
    
    def commencer(self):
        """Commence l'aventure"""
        print(f"\n{'🎮'*25}")
        print(f"🎮 L'AVENTURE COMMENCE !")
        print(f"{'🎮'*25}")
        print(f"\n{self.personnage.prenom}, préparez-vous à traverser {self.nombre_salles_total} salles !")
        print(f"Race : {self.personnage.race.nom} | Classe : {self.personnage.classe.nom}")
        print(f"Stats : {self.personnage.stats}")
        
        self.en_cours = True
        self.salle_actuelle = 1
        
        # Boucle principale de l'aventure
        while self.en_cours and self.salle_actuelle <= self.nombre_salles_total:
            salle = Salle(self.salle_actuelle)
            salle.afficher()
            
            # Vérifier si c'est la dernière salle
            if self.salle_actuelle == self.nombre_salles_total:
                print("\n🎉 Félicitations ! Vous avez atteint la dernière salle !")
                self.terminer_aventure(victoire=True)
                break
            
            # Demander si le joueur veut continuer
            if not self.demander_continuer():
                self.terminer_aventure(victoire=False)
                break
            
            # Passer à la salle suivante
            self.salle_actuelle += 1
    
    def demander_continuer(self):
        """Demande au joueur s'il veut passer à la salle suivante"""
        print(f"\n{'─'*50}")
        while True:
            reponse = input("Voulez-vous passer à la salle suivante ? (oui/non) : ").lower().strip()
            
            if reponse in ["oui", "o", "yes", "y"]:
                print("➡️  Vous avancez vers la prochaine salle...")
                return True
            elif reponse in ["non", "n", "no"]:
                print("🚪 Vous décidez d'abandonner l'aventure...")
                return False
            else:
                print("❌ Réponse invalide. Veuillez répondre par 'oui' ou 'non'.")
    
    def terminer_aventure(self, victoire=False):
        """Termine l'aventure"""
        self.en_cours = False
        
        print(f"\n{'='*50}")
        if victoire:
            print("🏆 VICTOIRE ! 🏆")
            print(f"{'='*50}")
            print(f"Félicitations {self.personnage.prenom} !")
            print(f"Vous avez traversé les {self.nombre_salles_total} salles avec succès !")
        else:
            print("❌ AVENTURE ABANDONNÉE")
            print(f"{'='*50}")
            print(f"Vous avez abandonné à la salle {self.salle_actuelle}/{self.nombre_salles_total}.")
            print(f"Peut-être la prochaine fois, {self.personnage.prenom}...")
        
        print(f"{'='*50}\n")
    
    def obtenir_progression(self):
        """Retourne la progression actuelle"""
        return f"Salle {self.salle_actuelle}/{self.nombre_salles_total}"