# Boards
ARENA_X = 16
ARENA_Y = 16

# Costs
TERRITORY_COST = {
    "Manpower": 500
}
TERRITORY_PRODUCTION = {
    "Manpower": 250,
    "Fuel": 100,
    "Metal": 100,
}

TERRITORY_ACQUISITION = 50

# Units
ATTACK = 10
DEFENCE = 10

# Starting Units
STARTING = {
    "Resources": {
        "Manpower": 1000,
        "Fuel": 500,
        "Metal": 500
    },
    "Positions": {
        # x, y with negatives being from the opposite side
        1: [
            (1, -2),
        ],
        2: [
            (-2, 1),
        ]
    }
}

# Religion
RELIGION_COST = 1
