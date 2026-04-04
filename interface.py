import pygame
from engine import Board, Pawn, Bishop, Knight, Rook, King, Queen

WIDTH = 640
ROWS = 8
CELL_SIZE = WIDTH // ROWS

IMAGES = {}

def load_images():
    pieces = [
        ('Pawn', 1, 'wp.png'), ('Pawn', -1, 'bp.png'),
        ('King', 1, 'wk.png'), ('King', -1, 'bk.png'),
        ('Queen', 1, 'wq.png'), ('Queen', -1, 'bq.png'),
        ('Rook', 1, 'wr.png'), ('Rook', -1, 'br.png'),
        ('Bishop', 1, 'wb.png'), ('Bishop', -1, 'bb.png'),
        ('Knight', 1, 'wn.png'), ('Knight', -1, 'bn.png'),
    ]

    for name, color, file in pieces:
        img = pygame.image.load(f'images/{file}')
        IMAGES[(name, color)] = pygame.transform.scale(img, (CELL_SIZE, CELL_SIZE))


def draw_board(screen):
    colors = [(238, 238, 210), (118, 150, 86)]

    for row in range(ROWS):
        for col in range(ROWS):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color,
                             (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_pieces(screen):
    for cell, piece in Board.cells_map.items():
        if piece:
            col = ord(cell[0]) - ord('a')
            row = 8 - int(cell[1])

            screen.blit(
                IMAGES[(piece.name, piece.color)],
                (col * CELL_SIZE, row * CELL_SIZE)
            )


def mouse_to_cell(pos):
    x, y = pos
    col = x // CELL_SIZE
    row = y // CELL_SIZE

    letter = chr(ord('a') + col)
    number = str(8 - row)

    return letter + number


def set_pieces():
    pawn_aw=Pawn('a2',1)
    pawn_bw=Pawn('b2',1)
    pawn_cw=Pawn('c2',1)
    pawn_dw=Pawn('d2',1)
    pawn_ew=Pawn('e2',1)
    pawn_fw=Pawn('f2',1)
    pawn_gw=Pawn('g2',1)
    pawn_hw=Pawn('h2',1)

    pawn_ab = Pawn('a7', -1)
    pawn_bb = Pawn('b7', -1)
    pawn_cb = Pawn('c7', -1)
    pawn_db = Pawn('d7', -1)
    pawn_eb = Pawn('e7', -1)
    pawn_fb = Pawn('f7', -1)
    pawn_gb = Pawn('g7', -1)
    pawn_hb = Pawn('h7', -1)

    rook_wa=Rook('a1',1)
    rook_wh=Rook('h1',1)
    rook_ba=Rook('a8',-1)
    rook_bh=Rook('h8',-1)

    knight_wb=Knight('b1',1)
    knight_wg=Knight('g1',1)
    knight_bb=Knight('b8',-1)
    knight_bg=Knight('g8',-1)

    bishop_wc=Bishop('c1',1)
    bishop_wf=Bishop('f1',1)
    bishop_bc=Bishop('c8',-1)
    bishop_bf=Bishop('f8',-1)

    king_we=King('e1',1)
    king_be=King('e8',-1)

    queen_wd=Queen('d1',1)
    queen_bd=Queen('d8',-1)


