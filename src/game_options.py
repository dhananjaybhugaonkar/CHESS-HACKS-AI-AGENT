from .config import * 


class GameOptions:

    def drawOptionsText(pg, screen):
        '''
        Function for drawing options text
        '''
        color = '#B27A42'
        font = pg.font.SysFont('Calibri',18, True, False) 
        screen.fill('white')
        GameOptions.drawLogo(pg, screen)

        pg.draw.rect(screen, color, [457, 550, 170 , 40], border_radius=15)
        
        text = font.render('Play with AI' , True , 'BLACK')
        screen.blit(text , (498 , 560))

        pg.draw.rect(screen, color, [275, 550, 170 , 40], border_radius=15)
        text = font.render('Play with Human' , True , 'BLACK')

        screen.blit(text , (298 , 560))
    
    def drawLevelsText(pg, screen):
        '''
        Function for drawing options text
        '''
        screen.fill('white')
        color = '#B27A42'
        font = pg.font.SysFont('Calibri',19, True, False) 
        
        GameOptions.drawLogo(pg, screen)
        
        pg.draw.rect(screen, color, [510, 550, 100 , 40], border_radius=15)
        text = font.render('Level 3' , True , 'black')
        screen.blit(text , (534 , 560))

        pg.draw.rect(screen, color, [400, 550, 100 , 40], border_radius=15)
        text = font.render('Level 2' , True , 'black')
        screen.blit(text , (424 , 560))

        pg.draw.rect(screen, color, [290, 550, 100 , 40], border_radius=15)
        text = font.render('Level 1' , True , 'black')
        screen.blit(text , (314 , 560))


    def drawEndGameText(pg, screen, text):
        '''
        Function for drawing checkmate and stalemate text
        '''
        font = pg.font.SysFont("Calibri", 32, True, False)
        textObject = font.render(text, 0, pg.Color("Gray"))
        textLocation = pg.Rect(0, 0, WIDTH, HEIGHT).move(
            WIDTH / 2 - textObject.get_width() / 2,
            HEIGHT / 2 - textObject.get_height() / 2)
        screen.blit(textObject, textLocation)
        textObject = font.render(text, 0, pg.Color("Black"))
        screen.blit(textObject, textLocation.move(2, 2))


    def drawCleargame(pg, screen):
        '''
        Function for drawing options text
        '''
        color = '#B27A42'
        font = pg.font.SysFont('Calibri',14, True, False) 
        
        pg.draw.rect(screen, color, [810, 100, 83 , 30], border_radius=15)
        text = font.render('New Game' , True , 'black')
        screen.blit(text , (818 , 106))
        
        pg.draw.rect(screen, color, [810, 150, 83 , 30], border_radius=15)
        text = font.render('Reset Game' , True , 'black')
        screen.blit(text , (815 , 156))


    def drawLogo(pg, screen):
        img = pg.image.load("src/images/logo.png")
        screen.blit(img, (150, 0))