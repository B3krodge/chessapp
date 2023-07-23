from constants import *
from square import Square
from piece import *
from move import Move

class Board:
    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")

    def move(self, piece, move):
        
        initial = move.initial
        final = move.final
        #console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        #moving piece
        if (initial != final):
            piece.moved = True
        
        if isinstance(piece, King):
            if self.castling(initial, final):
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])
        #clear valid moves
        piece.clear_moves()
        #set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves
    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def calc_moves(self, piece, row, col):
        def pawn_moves():
            steps = 1 if piece.moved else 2
            #vertical moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else:
                        break
                else:
                    break
            possible_move_row = row + piece.dir
            possible_move_cols = (col - 1, col + 1)
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def knight_moves():
            possible_moves = [
                (row - 2, col - 1),
                (row - 2, col + 1),
                (row + 2, col - 1),
                (row + 2, col + 1),
                (row - 1, col + 2),
                (row - 1, col - 2),
                (row + 1, col + 2),
                (row + 1, col - 2),
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)
        
        def straight_line_moves(incs):
            for inc in incs:
                row_inc, col_inc = inc
                possible_move_row = row + row_inc
                possible_move_col = col + col_inc
                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial  = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            piece.add_move(move)
                        if self.squares[possible_move_row][possible_move_col].has_rival_piece(piece.color):
                            piece.add_move(move)
                            break
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    else:
                        break
                    possible_move_row = possible_move_row + row_inc
                    possible_move_col = possible_move_col + col_inc

        def king_moves():
            
            possible_moves =[
                (row - 1, col + 1),
                (row - 1, col - 1),
                (row + 1, col + 1),
                (row + 1, col -1),
                (row, col +1),
                (row, col -1),
                (row + 1, col),
                (row - 1, col),
            ]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rival(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)
            if not piece.moved:
                #queen castling
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                break

                            if c == 3:
                                piece.left_rook = left_rook
                                
                                initial = Square(row,0)
                                final = Square(row, 3)
                                move = Move(initial, final)
                                left_rook.add_move(move)

                                initial = Square(row,col)
                                final = Square(row, 2)
                                move = Move(initial, final)
                                piece.add_move(move)
                #king castling
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7):
                            if self.squares[row][c].has_piece():
                                break

                            if c == 6:
                                piece.right_rook = right_rook
                                
                                initial = Square(row,7)
                                final = Square(row, 5)
                                move = Move(initial, final)
                                right_rook.add_move(move)

                                initial = Square(row,col)
                                final = Square(row, 6)
                                move = Move(initial, final)
                                piece.add_move(move)
        if piece.name == "pawn": pawn_moves()

        
        elif piece.name == "knight": knight_moves()

        elif piece.name == "bishop": 
            straight_line_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
            ])
            
        elif piece.name == "rook":
            straight_line_moves([
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
            ])
            
        elif piece.name == "queen":
            straight_line_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
                (0, 1),
                (0, -1),
                (1, 0),
                (-1, 0),
            ])
            
        elif piece.name == "king":
            king_moves()
            

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self,color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)
    ##creation of pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
    #knights
        self.squares[row_other][1]= Square(row_other, 1, Knight(color))
        self.squares[row_other][6]= Square(row_other, 6, Knight(color))
    #bishops
        self.squares[row_other][2]= Square(row_other, 2, Bishop(color)) 
        self.squares[row_other][5]= Square(row_other, 5, Bishop(color))
        
    #rooks
        self.squares[row_other][0]= Square(row_other, 0, Rook(color)) 
        self.squares[row_other][7]= Square(row_other, 7, Rook(color))
    #queen
        self.squares[row_other][3]= Square(row_other, 3, Queen(color)) 
    #king
        self.squares[row_other][4]= Square(row_other, 4, King(color))
    
