"""
A doubly-linked tree of chess moves. Each node optionally contains data
about that sequence from moves.

The root of a MoveTree should be the original starting board (no moves)
"""
from __future__ import annotations
from typing import Optional

import pandas as pd

PADDING = 12
# TODO: Move this into a new file
class ChessData:
    """
    A dataclass that stores data about a chess state

    # TODO: Make it so data is stored in an actual way (currently it is absolute ugh)
    # Also probalby is a good idea to rename this.
    """
    name: Optional[str]
    win_data: dict[int, dict[str, float]]
    playrate: dict[int, float]
    plays: dict[int, float]
    move_sequence: list[str]
    def __init__(self, move_sequence: list[str], data: pd.DataFrame, name: Optional[str] = None):
        self.name = name
        self.move_sequence = move_sequence
        self._calc_data(move_sequence, data)

    def _calc_data(self, move_sequence: list[str], data: pd.DataFrame) -> None:
        """Calculate the win rate if this move is played for different time controls."""
        # print(move_sequence)  # Debugging

        win_data = {}
        playrate = {}
        plays = {}
        tcs = data['time_control'].unique()

        for tc in tcs:
            # Filter by time control first
            filtered_curr = data[(data['time_control'] == tc) &
                                 (data['moves'].apply(lambda moves: isinstance(moves, list) and moves[:len(
                                     move_sequence)] == move_sequence))]

            plays[tc] = len(filtered_curr)
            win_data[tc] = {}
            for winner in ["white", "black", "draw"]:
                # Avoid NaN values
                win_data[tc][winner] = len(filtered_curr[filtered_curr['winner'] == winner]) / len(filtered_curr)\
                    if not filtered_curr.empty else 0.0
            # print(f"Winrate for {tc}: {winrate[tc]}")

            # Previous move sequence filtering
            filtered_prev = data[(data['time_control'] == tc) &
                                 (data['moves'].apply(lambda moves: isinstance(moves, list) and moves[:max(len(
                                     move_sequence) - 1, 0)] == move_sequence[:-1]))]

            # print(f"Filtered previous size for {tc}: {filtered_prev.shape}")

            # Avoid division by zero
            playrate[tc] = len(filtered_curr) / len(filtered_prev) if len(filtered_prev) > 0 else 0.0

        self.win_data = win_data
        self.playrate = playrate
        self.plays = plays

    # def str(self, tc: int) -> str:
    #     """ to string but uses tc """
    #     # TODO: make it take the tc in general
    #     return f"{self.name if self.name else ''} ({percentify(self.playrate.get(tc, 0), 2)})"


    def output_stats(self, tc: int) -> None:
        """Print out the stats for this board state, given the time control."""
        print(f"{self.name if self.name else "Not an opening"}")
        # TODO: Create a better way to represent move_sequence as a string
        print(f"Move sequence: {str(self.move_sequence)}")
        print(f"Chosen Timecontrol: {tc}")
        if tc not in self.win_data:
            print(f"<NO DATA FOR TC {tc} SECONDS>")
            return

        print(f"{'GAME RESULT':>{PADDING}}{'PERCENT':>{PADDING}}")

        win_dat = self.win_data[tc]
        for winner in win_dat:
            print(f"{winner:>{PADDING}}{f"{percentify(win_dat[winner], 2)}":>{PADDING}}")

        print(f"PLAYS: {self.plays[tc]}")
        if self.move_sequence:  # special case. It doesn't make sense to have a previous move.
            print(f"Players played this {percentify(self.playrate[tc], 2)} of the time after the previous move.")

    def get_name(self) -> str:
        """
        Return whether this seuqence of moves has a name. That is, whether this sequence is a
        documented opening. Return "(None)" if it is not.
        """
        return self.name if self.name else "(None)"

    def get_playrate(self, tc: Optional[int]) -> float:
        return self.playrate.get(tc, 0.0)


class MoveTree:
    """A Tree of Chess Moves. Legality is not checked."""
    move: str
    parent: MoveTree
    data: Optional[ChessData] = None
    next_moves: list[MoveTree]

    def __init__(self, move: str, parent: Optional[MoveTree] = None,
                 next_moves: Optional[list[MoveTree]] = None,
                 data: Optional[ChessData] = None):
        self.move = move
        self.parent = parent
        self.next_moves = next_moves if next_moves else []
        self.data = data if data else None

    def insert_sequence(self, move_sequence: list[str], games_database: Optional[pd.DataFrame] = None,
                        openings_database: Optional[dict[tuple[str, ...], str]] = None) -> None:
        """Insert the sequence of moves into this MoveTree. If games_database is provided, will update the
        data for each node too based on the games

        If openings_database is provided, will label sequences with the respective name if found"""
        if not move_sequence:
            return
        else:
            existing = False
            for next_move in self.next_moves:
                if next_move.move == move_sequence[0] and not existing:  # found an existing path go continue
                    next_move.insert_sequence(move_sequence[1:], games_database, openings_database)
                    existing = True

            if not existing:  # existing subtree not found; create own
                # TODO: Make creating the new MoveTree easier somehow(helper function, or constructor of ChessData)

                new_sequence = self.get_path() + [move_sequence[0]]
                name = openings_database[tuple(new_sequence)] if tuple(new_sequence) in openings_database else None
                data = ChessData(new_sequence, games_database, name)
                new_seq = MoveTree(move_sequence[0], self)
                new_seq.data = data

                self.next_moves.append(new_seq)
                new_seq.insert_sequence(move_sequence[1:], games_database, openings_database)

    def get_path(self) -> list[str]:
        """
        Return the sequence of moves to get to this node.
        """
        current = self.parent
        if not current:  # true root
            return []

        path = [self.move]
        while current.parent:  # don't want the true root of the tree
            path.append(current.move)
            current = current.parent

        path.reverse()  # since its in reverse order
        return path

    def print_stats(self, tc: int) -> None:
        # TODO: Might be a good idea to make handling time controls easier instead of always as param
        if not self.data:
            print("There is no data associated with this board state.")
        else:
            print(self.data.output_stats(tc))
    # ======================== added from ex3 or ex2 whatever
    def is_empty(self) -> bool:
        """Return whether this MoveTree is empty"""
        return self.move is None

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented(0).rstrip()

    def _str_indented(self, depth: int, tc: int = 180) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            if self.move == '':
                str_so_far = '(Root)\n'  # Don't want to print out the true root.
            else:
                str_so_far = ('    ' * depth + '╚══ ' + f'{self.move}')
                if self.data and self.data.name:
                    str_so_far += ' | ' + self.data.get_name()

                str_so_far += '\n'

            for next_move in self.next_moves:
                str_so_far += next_move._str_indented(depth + 1, tc)
            return str_so_far


def percentify(val: float, dp: int) -> str:
    """
    Return the value as a string percentange, rounded to dp decimal points.

    >>> percentify(0.7321, 2)
    '73.21%'
    """
    return f"{round(val * 100, dp)}%"
