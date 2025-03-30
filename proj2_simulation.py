"""Chess Opening Explorer - Simulation

Simulate an interactive session of the chess opening explorer
by feeding in a list of commands to be executed in sequence.
"""

from __future__ import annotations
from typing import Optional
from dataclasses import dataclass

from traverser import Traverser
from move_tree import MoveTree
from chess_data import ChessData
from game_reader import read_pgn
from openings_reader import get_openings


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


@dataclass
class SimulationConfig:
    """Configuration for setting up and running a chess explorer simulation."""
    dataset_choice: int
    opening_path: str
    max_moves_val: int
    default_tc: Optional[int]
    command_list: list[str]


class ChessExplorerSimulation:
    """A simulation of the chess opening explorer using a Traverser."""
    _traverser: Traverser
    _command_log: list[str]

    def __init__(self, sim_config: SimulationConfig) -> None:
        """Initialize the chess simulation with selected data and a command list."""
        game_file_paths = self._select_dataset(sim_config.dataset_choice)
        games_database = read_pgn(game_file_paths)
        openings_database = get_openings(sim_config.opening_path, sim_config.max_moves_val)

        root = MoveTree("", data=ChessData([], games_database))
        for move_sequence in openings_database:
            root.insert_sequence(list(move_sequence), games_database, openings_database)

        self._traverser = Traverser(root, sim_config.default_tc)
        self._command_log = sim_config.command_list

    def run(self) -> None:
        """Run the simulation by executing each command in order."""
        print("\n=== Starting Simulation ===\n")
        for cmd in self._command_log:
            print(f"> {cmd}")
            base, param = self._parse_command(cmd)
            if self._validate_command(base):
                self._traverser.handle_input(base, param)
            else:
                print(f"Invalid command: {cmd}")

    @staticmethod
    def _parse_command(command: str) -> tuple[str, Optional[str]]:
        split = command.strip().split(maxsplit=1)
        return (split[0], split[1] if len(split) > 1 else None)

    @staticmethod
    def _validate_command(cmd: str) -> bool:
        return cmd in {'ls', 'cd', 'tree', 'info', 'settc', 'help', 'find', 'stats', 'timecontrols'}

    @staticmethod
    def _select_dataset(choice: int) -> list[str]:
        if choice == 1:
            return ALL_GAMES
        elif choice == 2:
            return BLITZ_ONLY
        elif choice == 3:
            return BULLET_ONLY
        elif choice == 4:
            return RAPID_ONLY
        else:
            print("Invalid choice. Defaulting to all games.")
            return ALL_GAMES


if __name__ == '__main__':

    simulation_config = SimulationConfig(
        dataset_choice=2,
        opening_path="data/openings",
        max_moves_val=2,
        default_tc=180,
        command_list=[
            "ls desc",
            "ls asc",
            "cd e4",
            "ls",
            "cd e5",
            "settc 180",
            "stats",
            "tree",
            "cd ../..",
            "cd e4/e6/Nc3",
            "stats",
            "help",
            "timecontrols",
        ]
    )

    sim = ChessExplorerSimulation(simulation_config)
    sim.run()

    import doctest

    doctest.testmod(verbose=True)
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['E1136', 'W0221'],
        'extra-imports': ['move_tree',
                          'openings_reader',
                          'Optional',
                          'chess_data',
                          'traverser',
                          'Traverser',
                          'read_pgn',
                          'game_reader'],
        'allowed-io': ['ChessExplorerSimulation.run', 'ChessExplorerSimulation._select_dataset'],
        'max-nested-blocks': 4
    })
