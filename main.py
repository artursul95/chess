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
    letters={'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}
    numbers={'1', '2', '3', '4', '5', '6', '7', '8'}
    def __init__(self,pos,name):
        self.pos=pos
        self.cells_map[pos]=self
        self.name=name

    def __str__(self):
        return f"{self.name} - {self.pos}"

    def __repr__(self):
        return self.__str__()


class Pawn(Piece):
    start_positions = {'a2', 'b2', 'c2', 'd2', 'e2', 'f2', 'g2', 'h2','a7', 'b7', 'c7', 'd7', 'e7', 'f7', 'g7', 'h7'}
    def __init__(self,pos,color):
        super().__init__(pos,name="Pawn")
        self.color=color

    def is_legal_move(self,from_cell,to_cell):
        #нужна ли мне эта проверка?
        if not isinstance(self.cells_map[from_cell],self.__class__):
            return False

        if (from_cell[0] != to_cell[0] or
                to_cell not in self.cells_map or
                self.cells_map[to_cell] or
                self.pos==to_cell):
            return False

        if self.color=='w':
            if from_cell not in self.start_positions:
                return int(to_cell[-1])-int(from_cell[-1])==1
            return 0<int(to_cell[-1])-int(from_cell[-1])<=2
        else:
            if from_cell not in self.start_positions:
                return int(to_cell[-1])-int(from_cell[-1])==-1
            return 0<int(from_cell[-1])-int(to_cell[-1])<=2


    def move(self,from_cell,to_cell):
        if not self.is_legal_move(from_cell,to_cell):
            raise IllegalMoveError(from_cell,to_cell,self.name)

        self.cells_map[from_cell]=None
        self.cells_map[to_cell]=self
        self.pos=to_cell


pawn=Pawn('a7','b')
print(pawn.cells_map)
pawn.move('a7','a5')
print(pawn.cells_map)
