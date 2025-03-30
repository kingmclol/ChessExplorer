"""
main is where the program is run.
"""
from OpeningsReader import get_openings
from GameReader import read_pgn
from MoveTree import MoveTree
from ChessData import ChessData
from Traverser import Traverser

ALL_GAMES = [
    "data/games/lichess_tournament_2025.03.26_G0j0ZKLB_2000-superblitz (1).pgn",
    "data/games/lichess_tournament_2025.03.28_bHUDi9Ci_daily-rapid.pgn",
    "data/games/lichess_tournament_2025.03.24_aByKLmHE_daily-superblitz.pgn",
    "data/games/lichess_tournament_2025.03.25_45UeSiXu_daily-blitz.pgn",
    "data/games/lichess_tournament_2025.03.25_OvDcYlTU_daily-rapid.pgn",
    "data/games/lichess_tournament_2025.03.25_tqzGNmOv_daily-bullet.pgn"
]

BLITZ_ONLY = [
    "data/games/lichess_tournament_2025.03.25_45UeSiXu_daily-blitz.pgn",
    "data/games/lichess_tournament_2025.03.24_aByKLmHE_daily-superblitz.pgn"
]

BULLET_ONLY = [
    "data/games/lichess_tournament_2025.03.25_tqzGNmOv_daily-bullet.pgn"
]

RAPID_ONLY = [
    "data/games/lichess_tournament_2025.03.28_bHUDi9Ci_daily-rapid.pgn",
    "data/games/lichess_tournament_2025.03.25_OvDcYlTU_daily-rapid.pgn"
]


def start() -> None:
    """
    Welcome the user to the chess opening explorer.
    """
    print("\n=== Welcome to the Chess Opening Explorer ===")
    print(
        "You can navigate through chess openings, view statistics, and explore move trees under different time controls.\n")
    print("Type 'help' to view a list of available commands.\n")
    print("Starting Traverser...\n")


def select_dataset() -> list[str]:
    """
    Select the time control of the games that will be used in the opening explorer.
    """
    print("Select dataset to load:")
    print("1. All Games")
    print("2. Blitz Only")
    print("3. Bullet Only")
    print("4. Rapid Only")
    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        return ALL_GAMES
    elif choice == "2":
        return BLITZ_ONLY
    elif choice == "3":
        return BULLET_ONLY
    elif choice == "4":
        return RAPID_ONLY
    else:
        print("Invalid choice. Loading all games by default.")
        return ALL_GAMES


def max_moves() -> int:
    """
    Return max moves the user wants to use from 1-5
    :return:
    """
    choice = int(input("Enter maximum number of opening moves from 1-5: "))
    if 1 <= choice <= 5:
        return choice
    else:
        print("Please enter a number between 1 and 5.")


start()
openings_database = get_openings("data/openings", max_moves())

games_database = read_pgn(select_dataset())

tree = MoveTree("", data=ChessData([], games_database))
for move_sequence in openings_database:
    tree.insert_sequence(list(move_sequence), games_database, openings_database)

traverser = Traverser(tree, 180)
traverser.output_help()
traverser.interactive()
