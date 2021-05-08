import pygame # used for visualization
pygame.init()

# defining constant attributes for game
ROWS,COLS = 8,8
WIDTH,HEIGHT = 600,600
SQUARE_SIZE = WIDTH // COLS # floor division

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
OLIVE = (128, 128, 0)
KHAKI = (240, 230, 140)
GOLD = (255, 215, 0)


class Piece:
    PADDING = 15
    
    def __init__(self, row, col, color):
        self.x = 0
        self.y = 0
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.calculate_coordinates()
        
    def calculate_coordinates(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2
        
    def move(self, row, col):
        self.row = row
        self.col = col
        self.calculate_coordinates()

    def make_king(self):
        self.king = True
        
    def draw(self, window):
        radius = SQUARE_SIZE // 2 - self.PADDING
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        if self.king:
            pygame.draw.circle(window, GOLD, (self.x, self.y), radius + 5, 5)


class Board:

    def __init__(self):
        self.board = []
        self.black_pieces_left = self.white_pieces_left = 12
        self.black_kings = self.white_kings = 0
        self.make_board()
        
    def make_board(self): # creates lists for rows in board and places pieces in it
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, BLACK))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    
    def draw_squares(self, window):
        window.fill(OLIVE)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, KHAKI, (row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
    def draw(self, window):
        self.draw_squares(window)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)
                
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    def move(self, piece, row, col):
        self.board[row][col], self.board[piece.row][piece.col] = self.board[piece.row][piece.col], self.board[row][col] # swapping elements of board
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.black_kings += 1
        
    def remove(self, pieces): # remove captured pieces from board and update pieces count
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == WHITE:
                    self.white_pieces_left -= 1
                else:
                    self.black_pieces_left -= 1
                    
    def evaluation(self): # evaluation function for minimax ; optimized for WHITE player (AI based)
        return self.white_pieces_left - self.black_pieces_left + (self.white_kings * 0.5 - self.black_kings * 0.5)
    
    def winner(self):
        if self.black_pieces_left <= 0:
            return WHITE
        elif self.white_pieces_left <= 0:
            return BLACK
        else:
            return None

    def get_valid_moves(self, piece): # based on row and column of the piece
        moves = {}
        row = piece.row
        left = piece.col - 1
        right = piece.col + 1

        # update the mapping of moves dictionary according to the exploration
        if piece.color == BLACK or piece.king:
            moves.update(self.explore_left_moves(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self.explore_right_moves(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self.explore_left_moves(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self.explore_right_moves(row + 1, min(row + 3, ROWS), 1, piece.color, right))
    
        return moves

    def explore_left_moves(self, start, stop, step, color, left, captured=[]):
        moves = {}
        last_capture = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current_piece = self.board[r][left]
            if current_piece == 0:
                if captured and not last_capture:
                    break
                elif captured:
                    moves[(r, left)] = last_capture + captured # double piece capture
                else:
                    moves[(r, left)] = last_capture
                
                if last_capture:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    # recursive exploration for double piece capture
                    moves.update(self.explore_left_moves(r + step, row, step, color, left - 1, captured = last_capture))
                    moves.update(self.explore_right_moves(r + step, row, step, color, left + 1, captured = last_capture))
                break
            elif current_piece.color == color: # cannot land on piece of same color
                break
            else:
                last_capture = [current_piece]

            left -= 1
        return moves

    def explore_right_moves(self, start, stop, step, color, right, captured=[]):
        moves = {}
        last_capture = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current_piece = self.board[r][right]
            if current_piece == 0:
                if captured and not last_capture:
                    break
                elif captured:
                    moves[(r,right)] = last_capture + captured # double piece capture
                else:
                    moves[(r, right)] = last_capture
                
                if last_capture:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS)
                    # recursive exploration for double piece capture
                    moves.update(self.explore_left_moves(r + step, row, step, color, right - 1, captured = last_capture))
                    moves.update(self.explore_right_moves(r + step, row, step, color, right + 1, captured = last_capture))
                break
            elif current_piece.color == color: # cannot land on piece of same color
                break
            else:
                last_capture = [current_piece]

            right += 1
        return moves


class Checkers:

    def __init__(self, window):
        self.window = window
        self.board = Board()
        self.turn = BLACK
        self.valid_moves = {}
        self.selected = None

    def refresh(self): # to update the checkers board after players turn
        self.board.draw(self.window)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def winner(self):
        return self.board.winner()

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def get_board(self):
        return self.board

    def select(self, row, col):
        if self.selected:
            moved = self.move(row, col)
            if not moved:
                self.selected = None # reset selection
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def move(self, row, col): # to move the piece if valid and remove captures
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            captured = self.valid_moves[(row, col)]
            if captured:
                self.board.remove(captured)
            self.change_turn()
        else:
            return False

        return True

    def move_using_AI(self, new_board): # to update the board with the best move from minimax
        self.board = new_board
        self.change_turn()

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, GREEN, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)


def make_move(piece, move, board, capture):
    board.move(piece, move[0], move[1]) # move[0] is row and move[1] is column
    if capture:
        board.remove(capture)
    return board

from copy import deepcopy # to make exploration on a temporary board copy
def get_all_moves(board, color, game):
    moves = []
    no_more_moves = True

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        if valid_moves:
            no_more_moves = False # indicating that moves still exist
        
        for move, capture in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = make_move(temp_piece, move, temp_board, capture)
            moves.append(new_board)

    if no_more_moves:   # no moves left imply no more captures ; end of the game reached
        if color == WHITE:
            board.white_pieces_left = 0
        elif color == BLACK:
            board.black_pieces_left = 0

    return moves

def minimax(board, depth, max_turn, game):
    if depth == 0 or board.winner() != None:
        return board.evaluation(), board
    
    if max_turn:
        best_move = None
        max_evaluation = float('-inf')
        for move in get_all_moves(board, WHITE, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            max_evaluation = max(max_evaluation, evaluation)
            if max_evaluation == evaluation:
                best_move = move
        
        return max_evaluation, best_move   
    else:
        best_move = None
        min_evaluation = float('inf')
        for move in get_all_moves(board, BLACK, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            min_evaluation = min(min_evaluation, evaluation)
            if min_evaluation == evaluation:
                best_move = move
        
        return min_evaluation, best_move


WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) # initialize a window for display
pygame.display.set_caption('CHECKERS')

def get_coordinates_from_mouse(position):
    x, y = position
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    
    ongoing = True # to indicate game status

    game = Checkers(WINDOW)
    clock = pygame.time.Clock()

    while ongoing:
        clock.tick(60) # Frames Per Second set to 60
        
        if game.turn == WHITE: # the automated player
            new_board = minimax(game.get_board(), 4, WHITE, game)[1]
            game.move_using_AI(new_board)

        if game.winner() != None:
            if game.winner() == WHITE:
                print('\nPlayer WHITE is the winner\n')
                pygame.display.set_caption('CHECKERS    Player WHITE is the winner!!')
            elif game.winner() == BLACK:
                print('\nPlayer BLACK is the winner\n')
                pygame.display.set_caption('CHECKERS    Player BLACK is the winner!!')

            ongoing = False
            pygame.time.delay(5000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ongoing = False
            
            if event.type == pygame.MOUSEBUTTONDOWN: # get move for Player BLACK's turn
                position = pygame.mouse.get_pos()
                row, col = get_coordinates_from_mouse(position)
                game.select(row, col)
        
        game.refresh() # update board state after each players turn

    pygame.quit() # uninitializing


main() # call to start the game