from .config import *

class Board:

    def load_images(pg):
        '''
        Initialize images
        '''
        pieces_list = ['WPawn', 'WRook', 'WKnight', 'WBishop', 'WQueen', 'WKing', 'BPawn', 'BRook', 'BKnight', 'BBishop', 'BQueen', 'BKing']
        for piece in pieces_list:
            PIECE_IMG[piece] = pg.image.load('src/images/' + piece + '.png')


    def designBoard(pg,screen):
        '''
        design board of squares
        '''
        colors = [(234,235,200), (119, 154, 88)]
        font = font = pg.font.SysFont('monospace', 18, bold=True)
        ALPHACOLS = {7: 'a', 6: 'b', 5: 'c', 4: 'd', 3: 'e', 2: 'f', 1: 'g', 0: 'h'}

        for row in range(ROWS):
            for col in range(ROWS):
                color = colors[0] if ((row+col) % 2) == 0 else colors[1]
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)

                pg.draw.rect(screen, color, rect)

                if col == 0:
                    label = font.render(str(ROWS-row), 1, '#606060')
                    label_pos = (5, 5 + row * SQSIZE)
                    screen.blit(label, label_pos)
                if row == 7:      
                    label = font.render(ALPHACOLS[col], 1, '#606060')
                    label_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    screen.blit(label, label_pos)


    def showPieces(screen, board):
        '''
        show pieces from png files
        '''
        for row in range(ROWS):
            for col in range(ROWS):
                piece = board[row][col]
                if piece != '--':
                    i_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                    screen.blit(PIECE_IMG[piece], PIECE_IMG[piece].get_rect(center=i_center))


    def showValidSquares(pg, screen, gs, validMoves, sqSelected):
        '''
        Highlight squares when clicked
        '''
        if sqSelected != ():
            r, c = sqSelected
            if gs.board[r][c][0] == ('W' if gs.whiteToMove else 'B'):
                s = pg.Surface((SQSIZE, SQSIZE))
                s.set_alpha(100) # Transparency
                s.fill(pg.Color('blue'))
                screen.blit(s, (c*SQSIZE, r*SQSIZE))
                s.fill(pg.Color('yellow'))
                for move in validMoves:
                    if move.startRow == r and move.startCol == c:
                        screen.blit(s, (SQSIZE*move.endCol, SQSIZE*move.endRow))
    
    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()