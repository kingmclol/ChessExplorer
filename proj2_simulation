"""Chess Opening Explorer - Simulation

Simulate an interactive session of the chess opening explorer
by feeding in a list of commands to be executed in sequence.
"""

from __future__ import annotations
from typing import Optional
from Traverser import Traverser
from MoveTree import MoveTree
from ChessData import ChessData
from GameReader import read_pgn
from OpeningsReader import get_openings


class ChessExplorerSimulation:
    """A simulation of the chess opening explorer using a Traverser."""
    _traverser: Traverser
    _command_log: list[str]

    def __init__(self, game_file_paths: list[str], opening_path: str,
                 default_tc: Optional[int], command_list: list[str]) -> None:
        """Initialize the chess simulation with data and a command list."""
        games_database = read_pgn(game_file_paths)
        openings_database = get_openings(opening_path, 3)

        root = MoveTree("", data=ChessData([], games_database))

        for move_sequence in openings_database:
            root.insert_sequence(list(move_sequence), games_database, openings_database)

        self._traverser = Traverser(root, default_tc)
        self._command_log = command_list

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


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999']
    })
    commands = [
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

    sim = ChessExplorerSimulation(
        game_file_paths=["data/games/lichess_tournament_2025.03.26_G0j0ZKLB_2000-superblitz (1).pgn"],
        opening_path="data/openings",
        default_tc=180,
        command_list=commands
    )

    sim.run()
