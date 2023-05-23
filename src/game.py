'''
Class responsible for storing information about state of chess game
Determines valid moves at current position and keeps move log
'''
import copy, pygame
from .piece_moves import PMoves

class GameState():
    def __init__(self):
        self.board = [
            ['BRook', 'BKnight', 'BBishop', 'BQueen', 'BKing', 'BBishop', 'BKnight', 'BRook'],
            ['BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn'],
            ['WRook', 'WKnight', 'WBishop', 'WQueen', 'WKing', 'WBishop', 'WKnight', 'WRook']]

        self.whiteToMove = True
       
        self.wKingPos = (7, 4)
        self.bKingPos = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.sound = False
        self.enpassantPossible = ()
        self.currentCastlingRight = CastleRights(True, True, True, True)


    def makeMove(self, move):
        '''
        Moves pieces and handles updates of all logical operators
        '''
        self.board[move.startRow][move.startCol] = '--' # update present piece position on the board
        
        if self.sound:
            if self.board[move.endRow][move.endCol] == '--':            
                pygame.mixer.Sound.play(pygame.mixer.Sound('src/sounds/move.wav'))
            elif self.board[move.endRow][move.endCol] != '--':
                pygame.mixer.Sound.play(pygame.mixer.Sound('src/sounds/capture.wav'))
            self.sound = False
 
        self.board[move.endRow][move.endCol] = move.pieceMoved # update piece to new position on the board
        
        self.whiteToMove = not self.whiteToMove #update to opponent's turn

        # update king location if moves
        if move.pieceMoved == 'WKing':
            self.wKingPos = (move.endRow, move.endCol)
        if move.pieceMoved == 'BKing':
            self.bKingPos = (move.endRow, move.endCol)

        self.specialMoves(move)


    def specialMoves(self,move):
        
        if move.isPawnPromotion: # Pawn Promotion logic
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
       
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2: # Logic to find possible enpassant positions 
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

        if move.isEnpassantMove: # update captured piece to empty square for en passant move
            self.board[move.startRow][move.endCol] = '--'
      
        if move.isCastleMove: # Unique piece position for castle move
            if move.endCol - move.startCol == 2: # kingside castle move
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else: # Else it is queenside castle move
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'

        self.updateCastleRights(move)


    def updateCastleRights(self, move):
        if move.pieceMoved == 'WKing':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False

        elif move.pieceMoved == 'BKing':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False

        elif move.pieceMoved == 'WRook':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.wks = False

        elif move.pieceMoved == 'BRook':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRight.bks = False

        if move.pieceCaptured == 'WRook':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False

        if move.pieceCaptured == 'BRook':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False


    def getValidMoves(self):

        moves, pieces = self.getAllPossibleMoves() # Generate all possible moves
        if self.whiteToMove:
            PMoves.CastleMoves(self, self.wKingPos[0], self.wKingPos[1], moves)
        else:
            PMoves.CastleMoves(self,self.bKingPos[0], self.bKingPos[1], moves)
        
        checkrule = copy.deepcopy(self)
        for i in range(len(moves) - 1, -1, -1): # for each move, generates the move and checks if the move attacks the king scenarios
            
            checkrule.makeMove(moves[i])

            checkrule.whiteToMove = not checkrule.whiteToMove
            if checkrule.inCheck():
                moves.remove(moves[i])
            checkrule.whiteToMove = not checkrule.whiteToMove
            checkrule = copy.deepcopy(self)
            
        if len(moves) != 0 and len(pieces) == 2:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
             
        return moves
    

    def inCheck(self):
        '''
        Helper method for determinig if king is in check
        '''
        if self.whiteToMove:
            return self.squareUnderAttack(self.wKingPos[0], self.wKingPos[1])
        else:
            return self.squareUnderAttack(self.bKingPos[0], self.bKingPos[1])

    def squareUnderAttack(self, r, c):
        '''
        Helper method for determining if a square is under attack
        Used for castling logic
        '''
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()[0]
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        '''
        Determines all possible moves before filtering for whether or not your king will be put in check
        Returns: moves (list), pieces (list)
        '''
        moves = []
        pieces = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                if self.board[r][c] != '--':
                    pieces.append(self.board[r][c])
                team = self.board[r][c][0]
                
                if ((team == 'W' and self.whiteToMove) or (team == 'B' and not self.whiteToMove)):
                    piece = self.board[r][c][1:]
                    if piece == 'Pawn':
                        PMoves.PawnMoves(self, r, c, moves)
                    elif piece == 'Rook':
                        PMoves.RookMoves(self, r, c, moves)
                    elif piece == 'Bishop':
                        PMoves.BishopMoves(self, r, c, moves)
                    elif piece == 'Knight':
                        PMoves.KnightMoves(self, r, c, moves)
                    elif piece == 'Queen':
                        PMoves.QueenMoves(self, r, c, moves)
                    elif piece == 'King':
                        PMoves.KingMoves(self, r, c, moves)
        return moves, pieces


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs
