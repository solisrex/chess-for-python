#https://stackoverflow.com/questions/25149892/how-to-get-the-width-of-text-using-pygame
#https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangle-in-pygame
#https://stackoverflow.com/questions/390250/elegant-ways-to-support-equivalence-equality-in-python-classes#25176504

import pygame, sys, math, ctypes
from pygame.locals import *
from Board import *

files = ["a","b","c","d","e","f","g","h"]
filesDict = {"a": 1, "b": 2,"c": 3,"d": 4,"e": 5,"f": 6,"g": 7,"h": 8}

def get_file(piece):
    return filesDict[piece.square.file]

pygame.init()
length = 500
tileSizeX = 9
tileSizeY = 9
DISPLAYSURF = pygame.display.set_mode((length,length))
pygame.display.set_caption("Rudimentary Chess")
WHITE = (255,255,255)
LITEGREY = (200, 200, 200)
GREY = (130, 130, 130)
BLACK = (  0, 0,   0)

white_pawns = [Pawn(Square(files[i],2),True) for i in range(8)]
white_knights =[Knight(Square("b",1),True),Knight(Square("g",1),True)]
white_bishops =[Bishop(Square("c",1),True),Bishop(Square("f",1),True)]
white_rooks =[Rook(Square("a",1),True),Rook(Square("h",1),True)]
white_queens =[Queen(Square("d",1),True)]
white_king = [King(Square("e",1),True)]

black_pawns = [Pawn(Square(files[i],7),False) for i in range(8)]
black_knights =[Knight(Square("b",8),False),Knight(Square("g",8),False)]
black_bishops =[Bishop(Square("c",8),False),Bishop(Square("f",8),False)]
black_rooks =[Rook(Square("a",8),False),Rook(Square("h",8),False)]
black_queens =[Queen(Square("d",8),False)]
black_king = [King(Square("e",8),False)]

pieces = white_pawns+white_knights+white_bishops+white_rooks+white_queens+white_king+black_pawns+black_knights+black_bishops+black_rooks+black_queens+black_king

board = Board(pieces);

selected_piece = None;
white_turn = True;
promotion = False;

moves = []



def draw_files():
    for file in range(1,tileSizeX):
        fontObj = pygame.font.Font('freesansbold.ttf', 32)
        text = fontObj.render(files[file-1], False, WHITE)
        w,h = text.get_width(), text.get_height()
        DISPLAYSURF.blit(text,(length/tileSizeX*(file+1/2)-w/2, length/tileSizeX/2-h/2))

def draw_ranks():
    for rank in range(1,tileSizeY):
        fontObj = pygame.font.Font('freesansbold.ttf', 32)
        text = fontObj.render(str(tileSizeY-rank), False, WHITE)
        w,h = text.get_width(), text.get_height()
        DISPLAYSURF.blit(text,(length/tileSizeX/2-w/2,length/tileSizeY/2+length/tileSizeY*rank-h/2))

def draw_board():
    i=0
    for square in [[x,y] for x in range(1,9) for y in range(1,9)]:
        x, y = length/9*square[0],length/9*square[1]
        if i%2==0 and square[0]%2==0:
            pygame.draw.rect(DISPLAYSURF, LITEGREY, (x,y,length/9,length/9))
            i+=1;
        elif i%2!=0 and square[0]%2==0:
            pygame.draw.rect(DISPLAYSURF, GREY, (x,y,length/9,length/9))
            i+=1;
        elif i%2==0 and square[0]%2!=0:
            pygame.draw.rect(DISPLAYSURF, GREY, ((x,y,length/9,length/9)))
            i+=1;
        elif i%2!=0 and square[0]%2!=0:
            pygame.draw.rect(DISPLAYSURF, LITEGREY, (x,y,length/9,length/9))
            i+=1;

def draw_pieces():
    for piece in pieces:
        if piece.type == "p" and piece.white == True:
            center = (int(length/tileSizeX*(get_file(piece)+0.5)),int(length/9*(9.5-piece.square.rank)))
            pygame.draw.circle(DISPLAYSURF, WHITE, center, int(length/27)) 
        elif piece.type == "p" and piece.white == False:
            center = (int(length/tileSizeX*(get_file(piece)+0.5)),int(length/9*(9.5-piece.square.rank)))
            pygame.draw.circle(DISPLAYSURF, BLACK, center, int(length/27)) 

        elif piece.type == "r" and piece.white == True:
            pygame.draw.rect(DISPLAYSURF, WHITE, (length/tileSizeX*(get_file(piece)+1/6),length/9*(9-piece.square.rank+1/6),2*length/27,2*length/27))
        elif piece.type == "r" and piece.white == False:
            pygame.draw.rect(DISPLAYSURF, BLACK, (length/tileSizeX*(get_file(piece)+1/6),length/9*(9-piece.square.rank+1/6),2*length/27,2*length/27))

        elif piece.type == "n" and piece.white == True:
            width = 1/8
            padding = 1/5
            pygame.draw.rect(DISPLAYSURF, WHITE, (length/tileSizeX*(get_file(piece)+padding),length/9*(9-piece.square.rank+padding),length/tileSizeX*width,length/tileSizeY*(1-2*padding)))
            pygame.draw.rect(DISPLAYSURF, WHITE, (length/tileSizeX*(get_file(piece)+padding),length/9*(9-piece.square.rank+padding),length/tileSizeX*(1-2*padding),length/tileSizeY*width))
            pygame.draw.rect(DISPLAYSURF, WHITE, (length/tileSizeX*(get_file(piece)+1-padding-width),length/9*(9-piece.square.rank+padding),length/tileSizeX*width,length/tileSizeY*(1-2*padding)))
        elif piece.type == "n" and piece.white == False:
            width = 1/8
            padding = 1/5
            pygame.draw.rect(DISPLAYSURF, BLACK, (length/tileSizeX*(get_file(piece)+padding),length/9*(9-piece.square.rank+padding),length/tileSizeX*width,length/tileSizeY*(1-2*padding)))
            pygame.draw.rect(DISPLAYSURF, BLACK, (length/tileSizeX*(get_file(piece)+padding),length/9*(9-piece.square.rank+1-padding-width),length/tileSizeX*(1-2*padding),length/tileSizeY*width))
            pygame.draw.rect(DISPLAYSURF, BLACK, (length/tileSizeX*(get_file(piece)+1-padding-width),length/9*(9-piece.square.rank+padding),length/tileSizeX*width,length/tileSizeY*(1-2*padding)))
        
        elif piece.type == "b" and piece.white == True:
            cx, cy = length/tileSizeX*(get_file(piece)+1/2),length/9*(9-piece.square.rank+1/2)
            pygame.draw.polygon(DISPLAYSURF, WHITE, [[length/max(tileSizeX,tileSizeY)*(get_file(piece)+1/6),length/max(tileSizeX,tileSizeY)*(9-piece.square.rank+5/6)],[length/max(tileSizeX,tileSizeY)*(get_file(piece)+5/6),length/max(tileSizeX,tileSizeY)*(9-piece.square.rank+5/6)],[length/max(tileSizeX,tileSizeY)*(get_file(piece)+1/2),length/max(tileSizeX,tileSizeY)*(9-piece.square.rank+1/6)]])
        elif piece.type == "b" and piece.white == False:
            cx, cy = length/tileSizeX*(get_file(piece)+1/2),length/9*(9-piece.square.rank+1/2)
            pygame.draw.polygon(DISPLAYSURF, BLACK, [[length/max(tileSizeX,tileSizeY)*(get_file(piece)+1/6),length/max(tileSizeX,tileSizeY)*(9-piece.square.rank+1/6)],[length/max(tileSizeX,tileSizeY)*(get_file(piece)+5/6),length/max(tileSizeX,tileSizeY)*(9-piece.square.rank+1/6)],[length/max(tileSizeX,tileSizeY)*(get_file(piece)+1/2),length/max(tileSizeX,tileSizeY)*(9-piece.square.rank+5/6)]])
        
        elif piece.type == "q" and piece.white == True:
            R= length/max(tileSizeX,tileSizeY)/3
            angle = math.pi/25
            cx, cy = length/tileSizeX*(get_file(piece)+1/2),length/9*(9-piece.square.rank+1/2)

            vertices = [[cx+R*math.sin(math.pi/3-angle),cy-R*math.cos(math.pi/3-angle)]]
            vertices +=[[cx+R*math.sin(math.pi/3+angle),cy-R*math.cos(math.pi/3+angle)]]
            vertices +=[[cx+R*math.sin(4*math.pi/3-angle),cy-R*math.cos(4*math.pi/3-angle)]]
            vertices +=[[cx+R*math.sin(4*math.pi/3+angle),cy-R*math.cos(4*math.pi/3+angle)]]

            pygame.draw.polygon(DISPLAYSURF, WHITE, vertices)
            vertices = [[cx+R*math.sin(2*math.pi/3-angle),cy-R*math.cos(2*math.pi/3-angle)]]
            vertices +=[[cx+R*math.sin(2*math.pi/3+angle),cy-R*math.cos(2*math.pi/3+angle)]]
            vertices +=[[cx+R*math.sin(5*math.pi/3-angle),cy-R*math.cos(5*math.pi/3-angle)]]
            vertices +=[[cx+R*math.sin(5*math.pi/3+angle),cy-R*math.cos(5*math.pi/3+angle)]]

            pygame.draw.polygon(DISPLAYSURF, WHITE, vertices)
            vertices = [[cx+R*math.sin(math.pi-angle),cy-R*math.cos(math.pi-angle)]]
            vertices +=[[cx+R*math.sin(math.pi+angle),cy-R*math.cos(math.pi+angle)]]
            vertices +=[[cx+R*math.sin(-angle),cy-R*math.cos(-angle)]]
            vertices +=[[cx+R*math.sin(angle),cy-R*math.cos(angle)]]
            pygame.draw.polygon(DISPLAYSURF, WHITE, vertices)
            

        elif piece.type == "q" and piece.white == False:
            R= length/max(tileSizeX,tileSizeY)/3
            angle = math.pi/25
            cx, cy = length/tileSizeX*(get_file(piece)+1/2),length/9*(9-piece.square.rank+1/2)

            vertices = [[cx+R*math.sin(math.pi/3-angle),cy-R*math.cos(math.pi/3-angle)]]
            vertices +=[[cx+R*math.sin(math.pi/3+angle),cy-R*math.cos(math.pi/3+angle)]]
            vertices +=[[cx+R*math.sin(4*math.pi/3-angle),cy-R*math.cos(4*math.pi/3-angle)]]
            vertices +=[[cx+R*math.sin(4*math.pi/3+angle),cy-R*math.cos(4*math.pi/3+angle)]]

            pygame.draw.polygon(DISPLAYSURF, BLACK, vertices)
            vertices = [[cx+R*math.sin(2*math.pi/3-angle),cy-R*math.cos(2*math.pi/3-angle)]]
            vertices +=[[cx+R*math.sin(2*math.pi/3+angle),cy-R*math.cos(2*math.pi/3+angle)]]
            vertices +=[[cx+R*math.sin(5*math.pi/3-angle),cy-R*math.cos(5*math.pi/3-angle)]]
            vertices +=[[cx+R*math.sin(5*math.pi/3+angle),cy-R*math.cos(5*math.pi/3+angle)]]

            pygame.draw.polygon(DISPLAYSURF, BLACK, vertices)
            vertices = [[cx+R*math.sin(math.pi-angle),cy-R*math.cos(math.pi-angle)]]
            vertices +=[[cx+R*math.sin(math.pi+angle),cy-R*math.cos(math.pi+angle)]]
            vertices +=[[cx+R*math.sin(-angle),cy-R*math.cos(-angle)]]
            vertices +=[[cx+R*math.sin(angle),cy-R*math.cos(angle)]]
            pygame.draw.polygon(DISPLAYSURF, BLACK, vertices)
            
        elif piece.type == "k" and piece.white == True:
            width = 1/8
            padding = 1/8
            pygame.draw.rect(DISPLAYSURF, WHITE, (length/tileSizeX*(get_file(piece)+1/2-width/2),length/tileSizeY*(9-piece.square.rank+padding),length/tileSizeX*width,length/tileSizeY*(1-2*padding)))
            pygame.draw.rect(DISPLAYSURF, WHITE, (length/tileSizeX*(get_file(piece)+padding),length/tileSizeY*(9-piece.square.rank+1/2-width/2),length/tileSizeX*(1-2*padding),length/tileSizeY*width))
        elif piece.type == "k" and piece.white == False:
            width = 1/8
            padding = 1/8
            pygame.draw.rect(DISPLAYSURF, BLACK, (length/tileSizeX*(get_file(piece)+1/2-width/2),length/tileSizeY*(9-piece.square.rank+padding),length/tileSizeX*width,length/tileSizeY*(1-2*padding)))
            pygame.draw.rect(DISPLAYSURF, BLACK, (length/tileSizeX*(get_file(piece)+padding),length/tileSizeY*(9-piece.square.rank+1/2-width/2),length/tileSizeX*(1-2*padding),length/tileSizeY*width))
        
def draw_legal_moves(piece):
    for moves in board.legal_moves(piece):
        s = pygame.Surface((length/tileSizeX,length/tileSizeY), pygame.SRCALPHA)    # per-pixel alpha
        s.fill((255,255,0,175))                                                   # notice the alpha value in the color
        DISPLAYSURF.blit(s, (length/tileSizeX*filesDict[moves.file],length/tileSizeY*(9-moves.rank)))
    s = pygame.Surface((length/tileSizeX,length/tileSizeY), pygame.SRCALPHA)    # per-pixel alpha
    s.fill((175,175,0,175))                                                   # notice the alpha value in the color
    DISPLAYSURF.blit(s, (length/tileSizeX*filesDict[piece.square.file],length/tileSizeY*(9-piece.square.rank)))
    if piece.type ==  "k":
        if board.castle_short(piece.white) ==  True:
            s = pygame.Surface((length/tileSizeX,length/tileSizeY), pygame.SRCALPHA)    # per-pixel alpha
            s.fill((255,255,0,175))                                                   # notice the alpha value in the color
            DISPLAYSURF.blit(s, (length/tileSizeX*(filesDict[piece.square.file]+2),length/tileSizeY*(9-piece.square.rank)))
        if board.castle_long(piece.white) ==  True:
            s = pygame.Surface((length/tileSizeX,length/tileSizeY), pygame.SRCALPHA)    # per-pixel alpha
            s.fill((255,255,0,175))                                                   # notice the alpha value in the color
            DISPLAYSURF.blit(s, (length/tileSizeX*(filesDict[piece.square.file]-2),length/tileSizeY*(9-piece.square.rank)))


def main():
    while True:
        global selected_piece, white_turn, moves, promotion
        mousex = 0 # used to store x coordinate of mouse event
        mousey = 0
        mouseClicked = False;
        draw_board();
        draw_ranks();
        draw_files();
        if selected_piece != None:
            draw_legal_moves(selected_piece);
        draw_pieces();
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                tileX = math.floor(tileSizeX*mousex/length)
                tileY = 9-math.floor(tileSizeY*mousey/length)
                if 0 < tileX < 9 and 0 <tileY < 9:
                    mouseClicked = True
            elif event.type == KEYUP and promotion == True:
                promotion_square = selected_piece.square
                white = selected_piece.white
                if event.key == 113:
                    moves+=[selected_piece.square.file+str(selected_piece.square.rank)+files[tileX-1]+str(tileY)+"q"]
                    board.pieces.remove(board.get_piece_by_square(promotion_square))
                    board.pieces+=[Queen(promotion_square,white)]
                    selected_piece = None
                    white_turn = not white_turn
                    promotion = False
                elif event.key == 114:
                    moves+=[selected_piece.square.file+str(selected_piece.square.rank)+files[tileX-1]+str(tileY)+"r"]
                    board.pieces.remove(board.get_piece_by_square(promotion_square))
                    board.pieces+=[Rook(promotion_square,white)]
                    selected_piece = None
                    white_turn = not white_turn
                    promotion = False
                elif event.key == 98:
                    moves+=[selected_piece.square.file+str(selected_piece.square.rank)+files[tileX-1]+str(tileY)+"b"]
                    board.pieces.remove(board.get_piece_by_square(promotion_square))
                    board.pieces+=[Bishop(promotion_square,white)]
                    selected_piece = None
                    white_turn = not white_turn
                    promotion = False
                elif event.key == 110:
                    moves+=[selected_piece.square.file+str(selected_piece.square.rank)+files[tileX-1]+str(tileY)+"n"]
                    board.pieces.remove(board.get_piece_by_square(promotion_square))
                    board.pieces+=[Knight(promotion_square,white)]
                    selected_piece = None
                    white_turn = not white_turn
                    promotion = False

        #If a tile is clicked and a piece has not been selected,
        #if the tile is not empy and if the piece's color matches
        #the turn color, then select the piece. Else, select None.
        if mouseClicked == True and selected_piece == None and promotion == False:
            if board.get_piece_by_coord(files[tileX-1],tileY) != None:
                if board.get_piece_by_coord(files[tileX-1],tileY).white == white_turn:
                    selected_piece = board.get_piece_by_coord(files[tileX-1],tileY)
            else:
                selected_piece = None
        # If a tile is clicked and the selected piece is not empty,
        # if the selected square is in either the advancing squares
        # or the attacking squares, then possibly get an obstruction
        # and if it is non-empty, remove it from the board. Move the
        # piece to the selected square, set the selected piece to
        # none and change the turn to the other side.

        # Else if the selected square is non-empty and the piece is
        # on the same side as the current player, select that piece.
        # Else select none.
        if mouseClicked == True and selected_piece != None and promotion == False:
            if selected_piece.type == "k" and selected_piece.white ==  True:
                if Square(files[tileX-1],tileY) == Square("g",1) and board.castle_short(True) ==  True:
                    selected_piece.move_to(Square("g",1))
                    board.get_piece_by_square(Square("h",1)).move_to(Square("f",1))
                    moves += ["e1g1"]
                    selected_piece = None
                    white_turn = not white_turn
                    board.white_king_moved = True
                    
                elif Square(files[tileX-1],tileY) == Square("c",1) and board.castle_long(True) ==  True:
                    selected_piece.move_to(Square("c",1))
                    board.get_piece_by_square(Square("a",1)).move_to(Square("d",1))
                    moves += ["e1c1"]
                    selected_piece = None
                    white_turn = not white_turn
                    board.white_king_moved = True
                    
                elif Square(files[tileX-1],tileY) in board.legal_moves(selected_piece):
                    obstruction = board.get_piece_by_coord(files[tileX-1],tileY)
                    if obstruction != None:
                        board.pieces.remove(obstruction)
                    moves+=[selected_piece.square.file+str(selected_piece.square.rank)+files[tileX-1]+str(tileY)]
                    selected_piece.move_to(Square(files[tileX-1],tileY))
                    selected_piece = None
                    white_turn = not white_turn
                    board.white_king_moved = True
                    
                else:
                    if board.get_piece_by_coord(files[tileX-1],tileY) != None:
                        if board.get_piece_by_coord(files[tileX-1],tileY).white == white_turn:
                            selected_piece = board.get_piece_by_coord(files[tileX-1],tileY)
                    else:
                        selected_piece =  None
                        
            elif selected_piece.type == "k" and selected_piece.white ==  False and promotion == False:
                if Square(files[tileX-1],tileY) == Square("g",8) and board.castle_short(False) ==  True:
                    selected_piece.move_to(Square("g",8))
                    board.get_piece_by_square(Square("h",8)).move_to(Square("f",8))
                    moves += ["e8g8"]
                    selected_piece = None
                    white_turn = not white_turn
                    board.black_king_moved == True
                    
                elif Square(files[tileX-1],tileY) == Square("c",8) and board.castle_long(False) ==  True:
                    selected_piece.move_to(Square("c",8))
                    board.get_piece_by_square(Square("a",8)).move_to(Square("d",8))
                    moves += ["e8c8"]
                    selected_piece = None
                    white_turn = not white_turn
                    board.black_king_moved == True
                    
                elif Square(files[tileX-1],tileY) in board.legal_moves(selected_piece):
                    obstruction = board.get_piece_by_coord(files[tileX-1],tileY)
                    if obstruction != None:
                        board.pieces.remove(obstruction)
                    moves+=[selected_piece.square.file+str(selected_piece.square.rank)+files[tileX-1]+str(tileY)]
                    selected_piece.move_to(Square(files[tileX-1],tileY))
                    selected_piece = None
                    white_turn = not white_turn
                    board.black_king_moved == True
                    
                else:
                    if board.get_piece_by_coord(files[tileX-1],tileY) != None:
                        if board.get_piece_by_coord(files[tileX-1],tileY).white == white_turn:
                            selected_piece = board.get_piece_by_coord(files[tileX-1],tileY)
                    else:
                        selected_piece =  None
            elif selected_piece.type == "p" and selected_piece.white == True and selected_piece.square.rank == 2 and tileY == 4 and Square(files[tileX-1],tileY) in board.legal_moves(selected_piece) and promotion == False:
                if tileX > 1: 
                    to_left = board.get_piece_by_coord(files[tileX-2],4)
                else:
                    to_left = None
                if tileX < 8:
                    to_right = board.get_piece_by_coord(files[tileX],4)
                else:
                    to_right = None
                if to_left !=  None and to_left.type == "p" and to_left.white == False:
                    to_left.enpassantl = True
                if to_right !=  None and to_right.type == "p" and to_right.white == False:    
                    to_right.enpassantr = True
                moves+=[selected_piece.square.file+str(selected_piece.square.rank)+files[tileX-1]+str(tileY)]
                selected_piece.move_to(Square(files[tileX-1],tileY))
                selected_piece = None
                white_turn = not white_turn
            elif selected_piece.type == "p" and selected_piece.white == False and selected_piece.square.rank == 7 and tileY == 5 and Square(files[tileX-1],tileY) in board.legal_moves(selected_piece) and promotion == False:
                if tileX < 8: 
                    to_left = board.get_piece_by_coord(files[tileX],4)
                else:
                    to_left = None
                if tileX > 1:
                    to_right = board.get_piece_by_coord(files[tileX-2],4)
                else:
                    to_right = None
                if to_left !=  None and to_left.type == "p" and to_left.white == True:
                    to_left.enpassantl = True
                if to_right !=  None and to_right.type == "p" and to_right.white == True:    
                    to_right.enpassantr = True
                moves+=[selected_piece.square.file+str(selected_piece.square.rank)+files[tileX-1]+str(tileY)]
                selected_piece.move_to(Square(files[tileX-1],tileY))
                selected_piece = None
                white_turn = not white_turn
            elif selected_piece.type == "p" and tileY == 8 and Square(files[tileX-1],tileY) in board.legal_moves(selected_piece) and promotion == False:
                obstruction = board.get_piece_by_coord(files[tileX-1],tileY)
                if obstruction != None:
                    board.pieces.remove(obstruction)
                moves+=[selected_piece.square.file+str(selected_piece.square.rank)+files[tileX-1]+str(tileY)]
                selected_piece.move_to(Square(files[tileX-1],tileY))
                MessageBox = ctypes.windll.user32.MessageBoxW
                MessageBox(None, 'Press q for queen,\nr for rook,\nb for bishop,\nor n for knight.', 'Promotion', 0)
                promotion = True
            elif selected_piece.type == "p" and tileY == 1 and Square(files[tileX-1],tileY) in board.legal_moves(selected_piece) and promotion == False:
                print("testing")
                obstruction = board.get_piece_by_coord(files[tileX-1],tileY)
                if obstruction != None:
                    board.pieces.remove(obstruction)
                moves+=[selected_piece.square.file+str(selected_piece.square.rank)+files[tileX-1]+str(tileY)]
                selected_piece.move_to(Square(files[tileX-1],tileY))
                MessageBox = ctypes.windll.user32.MessageBoxW
                MessageBox(None, 'Press q for queen,\nr for rook,\nb for bishop,\nor n for knight.', 'Promotion', 0)
                promotion = True;

            elif promotion == False:
                if Square(files[tileX-1],tileY) in board.legal_moves(selected_piece):
                    obstruction = board.get_piece_by_coord(files[tileX-1],tileY)
                    if obstruction != None:
                        board.pieces.remove(obstruction)
                    elif selected_piece.type == "p" and selected_piece.white == True and (selected_piece.enpassantl or selected_piece.enpassantl) == True:
                        obstruction = board.get_piece_by_coord(files[tileX-1],tileY-1)
                        board.pieces.remove(obstruction)
                    elif selected_piece.type == "p" and selected_piece.white == False and (selected_piece.enpassantl or selected_piece.enpassantl) == True:
                        obstruction = board.get_piece_by_coord(files[tileX-1],tileY+1)
                        board.pieces.remove(obstruction)
                    moves+=[selected_piece.square.file+str(selected_piece.square.rank)+files[tileX-1]+str(tileY)]
                    selected_piece.move_to(Square(files[tileX-1],tileY))
                    selected_piece = None
                    white_turn = not white_turn
                else:
                    if board.get_piece_by_coord(files[tileX-1],tileY) != None:
                        if board.get_piece_by_coord(files[tileX-1],tileY).white == white_turn:
                            selected_piece = board.get_piece_by_coord(files[tileX-1],tileY)
                    else:
                        selected_piece =  None
        pygame.display.update()

main()
