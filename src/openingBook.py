from .piece_moves import Move


class Repetoir:
    '''
    Class that hold dictionary of moves to be played in given positions
    '''
    def __init__(self, startMove=('e2', 'e4'), e4Response=('e7', 'e5')):
        self.myRepetoir = {}
        self.startPos = self.pos_to_key([
            ['BRook', 'BKnight', 'BBishop', 'BQueen', 'BKing', 'BBishop', 'BKnight', 'BRook'],
            ['BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn'],
            ['WRook', 'WKnight', 'WBishop', 'WQueen', 'WKing', 'WBishop', 'WKnight', 'WRook']])
        
    @staticmethod
    def pos_to_key(pos):
        'Converts position into a long string'
        board_string = ''
        for x in pos:
            for y in x:
                board_string += y

        return board_string


    @staticmethod
    def chessToComputer(startSq, endSq):
        '''
        Converts square notation into computer board notation
        '''
        ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4, 
                    '5': 3, '6': 2, '7': 1, '8': 0}
        filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                    'e': 4, 'f': 5, 'g': 6, 'h':7}
        return ((ranksToRows[startSq[1]], filesToCols[startSq[0]]), (ranksToRows[endSq[1]], filesToCols[endSq[0]]))

    def makeMove(self, move):
        '''
        Simplified version of make move function, can be used if you want '''
        self.board[move.startRow][move.startCol] = '--'
        self.board[move.endRow][move.endCol] = move.pieceMoved
    
    def add_position_response(self, board, move_tuple, isCastleMove=False, isEnPassantMove=False):
        '''
        Method for adding a position to myRepetoir
        '''
        self.myRepetoir[Repetoir.pos_to_key(board)] = (Repetoir.chessToComputer(move_tuple[0], move_tuple[1]), isCastleMove, isEnPassantMove)

# The Scotch opening repetoir
e4 = Repetoir()
e4.add_position_response(e4.startPos, (('e2'), ('e4')))
e4.add_position_response(e4.pos_to_key([
            ['BRook', 'BKnight', 'BBishop', 'BQueen', 'BKing', 'BBishop', 'BKnight', 'BRook'],
            ['BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn'],
            ['WRook', 'WKnight', 'WBishop', 'WQueen', 'WKing', 'WBishop', 'WKnight', 'WRook']
            ]), (('g1'), ('f3')))

e4.add_position_response(e4.pos_to_key([
            ['BRook', 'BKnight', 'BBishop', 'BQueen', 'BKing', 'BBishop', 'BKnight', 'BRook'],
            ['BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn'],
            ['WRook', 'WKnight', 'WBishop', 'WQueen', 'WKing', 'WBishop', 'WKnight', 'WRook']
            ]), (('d2'), ('d4')))

e4.add_position_response(e4.pos_to_key([
            ['BRook', 'BKnight', 'BBishop', 'BQueen', 'BKing', 'BBishop', 'BKnight', 'BRook'],
            ['BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn'],
            ['WRook', 'WKnight', 'WBishop', 'WQueen', 'WKing', 'WBishop', 'WKnight', 'WRook']
            ]), (('f3'), ('d4')))

e4.add_position_response(e4.pos_to_key([
            ['BRook', 'BKnight', 'BBishop', 'BQueen', 'BKing', 'BBishop', 'BKnight', 'BRook'],
            ['BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn', 'BPawn'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['--', '--', '--', '--', '--', '--', '--', '--'],
            ['WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn', 'WPawn'],
            ['WRook', 'WKnight', 'WBishop', 'WQueen', 'WKing', 'WBishop', 'WKnight', 'WRook']
            ]), (('g1'), ('f3')))



