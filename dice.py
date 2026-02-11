import random
import time
import sys


class Dice:
    def __init__(self, f=6, c="red", m="plastic"):
        if f < 1:
            raise ValueError("Un dé doit avoir au moins 1 face")
        self.faces = f
        self.color = c
        self.material = m

    def __str__(self):
        return f"This is a {self.color} {self.material} dice with {self.faces} faces"

    def __eq__(self, another_dice):
        return (self.faces == another_dice.faces and 
                self.color == another_dice.color and 
                self.material == another_dice.material)

    def roll(self, animated=False):
        """Lance le dé avec ou sans animation"""
        if animated:
            return self._roll_animated()
        return random.randint(1, self.faces)
    
    def _roll_animated(self):
        """Animation simple"""
        print("🎲 Lancer du dé...")
        
        for i in range(15):
            random_num = random.randint(1, self.faces)
            sys.stdout.write(f"\r   [ {random_num} ]")
            sys.stdout.flush()
            time.sleep(0.1)
        
        result = random.randint(1, self.faces)
        print(f"\r✨ [ {result} ] ✨")
        return result
    
    def is_critical(self, roll_result):
        """
        Vérifie si c'est un critique ou un échec critique
        Seulement pour D20 et D100
        
        Returns:
            str: "success" pour réussite critique (20 ou 100)
                 "fail" pour échec critique (1)
                 None pour un résultat normal
        """
        # Vérifier si le dé peut faire des critiques (D20 ou D100)
        if self.faces == 20 or self.faces == 100:
            if roll_result == self.faces:
                return "success"  # Réussite critique (20 ou 100)
            elif roll_result == 1:
                return "fail"  # Échec critique (1)
        
        return None  # Pas de critique
    
    def roll_with_critical(self, animated=False):
        """Lance le dé et détecte les critiques"""
        result = self.roll(animated)
        critical_type = self.is_critical(result)
        
        if critical_type == "success":
            self._display_critical_success()
        elif critical_type == "fail":
            self._display_critical_fail()
        
        return result, critical_type
    
    def _display_critical_success(self):
        """Animation pour réussite critique"""
        success_frames = [
            "🔥💥 RÉUSSITE CRITIQUE ! 💥🔥",
            "✨💥 RÉUSSITE CRITIQUE ! 💥✨",
            "⚡💥 RÉUSSITE CRITIQUE ! 💥⚡",
        ]
        
        for frame in success_frames * 2:
            sys.stdout.write(f"\r{frame}")
            sys.stdout.flush()
            time.sleep(0.15)
        print()
    
    def _display_critical_fail(self):
        """Animation pour échec critique"""
        fail_frames = [
            "💀😱 ÉCHEC CRITIQUE ! 😱💀",
            "❌😱 ÉCHEC CRITIQUE ! 😱❌",
            "💔😱 ÉCHEC CRITIQUE ! 😱💔",
        ]
        
        for frame in fail_frames * 2:
            sys.stdout.write(f"\r{frame}")
            sys.stdout.flush()
            time.sleep(0.15)
        print()
    
    def roll_damage(self, base_damage=0, animated=False):
        """
        Lance le dé pour des dégâts
        - Réussite critique : dégâts doublés
        - Échec critique : 0 dégâts (tu te blesses toi-même ou tu rates)
        """
        result, critical_type = self.roll_with_critical(animated)
        
        if critical_type == "success":
            # Réussite critique : dégâts x2
            total = (result + base_damage) * 2
            print(f"⚔️  Dégâts CRITIQUES : {total} (doublés !)")
            return total, critical_type
        
        elif critical_type == "fail":
            # Échec critique : aucun dégât (ou dégâts sur soi-même)
            print(f"💀 Échec critique ! Aucun dégât infligé...")
            return 0, critical_type
        
        else:
            # Lancer normal
            total = result + base_damage
            print(f"⚔️  Dégâts : {total}")
            return total, critical_type
    
    def roll_attack(self, target_defense=10, base_damage=5, animated=False):
        """
        Système complet d'attaque avec gestion des critiques
        - Réussite critique (20 ou 100) : touche automatiquement + dégâts x2
        - Échec critique (1) : rate automatiquement + effet négatif possible
        """
        print(f"\n🎯 Jet d'attaque (défense cible: {target_defense})")
        attack_roll, critical_type = self.roll_with_critical(animated)
        
        # Réussite critique : touche automatiquement
        if critical_type == "success":
            print("✅ Attaque réussie avec RÉUSSITE CRITIQUE !")
            damage = (attack_roll + base_damage) * 2
            print(f"⚔️  Dégâts CRITIQUES : {damage}")
            return {
                "hit": True,
                "attack_roll": attack_roll,
                "critical_type": critical_type,
                "total_damage": damage
            }
        
        # Échec critique : rate automatiquement
        elif critical_type == "fail":
            print("❌ ÉCHEC CRITIQUE ! Tu te blesses toi-même !")
            self_damage = random.randint(1, 3)  # Dégâts sur soi-même
            print(f"💔 Tu perds {self_damage} PV...")
            return {
                "hit": False,
                "attack_roll": attack_roll,
                "critical_type": critical_type,
                "total_damage": 0,
                "self_damage": self_damage
            }
        
        # Lancer normal
        else:
            if attack_roll >= target_defense:
                print("✅ Attaque réussie !")
                damage = attack_roll + base_damage
                print(f"⚔️  Dégâts : {damage}")
                return {
                    "hit": True,
                    "attack_roll": attack_roll,
                    "critical_type": None,
                    "total_damage": damage
                }
            else:
                print("❌ Attaque ratée !")
                return {
                    "hit": False,
                    "attack_roll": attack_roll,
                    "critical_type": None,
                    "total_damage": 0
                }
    
    def roll_many(self, n, animated=False):
        """Lance le dé n fois"""
        return [self.roll(animated) for _ in range(n)]


# # Tests et démonstration
# if __name__ == "__main__":
#     print("="*70)
#     print("🎮 SYSTÈME DE CRITIQUES COMPLET (Réussite ET Échec)")
#     print("="*70)
    
#     # TEST 1 : D20 avec critiques
#     print("\n" + "="*70)
#     print("TEST 1 : D20 - Réussite critique sur 20, Échec critique sur 1")
#     print("="*70)
    
#     d20 = Dice(f=20, c="gold", m="metal")
    
#     # Simulation pour montrer les différents cas
#     print("\n--- Simulation de plusieurs lancers ---")
#     for i in range(5):
#         print(f"\nLancer {i+1}:")
#         damage, crit_type = d20.roll_damage(base_damage=5, animated=True)
#         time.sleep(1.5)
    
#     # TEST 2 : Combat complet avec D20
#     print("\n" + "="*70)
#     print("⚔️  SIMULATION DE COMBAT")
#     print("="*70)
    
#     enemy_defense = 12
#     player_hp = 50
    
#     for round_num in range(5):
#         print(f"\n{'='*70}")
#         print(f"⚔️  ROUND {round_num + 1} - PV du joueur : {player_hp}")
#         print(f"{'='*70}")
        
#         result = d20.roll_attack(
#             target_defense=enemy_defense,
#             base_damage=8,
#             animated=True
#         )
        
#         if result["hit"]:
#             if result["critical_type"] == "success":
#                 print(f"\n💀💥 COUP DÉVASTATEUR ! {result['total_damage']} points de dégâts !")
#             else:
#                 print(f"\n💀 L'ennemi prend {result['total_damage']} points de dégâts !")
        
#         # Gérer les dégâts sur soi-même en cas d'échec critique
#         if "self_damage" in result:
#             player_hp -= result["self_damage"]
#             print(f"😰 PV restants : {player_hp}")
        
#         time.sleep(2)
    
#     # TEST 3 : D100
#     print("\n" + "="*70)
#     print("TEST 3 : D100 - Réussite critique sur 100, Échec critique sur 1")
#     print("="*70)
    
#     d100 = Dice(f=100, c="silver", m="metal")
    
#     for i in range(3):
#         print(f"\nLancer {i+1}:")
#         damage, crit_type = d100.roll_damage(base_damage=10, animated=True)
#         time.sleep(1.5)
    
#     # TEST 4 : D6 (pas de critiques)
#     print("\n" + "="*70)
#     print("TEST 4 : D6 - Pas de système de critiques")
#     print("="*70)
    
#     d6 = Dice(f=6, c="red", m="plastic")
    
#     for i in range(3):
#         print(f"\nLancer {i+1}:")
#         damage, crit_type = d6.roll_damage(base_damage=3, animated=True)
#         time.sleep(1.5)
    
#     print("\n" + "="*70)
#     print("FIN DES TESTS")
#     print("="*70)


if __name__ == "__main__":
    d2 = Dice(2, "golden", "coin")
    d4 = Dice(4, "blue", "wood")
    d6 = Dice(6, "green", "metal")
    d8 = Dice(8, "red", "obsidian")
    d10 = Dice(10, "violet", "bob")
    d12 = Dice(12, "green", "plastic")
    d20 = Dice(20, "blue", "platic")
    d100 = Dice(100, "scarlet", "strontium")


# print(d2.roll())
# print(d4.roll())
# print(d6.roll())
# print(d8.roll())
# print(d10.roll())
# print(d12.roll())
# print(d20.roll())
# print(d100.roll())

print("=== Test d'attaque ===")
attack_roll = d20.roll_many(20,animated=True)

print("\n=== Dégâts ===")
damage_rolls = d6.roll_many(3, animated=True)
print(f"\nDégâts totaux : {sum(damage_rolls)}")