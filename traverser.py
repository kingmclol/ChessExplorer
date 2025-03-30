"""
Traverser is the class that takes in the MoveTree and allows for user interaction.

Commands emulate navigation of a filesystem using the terminal; directories are MoveTrees.
"""
from typing import Optional
from move_tree import MoveTree
from chess_data import percentify

PADDING_RATES = 12
PADDING_NEXT_MOVE = 12
PADDING_NAME = 50
PADDING_COMMAND = 25
COMMANDS = ['ls', 'cd', 'tree', 'info', 'settc', 'help', 'find', 'stats', 'timecontrols']


class Traverser:
    """
    A class that binds with a MoveTree to allow for user traversal and displaying stats.

    Different timecontrols can be selected when displaying stats.
    """
    # Private Instance Attributes:
    # - _home: The "home directory". That is, the default MoveTree Node
    # - _current: The MoveTree node that the traverser currently is in
    # - _path: The current path from the true root to _current
    # - _timecontrol: The current timecontrol set for this MoveTree.
    _home: MoveTree
    _path: list[str]
    _current: MoveTree
    _timecontrol: Optional[int] = None

    def __init__(self, home: MoveTree, default_tc: Optional[int] = None) -> None:
        """
        Create and bind a Traverser's home node to the given MoveTree.

        Sets the default time control to the given one, if provided. Otherwise, have no timecontrol
        set.
        """
        self._home = home
        self._path = home.get_path()
        self._current = home
        self._timecontrol = default_tc

    def interactive(self) -> None:
        """
        Start the interactivitiy of the Traverser, allowing for user input to navigate through the
        binded MoveTree.
        """
        while True:
            raw_user_input = input(f"{self._path_to_str()}: ").strip()
            base, parameter = parse_command(raw_user_input)
            if validate_command(base):
                self.handle_input(base, parameter)
            else:
                print(f"stkfsh: command not found: {base}")

    def handle_input(self, command: str, param: Optional[str] = None) -> None:
        """
        Attempts to handle the command and parameter.
        """
        if command == 'ls':
            if param and param not in {'asc', 'desc', 'played'}:  # If the parameter was invalid
                print(f"ls: Expected no parameter or one of ['asc', 'desc', 'played'], got {param}")
                return
            self.ls(param)
        elif command in {'info', 'stats'}:
            tc = self._extract_tc(param)
            if not tc:
                print(f"info: Expected positive int or no parameter, got {param}")
                return
            self.output_stats(tc)
        elif command == 'help':
            self.output_help()
        elif command == 'tree':
            self.output_tree()
        elif command == 'settc':
            tc = self._extract_tc(param)
            if not tc or not param:  # also if error in casting or no parameter given do nothing
                print(f"stats: Expected positive int, got {param}")
                return
            self._timecontrol = tc
            print(f"Set global timecontrol to {tc}.")
        elif command == 'cd':
            self.apply_traverse(param)
        elif command == 'timecontrols':
            self.timecontrols()

    def _extract_tc(self, param: Optional[str] = None) -> Optional[int]:
        """
        From the parameter, attempt to extract a time control value (integer). If no parameter, will return
        the global one.

        If the parsed time control is negative, return None
        If the parameter was provided and FAILS to cast to an integer, returns None.
        """
        if not param:
            return self._timecontrol
        else:
            try:
                tc = int(param)
                return tc if tc > 0 else None
            except ValueError:
                return None

    def output_help(self) -> None:
        """
        Print out help information.
        """
        print("Note: tc means time control (game duration in seconds). [] is optional parameter. () is required.")
        print("Commands:")
        print(f"  {'ls [asc|desc|played]':<{PADDING_COMMAND}}- List common moves from the current position. "
              f"Optional filters based on playrate.")
        print(f"  {'cd (move)':<{PADDING_COMMAND}}- Move to the position after a specified move")
        print(f"  {'cd ..':<{PADDING_COMMAND}}- Move back to the previous position")
        print(f"  {'stats [tc]':<{PADDING_COMMAND}}- Display winrate and best move calculations")
        print(f"  {'help':<{PADDING_COMMAND}}- Display the help menu")
        print(f"  {'settc (tc)':<{PADDING_COMMAND}}- Set the global time control")
        print(f"  {'timecontrols':<{PADDING_COMMAND}}- Display the time controls available")
        print(f"  {'tree':<{PADDING_COMMAND}}- Display the move tree constructed")

    def timecontrols(self) -> None:
        """
        Gives the user the 4 avaiable time controls
        """
        print("Time controls available: 60 sec, 180 sec, 300 sec, 600 sec")

    def output_tree(self) -> None:
        """
        Output the MoveTree, RELATIVE to the current node.
        """
        print(self._current)

    def output_stats(self, tc: Optional[int] = None) -> None:
        """
        Print out the statistics for the current MoveTree node, for the given time control.
        """
        if not tc:
            tc = self._timecontrol  # set to global version
        self._current.print_stats(tc)

    def ls(self, param: Optional[str] = None) -> None:
        """
        List-moves that are one level deeper tha n current, using global timecontrol

        Given the param, output in a specific way. If no param given, just output without any
        changes

        Preconditions:
         - param in {'asc', 'desc', 'played'}
        """
        next_moves = self._current.next_moves
        if param == "asc":
            next_moves = sorted(next_moves, key=lambda move: move.data.get_playrate(self._timecontrol))
        elif param == "desc":
            next_moves = sorted(next_moves, key=lambda move: move.data.get_playrate(self._timecontrol), reverse=True)
        elif param == "played":
            next_moves = [move for move in next_moves if move.data.playrate[self._timecontrol] != 0]

        self._print_moves(next_moves)

    def _print_moves(self, moves: list[MoveTree], tc: Optional[int] = None) -> None:
        """
        Print out the moves in a pretty formatted manner. If not given any tc, use default.
        """
        if not moves:
            print("There's no more moves to list...")
            return
        if not tc:
            tc = self._timecontrol
        print(f"{'NEXT MOVE':<{PADDING_NEXT_MOVE}}"
              f"{'PLAYRATE':<{PADDING_RATES}}"
              f"{'WHITE WIN':<{PADDING_RATES}}"
              f"{'BLACK WIN':<{PADDING_RATES}}"
              f"{'DRAW':<{PADDING_RATES}}"
              f"{'NAME':<{PADDING_NAME}}")

        for move in moves:
            print(f"{move.move:<{PADDING_NEXT_MOVE}}"
                  f"{percentify(move.data.get_playrate(tc), 2):<{PADDING_RATES}}"
                  f"{percentify(move.data.get_winrate("white", tc), 2):<{PADDING_RATES}}"
                  f"{percentify(move.data.get_winrate("black", tc), 2):<{PADDING_RATES}}"
                  f"{percentify(move.data.get_winrate("draw", tc), 2):<{PADDING_RATES}}"
                  f"{move.data.get_name():<{PADDING_NAME}}")

    def apply_traverse(self, param: str) -> None:
        """
        Attempt to traverse through the given path, just like how a cd in the terminal would.
        """
        moves = param.split("/")
        test = self._current
        test_path = self._path.copy()
        for move in moves:
            if move == "~":
                test = self._home
                test_path = self._home.get_path()
            elif move == ".." and test.parent:
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
                    print(f"cd: Could not navigate path {param}")
                    return
            if test:
                self._current = test
                self._path = test_path

    def _path_to_str(self) -> str:

        return "/" + "/".join(self._path)


def parse_command(command: str) -> tuple[str, Optional[str]]:
    """
    Parse command into the actual command and param as a tuple (choice, param).

    If no param is given, the param is None.
    If given empty string, choice is "", param is None.

    >>> parse_command("cd e4/e5")
    ('cd', 'e4/e5')
    >>> parse_command("ls")
    ('ls', None)
    >>> parse_command("apples 40")
    ('apples', '40')
    """
    split = command.split(maxsplit=1)
    choice, param = "", None
    # The split can have 0, 1, or 2 elements.
    # 0 element case (empty input) handled by default choice initialization.
    if len(split) == 1:
        choice = split[0]
    elif len(split) == 2:  # len(split) == 2 as max due to maxsplit=1
        choice, param = split[0], split[1]
    return choice, param


def validate_command(cmd: str) -> bool:
    """
    Return whether the command (the base command, without parameters) is a valid command.
    >>> validate_command('balls')
    False
    >>> validate_command('ls')
    True
    """
    return cmd in COMMANDS


if __name__ == '__main__':
    pass
    # import doctest
    # doctest.testmod(verbose=True)
    # import python_ta

    # python_ta.check_all(config={
    #     'max-line-length': 120,
    #     'disable': ['E1136', 'W0221'],
    #     'extra-imports': ['move_tree', 'percentify', 'Optional', 'chess_data'],
    #     'allowed-io': ['Traverser._print_moves',
    #                    'Traverser.output_tree',
    #                    'Traverser.output_help',
    #                    'Traverser.output_stats',
    #                    'Traverser.ls',
    #                    'Traverser.apply_traverse',
    #                    'Traverser.handle_input',
    #                    'Traverser.timecontrols',
    #                    'Traverser.interactive'],
    #     'max-nested-blocks': 4
    # })
