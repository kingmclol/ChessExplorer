"""
Class to convert PGN chess games into a picked dataframe as output
E.g., take a lichess chess database
then in console do 
zstdcat [games archive dataset] | GamesReader.py
which creates a dataset.pkl which can be read later into a dataframe for processing
"""

import sys
import chess
import chess.pgn
import pandas as pd
data = {
    "elo_white": [],
    "elo_black": [],
    "opening": [],
    "timecontrol": [],
    "winner": [],
    "termination": [],
}

def parse_pgn() -> pd.DataFrame:
    data = {
        "elo_white": [],
        "elo_black": [],
        "opening": [],
        "time_control": [],
        "winner": [],
        "termination": [],
        "moves": []
    }
    pgn_stream = sys.stdin
    # headers = []
    while True:
        # header = chess.pgn.read_headers(pgn_stream)
        # if header:
        #     data['elo_white'].append(header.get('WhiteElo', "N/A"))
        #     data['elo_black'].append(header.get('BlackElo', "N/A"))
        #     data['opening'].append(header.get('Opening', "N/A"))
        #     data['time_control'].append(header.get('TimeControl', "N/A"))
        #     data['winner'].append(header.get("Result", "N/A"))
        #     data['termination'].append(header.get("Termination", "N/A"))
        game = chess.pgn.read_game(pgn_stream)
        if game:
            data['elo_white'].append(game.headers.get('WhiteElo', "N/A"))
            data['elo_black'].append(game.headers.get('BlackElo', "N/A"))
            data['opening'].append(game.headers.get('Opening', "N/A"))
            data['time_control'].append(game.headers.get('TimeControl', "N/A"))
            data['winner'].append(game.headers.get("Result", "N/A"))
            data['termination'].append(game.headers.get("Termination", "N/A"))
            data['moves'].append(_get_moves(game))
            # if len(data['opening']) == 10:
            #     for key in data:
            #         print(key, len(data[key]))
            #     return pd.DataFrame(data)
        else:
            break
    return pd.DataFrame(data)

def _get_timecontrol(tc: str) -> int:
    """
    >>> _get_timecontrol("300+17")
    300
    """
    print(tc)
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
    "white"
    """
    if result == "1-0":
        return "white"
    elif result == "0-1":
        return "black"
    elif result == "1/2-1/2":
        return "draw"
    else:
        return "N/A"
# def _add_game(data: dict)
df = parse_pgn()

df.to_pickle("dataset.pkl")