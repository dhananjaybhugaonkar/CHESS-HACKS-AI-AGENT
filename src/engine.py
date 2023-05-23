import random as rnd,copy
from .openingBook import Repetoir
from .piece_moves import Move

class Engine:

    def __init__(self, repetoir={}):
        self.checkmate = float('inf')
        self.stalemate = 0
        self.depth = 1
        self.repetoir = repetoir
        self.pieceScore = {"King": 0, "Queen": 10, "Rook": 5, "Knight": 3, "Bishop": 3, "Pawn": 1}
        
        self.knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1], ]

        self.bishopScores = [[4, 3, 2, 1, 1, 2, 3, 4],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [2, 3, 4, 3, 3, 4, 3, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [4, 3, 2, 1, 1, 2, 3, 4], ]

        self.queenScores = [[1, 1, 1, 3, 1, 1, 1, 1],
               [1, 2, 3, 3, 3, 1, 1, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 2, 3, 3, 3, 2, 2, 1],
               [1, 4, 3, 3, 3, 4, 2, 1],
               [1, 1, 2, 3, 3, 1, 1, 1],
               [1, 1, 1, 3, 1, 1, 1, 1], ]

        self.rookScores = [[4, 3, 4, 4, 4, 4, 3, 4],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 2, 3, 4, 4, 3, 2, 1],
              [1, 1, 2, 3, 3, 2, 1, 1],
              [4, 4, 4, 4, 4, 4, 4, 4],
              [4, 3, 4, 4, 4, 4, 3, 4], ]

        self.whitePawnScores = [[8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0], ]

        self.blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 3, 3, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 3, 3, 5, 5, 3, 3, 2],
                   [5, 6, 6, 7, 7, 6, 6, 5],
                   [8, 8, 8, 8, 8, 8, 8, 8],
                   [8, 8, 8, 8, 8, 8, 8, 8], ]

        self.piecePositionScores = {"Knight": self.knightScores, "Bishop": self.bishopScores, "Queen": self.queenScores, "WPawn": self.whitePawnScores,
                       "BPawn": self.blackPawnScores, "Rook": self.rookScores}

    def findRandomMove(self, validMoves):
        return validMoves[rnd.randint(0, len(validMoves) - 1)]

    def findBestMove(self, gs, validMoves, depth):
        '''
        Method to make first recursive call
        '''
        global nextMove, counter
        self.depth = depth

        nextMove = None
        rnd.shuffle(validMoves)
        counter = 0
        board_as_key = Repetoir.pos_to_key(gs.board)

        if board_as_key in self.repetoir:
            return Move(self.repetoir[board_as_key][0][0], self.repetoir[board_as_key][0][1], gs.board, isCastleMove=self.repetoir[board_as_key][1], isEnpassantMove=self.repetoir[board_as_key][2])
        
        self.findMoveNegamaxAlphaBeta(gs, validMoves, depth, -self.checkmate, self.checkmate, 1 if gs.whiteToMove else -1)
        print(counter, currScore)
        
        return nextMove

    def findMoveNegamaxAlphaBeta(self, gs, validMoves, depth, alpha, beta, turnMultiplier):
        global nextMove, counter, currScore
        counter += 1
        if depth == 0:
            return turnMultiplier * self.scoreBoard(gs)

        maxScore = -self.checkmate
        checkrule = copy.deepcopy(gs)
        for move in validMoves:
            checkrule.makeMove(move)
            nextMoves = checkrule.getValidMoves()
            score = -self.findMoveNegamaxAlphaBeta(checkrule, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
            if score > maxScore:
                maxScore = score
                if depth == self.depth:
                    nextMove = move
           
            if maxScore > alpha:  # pruning happens here
                alpha = maxScore
            if alpha >= beta:
                break
            checkrule = copy.deepcopy(gs)
        currScore = maxScore
        
        return maxScore


    def scoreBoard(self, gs):
        """
        # increasing the number of valid moves per piece
        # Giving Bishops more open lanes
        # Queen open lanes
        # Castling (Capturing King safety)
        """
        if gs.checkmate:
            if gs.whiteToMove:
                return -self.checkmate
            else:
                return self.checkmate
        elif gs.stalemate:
            return self.stalemate

        score = 0
        for row in range(len(gs.board)):
            for col in range(len(gs.board[row])):
                square = gs.board[row][col]
                if square != "--":
                    piecePositionScore = 0
                    if square[1:] != "King":
                        if square[1:] == "Pawn":
                            piecePositionScore = self.piecePositionScores[square][row][col]
                        else:
                            piecePositionScore = self.piecePositionScores[square[1:]][row][col]

                    if square[0] == 'W':
                        score += self.pieceScore[square[1:]] + piecePositionScore * 0.1
                    elif square[0] == 'B':
                        score -= self.pieceScore[square[1:]] + piecePositionScore * 0.1

        return score

