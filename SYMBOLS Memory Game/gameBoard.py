import random
import pygame

SPEED = 3
COLOR0 = (250, 250, 250)
COLOR1 = (230, 230, 230)
COLOR2 = (100, 100, 100)
COLOR3 = (120, 120, 120)

class Card:
    def __init__(self, size, image, x, y):
        self.size = size
        self.image = image
        self.x = x
        self.y = y
        self.uncovered = False
        self.isHovered = False
        self.isMatched = False

    def changeState(self):
        if self.uncovered:
            self.uncovered = False
        elif not self.uncovered:
            self.uncovered = True

    def drawCard(self, surface, drawAnyway):
        if self.uncovered or drawAnyway:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, COLOR1, (self.x, self.y, self.size, self.size))
            if self.isHovered:
                self.drawHighliht(surface)

    def drawHighliht(self, surface):
        pygame.draw.rect(surface, COLOR3, (self.x - 3, self.y - 3, self.size + 6, self.size + 6), 2)

    def isCardHovered(self, event):
        mousex, mousey = event.pos
        rectangle = pygame.Rect(self.x, self.y, self.size, self.size)
        if rectangle.collidepoint(mousex, mousey):
            self.isHovered = True
        else:
            self.isHovered = False

class GameBoard:
    def __init__(self, width, height, cardSize, windowsize, screen, clock):
        self.width = width
        self.height = height
        self.imageL = ImageLibrary(cardSize)
        self.images = self.imageL.images
        self.windowsize = windowsize
        self.screen = screen
        self.card_size = cardSize
        self.gap_size = 5
        self.marginx = int((self.windowsize - (self.width * (self.card_size + self.gap_size))) / 2)
        self.marginy = int(((self.windowsize - (self.height * (self.card_size + self.gap_size))) / 2) + 50)
        self.BLACK = COLOR0
        self.clock = clock

    def createRandomizedBoard(self):
        images = self.images
        random.shuffle(images)
        numOfImages = int(self.width * self.height / 2)
        images = images[:numOfImages] * 2
        random.shuffle(images)

        game_board = []
        card_x_pos = self.marginx
        card_y_pos = self.marginy
        for i in range(self.width):
            line_of_cards = []
            for j in range(self.height):
                line_of_cards.append(Card(self.card_size, images.pop(), card_x_pos, card_y_pos))
                card_y_pos += self.card_size + self.gap_size
            game_board.append(line_of_cards)
            card_x_pos += self.card_size + self.gap_size
            card_y_pos = self.marginy
        return game_board

    def drawBoard(self, game_board):
        for i in range(self.width):
            for j in range(self.height):
                if game_board[i][j].isMatched == False:
                    game_board[i][j].drawCard(self.screen, False)

    def LeftTopCoordsOfBox(self, row, column):
        left = row * (self.card_size + self.gap_size) + self.marginx
        top = column * (self.card_size + self.gap_size) + self.marginy
        return (left, top)

    def getBoxAtPixel(self, x, y):
        for i in range(self.width):
            for j in range(self.height):
                left, top = self.LeftTopCoordsOfBox(i, j)
                rectangle = pygame.Rect(left, top, self.card_size, self.card_size)
                if rectangle.collidepoint(x, y):
                    return (i, j)
        return (None, None)

    def drawBoxCovers(self, board, boxes, coverage, show):
        for box in boxes:
            left, top = self.LeftTopCoordsOfBox(box[0], box[1])
            pygame.draw.rect(self.screen, self.BLACK, (left, top, self.card_size, self.card_size))
            board[box[0]][box[1]].drawCard(self.screen, show)

            if coverage > 0:
                pygame.draw.rect(self.screen, self.BLACK, (left, top, coverage, self.card_size))
        pygame.display.update()
        self.clock.tick(90)

    def revealBoxesAnimation(self, board, boxesToReveal, speed):
        for coverage in range(self.card_size, (-speed) - 1, - speed):
            self.drawBoxCovers(board, boxesToReveal, coverage, True)

    def coverBoxesAnimation(self, board, boxesToReveal, speed):
        for coverage in range(0, self.card_size + speed, speed):
            self.drawBoxCovers(board, boxesToReveal, coverage, True)

    def drawHighlight(self, row, column, screen):
        left, top = self.LeftTopCoordsOfBox(row, column)
        pygame.draw.rect(screen, COLOR1, (left - 3, top - 3, self.card_size + 6, self.card_size + 6), 2)

    def startGameAnimation(self, board, width, height):
        coveredBoxes = []
        for i in range(width):
            coveredBoxes.append([False] * height)

        boxes = []
        for x in range(width):
            for y in range(height):
                boxes.append((x, y))
        random.shuffle(boxes)

        if width == 4 and height == 4:
            boxGroups = self.splitIntoGroupsOf(2, boxes)
        elif width == 6 and height == 4:
            boxGroups = self.splitIntoGroupsOf(3, boxes)
        elif width == 6 and height == 5:
            boxGroups = self.splitIntoGroupsOf(5, boxes)
        else:
            boxGroups = self.splitIntoGroupsOf(6, boxes)

        self.drawBoard(board)
        for boxGroup in boxGroups:
            self.revealBoxesAnimation(board, boxGroup, SPEED)
            self.coverBoxesAnimation(board, boxGroup, SPEED)

    def splitIntoGroupsOf(self, groupSize, theList):
        result = []
        for i in range(0, len(theList), groupSize):
            result.append(theList[i:i + groupSize])
        return result

    def gameWon(self, cards):
        for line in cards:
            for card in line:
                if card.isMatched is False:
                    return False
        return True

class GameStats:
    def __init__(self, screen):
        self.tries = 0
        self.screen = screen

    def increaseTries(self):
        self.tries += 1

    def resetTries(self):
        self.tries = 0

    def displayNumberOfTries(self):
        font = pygame.font.Font('Resources/Norse-KaWl.otf', 30)
        textString = 'Tries: ' + str(self.tries)
        numOfTriesText = font.render(textString, True, COLOR2, COLOR0)
        textRect_tries = numOfTriesText.get_rect()
        textRect_tries.center = (325, 40)
        self.screen.blit(numOfTriesText, textRect_tries)

    def displayTime(self, startTime):
        elapsedMillis = pygame.time.get_ticks() - startTime
        elapsedTime = convertMillisecondsToMinAndSec(elapsedMillis)
        font = pygame.font.Font('Resources/Norse-KaWl.otf', 30)
        textString = 'Time: ' + str(elapsedTime[0]) + ":" + str(elapsedTime[1])
        elapsedTimeText = font.render(textString, True, COLOR2, COLOR0)
        textRect_time = elapsedTimeText.get_rect()
        textRect_time.center = (580, 40)
        self.screen.blit(elapsedTimeText, textRect_time)

    def displayGameWonText(self, endTime):
        endTimeMS = convertMillisecondsToMinAndSec(endTime)
        font = pygame.font.Font('Resources/Norse-KaWl.otf', 60)
        font2 = pygame.font.Font('Resources/Norse-KaWl.otf', 25)
        youWonText = 'You Won!'
        wonText = font.render(youWonText, True, COLOR2, COLOR0)
        textRect_won = wonText.get_rect()
        textRect_won.center = (325, 200)
        statText = 'You completed the game with ' + str(self.tries) + ' tries in ' + str(endTimeMS[0]) + ' min and ' \
                   + str(endTimeMS[1]) + ' s!'
        sText = font2.render(statText, True, COLOR2, COLOR0)
        textRectStat = sText.get_rect()
        textRectStat.center = (325, 260)
        self.screen.blit(wonText, textRect_won)
        self.screen.blit(sText, textRectStat)

def convertMillisecondsToMinAndSec(milliseconds):
    millis = int(milliseconds)
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    return (minutes, seconds)

class ImageLibrary:
    def __init__(self, imagesize):
        approx = pygame.image.load('Assets/Symbols/approx.jpg')
        approx = pygame.transform.scale(approx, (imagesize, imagesize))

        because = pygame.image.load('Assets/Symbols/because.jpg')
        because = pygame.transform.scale(because, (imagesize, imagesize))

        congruent = pygame.image.load('Assets/Symbols/congruent.jpg')
        congruent = pygame.transform.scale(congruent, (imagesize, imagesize))

        denial = pygame.image.load('Assets/Symbols/denial.jpg')
        denial = pygame.transform.scale(denial, (imagesize, imagesize))

        diff = pygame.image.load('Assets/Symbols/diff.jpg')
        diff = pygame.transform.scale(diff, (imagesize, imagesize))

        empty = pygame.image.load('Assets/Symbols/empty.jpg')
        empty = pygame.transform.scale(empty, (imagesize, imagesize))

        equal = pygame.image.load('Assets/Symbols/equal.jpg')
        equal = pygame.transform.scale(equal, (imagesize, imagesize))

        exists = pygame.image.load('Assets/Symbols/exists.jpg')
        exists = pygame.transform.scale(exists, (imagesize, imagesize))

        function = pygame.image.load('Assets/Symbols/function.jpg')
        function = pygame.transform.scale(function, (imagesize, imagesize))

        identical = pygame.image.load('Assets/Symbols/identical.jpg')
        identical = pygame.transform.scale(identical, (imagesize, imagesize))

        inf = pygame.image.load('Assets/Symbols/inf.jpg')
        inf = pygame.transform.scale(inf, (imagesize, imagesize))

        intergal = pygame.image.load('Assets/Symbols/intergal.jpg')
        intergal = pygame.transform.scale(intergal, (imagesize, imagesize))

        isnot = pygame.image.load('Assets/Symbols/isnot.jpg')
        isnot = pygame.transform.scale(isnot, (imagesize, imagesize))

        issubset = pygame.image.load('Assets/Symbols/issubset.jpg')
        issubset = pygame.transform.scale(issubset, (imagesize, imagesize))

        notconcur = pygame.image.load('Assets/Symbols/notconcur.jpg')
        notconcur = pygame.transform.scale(notconcur, (imagesize, imagesize))

        notidentical = pygame.image.load('Assets/Symbols/notidentical.jpg')
        notidentical = pygame.transform.scale(notidentical, (imagesize, imagesize))

        notsubset = pygame.image.load('Assets/Symbols/notsubset.jpg')
        notsubset = pygame.transform.scale(notsubset, (imagesize, imagesize))

        notsubset2 = pygame.image.load('Assets/Symbols/notsubset2.jpg')
        notsubset2 = pygame.transform.scale(notsubset2, (imagesize, imagesize))

        parallel = pygame.image.load('Assets/Symbols/parallel.jpg')
        parallel = pygame.transform.scale(parallel, (imagesize, imagesize))

        pi = pygame.image.load('Assets/Symbols/pi.jpg')
        pi = pygame.transform.scale(pi, (imagesize, imagesize))

        sets = pygame.image.load('Assets/Symbols/sets.jpg')
        sets = pygame.transform.scale(sets, (imagesize, imagesize))

        similar = pygame.image.load('Assets/Symbols/similar.jpg')
        similar = pygame.transform.scale(similar, (imagesize, imagesize))

        subset = pygame.image.load('Assets/Symbols/subset.jpg')
        subset = pygame.transform.scale(subset, (imagesize, imagesize))

        therefore = pygame.image.load('Assets/Symbols/therefore.jpg')
        therefore = pygame.transform.scale(therefore, (imagesize, imagesize))

        self.images = [approx, because, congruent, denial, diff, empty, equal, exists, function, identical, inf, intergal, isnot, issubset,
                       notconcur, notidentical, notsubset, notsubset2, parallel, pi, sets, similar, subset, therefore]