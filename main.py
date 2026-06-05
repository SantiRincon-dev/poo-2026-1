from __future__ import annotations

import random
import time  # noqa: I001
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
        hp: float = 10.0,
        attack: float = 1.0,
        defense: float = 0.5,
        special_attack: float = 1.0,
        special_defense: float = 1.0,
        speed: float = 1.0,
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
        level: int = 1,
        moveset: Moveset | None = None,
        evolution: str | None = None,
        evolution_level: int | None = None,
    ) -> None:

        self.name = name
        self.types = types
        self.stats = stats
        self.level = level

        self.experience = 0

        self.experience_to_level_up = self.level * 10

        self.moveset = moveset if moveset else Moveset()

        self.evolution = evolution
        self.evolution_level = evolution_level

    def get_stats(self) -> str:
        return f"{self.name} Estadísticas: {self.stats}"

    def attack(self, target: "Pokemon", move: Move, relations: TypeRelations) -> "Pokemon" | None:

        damage = CombatEngine.calculate_damage(self, target, move)

        print(f"{self.name} attacks {target.name} with {move.name}")

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
        damage_received = damage * (1 - self.stats.defense)
        self.stats.hp = self.stats.hp - damage_received

        if self.stats.hp <= 0:
            self.stats.hp = 0

        print(f"{self.name} received {damage_received:.2f} damage")

        print(f"Remaining life: {self.stats.hp:.2f}")

    def is_fainted(self) -> bool:
        return self.stats.hp <= 0

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

    def get_next_available_pokemon_index(self):
        for index, pokemon in enumerate(self.pokemon[1:], start=1):
            if pokemon.stats.hp > 0:
                return index
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


class Field:
    """Implementa el campo de batalla con sus características y efectos.

    Determina el orden del primer turno a partir de la velocidad del Pokémon activo de cada
    entrenador y luego alterna los turnos entre los participantes.
    """

    def __init__(self, trainer1: Trainer, trainer2: Trainer):
        self.trainer1 = trainer1
        self.trainer2 = trainer2

    def determine_turn_order(self):
        pokemon1 = self.trainer1.get_active_pokemon()
        pokemon2 = self.trainer2.get_active_pokemon()

        if pokemon1.stats.speed > pokemon2.stats.speed:
            return [pokemon1, pokemon2]
        elif pokemon2.stats.speed > pokemon1.stats.speed:
            return [pokemon2, pokemon1]
        else:
            # Si la velocidad es igual, se decide al azar
            return list(random.choice([(pokemon1, pokemon2), (pokemon2, pokemon1)]))

    def battle_finished(self, participants):

        for p in participants:
            if p.stats.hp <= 0:
                return True
        return False

    def battlefield(self):
        participants = self.determine_turn_order()
        turn_index = 0
        battle_active = True
        relations = TypeRelations()

        print("\n" + "=" * 60)
        print(f"BATALLA  : {self.trainer1.nombre} vs {self.trainer2.nombre}")
        print("\n" + "=" * 60)

        while battle_active and not self.battle_finished(participants):
            attacker = participants[turn_index]
            defender = participants[1 - turn_index]

            print(
                f"\n TURNO de {attacker.name.upper()} (Velocidad: {attacker.stats.speed}) CONTRA "
                f"{defender.name.upper()} (Velocidad: {defender.stats.speed})"
            )

            print(f"\n Movimientos disponibles para {attacker.name}:")
            for i, move in enumerate(attacker.moveset.get_moves()):
                print(
                    f"[{i + 1}] {move.name} | Tipo: {move.type} | Poder: {move.power}|PP: {move.pp}"
                )

            while True:
                try:
                    choice = (
                        int(
                            input(
                                f"Selecciona el movimiento para {attacker.name}"
                                f" (1-{len(attacker.moveset.get_moves())}): "
                            )
                        )
                        - 1
                    )
                    if 0 <= choice < len(attacker.moveset.get_moves()):
                        break
                    else:
                        raise ValueError("Número fuera de rango.")
                except ValueError as e:
                    print(f"Entrada no válida. {e}")

            movement = attacker.moveset.get_moves()[choice]

            print(f"{attacker.name} usa {movement.name}!")

            evolved = attacker.attack(defender, movement, relations)
            if evolved is not None:
                trainer = self.trainer1 if attacker in self.trainer1.pokemon else self.trainer2
                trainer.handle_evolution(attacker, evolved)
                attacker = evolved
                participants[turn_index] = evolved

            if defender.stats.hp <= 0:
                defender_trainer = (
                    self.trainer1 if defender in self.trainer1.pokemon else self.trainer2
                )
                next_pokemon_index = defender_trainer.get_next_available_pokemon_index()

                if next_pokemon_index is None:
                    print(f"\n¡{defender.name} ha sido derrotado! {attacker.name} gana la batalla.")
                    break

                defender_trainer.switch_pokemon(next_pokemon_index)
                next_defender = defender_trainer.get_active_pokemon()
                participants[1 - turn_index] = next_defender

                print(
                    f"\n{defender_trainer.nombre} envió a {next_defender.name} "
                    f"para continuar la batalla."
                )

            print(f"\n{'=' * 20}")
            print("¿Qué deseas hacer?")
            print("[1] Continuar la batalla")
            print("[2] Cambiar de Pokémon")
            print("[3] Rendirse")
            print(f"{'=' * 20}")
            while True:
                try:
                    decision = int(input("Selecciona una opción (1-3): "))
                    if decision == 1:
                        # Continuar
                        turn_index = 1 - turn_index
                        time.sleep(1)
                        break
                    elif decision == 2:
                        # Cambiar Pokémon
                        trainer = (
                            self.trainer1 if attacker in self.trainer1.pokemon else self.trainer2
                        )
                        print(f"\nPokémon disponibles en el equipo de {trainer.nombre}:")
                        for i, pok in enumerate(trainer.pokemon):
                            print(f"[{i + 1}] {pok.name} (Vida: {pok.stats.hp:.1f})")

                        while True:
                            try:
                                pok_choice = (
                                    int(
                                        input(
                                            "Selecciona Pokémon (1-{}): ".format(
                                                len(trainer.pokemon)
                                            )
                                        )
                                    )
                                    - 1
                                )
                                if 0 <= pok_choice < len(trainer.pokemon):
                                    trainer.switch_pokemon(pok_choice)
                                    active_pokemon = trainer.get_active_pokemon()
                                    print(f"¡{trainer.nombre} envió a {active_pokemon.name}!")
                                    participants[turn_index] = active_pokemon

                                    turn_index = 1 - turn_index
                                    time.sleep(1)
                                    break
                                else:
                                    raise ValueError("Índice inválido")
                            except ValueError as e:
                                print(f" {e}")
                        break
                    elif decision == 3:
                        # Rendirse
                        trainer = (
                            self.trainer1 if attacker in self.trainer1.pokemon else self.trainer2
                        )
                        print(f"\n¡{trainer.nombre} se rindió!")
                        battle_active = False
                        break
                    else:
                        raise ValueError("Opción no válida (1-3)")
                except ValueError as e:
                    print(f" {e}")


def main() -> None:

    charmander_stats = Stats(
        hp=20, attack=2, defense=0.5, special_attack=1, special_defense=1, speed=2
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
        moveset=charmander_moveset,
        evolution="Charmeleon",
        evolution_level=5,
    )

    bulbasaur_moveset = Moveset([vine_whip])

    bulbasaur = Pokemon(
        "Bulbasaur",
        ["Grass"],
        bulbasaur_stats,
        moveset=bulbasaur_moveset,
    )

    squirtle_moveset = Moveset([water_gun])
    squirtle = Pokemon("Squirtle", ["Water"], squirtle_stats, moveset=squirtle_moveset)

    entrenador1 = Trainer("Ash", "Team Rocket", [charmander, bulbasaur])
    entrenador2 = Trainer("Misty", "Team Water", [squirtle])

    campo = Field(entrenador1, entrenador2)
    campo.battlefield()


if __name__ == "__main__":
    main()
