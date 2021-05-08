# AI-based Checkers game with MiniMax Algorithm made using pygame module

Checkers is a strategy board game for two players which involves diagonal moves of uniform game pieces and mandatory captures by jumping over opponent pieces.

The goal of Checkers is to remove all your opponent's pieces from the board or prevent them from making a move. Pieces move diagonally, always staying on the dark squares.
Pieces can "slide" to an adjacent open square or "jump" over an opponent's pieces, removing them from the board. Normal pieces move toward the opposite side of the board.
When a normal piece reaches the last row on the opposite side of the board it is promoted into a "King" piece. Promoted pieces may move towards either side of the board.
The game is over when one player has no remaining pieces or can't make any valid moves. The player must make a jump move when available which can even be a double or
triple jump.

In this program the player plays against the computer which makes use of a simple implementation of the **minimax algorithm** for the opponent (WHITE Player).
It uses a very simple evaluation function:<br/>
`white_pieces_left - black_pieces_left + (white_kings * 0.5 - black_kings * 0.5)` which is optimized for the automated WHITE player.

## Some hints to play competitively

1. Use the side of the board to prevent being jumped over, but don't get stuck!
2. Always keep your pieces doubled up diagonally to block your opponent's jumps.
3. Quickly get your pieces promoted to kings so they can move forward and backward across the board.
4. Try to lure your opponent into a double or triple jump trap.

## A look into the game

<p align="center">
  <img width="451" alt="Capture" src="https://user-images.githubusercontent.com/60784823/117530987-9a936300-aff9-11eb-914f-4352563636ac.PNG">&nbsp;&nbsp;&nbsp;&nbsp;
  <img width="451" alt="Capture" src="https://user-images.githubusercontent.com/60784823/117531155-97e53d80-affa-11eb-978a-817e2c8a079d.png">
  <br/><br/>
  <img width="451" alt="Capture" src="https://user-images.githubusercontent.com/60784823/117531157-99af0100-affa-11eb-86d1-21b944703324.png">&nbsp;&nbsp;&nbsp;&nbsp;
  <img width="451" alt="Capture" src="https://user-images.githubusercontent.com/60784823/117531160-9c115b00-affa-11eb-8d54-ed48976c02d6.png">
  <br/><br/>
  <img width="451" alt="Capture" src="https://user-images.githubusercontent.com/60784823/117531161-9f0c4b80-affa-11eb-8807-07b93f17e9cf.png">&nbsp;&nbsp;&nbsp;&nbsp;
  <img width="451" alt="Capture" src="https://user-images.githubusercontent.com/60784823/117531163-a3386900-affa-11eb-9dad-da7466dc32ce.png">
  <br/>
</p>

## Requirements

Python3<br/>
Pygame Module<br/>
