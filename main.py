import pygame
from interface import WIDTH, set_pieces, load_images, draw_pieces, draw_board, mouse_to_cell
from engine import Board, IllegalMoveError


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Chess")

    set_pieces()
    load_images()

    selected_cell = None
    running = True
    is_white_move = True

    while running:
        draw_board(screen)
        draw_pieces(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                cell = mouse_to_cell(pygame.mouse.get_pos())

                # --- выбор фигуры ---
                if selected_cell is None:
                    piece = Board.cells_map[cell]

                    if piece:
                        if (is_white_move and piece.color == 1) or (not is_white_move and piece.color == -1):
                            selected_cell = cell

                # --- попытка хода ---
                else:
                    piece = Board.cells_map[selected_cell]
                    target = Board.cells_map[cell]

                    # если клик по своей же фигуре — смена выбора
                    if target and target.color == piece.color:
                        selected_cell = cell
                        continue

                    try:
                        if target:
                            piece.capture(selected_cell, cell)

                        else:
                            # сначала проверяем en passant
                            if hasattr(piece, "is_legal_en_passant") and piece.is_legal_en_passant(selected_cell, cell):
                                piece.en_passant(selected_cell, cell)
                            else:
                                piece.move(selected_cell, cell)

                        is_white_move = not is_white_move

                    except IllegalMoveError:
                        pass

                    selected_cell = None

    pygame.quit()


if __name__ == "__main__":
    main()