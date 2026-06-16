from typing import List
import random
from scr.models.move import Move
from scr.models.pokemon import Pokemon
from scr.engine.type_relations import TypeRelations

class CombatEngine:
    """
    Implementa los metodos para el calculo de damage y una funcion
    con numeros pseudoaleatorios para definir cuando se falla un ataque

    Asumiendo que existe class Move con las siguientes caracteristicas:
    Move: Debe contener los atributos de un ataque: name, type (string), power,
    accuracy, y pp.
    """

    @staticmethod
    def hit_accuracy(attack: Move, defender_types: List[str]):
        tp = TypeRelations()
        effect = tp.get_effectiveness(attack.type, defender_types)
        factor = random.random()

        return attack.accuracy > (factor * effect) / (
            factor + 1
        ), effect  # si es mayor entonces el ataque acierta

    @staticmethod
    def calculate_damage(attacker: Pokemon, defender: Pokemon, move: Move):
        att_stats = attacker.stats
        def_stats = defender.stats
        is_able_to_attack, multiplier = CombatEngine.hit_accuracy(move, defender.types)
        # tener en cuenta quien tiene mas nivel
        rlevel = attacker.level / defender.level
        # tener en cuenta si atacante tiene mas ataque que la defensa del defensa
        rdef = att_stats.attack / def_stats.defense
        # ataque -> si is_able_to_attack = 0 entonces ataque fallido, sino, calcular ataque
        damage = int(is_able_to_attack) * (rlevel * rdef * multiplier * move.power)
        print(f"Damage: {damage}")
        return damage
