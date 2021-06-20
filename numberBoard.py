import pygame
import random
from os import environ
from sys import platform as _sys_platform


def platform():
    if 'ANDROID_ARGUMENT' in environ:
        return "android"
    elif _sys_platform in ('linux', 'linux2', 'linux3'):
        return "linux"
    elif _sys_platform in ('win32', 'cygwin'):
        return 'win'


pygame.init()
clock = pygame.time.Clock()

WIN = pygame.display.set_mode((411, 890))  # ! REMEBER TO ADD FULL SCREEN
pygame.display.set_caption('board Game')
FPS = 20

WHITE = (215, 215, 215)  # board colour
GREAY = (70, 70, 70)  # text colour
BLACK = (0, 0, 0)  # line colour
BLUE = (10, 40, 100)  # checks colour
GREEN = (30, 220, 70)
TURTLEGREEN = (80, 200, 90)
VIOLET = (150, 50, 220)
ORANGE = (220, 120, 50)
PINK = (250, 160, 160)
CYAN = (30, 210, 180)
YELLOW = (255, 235, 0)
AMBER = (220, 0, 50)
TRANSPARENT = (0, 0, 0, 0)

windowClr = GREAY
tappedClr = GREEN
checksClr = BLUE
boardClr = WHITE
txtClr = GREAY
colourChoices = [GREAY, TURTLEGREEN, VIOLET, ORANGE,
                 PINK, CYAN, YELLOW, AMBER]  # list of colours for checks

translationFactor = 200


def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = (0, 0, 0)):
    return (pygame.font.Font(font, fontSize)).render(str(txt), True, fontColour)


class Grid():
    def __init__(self, cols: int = 4, rows: int = 4, width: int = 400, height: int = 400):
        self.rows = cols
        self.cols = rows
        self.numbers = {}
        self.positions = {}
        self.cubes = None
        self.width = width
        self.height = height
        self.toFind = None
        self.gameWon = False
        self.createBoard()

    def createBoard(self):
        start = 1
        self.numbers = {}
        self.positions = {}
        while(start < self.rows*self.cols + 1):
            col = random.randint(0, 9)
            row = random.randint(0, 9)
            key = (row, col)
            if not (key in self.numbers):
                self.numbers[key] = start
                self.positions[start] = key
                start += 1
        self.cubes = [
            [Cube(self.numbers[(i, j)], i, j, self.width, self.height, self.cols, self.rows)
             for j in range(self.cols)]
            for i in range(self.rows)
        ]
        self.toFind = random.randint(1, 100)
        self.gameWon = False

    def draw(self, win=None):
        if win == None:
            win = WIN
        win.fill(windowClr)
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

        thick = 1
        # pygame.draw.line(win, (0, 0, 0), (i * rowGap, 0),i * rowGap, self.height), thick)
        for i in range(self.rows+1):
            pygame.draw.line(win, BLACK, (0, translationFactor + i*rowGap),
                             (self.height, translationFactor + rowGap*i), thick)
        for i in range(self.cols+1):
            pygame.draw.line(
                win, BLACK, (i*colGap, 0 + translationFactor), (colGap*i, self.width + translationFactor))
        pygame.display.update()

    def reset(self):
        self.createBoard()
        self.draw()

    def clicked(self, pos: tuple) -> None:
        x, y = pos

        if x >= self.rows or y >= self.cols or x < 0:
            return -1
        if self.cubes[x][y].value == self.toFind:
            # TODO won function
            self.gameWon = True
            self.reset()
            return 0
        self.cubes[x][y].tapped = True
        self.cubes[x][y].show = True
        ClrChoice = random.choice(colourChoices)
        # ClrChoice = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.cubes[x][y].tappedClr = ClrChoice
        self.cubes[x][y].blink = True
        case = random.randint(0, 1)
        if case:
            x, y = self.positions[abs(self.cubes[x][y].value - self.toFind)]
        else:
            a, b = self.positions[self.toFind]
            x, y = self.positions[abs(x-a)+abs(y-b)]
        self.cubes[x][y].tapped = True
        self.cubes[x][y].show = True
        self.cubes[x][y].tappedClr = ClrChoice
        self.cubes[x][y].blink = True
        self.draw()


class Cube():
    def __init__(self, value, row, col, width, height, cols, rows):
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.value = value
        self.centerFactor = 10
        self.show = random.randint(0, 1)
        self.tapped = False
        self.tappedClr = tappedClr
        self.blink = False

    def draw(self, win):
        # fnt = pygame.font.SysFont("comicsans", 40)
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap + translationFactor
        if self.col % 2 == 0 and self.row % 2 == 0:
            pygame.draw.rect(win, checksClr, pygame.Rect(x, y, colGap, rowGap))
        elif self.col % 2 == 1 and self.row % 2 == 1:
            pygame.draw.rect(win, checksClr, pygame.Rect(x, y, colGap, rowGap))
        else:
            pygame.draw.rect(win, WHITE, pygame.Rect(x, y, colGap, rowGap))
        if self.tapped:
            pygame.draw.rect(win, self.tappedClr,
                             pygame.Rect(x, y, colGap, rowGap))

        if self.show:
            text = PYtxt(self.value, 22)
            win.blit(text, (x + (colGap/2 - text.get_width()/2),
                            y + (rowGap/2 - text.get_height()/2)))
        if self.blink == True:
            pass
            # pygame.display.flip()
            # pygame.draw.rect(win, WHITE,
            #                  pygame.Rect(x, y, colGap, rowGap))
            # pygame.display.flip()
            # pygame.draw.rect(win, self.tappedClr,
            #                  pygame.Rect(x, y, colGap, rowGap))
            # pygame.display.flip()
            # pygame.draw.rect(win, WHITE,
            #                  pygame.Rect(x, y, colGap, rowGap))
            # pygame.display.flip()
            # pygame.draw.rect(win, self.tappedClr,
            #                  pygame.Rect(x, y, colGap, rowGap))
            # pygame.display.flip()
            self.blink = False
# WIN.blit(PYtxt('Solved'), (20, 560) -> position)
# pygame.display.update()
# win.blit(text, (x + (colGap/2 - text.get_width()/2),
#                 y + (rowGap/2 - text.get_height()/2)))


board = Grid(10, 10, WIN.get_width(), WIN.get_width())
board.draw(WIN)


moves = 0
run = True
while run:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            y -= translationFactor
            board.clicked((y//((WIN.get_width())//board.cols),
                          x//(WIN.get_width()//board.rows)))
            moves += 1
            WIN.blit(PYtxt(f'moves : {moves}', fontColour=WHITE),
                     (5, board.height+translationFactor+30))
            if board.gameWon:
                moves = 0
            pygame.display.update()
pygame.quit()
