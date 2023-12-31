import pygame
from constants import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game:
    def __init__(self):
        self.next_player = "white"
        self.board = Board()
        self.hover_square = None
        self.dragger = Dragger()
        self.config = Config()
        # self.square = Square()

        #Show Methods
    def show_bg(self, surface):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    label = self.config.font.render(str(ROWS - row), 1, color)
                    label_pos = (5, 5 + row * SQSIZE)
                    surface.blit(label, label_pos)
                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    label = self.config.font.render(Square.get_alphacol(col), 1, color)
                    # Square.get_alphacol(col)
                    label_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    surface.blit(label, label_pos)


    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece on that square or not
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE//2, row * SQSIZE + SQSIZE//2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect)
    def show_moves(self, surface):
        theme = self.config.theme
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    def show_last_move(self, surface):
        theme = self.config.theme
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
    def show_hover(self, surface):
        if self.hover_square:
            color = (180, 180, 180)
            rect = (self.hover_square.col * SQSIZE, self.hover_square.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"
    def set_hover(self, row, col):
        self.hover_square = self.board.squares[row][col]
    def change_theme(self):
        self.config.change_theme()
    def play_sound(self, capture=False):
        if capture:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
    def restart(self, surface):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    self.board.squares[row][col].piece = None
                    self.board._add_pieces("white")
                    self.board._add_pieces("black")
                    self.next_player = "white"
        if self.board.last_move:
            self.board.last_move = None
           

        
                

