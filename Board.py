files = ['a','b','c','d','e','f','g','h']
filesDict = {'a':1,'b':2,'c':3,'d':4,'e':5,'f':6,'g':7,'h':8}

def advancing(board,piece,directions,max_depth):
    moves = []
    for direction in directions:
        for i in [1,-1]:
            tempSquare = piece.square
            k=0
            while direction(tempSquare,i) != None and k < max_depth:
                tempSquare = direction(tempSquare,i)
                k+=1
                pcollision = board.get_piece_by_square(tempSquare)
                if pcollision != None:
                    break
                else:
                    moves+= [tempSquare]
    return moves

def attacking(board,piece,directions,max_depth):
    moves = []
    for direction in directions:
        for i in [1,-1]:
            tempSquare = piece.square
            k=0
            while direction(tempSquare,i) != None and k < max_depth:
                tempSquare = direction(tempSquare,i)
                k+=1
                pcollision = board.get_piece_by_square(tempSquare)
                if pcollision != None:
                    if pcollision.white == (not piece.white):
                        moves+= [tempSquare]
                        break
                    else:
                        break
                else:
                    pass
    return moves
            
                    

class Board:
    def __init__(self,pieces):
        self.pieces = pieces
        self.white_king_moved = False
        self.white_ksrook_moved = False
        self.white_qsrook_moved = False
        self.white_king_moved = False
        self.white_ksrook_moved = False
        self.white_qsrook_moved = False
        self.black_king_moved = False
        self.black_ksrook_moved = False
        self.black_qsrook_moved = False
        self.black_king_moved = False
        self.black_ksrook_moved = False
        self.black_qsrook_moved = False
        self.white_check = False
        self.black_check = False

    def get_piece_by_coord(self,file,rank):
        for piece in self.pieces:
            if piece.square.file == file and piece.square.rank  == rank:
                return piece
        return None
    def get_piece_by_square(self,square):
        return self.get_piece_by_coord(files[filesDict[square.file]-1],square.rank)

    def get_pieces_by_squares(self,squares):
        return [self.get_piece_by_square(s) for s in squares]

    def get_pieces_by_type(self,piece_type):
        return list(filter(lambda piece: piece.type ==piece_type, self.pieces))

    def get_pieces_by_color(self, white):
        return list(filter(lambda piece: piece.white ==white, self.pieces))
    
    def confirm_check(self,for_white):
        choosen_king = list(filter(lambda king : king.white == (not for_white), self.get_pieces_by_type("k")))[0]
        for piece in self.get_pieces_by_color(for_white):
            if choosen_king.square in self.attacking_moves(piece):
                return True
        return False

    def confirm_mate(self,for_white):
        if self.confirm_check(for_white) == True:
            for piece in list(filter(lambda p : p.type != "k" ,self.get_pieces_by_color(not for_white))):
                if self.legal_moves(piece) != []:
                    return False
            return True
        else:
            return False
        
    def moving_into_check(self,for_white,square):
        for piece in list(filter(lambda p : p.type != "k" ,self.get_pieces_by_color(not for_white))):
            if square in self.attacking_moves(piece):
                return True
            if square in self.advancing_moves(piece):
                return True
        return False

    def castle_short(self, for_white):
        if for_white == True:
         if for_white == True:
            return (self.white_king_moved == False) and (self.white_ksrook_moved == False) and (self.get_pieces_by_squares([Square("f",1),Square("g",1)]) == [None, None]) and (list(filter(lambda p : Square("f",1) in self.advancing_moves(p) or Square("g",1) in self.advancing_moves(p) , self.get_pieces_by_color(False))) == [])
        else:
            return (self.black_king_moved == False) and (self.black_ksrook_moved == False) and (self.get_pieces_by_squares([Square("f",8),Square("g",8)]) == [None, None]) and (list(filter(lambda p : Square("f",8) in self.advancing_moves(p) or Square("g",8) in self.advancing_moves(p) , self.get_pieces_by_color(True))) == [])

    def castle_long(self, for_white):
        if for_white == True:
            return (self.white_king_moved == False) and (self.white_qsrook_moved == False) and (self.get_pieces_by_squares([Square("d",1),Square("c",1),Square("b",1)]) == [None, None, None]) and (list(filter(lambda p : Square("d",1) in self.advancing_moves(p) or Square("c",1) in self.advancing_moves(p) or Square("b",1) in self.advancing_moves(p), self.get_pieces_by_color(False)))==[])
        else:
            return (self.black_king_moved == False) and (self.black_qsrook_moved == False) and (self.get_pieces_by_squares([Square("d",8),Square("c",8),Square("b",8)]) == [None, None, None]) and (list(filter(lambda p : Square("d",8) in self.advancing_moves(p) or Square("c",8) in self.advancing_moves(p) or Square("b",8) in self.advancing_moves(p), self.get_pieces_by_color(True)))==[])

    def castle_moves(self, for_white):
        moves = []
        if for_white ==  True:
            if self.castle_short(for_white) == True:
                moves += [Square("g",1)]
            if self.castle_long(for_white) == True:
                moves += [Square("c",1)]
        else:
            if self.castle_short(for_white) == True:
                moves += [Square("g",8)]
            if self.castle_long(for_white) == True:
                moves += [Square("c",8)]
        return moves

    def legal_moves(self,piece):
        moves = []
        origin = piece.square
        for move in self.advancing_moves(piece)+self.attacking_moves(piece):
            if move != None:
                p = self.get_piece_by_square(move)
                if p != None:
                    self.pieces.remove(p)
                piece.move_to(move)
                if self.confirm_check(not piece.white) ==  True:
                    if p != None:
                        self.pieces += [p]
                    pass
                else:
                    if p != None:
                        self.pieces+= [p]
                    moves += [move]
                
        piece.move_to(origin)
        return moves
    
    def advancing_moves(self,piece):
        moves = []
        if piece.type == "p" and piece.white == True and piece.square.rank < 8:
            if piece.square.rank == 2:
                if self.get_piece_by_square(piece.square.ud(1)) == None:
                    moves+=[piece.square.ud(1)]
                    if self.get_piece_by_square(piece.square.ud(2)) == None:
                        moves+=[piece.square.ud(2)]
            else:
                if self.get_piece_by_square(piece.square.ud(1)) == None:
                    moves+=[piece.square.ud(1)]

        if piece.type == "p" and piece.white == False and piece.square.rank > 1:
            if piece.square.rank == 7:
                if self.get_piece_by_square(piece.square.ud(-1)) == None:
                    moves+=[piece.square.ud(-1)]
                    if self.get_piece_by_square(piece.square.ud(-2)) == None:
                        moves+=[piece.square.ud(-2)]
            else:
                if self.get_piece_by_square(piece.square.ud(-1)) == None:
                    moves+=[piece.square.ud(-1)]

        elif piece.type == "n":
            nm = [[2,1],[2,-1],[1,2],[-1,2],[-2,1],[-2,-1],[-1,-2],[1,-2]]
            nm = list(filter(lambda m : piece.square.ud(m[0]) != None, nm))
            nm = list(filter(lambda m : piece.square.ud(m[0]).lr(m[1]) != None, nm))
            fm = []
            for m in nm:
                move_square = piece.square.ud(m[0]).lr(m[1]);
                pcollision = self.get_piece_by_coord(move_square.file,move_square.rank)
                if pcollision != None:
                    pass
                else:
                    fm += [m]
            moves = [piece.square.ud(m[0]).lr(m[1]) for m in fm];
        
        elif piece.type == "b":
            moves = advancing(self,  piece, [Square.du, Square.dd], 8)

        elif piece.type == "r":
            moves = advancing(self,  piece, [Square.lr, Square.ud], 8)
                        
        elif piece.type == "q":
            moves = advancing(self,  piece, [Square.lr, Square.ud, Square.du, Square.dd], 8)

        elif piece.type == "k":
            moves = advancing(self,  piece, [Square.lr, Square.ud, Square.du, Square.dd], 1)            
            
        return moves

    def attacking_moves(self,piece):
        moves = []

        if piece.type == "p" and piece.white == True:
            la = piece.square.dd(-1)
            ra = piece.square.du(1)
            if la != None:
                lap = self.get_piece_by_square(la)
            if ra != None:
                rap = self.get_piece_by_square(ra)
            if la != None and lap != None and lap.white == False:
                moves+=[la]
            if ra != None and rap != None and rap.white == False:
                moves+=[ra]
            if piece.enpassantl == True:
                moves+=[la]
            if piece.enpassantr == True:
                moves+=[ra]

        elif piece.type == "p" and piece.white == False:
            la = piece.square.dd(1)
            ra = piece.square.du(-1)
            if la != None:
                lap = self.get_piece_by_square(la)
            if ra != None:
                rap = self.get_piece_by_square(ra)
            if la != None and lap != None and lap.white == True:
                moves+=[la]
            if ra != None and rap != None and rap.white == True:
                moves+=[ra]
            if piece.enpassantl == True:
                moves+=[la]
            if piece.enpassantr == True:
                moves+=[ra]

        elif piece.type == "n":
            movelist = [[2,1],[2,-1],[1,2],[1,-2],[-1,2],[-1,-2],[-2,1],[-2,-1]]
            movelist1 = list(filter(lambda move : piece.square.ud(move[0]) != None, movelist))
            movelist2 = list(filter(lambda move : piece.square.ud(move[0]).lr(move[1]) != None, movelist1))
            nm = []
            for move in movelist2:
                move_square = piece.square.ud(move[0]).lr(move[1])
                pcollision = self.get_piece_by_square(move_square)
                if pcollision != None:
                    if pcollision.white == piece.white:
                        pass
                    else:
                        nm += [move]
                        pass
                else:
                    pass
            moves = list(map(lambda m : piece.square.ud(m[0]).lr(m[1]), nm))
        
        elif piece.type == "b":
            moves = attacking(self, piece, [Square.du,Square.dd], 8)

        elif piece.type == "r":
            moves = attacking(self, piece, [Square.ud,Square.lr], 8)

        elif piece.type == "q":
            moves = attacking(self, piece, [Square.ud,Square.lr,Square.du,Square.dd], 8)
                    
        elif piece.type == "k":
            moves = attacking(self, piece, [Square.ud,Square.lr,Square.du,Square.dd], 1)
        
        return moves

class Square:
    def __init__(self,file,rank):
        self.file=file
        self.rank=rank
    def __eq__(self,other):
        try:
            if self.file == other.file and self.rank == other.rank:
                return True
            else:
                return False
        except:
            pass
    def __str__(self):
        try:
            return self.file+str(self.rank)
        except:
            pass

    def __repr__(self):
        return str(self);

    def ud(self, n):
        if self.rank+n > 8 or self.rank+n < 1:
            return None
        else:
            return Square(self.file,self.rank+n)
    def lr(self, n):
        if filesDict[self.file]+n > 8 or filesDict[self.file]+n < 1 :
            return None
        else:
            return Square(files[filesDict[self.file]+(n-1)],self.rank)

    def du(self,n):
        out = self.ud(n)
        try:
            out = out.lr(n)
        except:
            return out
        return out

    def dd(self,n):
        out = self.ud(-n)
        try:
            out = out.lr(n)
        except:
            return out
        return out

class Piece:
    def __init__(self,square,white,piece_type):
        self.square=square;
        self.white=white;
        self.type = piece_type;

    def __str__(self):
        if self.type == "p" and self.white == True:
            return "wp"+self.square.file+str(self.square.rank)
        elif self.type == "p" and self.white == False:
            return "bp"+self.square.file+str(self.square.rank)
        if self.type == "n" and self.white == True:
            return "wn"+self.square.file+str(self.square.rank)
        elif self.type == "n" and self.white == False:
            return "bn"+self.square.file+str(self.square.rank)
        elif self.type == "b" and self.white == True:
            return "wb"+self.square.file+str(self.square.rank)
        elif self.type == "b" and self.white == False:
            return "bb"+self.square.file+str(self.square.rank)
        elif self.type == "r" and self.white == True:
            return "wr"+self.square.file+str(self.square.rank)
        elif self.type == "r" and self.white == False:
            return "br"+self.square.file+str(self.square.rank)
        elif self.type == "q" and self.white == True:
            return "wq"+self.square.file+str(self.square.rank)
        elif self.type == "q" and self.white == False:
            return "bq"+self.square.file+str(self.square.rank)
        elif self.type == "k" and self.white == True:
            return "wk"+self.square.file+str(self.square.rank)
        elif self.type == "k" and self.white == False:
            return "bk"+self.square.file+str(self.square.rank)
        else:
            return "Chess piece"

    def __repr__(self):
            return str(self)

    def move_to(square):
        self.square = square
        
    def ud(self, n):
        self.square = self.square.ud(n)

    def lr(self, n):
        self.square = self.square.lr(n);

    def du(self,n):
        self.square = self.square.lr(n)
        try:
            self.square = self.square.ud(n)
        except:
            pass

    def dd(self,n):
        self.square = self.square.lr(n)
        try:
            self.square = self.square.ud(-n)
        except:
            pass
    def move_to(self, new_square):
        self.square = new_square

    #The two directions du and dd are "linearly independent". But this is a grid,
    #not a vector space. Anyways.

class Pawn(Piece):
    def __init__(self,square,white):
        self.square = square
        self.white = white
        self.type = "p"
        self.enpassantl = False
        self.enpassantr = False

class Knight(Piece):
    def __init__(self,square,white):
        self.square = square
        self.white = white
        self.type = "n"
    
class Bishop(Piece):
    def __init__(self,square,white):
        self.square = square
        self.white = white
        self.type = "b"

class Rook(Piece):
    def __init__(self,square,white):
        self.square = square
        self.white = white
        self.type = "r"

class Queen(Piece):
    def __init__(self,square,white):
        self.square = square
        self.white = white
        self.type = "q"

class King(Piece):
    def __init__(self,square,white):
        self.square = square
        self.white = white
        self.type = "k"
