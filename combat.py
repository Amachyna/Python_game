import random
from dice import Dice
from inventaire import PotionSoin, PotionPerfection
from beastiary import Boss


class Combat:
    """Système de combat tour par tour — supporte 1 ou plusieurs monstres"""

    def __init__(self, equipe_ou_personnage, monstres):
        # Accepte une Equipe ou un personnage seul
        from equipe import Equipe
        if isinstance(equipe_ou_personnage, Equipe):
            self.equipe    = equipe_ou_personnage
            self.personnage = equipe_ou_personnage.joueur
        else:
            from equipe import Equipe as Eq
            self.equipe    = Eq(equipe_ou_personnage)
            self.personnage = equipe_ou_personnage
        # Accepte un monstre seul ou une liste
        if isinstance(monstres, list):
            self.monstres = [m for m in monstres]
        else:
            self.monstres = [monstres]
        self.monstre = self.monstres[0]  # Cible active par défaut
        self.de20 = Dice(20, "gold", "metal")
        self.tour = 0
        self.en_cours = True
        self.tours_perfection = 0

    # ─── Lancement ───────────────────────────────────────────────────────────

    def commencer(self):
        """Démarre le combat"""
        print(f"\n{'⚔️ '*25}")
        print(f"⚔️  COMBAT COMMENCE !")
        print(f"{'⚔️ '*25}\n")
        noms = " & ".join(m.nom for m in self.monstres)
        print(f"{self.personnage.prenom} {self.personnage.nom} VS {noms}")

        self.afficher_stats_combat()

        # Afficher l'ordre d'initiative
        self._afficher_initiative()

        while self.en_cours:
            self.tour += 1
            print(f"\n{'─'*60}")
            print(f"🎲 TOUR {self.tour}")
            print(f"{'─'*60}")

            # Construire la file d'initiative du tour (tous les vivants triés par VIT décroissante)
            file = self._construire_file_initiative()

            for acteur in file:
                if not self.en_cours:
                    break

                if acteur["type"] == "membre":
                    membre = acteur["obj"]
                    if membre.stats.pv <= 0:
                        continue  # Mort entre-temps
                    self.personnage = membre
                    if not self.tour_joueur(membre):
                        self.en_cours = False
                        break
                    if not self._monstres_vivants():
                        self.victoire()
                        break

                elif acteur["type"] == "monstre":
                    monstre = acteur["obj"]
                    if not monstre.is_alive():
                        continue  # Mort entre-temps
                    if hasattr(monstre, 'peut_attaquer') and not monstre.peut_attaquer:
                        print(f"\n💤 {monstre.nom} ne fait rien... (C'est un mannequin d'entraînement)")
                    else:
                        self.tour_monstre(monstre)
                    if not self.equipe.est_en_vie():
                        self.defaite()
                        break

            self.personnage = self.equipe.joueur  # Remettre le joueur principal

    # ─── Tours ───────────────────────────────────────────────────────────────

    def _construire_file_initiative(self):
        """Retourne la liste de tous les acteurs vivants triés par VIT décroissante."""
        file = []
        for m in self.equipe.membres_vivants():
            file.append({"type": "membre", "obj": m, "vit": m.stats.vitesse})
        for m in self.monstres:
            if m.is_alive():
                file.append({"type": "monstre", "obj": m, "vit": getattr(m, "vitesse", 3)})
        # Tri décroissant ; égalité : membres avant monstres (avantage joueur)
        file.sort(key=lambda x: (x["vit"], x["type"] == "membre"), reverse=True)
        return file

    def _afficher_initiative(self):
        """Affiche l'ordre d'initiative au début du combat."""
        file = self._construire_file_initiative()
        print(f"\n💨 Ordre d'initiative :")
        for i, acteur in enumerate(file, 1):
            obj = acteur["obj"]
            if acteur["type"] == "membre":
                print(f"   {i}. {obj.prenom} {obj.nom} (VIT {obj.stats.vitesse})")
            else:
                print(f"   {i}. {obj.nom} (VIT {getattr(obj, 'vitesse', 3)})")

    def tour_joueur(self, membre=None):
        """Gère le tour d'un membre de l'équipe"""
        if membre is None:
            membre = self.personnage
        print(f"\n⚔️  C'est le tour de {membre.prenom} !")

        while True:
            if self.tours_perfection > 0:
                print(f"  ⚗️  Double attaque active : {self.tours_perfection} tour(s) restant(s)")

            action = input(
                "Que voulez-vous faire ? (1: Attaquer | 2: Inventaire | 3: Stock équipement | 4: Équipement | 5: Fuir) : "
            ).strip()

            if action == "1":
                # Choisir la cible si plusieurs monstres vivants
                self._choisir_cible()
                # Choisir le type d'attaque
                while True:
                    print(f"\n  Type d'attaque :")
                    print(f"  1. ⚔️  Attaque physique  (ATK: {self.personnage.stats.attaque})")
                    print(f"  2. ✨ Attaque magique   (ATK MAG: {self.personnage.stats.attaque_magique})")
                    print(f"  3. ↩️  Retour")
                    choix_type = input("  Votre choix : ").strip()
                    if choix_type == "1":
                        self._executer_attaque(magique=False)
                        return True
                    elif choix_type == "2":
                        self._executer_attaque(magique=True)
                        return True
                    elif choix_type == "3":
                        break
                    else:
                        print("  ❌ Choix invalide.")

            elif action == "2":
                # Potions
                utilise = self.equipe.inventaire.choisir_et_utiliser(
                    membre, combat=self, equipe=self.equipe)
                if utilise:
                    return True

            elif action == "3":
                # Stock armes/armures — consulter sans consommer le tour
                self.equipe.stock.gerer(self.equipe)

            elif action == "4":
                membre.afficher_equipement()

            elif action == "5":
                print(f"\n🏃 Vous prenez la fuite !")
                self.en_cours = False
                return False

            else:
                print("❌ Choix invalide. Tapez 1-5.")

    def _choisir_cible(self):
        """Demande au joueur de choisir sa cible si plusieurs monstres vivants"""
        vivants = [m for m in self.monstres if m.is_alive()]
        if len(vivants) <= 1:
            self.monstre = vivants[0] if vivants else self.monstre
            return

        print(f"\n  🎯 Choisissez votre cible :")
        for i, m in enumerate(vivants, 1):
            barre = self._creer_barre_vie(m.pv, m.pv_max)
            print(f"  [{i}] {m.nom} {barre} {m.pv}/{m.pv_max} PV")

        while True:
            choix = input(f"  Votre cible (1-{len(vivants)}) : ").strip()
            if choix.isdigit() and 1 <= int(choix) <= len(vivants):
                self.monstre = vivants[int(choix) - 1]
                print(f"  🎯 Cible : {self.monstre.nom}")
                return
            print("  ❌ Choix invalide.")

    def tour_monstre(self, monstre=None):
        """Un monstre attaque le joueur"""
        if monstre is None:
            monstre = self.monstre
        print(f"\n🔴 {monstre.nom} attaque !")

        atk_phys = getattr(monstre, 'attaque', 0)
        atk_mag  = getattr(monstre, 'attaque_magique', 0)

        degats_nets_phys = max(0, atk_phys - self.personnage.stats.defense)
        degats_nets_mag  = max(0, atk_mag  - self.personnage.stats.defense_magique)
        peut_attaquer_magique = atk_mag > 0

        if peut_attaquer_magique and degats_nets_mag >= degats_nets_phys:
            magique  = True
            stat_atk = atk_mag
            print(f"✨ {monstre.nom} prépare une attaque magique !")
        else:
            magique  = False
            stat_atk = atk_phys

        jet, critical_type = self.de20.roll_with_critical(animated=False)

        if critical_type == "success":
            degats_base = int(stat_atk * 1.5)
            print(f"💥 {monstre.nom} frappe avec une force CRITIQUE !")
        elif critical_type == "fail":
            degats_base = 0
            print(f"😅 {monstre.nom} rate complètement son attaque !")
        else:
            multiplicateur = 0.75 + (jet / 20) * 0.25
            degats_base = int(stat_atk * multiplicateur)
            if jet >= 15:
                print(f"😤 {monstre.nom} frappe fort ! (Jet: {jet}/20)")
            elif jet >= 10:
                print(f"😠 {monstre.nom} vous attaque. (Jet: {jet}/20)")
            else:
                print(f"😑 {monstre.nom} frappe faiblement... (Jet: {jet}/20)")

        if degats_base > 0:
            resistance = self.personnage.stats.defense_magique if magique else self.personnage.stats.defense
            type_res   = "DEF MAG" if magique else "DEF"
            degats_reduits = max(1, degats_base - resistance)
            self.personnage.stats.pv -= degats_reduits
            print(f"🩸 Vous subissez {degats_reduits} dégâts ! ({degats_base} - {resistance} {type_res})")
        else:
            print(f"🛡️  Vous ne subissez aucun dégât.")

        barre_vie = self._creer_barre_vie(self.personnage.stats.pv, self.personnage.stats.pv_max)
        print(f"❤️  {self.personnage.prenom} : {barre_vie} {self.personnage.stats.pv}/{self.personnage.stats.pv_max} PV")

    # ─── Attaques joueur ─────────────────────────────────────────────────────

    def activer_perfection(self, duree):
        self.tours_perfection = duree
        print(f"⚗️  Double attaque active pour {duree} tours !")

    def _executer_attaque(self, magique=False):
        """Exécute une ou deux attaques selon la perfection active"""
        self.attaque_joueur(magique=magique)
        # Vérifier si la cible est morte après la première attaque
        if not self.monstre.is_alive():
            self._annoncer_mort_monstre(self.monstre)

        if self.tours_perfection > 0:
            if self._monstres_vivants():
                print(f"\n⚗️  DOUBLE ATTAQUE !")
                # Re-choisir la cible si la première est morte
                self._choisir_cible()
                self.attaque_joueur(magique=magique)
                if not self.monstre.is_alive():
                    self._annoncer_mort_monstre(self.monstre)
            self.tours_perfection -= 1
            if self.tours_perfection > 0:
                print(f"   ({self.tours_perfection} tour(s) de double attaque restant(s))")
            else:
                print(f"   (L'effet de la potion de perfection s'est dissipé.)")

    def attaque_joueur(self, magique=False):
        """Le joueur attaque la cible active"""
        stat_atk  = self.personnage.stats.attaque_magique if magique else self.personnage.stats.attaque
        label_atk = "✨ Attaque magique" if magique else "⚔️  Attaque physique"
        print(f"\n{self.personnage.prenom} — {label_atk} sur {self.monstre.nom} !")

        jet, critical_type = self.de20.roll_with_critical(animated=True)

        if critical_type == "success":
            degats_base = int(stat_atk * 1.5)
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

    # ─── Utilitaires ─────────────────────────────────────────────────────────

    def _monstres_vivants(self):
        return any(m.is_alive() for m in self.monstres)

    def _annoncer_mort_monstre(self, monstre):
        """Annonce la mort d'un monstre et distribue sa récompense"""
        print(f"\n💀 {monstre.nom} est vaincu !")
        reward = getattr(monstre, 'reward', None)
        if reward:
            xp   = reward.get("xp", 0)
            gold = reward.get("gold", 0)
            for membre in self.equipe.membres_vivants():
                membre.gagner_xp(xp, gold)
        # Mettre à jour la cible si c'était la cible active
        vivants = [m for m in self.monstres if m.is_alive()]
        if vivants:
            self.monstre = vivants[0]
            print(f"🎯 Nouveau cible : {self.monstre.nom}")

    def afficher_stats_combat(self):
        """Affiche les stats du joueur et de tous les monstres"""
        print(f"\n{'='*60}")
        for i, m in enumerate(self.equipe.membres):
            statut = "✅" if m.stats.pv > 0 else "💀"
            role   = " (Principal)" if i == 0 else " (Compagnon)"
            barre  = self._creer_barre_vie(m.stats.pv, m.stats.pv_max)
            print(f"👤 {statut} {m.prenom} {m.nom}{role}")
            print(f"   {barre} {m.stats.pv}/{m.stats.pv_max} PV")
            print(f"   ⚔️  ATK: {m.stats.attaque} | 🛡️  DEF: {m.stats.defense} | "
                  f"✨ ATK MAG: {m.stats.attaque_magique} | "
                  f"🔮 DEF MAG: {m.stats.defense_magique} | "
                  f"💨 VIT: {m.stats.vitesse}")
        for m in self.monstres:
            m.afficher_stats()
        print(f"{'='*60}")

    def _creer_barre_vie(self, pv, pv_max):
        longueur_barre = 20
        pourcentage = pv / pv_max if pv_max > 0 else 0
        blocs_pleins = int(pourcentage * longueur_barre)
        blocs_vides  = longueur_barre - blocs_pleins
        return f"[{'█' * blocs_pleins}{'░' * blocs_vides}]"

    def victoire(self):
        """Tous les monstres sont vaincus"""
        print(f"\n{'🏆'*30}")
        print(f"🏆 VICTOIRE !")
        print(f"{'🏆'*30}")
        noms = " & ".join(m.nom for m in self.monstres)
        equipe_noms = " & ".join(f"{m.prenom}" for m in self.equipe.membres_vivants())
        print(f"\n{equipe_noms} {'ont' if len(self.equipe.membres_vivants()) > 1 else 'a'} vaincu {noms} !")
        print(f"Combat terminé en {self.tour} tours.")
        self.en_cours = False
        # Les XP/gold ont déjà été distribués à la mort de chaque monstre

        # Soin total si boss vaincu
        est_boss = any(isinstance(m, Boss) for m in self.monstres)
        if est_boss:
            print(f"\n✨ Victoire contre un boss ! Toute l'équipe est soignée entièrement !")
            for membre in self.equipe.membres:
                membre.stats.pv = membre.stats.pv_max
                print(f"   ❤️  {membre.prenom} : {membre.stats.pv}/{membre.stats.pv_max} PV")

        # Drop de potion (25% par monstre vaincu, après le combat entier)
        self._tenter_drop_potions()

    def _tenter_drop_potions(self):
        """25% de chance par monstre vaincu de dropper une potion (après le combat)"""
        for monstre in self.monstres:
            if random.random() < 0.25:
                # 50/50 entre potion de soin et potion de perfection
                if random.random() < 0.5:
                    objet = PotionSoin()
                else:
                    objet = PotionPerfection()
                # Donner au premier membre vivant avec de la place
                if self.equipe.inventaire.ajouter(objet):
                    print(f"\n🎁 {monstre.nom} a droppé : {objet} → ajouté à l'inventaire de l'équipe !")

    def defaite(self):
        print(f"\n{'💀'*30}")
        print(f"💀 DÉFAITE...")
        print(f"{'💀'*30}")
        vivants_monstres = [m.nom for m in self.monstres if m.is_alive()]
        print(f"\nVotre équipe a été vaincue par {' & '.join(vivants_monstres)}...")
        print(f"Combat terminé en {self.tour} tours.\n")
        self.en_cours = False