'''
Driver file, handles user input and displays position
'''
import sys, pygame as pg
import src.game as game

from src.config import *
from src.chessboard import Board
from src.game_options import GameOptions
from src.engine import Engine
from src.piece_moves import Move

class Main:
    
    def __init__(self):
        self.player1 = True # True for human and false for AI.
        self.player2 = True # True for human and false for AI.

        #Game options 
        self.gameoption = True
        self.options=["Press Q for two player", "Press W for White vs AI", "Press E for Black vs AI"]
        self.leveloption = False
        self.cleargame = False
        
        self.depth = 1
        self.selSquare = () # will keep track of last click of the user
        self.playerClicks = [] # keeps track of player clicks
        self.validMoves=[] # stores all the valid moves at a given game state

        self.gameStart = True
        self.gameOver = False # flag when a game is over
        self.moveMade = False # flag when a move is made

        pg.init()
        pg.display.set_caption('Chess')

        self.screen = pg.display.set_mode((WIDTH+LOG_PANEL, HEIGHT))
        self.screen.fill('white')

        self.gs = game.GameState()
        self.chessEngine = Engine()

    def mainloop(self):

        self.validMoves = self.gs.getValidMoves()
        
        Board.load_images(pg)

        while True:
            self.PlayerTurn = (self.gs.whiteToMove and self.player1) or (not self.gs.whiteToMove and self.player2)
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif e.type == pg.MOUSEBUTTONDOWN: # Mouse click event                           
                    self.mouseClick()        
            
            self.moveAction()

            self.AITurn() # function call for AI turn

            self.moveAction()

            if self.gameoption:
                GameOptions.drawOptionsText(pg, self.screen)
            elif self.leveloption:
                GameOptions.drawLevelsText(pg, self.screen)
            else:
                self.GameState(self.screen, self.selSquare)
            
            if self.gs.checkmate or self.gs.stalemate:
                self.gameOver = True
                if self.gs.stalemate:
                    text = 'Stalemate'
                else:
                    text = 'Black wins by checkmate' if self.gs.whiteToMove else 'White wins by checkmate'
                
                
                GameOptions.drawEndGameText(pg, self.screen, text)

            pg.display.flip()
        

    def moveAction(self):
        if self.moveMade and not self.gameOver:
            self.validMoves = self.gs.getValidMoves()
            self.moveMade = False
                
            if len(self.validMoves) < 1: 
                self.gameOver = True
                if self.gs.inCheck():
                    self.gs.checkmate = True
                else:
                    self.gs.stalemate = True


    def mouseClick(self):
        square = pg.mouse.get_pos() # position of the clicked square
        if not self.gameOver and self.PlayerTurn:
            if self.gameoption or self.leveloption:
                self.buttonClick(square)
            else:
                if self.cleargame:
                    self.buttonClick(square)
                self.gameStart = False
                col = square[0] // SQSIZE
                row = square[1] // SQSIZE
                if self.selSquare == (row, col) or col >= 8: # clear clicks when the same square is clicked
                    self.selSquare = ()
                    self.playerClicks = []
                else:
                    self.selSquare = (row, col) 
                    self.playerClicks.append(self.selSquare) # append player clicks to list
                    
                if len(self.playerClicks) == 2:
                    move = Move(self.playerClicks[0], self.playerClicks[1], self.gs.board)
                    for i in range(len(self.validMoves)):
                        if move == self.validMoves[i]: # check if the move is in valid moves
                            self.gs.sound = True
                            self.gs.makeMove(self.validMoves[i])
                            self.moveMade = True
                            self.selSquare = ()
                            self.playerClicks = []
                    if not self.moveMade:
                        self.playerClicks = [self.selSquare]
        
        elif self.cleargame:
             self.buttonClick(square)

    
    def buttonClick(self, square):

        def reset():
            self.gs = game.GameState()
            self.validMoves = self.gs.getValidMoves()
            self.selSquare = ()
            self.playerClicks = []
            self.moveMade = False
            self.gs.checkmate = False
            self.gs.stalemate = False
            self.gameStart = True
            self.gameOver = False

        if self.gameoption:
            if 457 <= square[0] <= 457+170 and 550 <= square[1] <= 590: # play with AI option
                self.player1 = True
                self.player2 = False
                self.gameoption = False
                self.leveloption = True
            elif 275 <= square[0] <= 275+170 and 550 <= square[1] <= 590: # play with Human option
                self.player1 = True
                self.player2 = True
                self.gameoption = False
        
        elif self.leveloption:
            if 510 <= square[0] <= 610 and 550 <= square[1] <= 590: # play with AI option
                self.depth = 3
                self.leveloption = False
            elif 400 <= square[0] <= 500 and 550 <= square[1] <= 590: # play with Human option
                self.depth = 2
                self.leveloption = False
            elif 290 <= square[0] <= 390 and 550 <= square[1] <= 590: # play with Human option
                self.depth = 1
                self.leveloption = False
        elif self.cleargame:          
            if 810 <= square[0] <= 893: 
                if 100 <= square[1] <= 130: # play with AI option
                    self.gameoption = True
                    reset()      
                elif 150 <= square[1] <= 180: # play with Human option
                    reset()


    def GameState(self,screen, selSquare):
        '''
        design the board
        '''
        Board.designBoard(pg,screen)
        Board.showValidSquares(pg, screen, self.gs, self.validMoves, selSquare)
        Board.showPieces(screen, self.gs.board)
        GameOptions.drawCleargame(pg, self.screen)
        if not self.cleargame:
            self.cleargame = True


    def AITurn(self):
        if not self.gameOver and not self.PlayerTurn and not self.gameStart:
            AIMove = self.chessEngine.findBestMove(self.gs, self.validMoves, self.depth)
            
            if AIMove is None:
                if len(self.validMoves) > 0: 
                    AIMove = self.chessEngine.findRandomMove(self.validMoves)
                    
                    self.gs.makeMove(AIMove)
                    self.gs.sound = True 
                    self.moveMade = True
                else:
                    self.gameOver = True
                    if self.gs.inCheck():
                        self.gs.checkmate = True
                    else:
                        self.gs.stalemate = True
            else:
                self.gs.makeMove(AIMove)
                self.gs.sound = True
                self.moveMade = True
                

main = Main()
main.mainloop()



