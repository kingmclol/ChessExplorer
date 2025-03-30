"""
main is where the program is run.
"""
from openings_reader import get_openings
from game_reader import read_pgn
from move_tree import MoveTree
from chess_data import ChessData
from traverser import Traverser

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
        "You can navigate through chess openings, view statistics, "
        "and explore move trees under different time controls.\n")
    print("Type 'help' to view a list of available commands.\n")
    print("Starting Traverser...\n")


def select_dataset() -> tuple[list[str], int]:
    """
    Select the time control of the games that will be used in the opening explorer.
    Also, return the timecontrol of the chosen dataset
    """
    print("Select dataset to load:")
    print("1. All Games (60s, 180s, 300s, 600s)")
    print("2. Blitz Only (180s, 300s)")
    print("3. Bullet Only (60s)")
    print("4. Rapid Only (600s)")
    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        return ALL_GAMES, 180
    elif choice == "2":
        return BLITZ_ONLY, 180
    elif choice == "3":
        return BULLET_ONLY, 60
    elif choice == "4":
        return RAPID_ONLY, 600
    else:
        print("Invalid choice. Loading all games by default.")
        return ALL_GAMES, 180


def max_moves() -> int:
    """
    Return max moves the user wants to use from 1-5
    """
    while True:  # literally can't bother fixing your stuff
        try:
            choice = int(input("Enter maximum number of opening moves from 1-5: "))
            if 1 <= choice <= 5:
                return choice
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("Please enter a number between 1 and 5.")
        except TypeError:
            print("Please enter a number between 1 and 5.")

if __name__ == '__main__':
    # Comment out later.
    import doctest

    doctest.testmod(verbose=True)
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221'],
        'extra-imports': ['move_tree',
                          'chess_data',
                          'traverser',
                          'openings_reader',
                          'game_reader'],
        'allowed-io': ['select_dataset', 'start', 'max_moves'],
        'max-nested-blocks': 4
    })

    start()
    moves = max_moves()
    print("Loading openings...")
    openings_database = get_openings("data/openings", moves)
    print("Finished loading openings")
    files, tc = select_dataset()
    print("Loading games...")
    games_database = read_pgn(files)
    print("Finished loading games.")

    print("Building tree...")
    tree = MoveTree("", data=ChessData([], games_database))

    for move_sequence in openings_database:
        tree.insert_sequence(list(move_sequence), games_database, openings_database)

    print("Finished building tree.")
    traverser = Traverser(tree, tc)
    traverser.output_help()
    traverser.interactive()
