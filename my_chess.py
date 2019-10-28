import pygame
from pygame.locals import *
from sys import exit



pygame.init()
screen = pygame.display.set_mode((80*8, 80*8), 0, 32)
pygame.display.set_caption("chess")

from chess_piece import *
from player import Player
from point import Point
loaded_img = {
    Player.white : {
        King: pygame.image.load('source/chess_pieces/White_King.png'),
        Queen: pygame.image.load('source/chess_pieces/White_Queen.png'),
        Bishop: pygame.image.load('source/chess_pieces/White_Bishop.png'),
        Knight: pygame.image.load('source/chess_pieces/White_Knight.png'),
        Rook: pygame.image.load('source/chess_pieces/White_Rook.png'),
        Pawn: pygame.image.load('source/chess_pieces/White_Pawn.png')
    },
    Player.black: {
        King: pygame.image.load('source/chess_pieces/Black_King.png'),
        Queen: pygame.image.load('source/chess_pieces/Black_Queen.png'),
        Bishop: pygame.image.load('source/chess_pieces/Black_Bishop.png'),
        Knight: pygame.image.load('source/chess_pieces/Black_Knight.png'),
        Rook: pygame.image.load('source/chess_pieces/Black_Rook.png'),
        Pawn: pygame.image.load('source/chess_pieces/Black_Pawn.png')
    }
}

white_select_pic = pygame.image.load('source/select/White_Select.png')
black_select_pic = pygame.image.load('source/select/Black_Select.png')

def get_loaded_img(chess_piece:ChessPiece):
    return loaded_img[chess_piece.player][type(chess_piece)]

def get_screen_coor(position:Point):
    return (position.x*80+8, position.y*80+8)

from controller import Controller
controller = Controller()
controller.restart()

def draw(controller:Controller):
    fill_colors = [(0,0,0),(255,255,255)]
    for i in range(8):
        for j in range(8):

            rc = fill_colors[(i+j)%2]# 矩形的颜色
            rp = (i*80,j*80)
            rs = (80,80)
            pygame.draw.rect(screen, rc, Rect(rp, rs))

    for player in Player:
        for chess_piece in controller.chess_pieces[player]:
            screen.blit(get_loaded_img(chess_piece), get_screen_coor(chess_piece.position))
    
    if controller.focused_chess_piece is not None:
        fcp = controller.focused_chess_piece
        for position, chess_piece in fcp.get_reachable_points(controller.chess_pieces):
            if (position.x + position.y) % 2:
                screen.blit(black_select_pic, get_screen_coor(position))
            else:
                screen.blit(white_select_pic, get_screen_coor(position))

    if controller.some_player_win:
        if controller.some_player_win is Player.white:
            surface = screen.convert_alpha()
            surface.fill((255,255,255,0))
            pygame.draw.rect(surface, (0, 0, 0, 128), pygame.Rect(0, 0, 8*80, 8*80))
            screen.blit(surface,(0,0))

            screen.blit(pygame.font.Font(None,130).render("WHITE WIN",True,(255,255,255)),(60,120))
            screen.blit(pygame.font.Font(None,50).render("Click To Restart",True,(255,255,255)),(63,220))
            screen.blit(pygame.font.Font(None,25).render("Tip:  Whenever you can press R to restart",True,(255,255,255)),(65,270))

            screen.blit(pygame.font.Font(None,25).render("Thank you for your running my program",True,(255,255,255)),(240,540))
            screen.blit(pygame.font.Font(None,25).render("Author: NWU_zhangjunbo",True,(255,255,255)),(350,560))
        else:
            surface = screen.convert_alpha()
            surface.fill((255,255,255,0))
            pygame.draw.rect(surface, (255, 255, 255, 128), pygame.Rect(0, 0, 8*80, 8*80))
            screen.blit(surface,(0,0))

            screen.blit(pygame.font.Font(None,130).render("BLACK WIN",True,(0,0,0)),(60,120))
            screen.blit(pygame.font.Font(None,50).render("Click To Restart",True,(0,0,0)),(63,220))
            screen.blit(pygame.font.Font(None,25).render("Tip:  Whenever you can press R to restart",True,(0,0,0)),(65,270))

            screen.blit(pygame.font.Font(None,25).render("Thank you for your running my program",True,(0,0,0)),(240,540))
            screen.blit(pygame.font.Font(None,25).render("Author: NWU_zhangjunbo",True,(0,0,0)),(350,560))

        

        
    
    pygame.display.update()

draw(controller)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

        if event.type == KEYDOWN and event.key==K_r:
            controller.restart()
            draw(controller)
    
        if event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            controller.click_square(Point(x//80,y//80))
            draw(controller)
                    
    





