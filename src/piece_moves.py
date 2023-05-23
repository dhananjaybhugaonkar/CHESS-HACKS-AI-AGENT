


class Move():
    '''
    Class for handling moves and special move logic like en passant, castling, and promotion are handled here
    '''

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        # If a pawn makes it the last rank then it promotes
        self.isPawnPromotion = False
        if (self.pieceMoved == 'WPawn' and self.endRow == 0) or (self.pieceMoved == 'BPawn' and self.endRow == 7):
            self.isPawnPromotion = True

        # If a move is en passant than piece captured logic must change (it doesn't capture an empty square)
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "WPawn" if self.pieceMoved == "BPawn" else "BPawn"

        self.isCastleMove = isCastleMove
        self.isCapture = self.pieceCaptured != '--'
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


class PMoves:

    def PawnMoves(self, r, c, moves):
         
        def PawnSquares(row,r, p):

            if self.board[r][c] == "--":  # the square in front of a pawn is empty
                moves.append(Move((row, c), (r, c), self.board))   
                
                if row == 6 and self.board[r - 1][c] == "--": # second square in front of pawn is empty
                    moves.append(Move((row, c), (r - 1, c), self.board))

                elif row == 1 and self.board[r + 1][c] == "--": # second square in front of pawn is empty
                    moves.append(Move((row, c), (r + 1, c), self.board))

            if c - 1 >= 0: 
                if (self.board[r][c - 1][0] == p):  # there's an enemy piece to capture
                    moves.append(Move((row, c), (r, c - 1), self.board))
                elif (r, c - 1) == self.enpassantPossible:
                    moves.append(Move((row, c), (r, c - 1), self.board, isEnpassantMove=True))

            if c + 1 <= 7:  
                if (self.board[r][c + 1][0] == p):  # there's an enemy piece to capture
                    moves.append(Move((row, c), (r, c + 1), self.board))
                elif (r, c + 1) == self.enpassantPossible:
                    moves.append(Move((row, c), (r, c + 1), self.board, isEnpassantMove=True))

        if self.whiteToMove:  # white pawn move
            PawnSquares(r,r-1,"B")
        else:                 # black pawn move
            PawnSquares(r,r+1,"W")
        
       


    def RookMoves(self, r, c, moves):

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1)) # Rooks can move up, down, left, and right
        enemyTeam = 'B' if self.whiteToMove else 'W' # Enemy pieces can be captured so need different logic for enemy pieces and friendly pieces
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8: # Make sure move doesn't go off the board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--": # If square is empty, then its a legal move
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyTeam: # If square has an enemy piece, move can be captured but then must break
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def BishopMoves(self, r, c, moves):

        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1)) # Bishops move diagonally
        enemyTeam = 'B' if self.whiteToMove else 'W'
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyTeam:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:
                        break
                else:
                    break


    def KnightMoves(self, r, c, moves):

        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyTeam = 'W' if self.whiteToMove else 'B'
        for d in directions:
            endRow = r + d[0]
            endCol = c + d[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyTeam:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    def QueenMoves(self, r, c, moves):
        '''
        Queen just moves like a rook and a bishop combined
        '''
        PMoves.RookMoves(self, r, c, moves)
        PMoves.BishopMoves(self, r, c, moves)


    def KingMoves(self, r, c, moves):

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        allyTeam = 'W' if self.whiteToMove else 'B'
        for i in range(8):
            endRow = r + directions[i][0]
            endCol = c + directions[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyTeam:
                    moves.append(Move((r, c), (endRow, endCol), self.board))


    def CastleMoves(self, r, c, moves):

        if self.squareUnderAttack(r, c):
            return

        #Check King Side Castle Moves
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
                if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                    moves.append(Move((r, c), (r, c + 2), self.board, isCastleMove=True))
        
        #Check Queen Side Castle Moves
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--' and (not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2)):
                moves.append(Move((r, c), (r, c - 2), self.board, isCastleMove=True))
