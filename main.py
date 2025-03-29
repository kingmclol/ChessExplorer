"""
Stuff.
"""
from OpeningsReader import get_openings
from GameReader import read_pgn
from MoveTree import MoveTree, ChessData
from Traverser import Traverser

openings_database = get_openings("data/openings", 3)
print("Done")

# games_database = read_pgn(["data/games/lichess_tournament_2025.03.26_G0j0ZKLB_2000-superblitz (1).pgn",
#                            "data/games/lichess_tournament_2025.03.28_bHUDi9Ci_daily-rapid.pgn",
#                            "data/games/lichess_tournament_2025.03.24_aByKLmHE_daily-superblitz.pgn",
#                            "data/games/lichess_tournament_2025.03.25_45UeSiXu_daily-blitz.pgn",
#                            "data/games/lichess_tournament_2025.03.25_OvDcYlTU_daily-rapid.pgn",
#                            "data/games/lichess_tournament_2025.03.25_tqzGNmOv_daily-bullet.pgn"]
#                           )
games_database = read_pgn(["data/games/lichess_tournament_2025.03.26_G0j0ZKLB_2000-superblitz (1).pgn"])
print("Done")

tree = MoveTree("", data=ChessData([], games_database))
for move_sequence in openings_database:
    tree.insert_sequence(list(move_sequence), games_database, openings_database)

print(tree)
print(games_database)

traverser = Traverser(tree, 180)
traverser.interactive()
