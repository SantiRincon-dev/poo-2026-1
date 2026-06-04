from __future__ import annotations

import random
import time
from typing import List


class TypeRelations:
    def __init__(self) -> None:
        self.type_chart: dict[str, dict[str, float]] = {
            "Fire": {
                "Fire": 0.5,
                "Water": 0.5,
                "Grass": 2.0,
                "Electric": 1.0,
                "Ground": 1.0,
            },
            "Water": {
                "Fire": 2.0,
                "Water": 0.5,
                "Grass": 0.5,
                "Electric": 1.0,
                "Ground": 2.0,
            },
            "Grass": {
                "Fire": 0.5,
                "Water": 2.0,
                "Grass": 0.5,
                "Electric": 1.0,
                "Ground": 2.0,
            },
            "Electric": {
                "Fire": 1.0,
                "Water": 2.0,
                "Grass": 0.5,
                "Electric": 0.5,
                "Ground": 0.0,
            },
            "Ground": {
                "Fire": 2.0,
                "Water": 1.0,
                "Grass": 0.5,
                "Electric": 2.0,
                "Ground": 1.0,
            },
        }

    def get_effectiveness(self, attack_type: str, defender_types: List[str]) -> float:

        multiplier: float = 1.0

        for defender in defender_types:
            if attack_type in self.type_chart:
                if defender in self.type_chart[attack_type]:
                    multiplier *= self.type_chart[attack_type][defender]

                else:
                    multiplier *= 1.0

            else:
                multiplier *= 1.0

        return multiplier


class Stats:
    def __init__(
        self,
        hp: float,
        attack: float,
        defense: float,
        special_attack: float,
        special_defense: float,
        speed: float,
    ):

        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed

    def __str__(self):

        return (
            f"HP: {self.hp}, "
            f"Attack: {self.attack}, "
            f"Defense: {self.defense}, "
            f"Sp. Attack: {self.special_attack}, "
            f"Sp. Defense: {self.special_defense}, "
            f"Speed: {self.speed}"
        )


class Move:
    def __init__(self, name: str, type: str, power: float, accuracy: int, pp: int):

        self._name = name
        self._type = type
        self._power = power
        self._accuracy = accuracy
        self._pp = pp

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def power(self) -> float:
        return self._power

    @property
    def accuracy(self) -> int:
        return self._accuracy

    @property
    def pp(self) -> int:
        return self._pp


class Moveset:
    def __init__(self, moves: List[Move] | None = None):

        self.moves: List[Move] = []

        if moves:
            for move in moves:
                self.add_move(move)

    def add_move(self, move: Move) -> bool:

        if len(self.moves) < 4:
            self.moves.append(move)

            print(f"The Pokémon learned {move.name}!")

            time.sleep(0.5)

            return True

        else:
            print(f"The Pokémon tried to learn {move.name}, but it already knows 4 moves.")

            time.sleep(0.5)

            return False

    def remove_move(self, index: int) -> bool:

        if 0 <= index < len(self.moves):
            removed_move = self.moves.pop(index)

            print("1, 2 y... ¡Poof!")

            time.sleep(1)

            print(f"The Pokémon forgot how to use {removed_move.name}.")

            time.sleep(0.5)

            return True

        else:
            print("Invalid index. The Pokémon could not forget the move.")

            return False

    def replace_move(self, index: int, new_move: Move) -> bool:

        if 0 <= index < len(self.moves):
            old_move = self.moves[index]

            print("1, 2 and... ¡Poof!")

            time.sleep(1)

            print(f"The Pokémon forgot how to use {old_move.name} and...")
            time.sleep(1)

            self.moves[index] = new_move

            print(f"The Pokémon learned {new_move.name}!")

            time.sleep(0.5)

            return True

        else:
            print("Invalid index. The Pokémon could not replace the move.")

            return False

    def get_moves(self) -> List[Move]:
        return self.moves

    def show_moves(self) -> None:

        if not self.moves:
            print("The Pokémon still doesn't know any moves.")

            time.sleep(0.5)

        else:
            print("\n" + "=" * 45)
            print("                 MOVES")
            print("=" * 45)

            for i, move in enumerate(self.moves):
                print(
                    f"[{i + 1}] "
                    f"{move.name.ljust(12)} | "
                    f"Type: {move.type.ljust(8)} | "
                    f"Power: {str(move.power).ljust(3)} | "
                    f"PP: {move.pp}"
                )

            print("=" * 45 + "\n")

            time.sleep(0.5)


class Pokemon:
    def __init__(
        self,
        name: str,
        types: List[str],
        stats: Stats,
        life: float = 10,
        attack: float = 1,
        defense: float = 0.5,
        level: int = 1,
        special_ability: str = "None",
        moveset: Moveset | None = None,
        evolution: str | None = None,
        evolution_level: int | None = None,
    ) -> None:

        self.name = name
        self.types = types
        self.life = life
        self.attack_power = attack
        self.stats = stats
        self.defense = defense
        self.level = level

        self.experience = 0

        self.experience_to_level_up = self.level * 10

        self.special_ability = special_ability

        self.moveset = moveset if moveset else Moveset()

        self.evolution = evolution
        self.evolution_level = evolution_level

    def get_stats(self) -> str:
        return f"{self.name} Stats: {self.stats}"

    def attack(self, target: "Pokemon", move: Move, relations: TypeRelations) -> "Pokemon" | None:

        damage = CombatEngine.calculate_damage(self, target, move)

        multiplier = relations.get_effectiveness(move.type, target.types)

        print(f"{self.name} attacks {target.name} with {move.name}")

        print(f"Effectiveness: x{multiplier}")

        was_alive = not target.is_fainted()

        target.defender(damage)

        if was_alive and target.is_fainted():
            print(f"\n{target.name} was defeated!")

            exp_gained = target.level * 5

            if target.level > self.level:
                exp_gained = int(exp_gained * 1.5)

                print("Bonus experience for defeating a stronger opponent!")

            return self.gain_experience(exp_gained)
        else:
            return None


    def gain_experience(self, amount: int) -> "Pokemon" | None:

        self.experience += amount

        print(f"{self.name} gained {amount} experience points.")

        print(f"EXP current: {self.experience}/{self.experience_to_level_up}")

        return self.level_up()

    def level_up(self) -> "Pokemon" | None:

        while self.experience >= self.experience_to_level_up:
            self.experience -= self.experience_to_level_up

            self.level += 1

            self.experience_to_level_up = self.level * 10

            self.stats.attack += random.randint(1, 3)

            self.stats.defense += round(random.uniform(0.2, 1.0), 2)

            self.stats.special_attack += random.randint(1, 3)

            self.stats.special_defense += round(random.uniform(0.2, 1.0), 2)

            self.stats.speed += round(random.uniform(0.2, 1.0), 2)

            self.stats.hp += random.randint(4, 8)

            self.life = self.stats.hp

            new = self.evolve()

            if new:
                print(
                    f"\n{new.name} evolved to level {new.level}\n"
                    f"--New Statistics:--\n"
                    f"HP: {new.stats.hp}\n"
                    f"Attack: {new.stats.attack}\n"
                    f"Defense: {new.stats.defense}\n"
                    f"Special Attack: {new.stats.special_attack}\n"
                    f"Special Defense: {new.stats.special_defense}\n"
                    f"Speed: {new.stats.speed}\n"
                    f"EXP necessary for the next level: {new.experience_to_level_up}"
                )
                return new
            else:
                print(f"\n{self.name} leveled up to {self.level}!")

                print(
                    f"\nNew Statistics:"
                    f"\nHP: {self.stats.hp}"
                    f"\nAttack: {self.stats.attack}"
                    f"\nDefense: {self.stats.defense}"
                    f"\nSpecial Attack: {self.stats.special_attack}"
                    f"\nSpecial Defense: {self.stats.special_defense}"
                    f"\nSpeed: {self.stats.speed}"
                )

                print(f"\nEXP necessary for the next level: {self.experience_to_level_up}")
        return None

    def defender(self, damage: float) -> None:

        damage_received = damage * (1 - self.defense)

        self.life -= damage_received

        if self.life < 0:
            self.life = 0

        print(f"{self.name} received {damage_received:.2f} damage")

        print(f"Remaining life: {self.life:.2f}")

    def is_fainted(self) -> bool:
        return self.life <= 0

    def evolve(self):

        if (
            self.evolution is not None
            and self.evolution_level is not None
            and self.level >= self.evolution_level
        ):
            old_name = self.name

            print(f"{old_name} is evolving...")

            if self.evolution == "Charmeleon":
                new_pokemon = Charmeleon(level=self.level)
                new_pokemon.moveset = self.moveset
                new_pokemon.experience = self.experience
                new_pokemon.experience_to_level_up = self.experience_to_level_up
                print(f"{old_name} evolved into {new_pokemon.name}!")
                return new_pokemon

        return None


class Charmeleon(Pokemon):
    def __init__(self, level):
        super().__init__(
            name="Charmeleon",
            types=["Fire"],
            stats=Stats(
                hp=30,
                attack=4,
                defense=0.5,
                special_attack=2,
                special_defense=2,
                speed=2,
            ),
            life=30,
            attack=4,
            defense=0.5,
            level=level,
        )


class CombatEngine:
    @staticmethod
    def hit_accuracy(attack: Move, defender_types: List[str]):

        tp = TypeRelations()

        effect = tp.get_effectiveness(attack.type, defender_types)

        factor = random.random()

        return (attack.accuracy > (factor * effect) / (factor + 1), effect)

    @staticmethod
    def calculate_damage(attacker: Pokemon, defender: Pokemon, move: Move):

        att_stats = attacker.stats
        def_stats = defender.stats

        is_able_to_attack, multiplier = CombatEngine.hit_accuracy(move, defender.types)

        rlevel = attacker.level / defender.level

        rdef = att_stats.attack / def_stats.defense

        damage = int(is_able_to_attack) * (rlevel * rdef * multiplier * move.power)

        print(f"Damage: {damage}")

        return damage


class Trainer:
    def __init__(self, nombre: str, team: str, pokemon: List[Pokemon]):

        self.nombre = nombre
        self.team = team
        self.pokemon = pokemon if pokemon is not None else []

    def add_pokemon(self, pokemon: Pokemon):

        if len(self.pokemon) < 6 and pokemon not in self.pokemon:
            self.pokemon.append(pokemon)

        else:
            print("You cannot add more Pokémon or the Pokémon is already in the team.")

    def get_active_pokemon(self):

        if self.pokemon:
            return self.pokemon[0]

        else:
            print("You don't have any Pokémon in your team.")

            return None

    def switch_pokemon(self, pokemon_index):

        if 0 <= pokemon_index < len(self.pokemon):
            self.pokemon[0], self.pokemon[pokemon_index] = (
                self.pokemon[pokemon_index],
                self.pokemon[0],
            )

        else:
            print("Invalid Pokémon index.")

    def handle_evolution(self, old_pokemon, new_pokemon):
        for i, p in enumerate(self.pokemon):
            if p == old_pokemon:
                self.pokemon[i] = new_pokemon


def main() -> None:

    relations = TypeRelations()

    charmander_stats = Stats(
        hp=20, attack=2, defense=0.5, special_attack=1, special_defense=1, speed=1
    )

    bulbasaur_stats = Stats(
        hp=20, attack=1, defense=0.3, special_attack=1, special_defense=1, speed=1
    )

    squirtle_stats = Stats(
        hp=20, attack=1, defense=0.5, special_attack=1, special_defense=1, speed=1
    )

    flame_burst = Move(name="Flame Burst", type="Fire", power=5, accuracy=100, pp=25)

    vine_whip = Move(name="Vine Whip", type="Grass", power=5, accuracy=100, pp=25)

    water_gun = Move(name="Water Gun", type="Water", power=5, accuracy=100, pp=25)

    charmander_moveset = Moveset([flame_burst])

    charmander = Pokemon(
        "Charmander",
        ["Fire"],
        charmander_stats,
        life=20,
        attack=2,
        moveset=charmander_moveset,
        evolution="Charmeleon",
        evolution_level=5,
    )

    bulbasaur_moveset = Moveset([vine_whip])

    bulbasaur = Pokemon(
        "Bulbasaur",
        ["Grass"],
        bulbasaur_stats,
        life=20,
        defense=0.3,
        moveset=bulbasaur_moveset,
    )

    squirtle_moveset = Moveset([water_gun])

    squirtle = Pokemon("Squirtle", ["Water"], squirtle_stats, life=20, moveset=squirtle_moveset)
    trainer = Trainer("Ash", "Fire", [charmander])

    print("\n--- BATTLE 1 ---")
    result = charmander.attack(bulbasaur, flame_burst, relations)
    if result:
        trainer.handle_evolution(charmander, result)
        charmander = result

    print("\n--- BATTLE 2 ---")
    bulbasaur.attack(squirtle, vine_whip, relations)

    print("\n--- BATTLE 3 ---")
    squirtle.attack(charmander, water_gun, relations)


if __name__ == "__main__":
    main()
