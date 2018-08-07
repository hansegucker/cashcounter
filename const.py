#############
# CONSTANTS #
#############
# Trap modes
TRAP_MODE_CLOSED = 0
TRAP_MODE_HALF = 1
TRAP_MODE_OPEN = 2

# "White" values for color sensor (in rgb 255)
R_MAX = 330
G_MAX = 340
B_MAX = 350

# Measure settings
STEP_BEGINN = 2000
STEP_WIDTH = 200
STEP_MAX = 1000

# Coins
COINS = {
    200: {
        "amount": 2.00,
        "res": "2.png"
    },
    100: {
        "amount": 1.00,
        "res": "1.png"
    },
    50: {
        "amount": 0.50,
        "res": "50.png"
    },
    20: {
        "amount": 0.20,
        "res": "20.png"
    },
    10: {
        "amount": 0.10,
        "res": "10.png"
    },
    0: {
        "amount": 0,
        "res": "0.png"
    },
}
