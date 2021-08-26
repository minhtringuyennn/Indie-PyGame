import pygame

COLOR1 = (90, 90, 90)
COLOR2 = (120, 120, 120)

class Button:
    def __init__(self, width, height, image, x, y):
        self.width = width
        self.height = height
        self.image = image
        self.x = x
        self.y = y
        self.isHovered = False

    def show(self, surface):
        surface.blit(self.image, (self.x, self.y))
        if self.isHovered:
            self.drawHighlight(surface)

    def isButtonHovered(self, event):
        mousex, mousey = event.pos
        rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        if rectangle.collidepoint(mousex, mousey):
            self.isHovered = True
        else:
            self.isHovered = False

    def drawHighlight(self, screen):
        pygame.draw.rect(screen, COLOR1, (self.x - 3, self.y - 3, self.width + 6, self.height + 6), 1)

    def handleClick(self, event):
        mousex, mousey = event.pos
        rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        if rectangle.collidepoint(mousex, mousey):
            return True
        return False

class ActionButton(Button):
    def __init__(self, width, height, image, x, y):
        super().__init__(width, height, image, x, y)

class BoardSizeButton(Button):
    def __init__(self, width, height, cardSize, image, x, y, boardSize):
        super().__init__(width, height, image, x, y)
        self.boardSize = boardSize
        self.cardSize = cardSize
        self.isSelected = False

    def handleClick(self, event):
        mousex, mousey = event.pos
        rectangle = pygame.Rect(self.x, self.y, self.width, self.height)
        if rectangle.collidepoint(mousex, mousey):
            self.isSelected = True
            return True
        self.isSelected = False
        return False

    def show(self, surface):
        surface.blit(self.image, (self.x, self.y))
        if self.isHovered:
            self.drawHighlight(surface)
        if self.isSelected:
            self.drawHighlightSelected(surface)

    def drawHighlightSelected(self, screen):
        pygame.draw.rect(screen, COLOR2, (self.x - 3, self.y - 3, self.width + 6, self.height + 6), 2)