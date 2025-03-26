"""
An attempt to make a class that can read the .zst file with all of PGN chess games from lichess.

--> Seems to have worked.
"""
import chess
import chess.pgn
import pandas as pd
import zstandard as zstd 
from typing import Optional

def parse_pgn(filename: str, output_loc: Optional[str] = None) -> pd.DataFrame:
    print(f"Attempting to read games from {filename}.")
    data = {
        "elo_white": [],
        "elo_black": [],
        "opening": [],
        "time_control": [],
        "winner": [],
        "termination": [],
        "moves": []
    }
    # Attempt to read the file
    with zstd.open(filename, 'rt') as f:
        game = chess.pgn.read_game(f)  # Try reading a game
        while game:  # As long as a game can be read
            # Add the entries to the data
            data['elo_white'].append(game.headers.get('WhiteElo', "N/A"))
            data['elo_black'].append(game.headers.get('BlackElo', "N/A"))
            data['opening'].append(game.headers.get('Opening', "N/A"))
            data['time_control'].append(game.headers.get('TimeControl', "N/A"))
            data['winner'].append(game.headers.get("Result", "N/A"))
            data['termination'].append(game.headers.get("Termination", "N/A"))
            data['moves'].append(_get_moves(game))

            game = chess.pgn.read_game(f)  # Read next game
            

        # Write the dataframe       
        df = pd.DataFrame(data)

        if output_loc:  # Save if told to
            df.to_pickle(output_loc)
            print(f"Saved .pkl to {output_loc}.")
        
        print(f"Done ({len(df)} games).")
        
        return pd.DataFrame(data)  # Return the dataframe


def _get_moves(game: chess.pgn.Game) -> list[str]:
    """
    Get the moves in the given chess Game as a list of strings in algebraic notation.
    """
    moves = []
    board = game.board()
    for move in game.mainline_moves():
        moves.append(board.san(move))
        board.push(move)
    
    return moves
        
if __name__ == "__main__":
    # Running this directly --> Convergint the PGN games to dataset
    filepath = input("Filepath to a valid .zst file of lichess chess games: ")

    outpath = input("Where to write the .pkl (processed dataset): ")

    parse_pgn(filepath, outpath)

