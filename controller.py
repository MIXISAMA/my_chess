from chess_piece import ChessPiece, King, Queen, Bishop, Knight, Rook, Pawn
from point import Point
from player import Player

class Controller():

    def __init__(self):
        self.chess_pieces = {
            Player.white: list(),
            Player.black: list()
        }
        self.focused_chess_piece = None
        self.operator = Player.black
        self.init_positions = {
            Player.white: {
                Rook: [ Point(0,0), Point(7,0) ],
                Knight: [ Point(1,0), Point(6,0) ],
                Bishop: [ Point(2,0), Point(5,0) ],
                Queen: [ Point(3,0) ],
                King: [ Point(4,0) ],
                Pawn: list( Point(x,1) for x in range(8) )
            },
            Player.black: {
                Rook: [ Point(0,7), Point(7,7) ],
                Knight: [ Point(1,7), Point(6,7) ],
                Bishop: [ Point(2,7), Point(5,7) ],
                Queen: [ Point(3,7) ],
                King: [ Point(4,7) ],
                Pawn: list( Point(x,6) for x in range(8) )
            }
        }
        self.some_player_win = None
    
    def click_square(self, position:Point):
        print(position, self.get_chess_piece_by_position(position))
        
        if self.some_player_win:
            self.restart()

        if self.focused_chess_piece is None:
            chess_piece = self.get_chess_piece_by_position(position)
            if chess_piece is not None and chess_piece.player == self.operator: # selected a chess piece
                self.focused_chess_piece = chess_piece
            if chess_piece is not None and chess_piece.is_promotion:
                self.promotion(chess_piece)
        else:
            rp = self.focused_chess_piece.get_reachable_points(self.chess_pieces)
            for reachable_point, captured_chess_piece in rp:
                if position == reachable_point:     # move or capture
                    if captured_chess_piece is not None: # capture
                        self.capture(captured_chess_piece)
                        if type(captured_chess_piece) is King:
                            self.some_player_win = self.operator
                    self.move(self.focused_chess_piece, position) # move
                    self.operator = Player.white if (self.operator is Player.black) else Player.black
                    if self.focused_chess_piece.is_promotion:   #promotion
                        self.promotion(self.focused_chess_piece)
            self.focused_chess_piece = None

    def move(self, chess_piece:ChessPiece, position:Point): # 移子
        chess_piece.position = position
    
    def capture(self, chess_piece:ChessPiece): # 吃子
        self.drop_a_chess_piece(chess_piece)

    def promotion(self, chess_piece:ChessPiece): # 升变
        self.drop_a_chess_piece(chess_piece)
        self.join_a_chess_piece(chess_piece.promotion_next_chess_piece(chess_piece = chess_piece))

    def restart(self):
        self.drop_all_chess_piece()
        self.focused_chess_piece = None
        self.operator = Player.black
        self.some_player_win = None
        ChessPiece.total_step_counter = 0
        for player in Player:
            for chess_piece, positions in self.init_positions[player].items():
                for position in positions:
                    self.join_a_chess_piece( chess_piece(position = position, player = player) )
        
    def join_a_chess_piece(self, chess_piece:ChessPiece):
        self.chess_pieces[chess_piece.player].append(chess_piece)

    def drop_a_chess_piece(self, chess_piece:ChessPiece):
        self.chess_pieces[chess_piece.player].remove(chess_piece)
    
    def drop_all_chess_piece(self):
        for player in Player:
            self.chess_pieces[player].clear()
    
    def get_chess_piece_by_position(self, position:Point):
        for player in Player:
            for chess_piece in self.chess_pieces[player]:
                if chess_piece.position == position:
                    return chess_piece
        return None