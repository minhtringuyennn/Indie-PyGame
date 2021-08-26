from pygame.locals import *

from Button import BoardSizeButton, ActionButton
from gameBoard import *

FPS = 60
WINDOWSIZE = 650
BLACK = (250, 250, 250)
COLOR1 = (120, 120, 120)
VOLUME = 0.2

def main():
    tempRowCol = (None, None)
    pygame.init()
    screen = pygame.display.set_mode((WINDOWSIZE, WINDOWSIZE))
    pygame.display.set_caption('SYMBOLS Memory Game')
    icon = pygame.image.load('Assets/Symbols/therefore.jpg')
    icon = pygame.transform.scale(icon, (32, 32))

    menu_bg_sound = pygame.mixer.Sound('Assets/Sound/menu_bg.mp3')
    bg_sound = pygame.mixer.Sound('Assets/Sound/bg.mp3')
    win_sound = pygame.mixer.Sound('Assets/Sound/win.mp3')
    correct_sound = pygame.mixer.Sound('Assets/Sound/correct.mp3')
    menu_bg_sound.set_volume(VOLUME)
    bg_sound.set_volume(VOLUME)
    win_sound.set_volume(VOLUME)

    pygame.display.set_icon(icon)
    screen.fill(BLACK)

    pygame.display.flip()

    BOARD_SIZE_BUTTON = 100

    FPSCLOCK = pygame.time.Clock()

    four_x_four = pygame.image.load('Resources/4x4.jpg')
    four_x_four = pygame.transform.scale(four_x_four, (BOARD_SIZE_BUTTON, BOARD_SIZE_BUTTON))

    four_x_six = pygame.image.load('Resources/4x6.jpg')
    four_x_six = pygame.transform.scale(four_x_six, (BOARD_SIZE_BUTTON, BOARD_SIZE_BUTTON))

    five_x_six = pygame.image.load('Resources/5x6.jpg')
    five_x_six = pygame.transform.scale(five_x_six, (BOARD_SIZE_BUTTON, BOARD_SIZE_BUTTON))

    six_x_six = pygame.image.load('Resources/6x6.jpg')
    six_x_six = pygame.transform.scale(six_x_six, (BOARD_SIZE_BUTTON, BOARD_SIZE_BUTTON))

    six_x_seven = pygame.image.load('Resources/6x7.jpg')
    six_x_seven = pygame.transform.scale(six_x_seven, (BOARD_SIZE_BUTTON, BOARD_SIZE_BUTTON))

    six_x_eight = pygame.image.load('Resources/6x8.jpg')
    six_x_eight = pygame.transform.scale(six_x_eight, (BOARD_SIZE_BUTTON, BOARD_SIZE_BUTTON))

    start_game_button_image = pygame.image.load('Resources/startGame.jpg')
    start_game_button_image = pygame.transform.scale(start_game_button_image, (180, 95))

    start_image = pygame.image.load('Resources/logo.jpg')
    start_image = pygame.transform.scale(start_image, (280, 210))

    backButtonImage = pygame.image.load('Resources/backButton.jpg')
    backButtonImage = pygame.transform.scale(backButtonImage, (100, 50))

    mainMenuButtonImage = pygame.image.load('Resources/mainMenu.jpg')
    mainMenuButtonImage = pygame.transform.scale(mainMenuButtonImage, (150, 75))

    soundIndex = 1
    soundOnImage = pygame.image.load('Resources/soundOn.png')
    soundOnImage = pygame.transform.scale(soundOnImage, (180, 95))
    soundOffImage = pygame.image.load('Resources/soundOff.png')
    soundOffImage = pygame.transform.scale(soundOffImage, (180, 95))

    aboutImage = pygame.image.load('Resources/about.png')
    aboutImage = pygame.transform.scale(aboutImage, (180, 95))

    stats = GameStats(screen)
    board = GameBoard(0, 0, 0, WINDOWSIZE, screen, FPSCLOCK)
    game_board = board.createRandomizedBoard()

    mousex = 0
    mousey = 0
    row, column = (None, None)
    first_selection = None
    gameState = 'game_not_started'
    b4x4 = BoardSizeButton(100, 100, 100, four_x_four, 160, 270, (4, 4))
    b4x6 = BoardSizeButton(100, 100, 95, four_x_six, 270, 270, (6, 4))
    b5x6 = BoardSizeButton(100, 100, 95, five_x_six, 380, 270, (6, 5))
    b6x6 = BoardSizeButton(100, 100, 85, six_x_six, 160, 380, (6, 6))
    b6x7 = BoardSizeButton(100, 100, 80, six_x_seven, 270, 380, (7, 6))
    b6x8 = BoardSizeButton(100, 100, 72, six_x_eight, 380, 380, (8, 6))

    start_game_button = ActionButton(180, 95, start_game_button_image, 232, 510)
    about_button = ActionButton(180, 95, aboutImage, 20, 510)
    sound_button = [ActionButton(180, 95, soundOffImage, 450, 510), ActionButton(180, 95, soundOnImage, 450, 510)]
    backToMainScreen = ActionButton(100, 50, backButtonImage, 15, 15)
    mainMenuButton = ActionButton(150, 75, mainMenuButtonImage, 240, 300)

    buttons = [b4x4, b4x6, b5x6, b6x6, b6x7, b6x8, start_game_button, about_button, 
                sound_button[0], sound_button[1],backToMainScreen, mainMenuButton]

    width, height = 0, 0

    trigger = True

    while True:
        mouse_clicked = False
        screen.fill(BLACK)

        if gameState == 'game_not_started':
            font = pygame.font.Font('Resources/Norse-KaWl.otf', 80)
            text_runes = font.render('SYMBOLS', True, COLOR1, BLACK)
            textRect_runes = text_runes.get_rect()
            textRect_runes.center = (160, 180)
            screen.blit(text_runes, textRect_runes)
            menu_bg_sound.play(-1, 0, 1500)
            bg_sound.stop()

            font2 = pygame.font.Font('Resources/Norse-KaWl.otf', 35)
            text_game = font2.render('Memory Game', True, COLOR1, BLACK)
            textRect_game = text_game.get_rect()
            textRect_game.center = (230, 230)
            screen.blit(text_game, textRect_game)

            screen.blit(start_image, (315, 40))

            b4x4.show(screen)
            b4x6.show(screen)
            b5x6.show(screen)
            b6x6.show(screen)
            b6x7.show(screen)
            b6x8.show(screen)

            start_game_button.show(screen)
            about_button.show(screen)
            sound_button[soundIndex].show(screen)
        
        elif gameState == 'show_info':
            infoImage = pygame.image.load('Resources/info.png')
            screen.blit(infoImage, (0, 0))
            backToMainScreen.show(screen)

        elif gameState == 'start_animation_not_played':
            menu_bg_sound.stop()
            bg_sound.play(-1, 0, 1500)
            trigger = True
            stats.displayNumberOfTries()
            stats.displayTime(pygame.time.get_ticks())
            backToMainScreen.show(screen)
            board.startGameAnimation(game_board, board.width, board.height)
            gameState = 'start_time_not_taken'

        elif gameState == 'start_time_not_taken':
            startTime = pygame.time.get_ticks()
            gameState = 'game_started'

        elif gameState == 'game_started':
            screen.fill(BLACK)
            board.drawBoard(game_board)
            stats.displayNumberOfTries()
            stats.displayTime(startTime)
            backToMainScreen.show(screen)
            row, column = board.getBoxAtPixel(mousex, mousey)

        elif gameState == 'end_time_not_taken':
            screen.fill(BLACK)
            endTime = pygame.time.get_ticks() - startTime
            board = GameBoard(0, 0, 0, WINDOWSIZE, screen, FPSCLOCK)
            tempRowCol = (None, None)
            gameState = 'game_won'

        elif gameState == 'game_won':
            screen.fill(BLACK)
            if trigger == True:
                win_sound.play()
                trigger = False
            
            mainMenuButton.show(screen)
            stats.displayGameWonText(endTime)

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == pygame.MOUSEMOTION:
                mousex, mousey = event.pos
                if gameState == 'game_not_started':
                    for button in buttons:
                        button.isButtonHovered(event)
                    start_game_button.isButtonHovered(event)
                if gameState == 'game_started' and row is not None and column is not None:
                    game_board[row][column].isCardHovered(event)
                if gameState == 'game_started' or gameState == 'show_info':
                    backToMainScreen.isButtonHovered(event)
                if gameState == 'game_won':
                    mainMenuButton.isButtonHovered(event)
            if event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouse_clicked = True

        if gameState == 'game_not_started' and mouse_clicked:
            sound_trigger = True

            for button in buttons:
                if button.handleClick(event):
                    if type(button) is BoardSizeButton:
                        width, height = button.boardSize
                        size = button.cardSize
                    if start_game_button.handleClick(event) and width != 0 and height != 0:
                        board = GameBoard(width, height, size, WINDOWSIZE, screen, FPSCLOCK)
                        game_board = board.createRandomizedBoard()
                        screen.fill(BLACK)
                        gameState = 'start_animation_not_played'
                    if about_button.handleClick(event):
                        gameState = 'show_info'
                    if sound_button[soundIndex].handleClick(event):
                        if sound_trigger == True:
                            soundIndex += 1
                            soundIndex %= 2

                            if soundIndex == 1:
                                pygame.mixer.stop()
                                menu_bg_sound.set_volume(VOLUME)
                                bg_sound.set_volume(VOLUME)
                                win_sound.set_volume(VOLUME)
                                correct_sound.set_volume(1)
                            else:
                                pygame.mixer.pause()

                            sound_trigger = False

        if gameState == 'game_started' and mouse_clicked:
            for button in buttons:
                if button.handleClick(event):
                    if backToMainScreen.handleClick(event):
                        board = GameBoard(0, 0, 0, WINDOWSIZE, screen, FPSCLOCK)
                        first_selection = None
                        tempRowCol = (None, None)
                        gameState = 'game_not_started'
                        stats.resetTries()
                        screen.fill(BLACK)

        if gameState == 'show_info' and mouse_clicked:
            for button in buttons:
                if button.handleClick(event):
                    if backToMainScreen.handleClick(event):
                        gameState = 'game_not_started'
                        screen.fill(BLACK)

        if gameState == 'game_won' and mouse_clicked:
            for button in buttons:
                if button.handleClick(event):
                    if mainMenuButton.handleClick(event):
                        screen.fill(BLACK)
                        first_selection = None
                        tempRowCol = (None, None)
                        gameState = 'game_not_started'
                        stats.resetTries()

        if mouse_clicked and row is not None and column is not None and (row, column) != tempRowCol and not game_board[row][column].isMatched:
            game_board[row][column].changeState()
            board.revealBoxesAnimation(game_board, [(row, column)], 5)

            if first_selection is None:
                tempRowCol = (row, column)
                first_selection = (row, column)
                stats.increaseTries()
            else:
                if game_board[row][column].image is game_board[first_selection[0]][first_selection[1]].image:
                    correct_sound.play()
                    pygame.time.wait(450)
                    game_board[row][column].isMatched = True
                    game_board[first_selection[0]][first_selection[1]].isMatched = True

                if game_board[row][column].image is not game_board[first_selection[0]][first_selection[1]].image:
                    pygame.time.wait(450)
                    board.coverBoxesAnimation(game_board, [(first_selection[0], first_selection[1]), (row, column)], 5)
                    game_board[first_selection[0]][first_selection[1]].changeState()
                    game_board[row][column].changeState()

                elif board.gameWon(game_board):
                    tempRowCol = (None, None)
                    row, column = (None, None)
                    gameState = 'end_time_not_taken'

                first_selection = None

        pygame.display.update()

if __name__ == '__main__':
    main()
