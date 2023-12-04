# Tetris
This is a project involving the classic game Tetris. The objective is to develop an algorithm for the highest possible score with a limited number of blocks.

## Example "Gameplay"
![](https://github.com/20tsange1/Tetris/blob/main/TetrisExample.gif)

## What does it consists of?
The player.py file contains my algorithms and functions written to pick and optimise the next move.
The considerations include:
- Number of holes created
- Depth of Wells
- Smoothness
- Line clears
- Lines remaining

The logic is as follows:
- Calculate all the possible moves.
- Use the top 10 moves and calculate all possible proceeding moves.
- Return the highest score and move.
- Repeat

## Finding the correct weightings
In order to balance and create the most effective algorithm, the weightings of the considerations had to be adjusted.
This was done initially through manual alterations. However, there was a clear opportunity to drive this process using a genetic algorithm.
A simple genetic algorithm involving Elitist Selection and a mutation was developed.
