"""
A doubly-linked tree of chess moves. Each node optionally contains data
about that sequence from moves.

The root of a MoveTree should be the original starting board (no moves)
"""
from __future__ import annotations
from typing import Optional
import pandas as pd
from chess_data import ChessData


class MoveTree:
    """A Tree of Chess Moves. Legality is not checked."""
    move: str
    parent: MoveTree
    data: Optional[ChessData] = None
    next_moves: list[MoveTree]

    def __init__(self, move: str, parent: Optional[MoveTree] = None,
                 next_moves: Optional[list[MoveTree]] = None,
                 data: Optional[ChessData] = None) -> None:
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
        """
        prints out the stats for this node, given the time control.
        """
        if not self.data:
            print("There is no data associated with this board state.")
        else:
            self.data.output_stats(tc)

    def is_empty(self) -> bool:
        """Return whether this MoveTree is empty"""
        return self.move is None

    # These following functions are modified from exercise 2 by CSC111 teaching team
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
                str_so_far = '(Root)\n'  # Don't want to print out the true root normally; handle differently
            else:
                str_so_far = '    ' * depth + '╚══ ' + f'{self.move}'
                if self.data and self.data.name:
                    str_so_far += ' | ' + self.data.get_name()

                str_so_far += '\n'

            for next_move in self.next_moves:
                str_so_far += next_move._str_indented(depth + 1, tc)
            return str_so_far


if __name__ == '__main__':
    pass
    # import doctest
    # doctest.testmod(verbose=True)
    # import python_ta

    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['E1136', 'W0221'],
    #     'extra-imports': ['Optional', 'pandas', 'chess_data'],
    #     'allowed-io': ['MoveTree.print_stats'],
    #     'max-nested-blocks': 4
    # })
