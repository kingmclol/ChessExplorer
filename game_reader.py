"""
Functions to read a .pgn file, and to convert its main data to a pandas dataframe
"""
import chess
import chess.pgn
import pandas as pd

# The data we will actually collect
HEADERS = ['elo_white', 'elo_black', 'opening', 'time_control', 'winner', 'termination', 'moves']


def read_pgn(filenames: list[str]) -> pd.DataFrame:
    """
    Read the .pgn files given, writing its useful data into a single combined dataframe
    """
    data = _build_headers(HEADERS)
    for filename in filenames:
        with open(filename, 'r') as f:
            game = chess.pgn.read_game(f)
            while game:
                data['elo_white'].append(game.headers.get('WhiteElo', "N/A"))
                data['elo_black'].append(game.headers.get('BlackElo', "N/A"))
                data['opening'].append(game.headers.get('Opening', "N/A"))
                data['time_control'].append(_get_timecontrol(game.headers.get('TimeControl', "N/A")))
                data['winner'].append(_get_winner(game.headers.get("Result", "N/A")))
                data['termination'].append(game.headers.get("Termination", "N/A"))
                data['moves'].append(_get_moves(game))

                game = chess.pgn.read_game(f)  # Read next game

    df = pd.DataFrame(data)
    return df


def _build_headers(headers: list[str]) -> dict:
    """
    Return a dictionary mapping str -> empty list that would be used to build a dataframe
    with the header strings given.

    >>> _build_headers(["Apples", "Bananas"]) == {"Apples": [], "Bananas": []}
    True
    """
    d = {}
    for h in headers:
        d[h] = []

    return d


def _get_timecontrol(tc: str) -> int:
    """
    >>> _get_timecontrol("300+17")
    300
    """
    return int(tc.partition("+")[0])


def _get_moves(game: chess.pgn.Game) -> list[str]:
    moves = []
    board = game.board()
    for move in game.mainline_moves():
        moves.append(board.san(move))
        board.push(move)

    return moves


def _get_winner(result: str) -> str:
    """
    Given the result score, return the winner.

    >>> _get_winner("1-0")
    'white'
    """
    if result == "1-0":
        return "white"
    elif result == "0-1":
        return "black"
    elif result == "1/2-1/2":
        return "draw"
    else:
        return "N/A"


if __name__ == '__main__':
    pass
    # import doctest
    # doctest.testmod(verbose=True)
    # import python_ta

    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['E1136', 'W0221', 'E9998'],
    #     'extra-imports': ['chess', 'chess.pgn', 'pandas'],
    #     'allowed-io': ['read_pgn'],
    #     'max-nested-blocks': 4

    # })
