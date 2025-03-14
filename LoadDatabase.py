import pandas as pd
from Classes import Opening, Tree
import chess
from Parser import clean_moves
import csv

MAX_MOVE_LENGTH = 5

def create_dataframe(path: str, max_moves: int) -> pd.DataFrame:
    """
    Create a dataframe of known chess openings, restricted to the max number of moves given from the
    .tsv files located in the given path

    Preconditions:
        - max_moves = 0
    """
    data = {
        "eco": [],
        "name": [],
        "moves": [],
        "num_moves": []
    }
    # Load all relevant data from the .tsv files first into a list before converting to dataframe
    for letter in "abcde":
        filepath = f"{path}/{letter}.tsv"
        with open(filepath) as file:
            reader = csv.reader(file, delimiter="\t")
            next(reader)  # clear headers
            for row in reader:
                data['eco'].append(row[0])
                data['name'].append(row[1])
                moves = clean_moves(row[2])
                data['moves'].append(moves)
                data['num_moves'].append(len(moves))

    df = pd.DataFrame(data)  # Create dataframe
    df = df[df['num_moves'] <= max_moves]  # filter to only those with moves <= the maximum moves
    return df


def generate_tree(data: pd.DataFrame) -> Tree:
    """
    Generate a tree of moves that end up with known chess openings.
    """
    op_tree = Tree("", [])
    for index, row in data.iterrows():
        opening = Opening(
            eco = row['eco'],
            name = row['name'],
            moves = row['moves']
        )
        path = row['moves']
        op_tree.insert_sequence(path, opening)
    return op_tree

tree = generate_tree(create_dataframe("data/openings", MAX_MOVE_LENGTH))
print(tree)

