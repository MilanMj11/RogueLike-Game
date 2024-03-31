LOBBY_WALLS = []

# Personal Room
for j in range(5, 10):
    LOBBY_WALLS.append([0, j])
for i in range(1, 6):
    LOBBY_WALLS.append([i, 4])
    LOBBY_WALLS.append([i, 10])
LOBBY_WALLS.append([6, 5])
LOBBY_WALLS.append([6, 6])
LOBBY_WALLS.append([6, 8])
LOBBY_WALLS.append([6, 9])

# Hallway
for j in range(10, 17):
    LOBBY_WALLS.append([6, j])
for j in range(9, 25):
    if j == 15 or j == 16 or j == 17:
        continue
    LOBBY_WALLS.append([10, j])
LOBBY_WALLS.append([10, 5])
for i in range(7, 10):
    LOBBY_WALLS.append([i, 4])
for j in range(22, 25):
    LOBBY_WALLS.append([6, j])

# Gamble Room
for j in range(1, 5):
    LOBBY_WALLS.append([11, j])
for i in range(12, 17):
    LOBBY_WALLS.append([i, 0])
for j in range(1, 24):
    LOBBY_WALLS.append([17, j])
for j in range(10, 14):
    LOBBY_WALLS.append([11, j])
for i in range(12, 17):
    LOBBY_WALLS.append([i, 12])

# Black Smith
for i in range(12, 17):
    LOBBY_WALLS.append([i, 13])
for i in range(11, 17):
    LOBBY_WALLS.append([i, 24])

# Shop
for i in range(1, 7):
    LOBBY_WALLS.append([i, 13])
for i in range(1, 7):
    LOBBY_WALLS.append([i, 24])
for j in range(14, 24):
    LOBBY_WALLS.append([0, j])

# Dungeon Entrance
LOBBY_WALLS.append([5, 25])
for j in range(26, 29):
    LOBBY_WALLS.append([4, j])
LOBBY_WALLS.append([5, 29])
LOBBY_WALLS.append([11, 25])
for j in range(26, 29):
    LOBBY_WALLS.append([12, j])
LOBBY_WALLS.append([11, 29])
LOBBY_WALLS.append([6, 30])
LOBBY_WALLS.append([6, 31])
LOBBY_WALLS.append([10, 30])
LOBBY_WALLS.append([10, 31])
for i in range(7, 10):
    LOBBY_WALLS.append([i, 32])

# making the outside full of BLANKS
LOBBY_BLANKS = []

for i in range(11):
    for j in range(4):
        LOBBY_BLANKS.append([i, j])
LOBBY_BLANKS.append([6, 4])
LOBBY_BLANKS.append([10, 4])
LOBBY_BLANKS.append([11, 0])
LOBBY_BLANKS.append([17, 0])
LOBBY_BLANKS.append([0, 4])
for j in range(10, 14):
    LOBBY_BLANKS.append([0, j])
for i in range(1, 6):
    LOBBY_BLANKS.append([i, 11])
    LOBBY_BLANKS.append([i, 12])

for i in range(4):
    for j in range(25, 33):
        LOBBY_BLANKS.append([i, j])
        LOBBY_BLANKS.append([17 - i, j])
LOBBY_BLANKS.append([0, 24])
LOBBY_BLANKS.append([4, 25])
for j in range(29, 33):
    LOBBY_BLANKS.append([4, j])
for j in range(30, 33):
    LOBBY_BLANKS.append([5, j])
LOBBY_BLANKS.append([6, 32])

for j in range(25, 33):
    LOBBY_BLANKS.append([13, j])
LOBBY_BLANKS.append([17, 24])
LOBBY_BLANKS.append([12, 25])
for j in range(29, 33):
    LOBBY_BLANKS.append([12, j])
for j in range(30, 33):
    LOBBY_BLANKS.append([11, j])
LOBBY_BLANKS.append([10, 32])

