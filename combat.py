import random
from dice import Dice


class Combat:
    """Système de combat tour par tour"""
    
    def __init__(self, personnage, monstre):
        self.personnage = personnage
        self.monstre = monstre
        self.de20 = Dice(20, "gold", "metal")
        self.tour = 0
        self.en_cours = True
    
    def commencer(self):
        """Démarre le combat"""
        print(f"\n{'⚔️ '*25}")
        print(f"⚔️  COMBAT COMMENCE !")
        print(f"{'⚔️ '*25}\n")
        print(f"{self.personnage.prenom} {self.personnage.nom} VS {self.monstre.nom}")
        
        self.afficher_stats_combat()
        
        # Déterminer l'ordre d'initiative selon la vitesse
        vit_joueur  = self.personnage.stats.vitesse
        vit_monstre = getattr(self.monstre, 'vitesse', 3)
        if vit_joueur >= vit_monstre:
            print(f"\n💨 {self.personnage.prenom} est plus rapide et agit en premier ! (VIT {vit_joueur} vs {vit_monstre})")
            joueur_first = True
        else:
            print(f"\n💨 {self.monstre.nom} est plus rapide et agit en premier ! (VIT {vit_monstre} vs {vit_joueur})")
            joueur_first = False

        # Boucle principale du combat
        while self.en_cours:
            self.tour += 1
            print(f"\n{'─'*60}")
            print(f"🎲 TOUR {self.tour}")
            print(f"{'─'*60}")

            if joueur_first:
                # Joueur en premier
                if not self.tour_joueur():
                    break
                if not self.monstre.is_alive():
                    self.victoire()
                    break
                # Tour du monstre
                if hasattr(self.monstre, 'peut_attaquer') and not self.monstre.peut_attaquer:
                    print(f"\n💤 {self.monstre.nom} ne fait rien... (C'est un mannequin d'entraînement)")
                else:
                    self.tour_monstre()
                if self.personnage.stats.pv <= 0:
                    self.defaite()
                    break
            else:
                # Monstre en premier
                if hasattr(self.monstre, 'peut_attaquer') and not self.monstre.peut_attaquer:
                    print(f"\n💤 {self.monstre.nom} ne fait rien... (C'est un mannequin d'entraînement)")
                else:
                    self.tour_monstre()
                if self.personnage.stats.pv <= 0:
                    self.defaite()
                    break
                if not self.tour_joueur():
                    break
                if not self.monstre.is_alive():
                    self.victoire()
                    break
    
    def tour_joueur(self):
        """Gère le tour du joueur"""
        print(f"\n⚔️  C'est votre tour, {self.personnage.prenom} !")

        while True:
            action = input("Que voulez-vous faire ? (1: Attaquer | 2: Équipement | 3: Fuir) : ").strip()

            if action == "1":
                # Sous-menu type d'attaque
                while True:
                    print(f"\n  Type d'attaque :")
                    print(f"  1. ⚔️  Attaque physique  (ATK: {self.personnage.stats.attaque})")
                    print(f"  2. ✨ Attaque magique   (ATK MAG: {self.personnage.stats.attaque_magique})")
                    print(f"  3. ↩️  Retour")
                    choix_type = input("  Votre choix : ").strip()
                    if choix_type == "1":
                        self.attaque_joueur(magique=False)
                        return True
                    elif choix_type == "2":
                        self.attaque_joueur(magique=True)
                        return True
                    elif choix_type == "3":
                        break  # Retour au menu principal du tour
                    else:
                        print("  ❌ Choix invalide.")
            elif action == "2":
                self.personnage.afficher_equipement()
            elif action == "3":
                print(f"\n🏃 Vous prenez la fuite !")
                self.en_cours = False
                return False
            else:
                print("❌ Choix invalide. Tapez 1 pour attaquer, 2 pour l'équipement ou 3 pour fuir.")
    
    def attaque_joueur(self, magique=False):
        """Le joueur attaque le monstre (physique ou magique)"""
        stat_atk  = self.personnage.stats.attaque_magique if magique else self.personnage.stats.attaque
        label_atk = "✨ magique" if magique else "⚔️  physique"
        print(f"\n{label_atk.strip()}  Vous attaquez {self.monstre.nom} !")

        jet, critical_type = self.de20.roll_with_critical(animated=True)

        if critical_type == "success":
            degats_base = stat_atk * 2
            print(f"💥 Dégâts CRITIQUES : {degats_base} !")
        elif critical_type == "fail":
            degats_base = 0
            print(f"💀 Vous ratez complètement votre attaque !")
        else:
            multiplicateur = 0.75 + (jet / 20) * 0.25
            degats_base = int(stat_atk * multiplicateur)
            if jet >= 15:
                print(f"Belle frappe ! (Jet: {jet}/20)")
            elif jet >= 10:
                print(f"Coup correct. (Jet: {jet}/20)")
            else:
                print(f"Coup faible... (Jet: {jet}/20)")

        if degats_base > 0:
            degats_infliges = self.monstre.take_damage(degats_base, magique=magique)
            type_label = "magiques" if magique else "physiques"
            print(f"Vous infligez {degats_infliges} dégâts {type_label} à {self.monstre.nom} !")
        else:
            print(f"Aucun dégât infligé...")

        self.monstre.afficher_stats()
    
    def tour_monstre(self):
        """Le monstre attaque le joueur (physique ou magique selon les dégâts nets estimés)"""
        print(f"\n🔴 C'est au tour de {self.monstre.nom} !")

        atk_phys = getattr(self.monstre, 'attaque', 0)
        atk_mag  = getattr(self.monstre, 'attaque_magique', 0)

        # Calculer les dégâts nets estimés pour chaque type
        degats_nets_phys = max(0, atk_phys - self.personnage.stats.defense)
        degats_nets_mag  = max(0, atk_mag  - self.personnage.stats.defense_magique)

        # Un monstre sans ATK MAG ne peut pas attaquer magiquement
        peut_attaquer_magique = atk_mag > 0

        # Choisir l'attaque qui infligera le plus de dégâts nets
        if peut_attaquer_magique and degats_nets_mag >= degats_nets_phys:
            magique = True
            stat_atk = atk_mag
            print(f"✨ {self.monstre.nom} prépare une attaque magique !")
        else:
            magique = False
            stat_atk = atk_phys

        jet, critical_type = self.de20.roll_with_critical(animated=False)

        if critical_type == "success":
            degats_base = stat_atk * 2
            print(f"💥 {self.monstre.nom} frappe avec une force CRITIQUE !")
        elif critical_type == "fail":
            degats_base = 0
            print(f"😅 {self.monstre.nom} rate complètement son attaque !")
        else:
            # Plancher à 0.75 pour que les monstres restent menaçants même sur mauvais jet
            multiplicateur = 0.75 + (jet / 20) * 0.25
            degats_base = int(stat_atk * multiplicateur)
            if jet >= 15:
                print(f"😤 {self.monstre.nom} frappe fort ! (Jet: {jet}/20)")
            elif jet >= 10:
                print(f"😠 {self.monstre.nom} vous attaque. (Jet: {jet}/20)")
            else:
                print(f"😑 {self.monstre.nom} frappe faiblement... (Jet: {jet}/20)")

        if degats_base > 0:
            resistance = self.personnage.stats.defense_magique if magique else self.personnage.stats.defense
            type_res   = "DEF MAG" if magique else "DEF"
            degats_reduits = max(0, degats_base - resistance)
            self.personnage.stats.pv -= degats_reduits
            if degats_reduits > 0:
                print(f"🩸 Vous subissez {degats_reduits} dégâts ! ({degats_base} - {resistance} {type_res})")
            else:
                print(f"🛡️  Votre défense absorbe entièrement l'attaque !")
        else:
            print(f"🛡️  Vous ne subissez aucun dégât.")

        barre_vie = self._creer_barre_vie(self.personnage.stats.pv, self.personnage.stats.pv_max)
        print(f"❤️  {self.personnage.prenom} : {barre_vie} {self.personnage.stats.pv}/{self.personnage.stats.pv_max} PV")
    
    def afficher_stats_combat(self):
        """Affiche les stats des deux combattants"""
        print(f"\n{'='*60}")
        
        # Stats du joueur
        barre_vie_joueur = self._creer_barre_vie(self.personnage.stats.pv, self.personnage.stats.pv_max)
        print(f"👤 {self.personnage.prenom} {self.personnage.nom}")
        print(f"   {barre_vie_joueur} {self.personnage.stats.pv}/{self.personnage.stats.pv_max} PV")
        print(f"   ⚔️  ATK: {self.personnage.stats.attaque} | 🛡️  DEF: {self.personnage.stats.defense} | ✨ ATK MAG: {self.personnage.stats.attaque_magique} | 🔮 DEF MAG: {self.personnage.stats.defense_magique} | 💨 VIT: {self.personnage.stats.vitesse}")
        
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
        print(f"Combat terminé en {self.tour} tours.")
        self.en_cours = False

        # Distribuer xp et gold
        reward = getattr(self.monstre, 'reward', None)
        if reward:
            self.personnage.gagner_xp(reward.get("xp", 0), reward.get("gold", 0))
    
    def defaite(self):
        """Le joueur a perdu"""
        print(f"\n{'💀'*30}")
        print(f"💀 DÉFAITE...")
        print(f"{'💀'*30}")
        print(f"\n{self.personnage.prenom} a été vaincu par {self.monstre.nom}...")
        print(f"Combat terminé en {self.tour} tours.\n")
        self.en_cours = False