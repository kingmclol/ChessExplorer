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

do some `pip install -r requirements.txt`

And run `main.py`.

# Sourcing and Using datasets
I believe that these chess datasets were taken from `lichess.com` games databases. But really, it just needs to be `.pgn` files.

In `main.py`, you'll just need to do some work (or honestly delete the intro code and just load in the files directly.

# Usage
Basically, it's like navigating your filesystem in terminal. Except directories are moves.

I'll fix up this README later (probably not though) to add actual instructions.

# Places for Improvement
- Rather than calculating all of the statistics and saving them in the tree itself, just calculate it by taking in the sequence of chess moves when the respective command is run.
- Code cleanup would have been nice to have, but everything seemed to work without errors during testing.
- The way we structured the data in a tree (and in the `ChessData` class) should be reworked probably (a dictionary that maps to a dictionary feels bad). Although this can likely be solved by the first point.
