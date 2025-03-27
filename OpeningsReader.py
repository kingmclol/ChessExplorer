"""
File with methods that involve reading the chess openings
"""
import csv


def get_openings(path: str, max_moves: int) -> dict[tuple[str, ...], str]:
    """
    Create a dataframe of known chess openings, restricted to the max number of moves given from the
    .tsv files located in the given path

    Preconditions:
        - max_moves >= 0
    """
    # Load all relevant data from the .tsv files first into a list before converting to dataframe
    mapping = {}
    for letter in "abcde":
        filepath = f"{path}/{letter}.tsv"
        with open(filepath) as file:
            reader = csv.reader(file, delimiter="\t")
            next(reader)  # clear headers
            for row in reader:
                moves = _clean_moves(row[2])
                if len(moves) > max_moves:
                    continue  # skip this opening
                mapping[tuple(moves)] = row[1]

    return mapping


def _clean_moves(moves: str) -> list[str]:
    """Given a movelist string, clean it up and return it as a list of moves instead.

    >>> _clean_moves('1. d4 f5 2. c4 Nf6 3. g3 e6 4. Bg2 Be7 5. Nf3 O-O 6. O-O d5')
    ['d4', 'f5', 'c4', 'Nf6', 'g3', 'e6', 'Bg2', 'Be7', 'Nf3', 'O-O', 'O-O', 'd5']
    """
    # pattern=r"\d\.\s"
    # clean = sub(pattern, "", moves)
    # return clean.split()
    return [move for move in moves.split() if move[-1] != '.']


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
