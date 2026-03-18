import random
from beastiary import (TrainingDummy, ratempereur, chauve_souris, Slime, rat, ratgéant,
                        loup_alpha, araignee_geante, goblin_archer, ent,
                        esprit_foret, sanglier_enrage,
                        gobelin_sergant, roi_gobelin)
from combat import Combat
from weapons import get_armes_pour_classe, choisir_arme
from npc import Marchand
from inventaire import PotionSoin, PotionPerfection
from dialogues.villageois import VICTOIRE_SERGANT
from equipe import Equipe, creer_compagnon

# Monstres disponibles dans les salles aléatoires
# Pool de monstres selon la progression dans les salles
MONSTRES_DEBUT  = [chauve_souris, Slime, rat]                              # Salles 2-8
MONSTRES_MILIEU = [chauve_souris, Slime, rat, ratgéant]                    # Salles 9-15
MONSTRES_FORET  = [loup_alpha, araignee_geante, goblin_archer, ent,
                   esprit_foret, sanglier_enrage]                           # Salles 16-30


class Salle:
    """Classe représentant une salle dans l'aventure"""
    
    def __init__(self, numero):
        self.numero = numero
        self.monstre = None
        self.monstres = []        # Pour les salles avec plusieurs monstres
        self.contient_armes = (numero == 5)
        self.est_salle_soin = False
        self.est_salle_loot = False
        self.npc = None

        # Salles scriptées
        if numero == 1:
            self.monstre = TrainingDummy()
        elif numero == 15:
            self.monstre = ratempereur()
        elif numero == 20:
            self.monstre = gobelin_sergant()
        elif numero == 30:
            self.monstre = roi_gobelin()
        elif numero == 8:
            self.npc = Marchand()
        elif numero not in (1, 5, 8, 15, 20, 30):
            # Salles libres : 65% monstre(s), 25% soin, 10% loot
            tirage = random.random()
            if tirage < 0.65:
                nb = random.randint(1, 2)
                if numero >= 16:
                    pool = MONSTRES_FORET
                elif numero >= 9:
                    pool = MONSTRES_MILIEU
                else:
                    pool = MONSTRES_DEBUT
                self.monstres = [random.choice(pool)() for _ in range(nb)]
                self.monstre = self.monstres[0]
            elif tirage < 0.90:
                self.est_salle_soin = True
            else:
                self.est_salle_loot = True
    
    def afficher(self):
        """Affiche la salle actuelle"""
        print(f"\n{'='*50}")
        print(f"🚪 SALLE {self.numero}/30")
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
        elif self.est_salle_loot:
            print(f"💎 Un objet scintille dans l'obscurité...")
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
    
    def __init__(self, equipe_ou_personnage):
        if isinstance(equipe_ou_personnage, Equipe):
            self.equipe     = equipe_ou_personnage
            self.personnage = equipe_ou_personnage.joueur
        else:
            self.equipe     = Equipe(equipe_ou_personnage)
            self.personnage = equipe_ou_personnage
        self.salle_actuelle = 0
        self.nombre_salles_total = 30
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
            
            # Salle loot
            if salle.est_salle_loot:
                self._gerer_salle_loot()

            # Salle soin
            elif salle.est_salle_soin:
                print(f"\n💚 La lumière dorée enveloppe toute l'équipe !")
                for m in self.equipe.membres:
                    if m.stats.pv > 0:
                        soin = max(1, int(m.stats.pv_max * 0.25))
                        avant = m.stats.pv
                        m.stats.pv = min(m.stats.pv_max, m.stats.pv + soin)
                        reel = m.stats.pv - avant
                        print(f"   {m.prenom} récupère {reel} PV → {m.stats.pv}/{m.stats.pv_max} PV")

            # Si la salle contient des monstres, un seul combat avec tous
            elif not salle.npc and not salle.est_salle_loot and salle.a_monstre():
                liste = salle.monstres if salle.monstres else [salle.monstre]
                combat = Combat(self.equipe, liste)
                combat.commencer()

                if not self.equipe.est_en_vie():
                    self.terminer_aventure(victoire=False)
                    break
                elif any(m.is_alive() for m in liste):
                    # Fuite
                    self.terminer_aventure(victoire=False)
                    break
            
            # Salle 5 : événement de choix d'arme
            if salle.contient_armes:
                nom_classe = self.equipe.joueur.classe.nom if self.equipe.joueur.classe else ""
                armes_proposees = get_armes_pour_classe(nom_classe, nombre=3)
                arme_choisie = choisir_arme(armes_proposees)
                self.equipe.joueur.equiper_arme(arme_choisie)
                print(f"📊 Nouvelles stats : {self.equipe.joueur.stats}")

            # Salle 8 : rencontre du PNJ
            if salle.npc:
                salle.npc.interagir(self.equipe.joueur)

            # Salle 15 : libérer le compagnon + transition forêt
            if self.salle_actuelle == 15 and len(self.equipe.membres) == 1:
                monstres_salle = salle.monstres if salle.monstres else ([salle.monstre] if salle.monstre else [])
                if not any(m.is_alive() for m in monstres_salle):
                    self._liberer_compagnon()
                    self._transition_foret()

            # Salle 20 : dialogue villageois après victoire contre le Gobelin Sergant
            if self.salle_actuelle == 20:
                monstres_salle = salle.monstres if salle.monstres else ([salle.monstre] if salle.monstre else [])
                if not any(m.is_alive() for m in monstres_salle):
                    self._dialogue_villageois()

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
    
    def _transition_foret(self):
        """Message de transition entre les égouts et la forêt"""
        print(f"\n{'='*60}")
        print("🌲 VOUS SORTEZ DES ÉGOUTS...")
        print(f"{'='*60}")
        print("L'air frais de la forêt vous accueille après l'obscurité des égouts.")
        print("Mais la forêt n'est pas sûre... de nouveaux dangers vous attendent.")
        input("  [ Appuyez sur Entrée pour continuer... ]")

    def _dialogue_villageois(self):
        """Dialogue des villageois après la victoire contre le Gobelin Sergant"""
        print(f"\n{'='*60}")
        print("🏘️  VOUS ARRIVEZ AU VILLAGE...")
        print(f"{'='*60}")
        print(f"\n🧑 Villageois :")
        print()
        for ligne in VICTOIRE_SERGANT.split('\n'):
            print(f"   {ligne}")
        print(f"{'='*60}")
        input("  [ Appuyez sur Entrée pour continuer... ]")

    def _liberer_compagnon(self):
        """Déclenche la rencontre du compagnon après la victoire contre le Rat Empereur"""
        print(f"\n{'='*60}")
        print("🔓 Dans un recoin sombre de la salle, vous apercevez une silhouette...")
        print("   Un survivant, enchaîné au mur. Vous brisez ses chaînes.")
        print(f"{'='*60}")
        compagnon = creer_compagnon(self.personnage)
        self.equipe.ajouter_membre(compagnon)

    def _gerer_salle_loot(self):
        """Gère l'événement d'une salle à butin"""
        tirage = random.random()

        if tirage < 0.40:
            xp = random.randint(15, 30)
            print(f"\n💡 Vous trouvez des inscriptions runiques et gagnez {xp} XP !")
            self.personnage.gagner_xp(xp, 0)

        elif tirage < 0.70:
            gold = random.randint(5, 20)
            self.personnage.gold += gold
            print(f"\n💰 Vous trouvez une bourse cachée : +{gold} Gold !")
            print(f"   Gold total : {self.personnage.gold}")

        elif tirage < 0.85:
            objet = PotionSoin()
            if self.equipe.inventaire.ajouter(objet):
                print(f"\n🧪 Vous trouvez une Potion de soin !")
                print(f"   Inventaire équipe : {self.equipe.inventaire}")

        else:
            objet = PotionPerfection()
            if self.equipe.inventaire.ajouter(objet):
                print(f"\n⚗️  Vous trouvez une Potion de perfection ! (Rare !)")
                print(f"   Inventaire équipe : {self.equipe.inventaire}")

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