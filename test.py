from Classes import Tree, Opening
from Parser import parse_openings, create_mapping

FILE="a.tsv"

openings = parse_openings(FILE)

database = create_mapping(openings)


tree = Tree("", [])

for opening in openings:
    path = opening.moves + [opening]
    # print(path)
    tree.insert_sequence(path)


grob_gambit = database["['g4', 'd5', 'Bg2']"]
print(grob_gambit)
print(grob_gambit in tree)

def extract_opening(tree: Tree, path: list[str])-> Opening | None:
    traversal = tree.traverse_path(path)
    for subtree in traversal.get_subtrees():
        if isinstance(subtree.get_root(), Opening):
            return subtree.get_root()
    
    return None

path = ["", 'g4', 'd5', 'Bg2']
print(extract_opening(tree, path))
