from functools import wraps


def is_legal_common(func):
    @wraps(func)
    def wrapper(obj, from_cell, to_cell):
        if not isinstance(obj.cells_map[from_cell], obj.__class__):
            return False

        if to_cell not in obj.cells_map or obj.pos == to_cell:
            return False

        return func(obj, from_cell, to_cell)

    return wrapper


class IllegalMoveError(Exception):
    def __init__(self, from_cell, to_cell, piece):
        self.from_cell = from_cell
        self.to_cell = to_cell
        self.piece = piece

    def __str__(self):
        return f"You are trying to make illegal move: {self.piece} {self.from_cell}-{self.to_cell}"


class IllegalPromotion(Exception):
    def __init__(self, piece):
        self.piece = piece

    def __str__(self):
        return f'You are trying to promote wrong piece: {self.piece}'


class Board:
    @staticmethod
    def generate_cells_map():
        cells_map = {}
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8']

        for letter in letters:
            for num in numbers:
                cell = letter + num
                cells_map[cell] = None

        return cells_map

    @staticmethod
    def generate_cells_matrix():
        cells_matrix = [[False] * 8 for _ in range(8)]

        for i in range(8):
            for j in range(8):
                cells_matrix[i][j] = True if i in [0, 1, 6, 7] else False

        return cells_matrix

    cells_matrix = generate_cells_matrix()
    cells_map = generate_cells_map()
    letters_to_num = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}
    numbers = {'1', '2', '3', '4', '5', '6', '7', '8'}


class Piece(Board):
    def __init__(self, pos, name, color):
        self.pos = pos
        self.cells_map[pos] = self
        self.name = name
        self.color = color
        num=int(pos[1]) - 1
        letter=self.letters_to_num[pos[0]]-1

        #возможно необязательная строка
        self.cells_matrix[num][letter]=True

    def replace_piece(self, from_cell, to_cell):
        self.cells_map[from_cell] = None
        self.cells_map[to_cell] = self
        self.pos = to_cell

    def replace_piece_matr(self,from_cell,to_cell):
        num_from = int(from_cell[1]) - 1
        letter_from = self.letters_to_num[from_cell[0]] - 1
        num_to = int(to_cell[1]) - 1
        letter_to = self.letters_to_num[to_cell[0]] - 1
        self.cells_matrix[num_from][letter_from]=False
        self.cells_matrix[num_to][letter_to]=True


    def __str__(self):
        return f"{self.name} {self.pos}"

    def __repr__(self):
        return "Object: " + self.__str__()


class Rook(Piece):
    def __init__(self, pos, color):
        super().__init__(pos, name='Rook', color=color)
        self.did_move = False

    @is_legal_common
    def is_legal_move(self, from_cell, to_cell):
        if from_cell[0] != to_cell[0] and from_cell[1] != to_cell[1]:
            return False

        #проверка на движение по горизонтали: сделал
        if from_cell[1] == to_cell[1]:
            from_letter_ind = self.letters_to_num[from_cell[0]]-1
            to_letter_ind=self.letters_to_num[to_cell[0]]-1
            ind_of_file=int(from_cell[1])-1
            if to_letter_ind>from_letter_ind:
                for i in range(from_letter_ind+1,to_letter_ind+1):
                    if self.cells_matrix[ind_of_file][i] is True:
                        return False
            else:
                for i in range(to_letter_ind,from_letter_ind):
                    if self.cells_matrix[ind_of_file][i] is True:
                        return False


        return True

    def move(self, from_cell, to_cell):
        if not self.is_legal_move(from_cell, to_cell):
            raise IllegalMoveError(from_cell, to_cell, self.name)

        self.replace_piece(from_cell, to_cell)
        self.replace_piece_matr(from_cell,to_cell)
        self.did_move = True


class Pawn(Piece):
    start_positions = {'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2', 'a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'}

    def __init__(self, pos, color):
        super().__init__(pos, name="Pawn", color=color)
        self.last_move = None

    def promote(self, to_cell, piece='Queen'):
        promotion_pieces = {'Queen', 'Bishop', 'Knight', 'Rook'}
        if piece not in promotion_pieces:
            raise IllegalPromotion(piece)
        self.cells_map[to_cell] = 'создать объект фигуры тут'

    @is_legal_common
    def is_legal_move(self, from_cell, to_cell):

        if from_cell[0] != to_cell[0] or self.cells_map[to_cell]:
            return False

        if self.color == 1:
            if from_cell not in self.start_positions:
                return int(to_cell[-1]) - int(from_cell[-1]) == 1
            return 0 < int(to_cell[-1]) - int(from_cell[-1]) <= 2
        else:
            if from_cell not in self.start_positions:
                return int(from_cell[-1]) - int(to_cell[-1]) == 1
            return 0 < int(from_cell[-1]) - int(to_cell[-1]) <= 2

    def move(self, from_cell, to_cell):
        if not self.is_legal_move(from_cell, to_cell):
            raise IllegalMoveError(from_cell, to_cell, self.name)

        self.replace_piece(from_cell, to_cell)
        self.last_move = (from_cell, to_cell)
        self.replace_piece_matr(from_cell,to_cell)


        if self.color == 1 and int(to_cell[1]) == 8:
            self.promote(to_cell, 'Нужна информация о фигуре, необходим ввод от пользователя (сейчас дефолт: квин)')

        elif self.color == -1 and int(to_cell[1]) == 1:
            self.promote(to_cell, 'Нужна информация о фигуре, необходим ввод от пользователя (сейчас дефолт: квин)')

    @is_legal_common
    def is_legal_capture(self, from_cell, to_cell):

        if not self.cells_map[to_cell]:
            return False

        if -self.cells_map[from_cell].color != self.cells_map[to_cell].color:
            return False

        num_of_letter_from = self.letters_to_num[from_cell[0]]
        num_of_letter_to = self.letters_to_num[to_cell[0]]
        if abs(num_of_letter_from - num_of_letter_to) != 1:
            return False

        if self.color == 1 and int(to_cell[-1]) - int(from_cell[-1]) != 1:
            return False

        if self.color == -1 and int(from_cell[-1]) - int(to_cell[-1]) != 1:
            return False

        return True

    def capture(self, from_cell, to_cell):
        if not self.is_legal_capture(from_cell, to_cell):
            raise IllegalMoveError(from_cell, to_cell, self.name)

        self.replace_piece(from_cell, to_cell)
        self.last_move = (from_cell, to_cell)
        self.replace_piece_matr(from_cell,to_cell)

        if self.color == 1 and int(to_cell[1]) == 8:
            self.promote(to_cell, 'Нужна информация о фигуре, необходим ввод от пользователя (сейчас дефолт: квин)')

        elif self.color == -1 and int(to_cell[1]) == 1:
            self.promote(to_cell, 'Нужна информация о фигуре, необходим ввод от пользователя (сейчас дефолт: квин)')

    @is_legal_common
    def is_legal_en_passant(self, from_cell, to_cell):

        if self.cells_map[to_cell]:
            return False

        captured_cell = to_cell[0] + from_cell[-1]

        if not isinstance(self.cells_map[captured_cell], Pawn):
            return False

        captured_piece = self.cells_map[captured_cell]

        if -self.cells_map[from_cell].color != self.cells_map[captured_cell].color:
            return False

        num_of_letter_from = self.letters_to_num[from_cell[0]]
        num_of_letter_to = self.letters_to_num[to_cell[0]]
        if abs(num_of_letter_from - num_of_letter_to) != 1:
            return False

        if not captured_piece.last_move:
            return False

        if abs(int(captured_piece.last_move[0][1]) - int(captured_piece.last_move[1][1])) != 2:
            return False

        if abs(int(from_cell[1]) - int(to_cell[1])) != 1:
            return False

        return True

    def en_passant(self, from_cell, to_cell):
        if not self.is_legal_en_passant(from_cell, to_cell):
            raise IllegalMoveError(from_cell, to_cell, self.name)

        self.replace_piece(from_cell, to_cell)
        captured_cell = to_cell[0] + from_cell[-1]
        self.cells_map[captured_cell] = None
        self.replace_piece_matr(from_cell,to_cell)


pawn_w = Pawn('f4', 1)
pawn_b = Pawn('b6', -1)


rook_w=Rook('e4',1)
print(pawn_w.cells_map)

rook_w.move('e4','f5')

print(pawn_w.cells_map)
