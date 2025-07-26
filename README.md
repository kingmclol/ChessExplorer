# ChessExplorer
Project for a certain computer science course in a certain university for the 2025 academic school year.

Contributors:
- Freeman Wang
- Brady Li
- Guanlin Chen
- Huaijin Hu

No further planned work will be done here, although there are definitely potential places to improve.
# Installation
Just have `python` installed to some reasonable version

`git clone` this

do some `pip install -r requirements.txt` inside the project folder (with these files)

And run `main.py`.

# Sourcing and Using datasets
I believe that these chess datasets were taken from [lichess.com games database](https://database.lichess.org/) but all you really need are `.pgn` files from anywhere you want.

In `main.py`, as it was designed with some existing sample datasets in mind, you will need to remove some existing starter code. I believe this code should work somewhat, with `<tc>` being a timecontrol of your choice:

```python3
def select_dataset():
  # Remove everything else that was here before
  return "path_to_your_chess_database.pgn", <tc>
```
*Note: I'm not fully familiar with how chess time controls work, but I believe they're the length of the game, in seconds. Choose a value that exists in your dataset.*

# Usage
Run `main.py`. You can use stuff like VSCode or PyCharm to do so, or use the terminal directly (`python main.py`).

Due to how we structured the data as a tree, we chose to make the ChessExplorer use filesystem commands to navigate through moves due to a filesystem's tree-like nature. If you are familiar with the terminal, you should find the ChessExplorer fairly easy to use.

## Starting
These instructions assume that `main.py` was not modified (using the sample code). Follow the prompts given.
- **Maximum # of opening moves:** Determines the maximum "levels", or moves deep in a game the ChessExplorer considers. We limited it to a max of 5 due to... performance concerns, but this limit can be removed by editing the `max_moves` function in `main.py`.
- **Dataset to load:** Determines which sample datasets to analyze.

## Traversing
Upon finishing the loading and processing, you are presented with a prompt, and a help menu of commands:

| COMMAND | DESCRIPTION | EXAMPLE | 
| -------- | ------------ | --------- |
|`ls [asc\|desc\|played]` | **List commonly played moves** from the current board state. Optional filter based on playrate. | `ls desc` |
|`cd (move)` | **Play the given moves** in algebraic notation, if legal. Can chain moves as a `/`-seperated list. | `cd c4/e5`|
|`cd ..` | **Undo** last move.| `cd ..` |
|`cd ~` | **Reset** to initial game state. | `cd ~` |
|`stats [tc]` | **Display data** (winrate, playrate) for current board state. Optional timecontrol override for using said timecontrol's data instead of using the `settc` command. | `stats 180`|
|`help`| Displays help menu | `help` |
|`settc (tc)` | **Set global default timecontrol** (for `ls`, `stats`, etc.) to given timecontrol. | `settc 300` |
|`timecontrols` | **Display common timecontrols**. Just a reminder for folks like me who don't know chess. |`timecontrols`|
|`tree`| **Display tree of next possible moves** from current board state. Alternative to `ls` with less data, but more deeper levels. | `tree`|

The prompt contains information about the current board state (what moves were played, in order) and allows you to input one of the commands above. It looks like a string of
moves in algebraic notation, seperated by a slash `/` and ends with a colon `:`. Examples being:
- `/:` Default board. No moves have been played.
- `/e4/e5/Nf3/Nc6:` The listed moves have been played, in order of their listing from left-to-right. This sequence corresponds with the opening _King's Knight Opening: Normal Variation_.

Suppose you want to calculate the statistics for games with timecontrol 300 seconds (5 minutes), finding the most common move played after the first move of `Nf3`:

```
/dunno/where/you/started/so/: cd ~
/: settc 300
Set global timecontrol to 300.
/: cd Nf3
/Nf3: ls desc
NEXT MOVE     PLAYRATE    WHITE WIN     BLACK WIN     DRAW       NAME
d5            32.62%      45.65%        54.35%        0.0%       Zukertort Opening
...           ...         ...           ...           ...        ...
...           ...         ...           ...           ...        ...
/Nf3:
```
So it seems that _for the used game dataset(s) and games with a timecontrol of 300_, the most common move played after a first move of `Nf3` is `d5`, with ~33% players facing said situation playing `d5`.

# Places for Improvement
- Rather than calculating all of the statistics and saving them in the tree itself, just calculate them by taking in the sequence of chess moves when the respective command is run. Or, only save the statistics after the initial calculation, so less time is wasted on calculating game paths that the user does not explore.
- Code cleanup would have been nice to have, but everything seemed to work without errors during testing. So, good enough.
- The way we structured the data in a tree (and in the `ChessData` class) should be reworked probably (a dictionary that maps to a dictionary feels bad). This is primarily because the original ChessExplorer was designed with specific time-controls in mind, so we needed to calculate the same statistics for each timecontrol. Surely, another data structure would be better, but I couldn't think of one at the time.
- Keeping the *actual* filesystem commands was not a good move, as it would be easy to convert them to more... *thematic* commands (like `ls` -> `nextmoves`, `cd (move) -> play (move)`, `cd .. -> reset`), but it would require a lot more testing for errors, where I would not have time to do so.  
- It should be possible to use `python-chess` to print out a text representation of the board, as we already store the played moves (the current "directory" path), but we did not have enough time to implement it.
