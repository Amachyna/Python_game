import random
from beastiary import TrainingDummy, ratempereur, chauve_souris, Slime, rat, ratgéant
from combat import Combat
from weapons import get_armes_pour_classe, choisir_arme
from npc import Marchand

# Monstres disponibles dans les salles aléatoires
MONSTRES_ALEATOIRES = [chauve_souris, Slime, rat, ratgéant]


class Salle:
    """Classe représentant une salle dans l'aventure"""
    
    def __init__(self, numero):
        self.numero = numero
        self.monstre = None
        self.monstres = []        # Pour les salles avec plusieurs monstres
        self.contient_armes = (numero == 5)
        self.est_salle_soin = False
        self.npc = None

        # Salles scriptées
        if numero == 1:
            self.monstre = TrainingDummy()
        elif numero == 15:
            self.monstre = ratempereur()
        elif numero == 8:
            self.npc = Marchand()
        elif numero not in (1, 5, 8, 15):
            # Salles libres : 75% monstre(s), 25% soin
            if random.random() < 0.70:
                # 1 ou 2 monstres aléatoires
                nb = random.randint(1, 2)
                self.monstres = [random.choice(MONSTRES_ALEATOIRES)() for _ in range(nb)]
                self.monstre = self.monstres[0]  # Compatibilité avec le reste du code
            else:
                self.est_salle_soin = True
    
    def afficher(self):
        """Affiche la salle actuelle"""
        print(f"\n{'='*50}")
        print(f"🚪 SALLE {self.numero}/15")
        print(f"{'='*50}")
        
        if self.est_salle_soin:
            print(f"💚 Une source de lumière dorée réchauffe la salle...")
        elif self.npc:
            print(f"🧟 Une silhouette se découpe dans l'obscurité des égouts...")
        elif self.monstres and len(self.monstres) > 1:
            noms = " et ".join(m.nom for m in self.monstres)
            print(f"⚠️  {noms} se trouvent dans cette salle !")
        elif self.monstre:
            print(f"⚠️  Un {self.monstre.nom} se trouve dans cette salle !")
        elif self.contient_armes:
            print(f"✨ Un coffre mystérieux brille dans cette salle...")
        else:
            print(f"La salle est calme et silencieuse.")
    
    def a_monstre(self):
        """Vérifie si la salle contient un monstre"""
        return self.monstre is not None
    
    def __str__(self):
        return f"Salle {self.numero}"


class Aventure:
    """Classe pour gérer l'aventure du joueur"""
    
    def __init__(self, personnage):
        self.personnage = personnage
        self.salle_actuelle = 0
        self.nombre_salles_total = 15
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
            
            # Salle soin
            if salle.est_salle_soin:
                soin = max(1, int(self.personnage.stats.pv_max * 0.25))
                avant = self.personnage.stats.pv
                self.personnage.stats.pv = min(self.personnage.stats.pv_max,
                                               self.personnage.stats.pv + soin)
                reel = self.personnage.stats.pv - avant
                print(f"\n💚 La lumière vous enveloppe et vous soigne de {reel} PV !")
                print(f"❤️  PV : {self.personnage.stats.pv}/{self.personnage.stats.pv_max}")

            # Si la salle contient des monstres, lancer les combats un par un
            elif salle.a_monstre():
                fuite = False
                for monstre in salle.monstres if salle.monstres else [salle.monstre]:
                    if not self.personnage.stats.pv > 0:
                        break
                    if len(salle.monstres) > 1:
                        print(f"\n🔀 Prochain adversaire : {monstre.nom} !")
                    combat = Combat(self.personnage, monstre)
                    combat.commencer()

                    if self.personnage.stats.pv <= 0:
                        self.terminer_aventure(victoire=False)
                        fuite = True
                        break
                    elif monstre.is_alive():
                        # Fuite
                        self.terminer_aventure(victoire=False)
                        fuite = True
                        break
                    else:
                        print(f"\n✅ Vous avez vaincu {monstre.nom} !")

                if fuite:
                    break
            
            # Salle 5 : événement de choix d'arme
            if salle.contient_armes:
                nom_classe = self.personnage.classe.nom if self.personnage.classe else ""
                armes_proposees = get_armes_pour_classe(nom_classe, nombre=3)
                arme_choisie = choisir_arme(armes_proposees)
                self.personnage.equiper_arme(arme_choisie)
                print(f"📊 Nouvelles stats : {self.personnage.stats}")

            # Salle 8 : rencontre du PNJ
            if salle.npc:
                salle.npc.interagir(self.personnage)

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
            print("❌ AVENTURE TERMINÉE")
            print(f"{'='*50}")
            print(f"Vous avez abandonné à la salle {self.salle_actuelle}/{self.nombre_salles_total}.")
            print(f"Peut-être la prochaine fois, {self.personnage.prenom}...")
        
        print(f"{'='*50}\n")
    
    def obtenir_progression(self):
        """Retourne la progression actuelle"""
        return f"Salle {self.salle_actuelle}/{self.nombre_salles_total}"