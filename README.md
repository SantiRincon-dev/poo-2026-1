# POKE — Sistema de Combate Pokémon

Sistema didáctico de combate tipo Pokémon construido en Python 3.10+,
diseñado para ilustrar los principios fundamentales de la Programación
Orientada a Objetos (POO).

---

## Tabla de contenidos

- [Objetivos](#objetivos)
- [Principios POO aplicados](#principios-poo-aplicados)
- [Estructura de módulos y paquetes](#estructura-de-módulos-y-paquetes)
- [Diseño del sistema](#diseño-del-sistema)
- [Diagrama UML](#diagrama-uml)
- [Instrucciones de uso](#instrucciones-de-uso)
- [Contribuir](#contribuir)

---

## Objetivos

1. Modelar un sistema de combate tipo Pokémon usando los principios de POO.
2. Definir clases con responsabilidades claras y bien delimitadas.
3. Representar relaciones entre entidades (composición, agregación, herencia) mediante UML.
4. Organizar el código en módulos y paquetes reutilizables.

---

## Principios POO aplicados

### 1. Encapsulamiento

Cada clase protege su estado interno y expone solo lo necesario:

- `Move` declara todos sus atributos como privados (`_name`, `_type`, `_power`,
  `_accuracy`, `_pp`) y los expone a través de `@property`, impidiendo
  modificaciones externas accidentales.
- `Moveset` controla la lista interna de movimientos; la única forma de
  agregar o reemplazar un movimiento es a través de sus métodos públicos
  (`add_move`, `replace_move`, `remove_move`), que aplican la restricción de
  máximo cuatro movimientos.
- `Pokemon` mantiene copias separadas de `stats_base` y `stats_max`, de modo
  que las estadísticas actuales pueden escalar con el nivel sin perder los
  valores originales.

### 2. Abstracción

Cada clase modela únicamente los conceptos necesarios para su responsabilidad:

- `Stats` encapsula el conjunto completo de estadísticas de combate en un
  único objeto, simplificando la firma del constructor de `Pokemon`.
- `CombatEngine` abstrae toda la lógica de cálculo de daño y precisión en
  métodos estáticos reutilizables, separando las reglas del juego de las
  entidades que participan en él.
- `TypeRelations` abstrae la tabla de efectividades de tipos en una consulta
  simple (`get_effectiveness`), ocultando la estructura interna del diccionario.

### 3. Herencia

La clase `Pokemon` actúa como clase base:

- `Charmeleon` hereda de `Pokemon` y sobrescribe nombre, tipos y estadísticas
  predeterminadas, reutilizando toda la lógica de combate y evolución del padre.
- Las subclases `FirePokemon`, `WaterPokemon` y `GrassPokemon` (diseño futuro)
  fijan el tipo del Pokémon, permitiendo especializaciones sin duplicar código.

La herencia permite que el sistema trate a cualquier especialización como un
`Pokemon` genérico (polimorfismo implícito), por ejemplo al iterar el equipo
de un `Trainer`.

### 4. Polimorfismo

`Field.battlefield()` y `CombatEngine.calculate_damage()` reciben objetos
`Pokemon` sin conocer su subclase concreta. Cuando un `Charmander` evoluciona
a `Charmeleon` durante la batalla, el campo reemplaza la referencia en
`participants` sin cambiar ninguna otra lógica.

### 5. Composición y Agregación

- **Composición fuerte** (`*--`): `Pokemon` posee un `Stats` y un `Moveset`
  que no tienen sentido fuera del Pokémon que los contiene. Si el Pokémon es
  eliminado, sus estadísticas y moveset dejan de existir.
- **Composición fuerte** (`*--`): `Moveset` posee sus `Move`; un movimiento
  pertenece a un único Moveset.
- **Agregación** (`o--`): `Trainer` gestiona una lista de Pokémon, pero los
  Pokémon pueden existir independientemente. `Field` referencia los dos
  Pokémon activos sin apropiarse de ellos.

---

## Estructura de módulos y paquetes

```
poke-repo/
├── src/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── pokemon.py        # Clase Pokemon y subclases (Charmeleon, …)
│   │   ├── pokemon_types.py  # FirePokemon, WaterPokemon, GrassPokemon
│   │   ├── move.py           # Move y Moveset
│   │   ├── stats.py          # Stats
│   │   └── trainer.py        # Trainer
│   ├── engine/
│   │   ├── __init__.py
│   │   ├── combat_engine.py  # CombatEngine (cálculo de daño y precisión)
│   │   ├── type_relations.py # TypeRelations (tabla de tipos)
│   │   └── field.py          # Field (bucle de batalla)
│   └── utils/
│       ├── __init__.py
│       └── constants.py      # Constantes globales (MAX_TEAM_SIZE, MAX_MOVES, …)
├── tests/
│   ├── __init__.py
│   ├── test_combat_engine.py
│   ├── test_battle_flow.py
│   └── test_evolution.py
├── main.py                   # Punto de entrada
├── README.md
├── requirements.txt
└── pyproject.toml
```

### Responsabilidad de cada módulo

| Módulo | Responsabilidad |
|---|---|
| `models/pokemon.py` | Entidad principal: atributos, combate, evolución y ganancia de experiencia |
| `models/pokemon_types.py` | Subclases tipadas que fijan el tipo del Pokémon |
| `models/move.py` | Representación de movimientos y colección de hasta 4 moves |
| `models/stats.py` | Contenedor de estadísticas de combate |
| `models/trainer.py` | Gestión de equipo (hasta 6 Pokémon) y cambio de activo |
| `engine/combat_engine.py` | Cálculo de daño, comprobación de precisión |
| `engine/type_relations.py` | Tabla de efectividades entre tipos |
| `engine/field.py` | Bucle de turnos, orden de ataque, fin de batalla |
| `utils/constants.py` | Valores globales reutilizables (evita magic numbers) |

---

## Diseño del sistema

### Entidades principales

| Clase | Rol |
|---|---|
| `Pokemon` | Entidad combatiente con estadísticas, moveset y lógica de evolución |
| `Stats` | Encapsula HP, ataque, defensa, velocidad y ataque especial |
| `Move` | Representa un movimiento con nombre, tipo, poder, precisión y PP |
| `Moveset` | Colección de hasta 4 movimientos con operaciones de gestión |
| `Trainer` | Gestor de equipo de hasta 6 Pokémon |
| `CombatEngine` | Lógica de cálculo de daño y verificación de impacto |
| `TypeRelations` | Tabla de multiplicadores de tipo (fuego, agua, planta…) |
| `Field` | Entorno de batalla: turnos, orden de ataque y condición de fin |

### Flujo de una batalla

```
Field.battlefield()
  └─ determine_turn_order()      # por velocidad, aleatorio si empate
  └─ (bucle de turnos)
       ├─ attacker elige Move
       ├─ CombatEngine.calculate_damage()
       │     └─ TypeRelations.get_effectiveness()
       ├─ defender.defender(damage)
       ├─ attacker.gain_experience()  ← si el defensor cae
       │     └─ level_up()
       │           └─ evolve()        ← si alcanza el nivel de evolución
       └─ Trainer.switch_pokemon()    ← si el defensor cae y queda equipo
```

---

## Diagrama UML

El diagrama completo se encuentra en `uml_diagram.mermaid` en la raíz del
repositorio. A continuación se muestra la versión embebida:

```mermaid
classDiagram
    direction TB

    %% ─── Composición / Agregación ───────────────────────────────────────────
    Trainer "1" *-- "1..6" Pokemon : owns / manages
    Pokemon "1" *-- "1" Stats       : has stats
    Pokemon "1" *-- "1" Moveset     : has moveset
    Moveset "1" *-- "0..4" Move     : contains
    Field "1" o-- "2" Pokemon       : active_pokemon

    %% ─── Dependencias ────────────────────────────────────────────────────────
    Field      --> CombatEngine    : uses
    CombatEngine --> Pokemon       : reads
    CombatEngine --> Move          : reads power / accuracy
    CombatEngine --> TypeRelations : delegates effectiveness

    %% ─── Herencia ────────────────────────────────────────────────────────────
    Pokemon <|-- Charmeleon
    Pokemon <|-- FirePokemon
    Pokemon <|-- WaterPokemon
    Pokemon <|-- GrassPokemon

    class Stats {
        +hp: float
        +attack: float
        +defense: float
        +special_attack: float
        +special_defense: float
        +speed: float
    }

    class Move {
        -_name: str
        -_type: str
        -_power: float
        -_accuracy: int
        -_pp: int
        +name «property»
        +type «property»
        +power «property»
        +accuracy «property»
        +pp «property»
    }

    class Moveset {
        -moves: list[Move]
        +add_move(move) bool
        +remove_move(index) bool
        +replace_move(index, new_move) bool
        +get_moves() list[Move]
        +show_moves() void
    }

    class Pokemon {
        +name: str
        +types: list[str]
        +stats: Stats
        +level: int
        +experience: int
        +moveset: Moveset
        +evolution: str | None
        +attack(target, move, relations) Pokemon|None
        +gain_experience(amount) Pokemon|None
        +level_up() Pokemon|None
        +defender(damage) void
        +is_fainted() bool
        +evolve() Pokemon|None
    }

    class Charmeleon {
        +name = "Charmeleon"
        +types = ["Fire"]
        +__init__(level)
    }

    class FirePokemon {
        +types = ["Fire"]
    }

    class WaterPokemon {
        +types = ["Water"]
    }

    class GrassPokemon {
        +types = ["Grass"]
    }

    class TypeRelations {
        -type_chart: dict
        +get_effectiveness(attack_type, defender_types) float
    }

    class CombatEngine {
        <<static>>
        +hit_accuracy(attack, defender_types) tuple
        +calculate_damage(attacker, defender, move) float
    }

    class Trainer {
        +nombre: str
        +team: str
        +pokemon: list[Pokemon]
        +add_pokemon(pokemon) void
        +get_active_pokemon() Pokemon|None
        +switch_pokemon(index) void
        +handle_evolution(old, new) void
    }

    class Field {
        +trainer1: Trainer
        +trainer2: Trainer
        +determine_turn_order() list[Pokemon]
        +battle_finished(participants) bool
        +battlefield() void
    }
```

### Notación utilizada

| Símbolo | Significado |
|---|---|
| `*--` | Composición — la parte no existe sin el todo |
| `o--` | Agregación — la parte puede existir de forma independiente |
| `-->` | Dependencia — una clase usa otra sin poseerla |
| `<\|--` | Herencia — la subclase extiende la superclase |
| `<<static>>` | La clase no se instancia; sus métodos son estáticos |
| `-` prefijo | Atributo o método privado |
| `+` prefijo | Atributo o método público |

---

## Instrucciones de uso

### Requisitos previos

- Python 3.10 o superior
- `pip` o `uv` disponible en el PATH

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/fegonzalez7/poo-2026-1.git
cd poo-2026-1

# (Recomendado) Crear entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Ejecutar la simulación

```bash
python main.py
```

Durante la ejecución el juego pedirá por consola qué movimiento usar en cada
turno y si deseas continuar, cambiar de Pokémon o rendirte.

### Ejecutar los tests

```bash
python -m pytest tests/
```

### Verificar estilo y tipos

```bash
# Formato (ruff)
ruff format --check .

# Tipos (mypy)
mypy .
```

El pipeline de CI (`.github/workflows/python_checks.yaml`) ejecuta estos
mismos pasos automáticamente en cada push o pull request contra `main` y `dev`.

