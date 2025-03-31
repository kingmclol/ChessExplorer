"""
ChessData stores data for each chess game, including win rates, play rates, and play counts.

The statistics are calculated for each time control and opening sequences.
"""
from __future__ import annotations
from typing import Optional

import pandas as pd

PADDING = 12


class ChessData:
    """
    A class that stores data about a chess state
    """
    name: Optional[str]
    win_data: dict[int, dict[str, float]]
    playrate: dict[int, float]
    plays: dict[int, float]
    move_sequence: list[str]

    def __init__(self, move_sequence: list[str], data: pd.DataFrame, name: Optional[str] = None) -> None:
        self.name = name
        self.move_sequence = move_sequence
        self._calc_data(move_sequence, data)

    def _calc_data(self, move_sequence: list[str], data: pd.DataFrame) -> None:
        """Calculate the win rate if this move is played for different time controls."""
        win_data = {}
        playrate = {}
        plays = {}
        tcs = data['time_control'].unique()

        for tc in tcs:
            # Filter by time control first
            filtered_curr = data[(data['time_control'] == tc)
                                 & (data['moves'].apply(lambda moves: isinstance(moves, list) and moves[:len(
                                     move_sequence)] == move_sequence))]

            plays[tc] = len(filtered_curr)
            win_data[tc] = {}
            for winner in ["white", "black", "draw"]:
                # Avoid NaN values
                win_data[tc][winner] = len(filtered_curr[filtered_curr['winner'] == winner]) / len(filtered_curr) \
                    if not filtered_curr.empty else 0.0
            # Previous move sequence filtering
            filtered_prev = data[(data['time_control'] == tc)
                                 & (data['moves'].apply(lambda moves: isinstance(moves, list) and moves[:max(len(
                                     move_sequence) - 1, 0)] == move_sequence[:-1]))]
            # Avoid division by zero
            playrate[tc] = len(filtered_curr) / len(filtered_prev) if len(filtered_prev) > 0 else 0.0

        self.win_data = win_data
        self.playrate = playrate
        self.plays = plays

    def output_stats(self, tc: int) -> None:
        """Print out the stats for this board state, given the time control."""
        print(f"{self.name if self.name else "Not an opening"}")
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
        """
        Return the play rate (% of games that played this after the last move) for the given timecontrol.
        Return 0.0 if no data.
        """
        return self.playrate.get(tc, 0.0)

    def get_winrate(self, winner: str, tc: int) -> float:
        """
        Return the win rate for the winner (yes, draw is a player but yeah) for the given
        timecontorl.

        Return 0.0 if no data for the timecontrol.

        Preconditions:
        - winner in {'black', 'white', 'draw'}
        """
        data = self.win_data.get(tc, None)
        if not data:
            return 0.0
        else:
            return data.get(winner, 0.0)


def percentify(val: float, dp: int) -> str:
    """
    Return the value as a string percentange, rounded to dp decimal points.

    >>> percentify(0.7321, 2)
    '73.21%'
    """
    return f"{round(val * 100, dp)}%"


if __name__ == '__main__':
    pass
    # import doctest
    # doctest.testmod(verbose=True)
    # import python_ta

    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['E1136', 'W0221'],
    #     'extra-imports': ['move_tree', 'percentify', 'Optional', 'chess_data', 'pandas'],
    #     'allowed-io': ['ChessData.output_stats'],
    #     'max-nested-blocks': 4
    # })
