"""
Stuff.
"""
from OpeningsReader import get_openings
from GameReader import read_pgn
from MoveTree import MoveTree, ChessData

openings_database = get_openings("data/openings", 3)
print("Done")

games_database = read_pgn(["data/games/lichess_tournament_2025.03.26_G0j0ZKLB_2000-superblitz (1).pgn"])
print("Done")

tree = MoveTree("", data=ChessData([], games_database))
for move_sequence in openings_database:
    tree.insert_sequence(list(move_sequence), games_database, openings_database)

print(tree)
print(games_database)


class Traverser:
    _home: MoveTree
    _path: list[str]
    _current: MoveTree

    def __init__(self, home: MoveTree):
        self._home = home
        self._path = home.get_path()
        self._current = home

    def interactive(self) -> None:
        while True:
            read = input(f"{self._path_to_str()}: ")
            self.apply_traverse(read)

    def apply_traverse(self, command: str) -> None:
        if command == "":
            return
        temp = command.strip().split(maxsplit=1)
        cmd = temp[0]
        if len(temp) == 2:
            param = temp[1]
        else:
            param = ""

        if cmd == "ls":
            for subtree in self._current.next_moves:
                print(f"{subtree.move} | {subtree.data if subtree.data else None}")
        elif cmd == "cd":
            moves = param.split("/")
            if moves and moves[0] == "~":
                self._current = self._home
                self._path = self._home.get_path()
                return
            test = self._current
            test_path = self._path.copy()
            for move in moves:
                if move == "~":
                    self._current = self._home
                    self._path = self._home.get_path()
                if move == ".." and test.parent:
                    test = test.parent
                    test_path.pop()
                else:
                    valid = False
                    for subtree in test.next_moves:
                        if subtree.move == move:
                            test = subtree
                            valid = True
                            test_path.append(move)
                            break
                    if not valid:
                        print("Cannot travel there")
                        return
            if test:
                self._current = test
                self._path = test_path
        elif cmd == "name":
            print(self._current.data.str() if self._current.data else "(None)")
        elif cmd == "stats":
            # temp
            self._current.print_stats(int(param))

    def _path_to_str(self) -> str:
        return "/" + "/".join(self._path)


traverser = Traverser(tree)
traverser.interactive()
