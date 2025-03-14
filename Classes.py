from __future__ import annotations
from typing import Optional, Any

class Opening:
    """
    A class to represent a chess opening.

    Instance Attributes:
    - moves: A list of strings that represent the moves that create this opening
    - name: The name of this opening
    - eco: ECO label for this opening
    """
    name: str
    moves: tuple[str]
    eco: str
    data: dict[str, dict[str, float]]  # key is time control, value is dict with winrate/plays/etc.

    def __init__(self, eco: str, name: str, moves: tuple[str], data: dict = None):
        self.name = name
        self.moves = moves
        self.eco = eco
        self.data = {} if not data else data

    def __str__(self) -> str:
        """Return the name of this opening.
        
        >>> print(Opening('A00', 'Opening A00', ['d4', 'idk']))
        Opening A00
        """
        return self.name
    
    def get_data(self, time_control: str):
        """
        Get the relevant data for this opening based on the time control given.
        """
        return self.data[time_control]

# class OpeningTree:
#     """
#     A tree for chess openings.
#     """
#     # Private Instance Attributes:
#     #  - _opening: An opening object that represents this chess opening
#     #  - _responses: The response openings to this opening
#     _opening: Optional[Opening]
#     _responses: list[OpeningTree]

#     def __init__(self, opening: Opening, responses: list[Opening] = None):
#         self._opening = opening
#         self._responses = responses
    
#     def is_empty(self) -> bool:
#         return not self._opening
    
#     def __len__(self) -> int:
#         if self.is_empty():
#             return 0
#         else:
#             size = 1
#             size += sum(response.__len__() for response in self._responses)
#             return size
    
#     def add_opening(self, opening: Opening) -> None:
#         path = opening.moves
#         self._insert_sequence(path, opening)

#     def _insert_sequence(self, path: list[str], opening: Opening):
#         if not path:  # An empty path always exists.
#             return
#         else:
#             existing = False
#             for response in self._responses:
#                 if response._root == path[0]:  # found an existing path go continue
#                     response.insert_sequence(path[1:])
#                     existing = True
#                     break

#             if not existing:  # existing subtree not found; create own
#                 new_sub = OpeningTree(
#                     Opening("N/A", "Name="), [])
#                 self._responses.append(new_sub)
#                 new_sub.insert_sequence(path[1:])
    
#     def get_opening(self) -> Opening:
#         return self._opening
    
class Tree:
    """A recursive tree data structure.

    Note the relationship between this class and RecursiveList; the only major
    difference is that _rest has been replaced by _subtrees to handle multiple
    recursive sub-parts.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    _root: Optional[Any]
    _subtrees: list[Tree]
    _data: Optional[Any]
    def __init__(self, root: Optional[Any], subtrees: list[Tree]) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees
        self._data = None

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
        >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

    def __len__(self) -> int:
        """Return the number of items contained in this tree.

        >>> t1 = Tree(None, [])
        >>> len(t1)
        0
        >>> t2 = Tree(3, [Tree(4, []), Tree(1, [])])
        >>> len(t2)
        3
        """
        if self.is_empty():
            return 0
        else:
            size = 1  # count the root
            for subtree in self._subtrees:
                size += subtree.__len__()  # could also write len(subtree)
            return size

    def __contains__(self, item: Any) -> bool:
        """Return whether the given is in this tree.

        >>> t = Tree(1, [Tree(2, []), Tree(5, [])])
        >>> t.__contains__(1)
        True
        >>> t.__contains__(5)
        True
        >>> t.__contains__(4)
        False
        """
        if self.is_empty():
            return False
        elif self._root == item:
            return True
        else:
            for subtree in self._subtrees:
                if subtree.__contains__(item):
                    return True
            return False

    def __str__(self) -> str:
        """Return a string representation of this tree.

        For each node, its item is printed before any of its
        descendants' items. The output is nicely indented.

        You may find this method helpful for debugging.
        """
        return self._str_indented(0).rstrip()

    def _str_indented(self, depth: int) -> str:
        """Return an indented string representation of this tree.

        The indentation level is specified by the <depth> parameter.
        """
        if self.is_empty():
            return ''
        else:
            str_so_far = '  ' * depth + f'{self._root}' + f'{'' if self._data is None else f" | {self._data}"}' + '\n'
            for subtree in self._subtrees:
                # Note that the 'depth' argument to the recursive call is
                # modified.
                str_so_far += subtree._str_indented(depth + 1)
            return str_so_far

    def remove(self, item: Any) -> bool:
        """Delete *one* occurrence of the given item from this tree.

        Do nothing if the item is not in this tree.
        Return whether the given item was deleted.
        """
        if self.is_empty():
            return False
        elif self._root == item:
            self._delete_root()  # delete the root
            return True
        else:
            for subtree in self._subtrees:
                deleted = subtree.remove(item)
                if deleted and subtree.is_empty():
                    # The item was deleted and the subtree is now empty.
                    # We should remove the subtree from the list of subtrees.
                    # Note that mutate a list while looping through it is
                    # EXTREMELY DANGEROUS!
                    # We are only doing it because we return immediately
                    # afterward, and so no more loop iterations occur.
                    self._subtrees.remove(subtree)
                    return True
                elif deleted:
                    # The item was deleted, and the subtree is not empty.
                    return True

            # If the loop doesn't return early, the item was not deleted from
            # any of the subtrees. In this case, the item does not appear
            # in this tree.
            return False

    def _delete_root(self) -> None:
        """Remove the root item of this tree.

        Preconditions:
            - not self.is_empty()
        """
        if self._subtrees == []:
            self._root = None
        else:
            # Strategy: Promote a subtree (the rightmost one is chosen here).
            # Get the last subtree in this tree.
            last_subtree = self._subtrees.pop()

            self._root = last_subtree._root
            self._subtrees.extend(last_subtree._subtrees)

    ############################################################################
    # Part 1.1: Tree methods
    ############################################################################
    def __repr__(self) -> str:
        """Return a one-line string representation of this tree.

        >>> t = Tree(2, [Tree(4, []), Tree(5, [])])
        >>> t
        Tree(2, [Tree(4, []), Tree(5, [])])
        """
        subtree_repr = f"[{", ".join([subtree.__repr__() for subtree in self._subtrees])}]"
        if self.is_empty():
            return "Tree(None, [])"
        elif not self._subtrees:
            return f"Tree({self._root}, [])"
        else:
            return f"Tree({self._root}, {subtree_repr})"

    def insert_sequence(self, items: list, data: Any = None) -> None:
        """Insert the given items into this tree.

        The inserted items form a chain of descendants, where:
            - items[0] is a child of this tree's root
            - items[1] is a child of items[0]
            - items[2] is a child of items[1]
            - etc.

        Do nothing if items is empty.

        Preconditions:
            - not self.is_empty()

        >>> t = Tree(111, [])
        >>> t.insert_sequence([1, 2, 3])
        >>> print(t)
        111
          1
            2
              3
        >>> t.insert_sequence([1, 3, 5])
        >>> print(t)
        111
          1
            2
              3
            3
              5

        >>> t = Tree(10, [Tree(2, [Tree(3, [])])])
        >>> t.insert_sequence([2, 3, 4])
        >>> t
        Tree(10, [Tree(2, [Tree(3, [Tree(4, [])])])])

        >>> t = Tree(10, [Tree(2, [Tree(3, [])])])
        >>> t.insert_sequence([2, 3])
        >>> t
        Tree(10, [Tree(2, [Tree(3, [])])])

        >>> t = Tree(10, [Tree(2, [Tree(3, [])])])
        >>> t.insert_sequence([10, 2, 3])
        >>> print(t)
        10
          2
            3
          10
            2
              3
        """
        if not items:
            return
        else:
            existing = False
            for subtree in self._subtrees:
                if subtree._root == items[0] and not existing:  # found an existing path go continue
                    subtree.insert_sequence(items[1:], data)
                    existing = True

            if not existing:  # existing subtree not found; create own
                new_sub = Tree(items[0], [])
                if len(items) == 1:  # If the last added one insert the data payload too
                    new_sub._data = data
                self._subtrees.append(new_sub)
                new_sub.insert_sequence(items[1:], data)

    def traverse_path(self, path: list[Any]) -> Optional[Tree]:
        """
        Return the (sub)tree at the end of the path. Return None if the path is not
        traversable (or empty).

        >>> tree = Tree("", [])
        >>> tree.insert_sequence([True, False, False, True, "Job"])
        >>> tree.insert_sequence([True, False, False, True, "Bob"])
        >>> res1 = tree.traverse_path(["", True, False, False, True])
        >>> res1
        Tree(True, [Tree(Job, []), Tree(Bob, [])])
        >>> tree.traverse_path([True, False, False, False]) is None
        True
        """
        if self.is_empty() or not path:
            return None
        elif self._root == path[0]:
            if len(path) == 1:  # last one has been found!
                return self

            for subtree in self._subtrees:
                result = subtree.traverse_path(path[1:])
                if result is not None:
                    return result

            return None
        else:  # already a dead path
            return None

    def get_subtrees(self) -> list[Tree]:
        """
        Return the subtrees of this tree.
        >>> tree = Tree(1, [Tree(2, []), Tree(3, [])])
        >>> tree.get_subtrees()
        [Tree(2, []), Tree(3, [])]
        """
        return self._subtrees

    def get_root(self) -> Any:
        """
        Return the root value of this tree.
        >>> tree = Tree(1, [Tree(2, []), Tree(3, [])])
        >>> tree.get_root()
        1
        """
        return self._root
    
if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)