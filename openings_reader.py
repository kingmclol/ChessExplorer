"""
File with methods that involve reading the chess openings .tsv files.
"""
import csv


def get_openings(path: str, max_moves: int = -1) -> dict[tuple[str, ...], str]:
    """
    Return a dictionary mapping between TUPLES of moves to the name of the opening,
    restricted to the max number of moves given from the ECO .tsv files located in the given PATH (directory)
    a.tsv, b.tsv, etc.

    If no max_moves given, there is no limit applied.
    """
    # Load all relevant data from the .tsv files
    mapping = {}
    for letter in "abcde":  # quick way to read from each file
        filepath = f"{path}/{letter}.tsv"
        with open(filepath) as file:
            reader = csv.reader(file, delimiter="\t")
            next(reader)  # clear headers
            for row in reader:
                moves = _clean_moves(row[2])
                if max_moves != -1 and len(moves) > max_moves:
                    continue  # skip this opening
                mapping[tuple(moves)] = row[1]

    return mapping


def _clean_moves(moves: str) -> list[str]:
    """Given a movelist string, clean it up and return it as a list of moves instead.

    >>> _clean_moves('1. d4 f5 2. c4 Nf6 3. g3 e6 4. Bg2 Be7 5. Nf3 O-O 6. O-O d5')
    ['d4', 'f5', 'c4', 'Nf6', 'g3', 'e6', 'Bg2', 'Be7', 'Nf3', 'O-O', 'O-O', 'd5']
    """
    return [move for move in moves.split() if move[-1] != '.']


if __name__ == "__main__":
    pass
    # import doctest

    # doctest.testmod(verbose=True)

    # import python_ta

    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['E1136', 'W0221'],
    #     'extra-imports': ['csv'],
    #     'allowed-io': ['get_openings'],
    #     'max-nested-blocks': 4
    # })
