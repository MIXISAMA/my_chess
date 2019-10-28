import abc #利用abc模块实现抽象类
from point import Point
from player import Player
class ChessPiece(metaclass=abc.ABCMeta):
    
    total_step_counter = 0

    def __init__(self, **kwargs):
        self.promotion_next_chess_piece = None
        if kwargs.__contains__('position') and kwargs.__contains__('player'):
            self._position = kwargs['position']
            self._is_promotion = False
            self.player = kwargs['player']
            self.step_counter = ChessPiece.total_step_counter
        elif kwargs.__contains__('chess_piece'):
            chess_piece = kwargs['chess_piece']
            self._position = chess_piece.position
            self._is_promotion = chess_piece.is_promotion
            print(chess_piece.is_promotion)
            self.player = chess_piece.player
            self.step_counter = chess_piece.step_counter
    
    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position:Point):
        ChessPiece.total_step_counter += 1
        self.step_counter = ChessPiece.total_step_counter
        self._position = position
        self._is_promotion = False
        print(ChessPiece.total_step_counter)

    @property
    def is_promotion(self):
        return self._is_promotion and self.step_counter == ChessPiece.total_step_counter

    @is_promotion.setter
    def is_promotion(self, is_promotion:bool):
        self._is_promotion = is_promotion

    @abc.abstractmethod
    def range_moving_vectors(self):
        pass
    
    def get_reachable_points(self, chess_pieces:dict):
        
        ret = list()

        for vectors in self.range_moving_vectors():
            for vector in vectors:
                x = self.position.x + vector.x
                y = self.position.y + vector.y
                if 0 <= x < 8 and 0 <= y < 8:
                    next_position = Point(x,y)
                    chess_piece = self.get_chess_piece_by_position(next_position, chess_pieces)
                    if chess_piece is None:
                        ret.append( (next_position, None ) )
                    elif chess_piece not in chess_pieces[self.player]:
                        ret.append( (next_position, chess_piece ) )
                        break
                    else:
                        break
        
        return ret
        
    def get_chess_piece_by_position(self, position:Point, chess_pieces:dict):
        for player in Player:
            for chess_piece in chess_pieces[player]:
                if chess_piece.position == position:
                    return chess_piece
        return None

class King(ChessPiece): #王
        
    def range_moving_vectors(self):
        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 and j == 0:
                    continue
                yield [ Point(j,i) ]

class Queen(ChessPiece): #后

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.promotion_next_chess_piece = Knight

    def range_moving_vectors(self):
        for i in range(-1,2):
            for j in range(-1,2):
                if i == 0 and j == 0:
                    continue
                yield list( Point(j*k,i*k) for k in range(1,9) )

class Rook(ChessPiece): #车

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.promotion_next_chess_piece = Queen

    def range_moving_vectors(self):
        base_vectors = [ Point(1,0), Point(0,1), Point(-1,0), Point(0,-1) ]
        for base_vector in base_vectors:
            yield list( Point(base_vector.x*k, base_vector.y*k) for k in range(1,9) )

class Pawn(ChessPiece): #兵

    def __init__(self, position:Point, player:Player):
        self.has_moved = False
        super().__init__(position = position, player = player)
        self.direction_of_attack = 1 if (self.player is Player.white) else -1
        self.attack_vectors = [ Point(1,self.direction_of_attack), Point(-1,self.direction_of_attack) ]
        self.promotion_next_chess_piece = Queen
        
    @property
    def is_promotion(self):
        if self.direction_of_attack == 1 and self.position.y == 7 \
            or self.direction_of_attack == -1 and self.position.y == 0:
            return True
        return False

    def is_passed(self):
        return ChessPiece.total_step_counter == self.step_counter and self.last_is_walked_two_square

    @property
    def position(self):
        return super().position

    @position.setter
    def position(self, position:Point):
        self.last_is_walked_two_square = False
        if not self.has_moved:
            self.has_moved = True
            if position.y - self.position.y == 2*self.direction_of_attack:
                self.last_is_walked_two_square = True
        super(Pawn, Pawn).position.__set__(self, position)
    
    def range_moving_vectors(self):
        ret = [ Point(0,self.direction_of_attack) ]
        if self.has_moved is False:
            ret.append( Point(0, ret[0].y*2) )
        yield ret
    
    def get_reachable_points(self, chess_pieces:dict):
        ret = list()
        for vectors in self.range_moving_vectors():
            for vector in vectors:
                x = self.position.x + vector.x
                y = self.position.y + vector.y
                if 0 <= x < 8 and 0 <= y < 8:
                    next_position = Point(x,y)
                    chess_piece = self.get_chess_piece_by_position(next_position, chess_pieces)
                    if chess_piece is None:
                        ret.append( (next_position, chess_piece) )
                    else:
                        break

        for vector in self.attack_vectors:
            x = self.position.x + vector.x
            y = self.position.y + vector.y
            if 0 <= x < 8 and 0 <= y < 8:
                next_position = Point(x,y)
                chess_piece = self.get_chess_piece_by_position(next_position, chess_pieces)
                if chess_piece is not None and chess_piece not in chess_pieces[self.player]:
                    ret.append( (next_position, chess_piece) )
                    continue

                passant_position = Point(x, self.position.y)
                passant_chess_piece = self.get_chess_piece_by_position(passant_position, chess_pieces)
                if isinstance(passant_chess_piece, Pawn) \
                    and passant_chess_piece not in chess_pieces[self.player] \
                    and passant_chess_piece.is_passed():

                    ret.append( (next_position, passant_chess_piece) )
                
        return ret


class Bishop(ChessPiece): #象

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.promotion_next_chess_piece = Rook

    def range_moving_vectors(self):
        base_vectors = [ Point(1,1), Point(-1,-1), Point(1,-1), Point(-1,1) ]
        for base_vector in base_vectors:
            yield list( Point(base_vector.x*k, base_vector.y*k) for k in range(1,9) )

class Knight(ChessPiece): #马

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.promotion_next_chess_piece = Bishop

    def range_moving_vectors(self):
        for i in range(-1,3,2):
            for j in range(-1,3,2):
                yield [ Point(1*i,2*j) ]
                yield [ Point(2*i,1*j) ]
        