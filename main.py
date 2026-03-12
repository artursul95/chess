from functools import wraps

def is_legal_common(func):
    @wraps(func)
    def wrapper(obj,from_cell,to_cell):
        if not isinstance(obj.cells_map[from_cell],obj.__class__):
            return False

        if to_cell not in obj.cells_map or obj.pos == to_cell:
            return False

        return func(obj,from_cell,to_cell)
    return wrapper


class IllegalMoveError(Exception):
    def __init__(self,from_cell,to_cell,piece):
        self.from_cell=from_cell
        self.to_cell=to_cell
        self.piece=piece

    def __str__(self):
        return f"You are trying to make illegal move: {self.piece} {self.from_cell}-{self.to_cell}"


class Board:
    pass


class Piece:
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

    cells_map=generate_cells_map()
    letters_to_num={'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8}
    numbers={'1', '2', '3', '4', '5', '6', '7', '8'}
    def __init__(self,pos,name,color):
        self.pos=pos
        self.cells_map[pos]=self
        self.name=name
        self.color=color

    def replace_piece(self,from_cell,to_cell):
        self.cells_map[from_cell] = None
        self.cells_map[to_cell] = self
        self.pos = to_cell

    def __str__(self):
        return f"{self.name} {self.pos}"

    def __repr__(self):
        return "Object: " + self.__str__()


class Pawn(Piece):
    start_positions = {'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2','a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'}
    def __init__(self,pos,color):
        super().__init__(pos,name="Pawn",color=color)

    @is_legal_common
    def is_legal_move(self,from_cell,to_cell):

        if from_cell[0] != to_cell[0] or self.cells_map[to_cell]:
            return False

        if self.color==1:
            if from_cell not in self.start_positions:
                return int(to_cell[-1])-int(from_cell[-1])==1
            return 0<int(to_cell[-1])-int(from_cell[-1])<=2
        else:
            if from_cell not in self.start_positions:
                return int(from_cell[-1])-int(to_cell[-1])==1
            return 0<int(from_cell[-1])-int(to_cell[-1])<=2


    def move(self,from_cell,to_cell):
        if not self.is_legal_move(from_cell,to_cell):
            raise IllegalMoveError(from_cell,to_cell,self.name)

        self.replace_piece(from_cell, to_cell)

    @is_legal_common
    def is_legal_capture(self,from_cell,to_cell):

        if not self.cells_map[to_cell]:
            return False

        if -self.cells_map[from_cell].color!=self.cells_map[to_cell].color:
            return False

        num_of_letter_from=self.letters_to_num[from_cell[0]]
        num_of_letter_to=self.letters_to_num[to_cell[0]]
        if abs(num_of_letter_from-num_of_letter_to)!=1:
            return False

        if self.color==1 and int(to_cell[-1])-int(from_cell[-1])!=1:
            return False

        if self.color==-1 and int(from_cell[-1])-int(to_cell[-1])!=1:
            return False

        return True

    def capture(self,from_cell,to_cell):
        if not self.is_legal_capture(from_cell,to_cell):
            raise IllegalMoveError(from_cell,to_cell,self.name)

        self.replace_piece(from_cell,to_cell)


    def is_legal_en_passant(self,from_cell,to_cell):
        pass


    def en_passant(self,from_cell,to_cell):
        if not self.is_legal_en_passant(from_cell,to_cell):
            raise IllegalMoveError



pawn_w=Pawn('c7',-1)
pawn_b=Pawn('b6',-1)

print(pawn_w.cells_map)
pawn_w.capture('c7','b6')
print(pawn_w.cells_map)
