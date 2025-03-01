import csv
from Classes import Opening
from re import sub
from typing import Optional

def parse_openings(filename: str) -> Optional[list[Opening]]:
    """Given a .tsv that contains chess openings, return a list of Opening objects that
    represent each opening.
    
    Raise FileNotFoundError if the given file does not exist."""
    try:
        openings = []
        with open(filename) as file:
            reader = csv.reader(file, delimiter="\t")  # tab-seperated file
            for line in reader:
                eco = line[0]
                name = line[1]
                moves = _clean_moves(line[2])
                openings.append(Opening(eco, name, moves))
        
        return openings
    except FileNotFoundError:  # File not found
        raise FileNotFoundError(f"File {filename} not found")
    except Exception:  # Likely error while parsing
        raise Exception("Something else went wrong (bad file formatting)?")


def create_mapping(openings: list[Opening]) -> dict[str, Opening]:
    """Return a mapping of a move list to opening object.
    
    >>> opening = Opening('A00', 'Opening A00', ['d4', 'f5'])
    >>> openings = [opening]
    >>> database = create_mapping(openings)
    >>> database == {"['d4', 'f5']" : opening}
    True
    """
    mapping = {}
    for opening in openings:
        mapping[str(opening.moves)] = opening

    return mapping


def _clean_moves(moves: str) -> list[str]:
    """Given a movelist string, clean it up and return it as a list of moves instead.

    >>> _clean_moves('1. d4 f5 2. c4 Nf6 3. g3 e6 4. Bg2 Be7 5. Nf3 O-O 6. O-O d5')
    ['d4', 'f5', 'c4', 'Nf6', 'g3', 'e6', 'Bg2', 'Be7', 'Nf3', 'O-O', 'O-O', 'd5']
    """
    pattern=r"\d\.\s"
    clean = sub(pattern, "", moves)
    return clean.split()


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)