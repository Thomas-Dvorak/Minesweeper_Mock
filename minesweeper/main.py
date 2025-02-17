# By Thomas Dvorak

# TODO: implement a reset game
import pygame, sys, time, random, math
from square import Square
from square import flag_cover
from number_display import NumberDisplay
# import modules and initialize pygame
pygame.init()
pygame.display.init()
pygame.mixer.init() # plan to add sound
# initialize global game variables
WIDTH, HEIGHT = 600, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # set window to 600px by 600px
pygame.display.set_caption("Minesweeper") # sets title of the window
pygame.display.set_icon(flag_cover) # sets the icon to a flagged mine
FONT_SOURCE = "font/mine-sweeper/mine-sweeper.ttf" # source of the font
MAIN_GUI = pygame.image.load("imgs/top_gui.png") # the top part of the playing field's GUI, without the reactive face
FONT = pygame.font.Font(FONT_SOURCE, 30) # main font
SMALL_FONT = pygame.font.Font(FONT_SOURCE, 24) # main font that's smaller than the normal font 

def drawGridOutline(rows: int, cols: int):
    """Draws the outline of the grid, with 'rows' rows and 'cols' columns."""
    # loops though the entire grid according to rows and cols and draws a grid
    for i in range(0, rows):
        for j in range(0, cols):
            pygame.draw.rect(WIN, (100, 100, 100), (i * 25, topBarHeight + (j * 25), 25, 25), 1)

def format(num: int, length: int):
    """Length is how many places you want the string to return. For example, length = 3 with num = 9 returns 009."""
    # convert the number to a string 
    numStr = str(num)
    newStr = ""
    # add 0s to the string and then append the number
    for _ in range(0,  length - len(numStr)):
        newStr += "0"
    return newStr + numStr

def generateGrid(rows: int, cols: int, mines: int):
    """Generates a grid with 'rows' rows and 'cols' columns, filled with 'mines' mines."""
    global grid
    if len(grid) > 1:
        grid = []
    numMines = mines
    # append all the squares to the array row by row
    for i in range(0, rows):
        row = []
        for j in range(0, cols):
            row.append(Square(pygame, WIN, grid, [WIDTH, HEIGHT], rows, cols,  i, j, False))
        grid.append(row)
    # update the grid for each square
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            grid[i][j].updateGrid(grid)
    # insert mines until we have as many as needed
    while numMines >= 0:
        randomPos = [random.randint(0, rows - 1), random.randint(0, cols - 1)]
        grid[randomPos[0]][randomPos[1]].isMine = True
        numMines -= 1
    # update the grid again
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            grid[i][j].updateGrid(grid)
            
def revealSquare(target: Square, grid: list):
    """Reveals the target square. It will continue revealing squares until it reaches spaces that have a mine near it."""
    global isAlive
    # if it's already revealed or it's flagged, don't do anything
    if target.isRevealed or target.isFlagged:
        return
    target.isRevealed = True
    # reveal the square
    # it it's a mine, kill the player and do nothing more
    if target.isMine:
        isAlive = False
        return
    # reveal blank spaces (no mines) until we reach spaces with numbers on them
    # do this recursively so that it follows through for every blank space
    if target.getNeighbors(grid, True) == 0:
        for i in range(0, len(target.getNeighbors(grid, False))):
            revealSquare(target.getNeighbors(grid, False)[i], grid)

def convertMouseToSquarePos():
    # the squares are 25x25
    """Each square goes by a row and column position. It converts the mouse's position (x, y) and converts it to the row and column position."""
    coors = [pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]]
    return [math.floor(coors[0] / 25), math.floor(coors[1] / 25) - 2]

def getMaxGridPos():
    # because of the dimensions, we can figure out the largest position of the playing field 
    global rows, cols
    return ((rows * 25) + 25,  (cols * 25) + 25)

def getMinGridPos():
    return (0, 50)

def checkGameWin():
    # checks to see if just all the mines remain not dug
    global state, grid
    for i in range(0, len(grid)):
        for j in range(0, len(grid[i])):
            square = grid[i][j]
            if not square.isMine and not square.isRevealed:
                return
    state = 'win'

# game variables
topBarHeight = 50 # height of the bar containing the information
rows = 0 # rows of the field
cols = 0 # columns of the field
mines =  0 # about 1/6 of the 25x27 grid (113)
flags = mines # there are as many flags as mines
state = 'main'
isMining = True # to see if a player is placing flags or revealing squares
isAlive = True # if not, game over
isFirstReveal = True
grid = [] # where the field is contained
startTime = 0 # for the timer
timeDifference = 0 # for the timer
clicks = 0 # counts clicks
timeDisplay = NumberDisplay(WIN, format(timeDifference, 3), (35, 13)) # for tracking the time
mineDisplay = NumberDisplay(WIN, format(mines, 3), (509, 13)) # for tracking how many mines are left

# main menu variables
MAIN_MENU_BUTTON_COLOR = (142, 107, 55) # default color for the main menu buttons
MAIN_MENU_BUTTON_HOVER_COLOR = (168, 121, 51) # default hover color for the main menu buttons
menuButtons = [pygame.Rect((180, 150), (250, 50)), pygame.Rect((180, 220), (250, 50)), pygame.Rect((180, 290), (250, 50)), pygame.Rect((180, 360), (250, 50))] # the menu buttons
menuText = [SMALL_FONT.render('Easy', False, (255, 255, 255)), SMALL_FONT.render('Medium', False, (255, 255, 255)), SMALL_FONT.render('Hard', False, (255, 255, 255)), SMALL_FONT.render('Expert', False, (255, 255, 255))] # the text for the menu buttons
menuTextPos = [(270, menuButtons[0].y + 8), (245, menuButtons[1].y + 8), (270, menuButtons[2].y + 8), (255, menuButtons[3].y + 8)] # positions for the buttons and texts

def main():
    global state, isAlive, rows, cols, mines, grid, startTime, mines, isMining, flags, timeDifference, menuButtons, menuText, menuTextPos, clicks, timeDisplay, mineDisplay, isFirstReveal
    # run main loop
    run = True
    clock = pygame.time.Clock()
    while run:
        # tick for 60fps
        # fill with default color if no image is available or rendered 
        clock.tick(60)
        WIN.fill((217, 217, 217))
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                run = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and state == 'main':
                # set default amounts and check to see if they are clicked 
                for i in range(0, len(menuButtons)):
                    if menuButtons[i].collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        if i == 0:
                            rows, cols, mines, flags = 6, 6, 6, 6
                        if i == 1:
                            rows, cols, mines, flags = 12, 12, 24, 24
                        if i == 2:
                            rows, cols, mines, flags = 18, 18, 54, 54
                        if i == 3:
                            rows, cols, mines, flags = 25, 22, 113, 113
                        state = 'play'
                        generateGrid(rows, cols, mines)
                        startTime = time.time()
                        break
            if (state == 'play' and event.type == pygame.MOUSEBUTTONDOWN) and (pygame.mouse.get_pos() < getMaxGridPos() and pygame.mouse.get_pos()[1] > getMinGridPos()[1]):
                # reveal the square if the player is mining
                square = grid[convertMouseToSquarePos()[0]][convertMouseToSquarePos()[1]]
                if pygame.mouse.get_pressed()[0]:
                # logic here for both mine clicking and generation on first click 
                    if isFirstReveal:
                        iterations = 0
                        while (square.isMine or square.getNeighbors(grid, True) != 0) and iterations < 100:
                            iterations += 1
                            # generate a new random square position
                            generateGrid(rows, cols, flags)
                            square = grid[convertMouseToSquarePos()[0]][convertMouseToSquarePos()[1]]
                        # change it to false so that it doesn't happen again
                        isFirstReveal = False
                    else:
                        # player hit a mine
                        if not square.isFlagged:
                            revealSquare(square, grid)
                            if square.isMine:
                                isAlive = False
                if pygame.mouse.get_pressed()[2] and isAlive:
                    # flag the square if there are enough left
                    if square.isFlagged:
                        flags += 1
                    else:
                        if flags > 0:
                            flags -= 1
                    square.isFlagged = not square.isFlagged
        if state == 'main':
            # render the title, difficulty selection
            title = FONT.render("Minesweeper", True, (150, 150, 150))
            WIN.blit(title, (170, 90))
            for i in range(0, len(menuButtons)):
                if menuButtons[i].collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                    pygame.draw.rect(WIN, MAIN_MENU_BUTTON_HOVER_COLOR, menuButtons[i])
                else:
                    pygame.draw.rect(WIN, MAIN_MENU_BUTTON_COLOR, menuButtons[i])
            for i in range(0, len(menuText)):
                WIN.blit(menuText[i], menuTextPos[i])
        elif state == 'play':
            # change to game over first if the player is dead
            WIN.blit(MAIN_GUI, (0, 0))
            if isAlive == False:
                state = 'game over'
                # this reveals the squares, and checks whether there were wrong guesses
                for i in range(0, len(grid)):
                    for j in range(0, len(grid[i])):
                        if not grid[i][j].isMine and grid[i][j].isFlagged:
                            grid[i][j].wasWrongGuess = True
                            grid[i][j].isRevealed = True
                        elif grid[i][j].isMine:
                            grid[i][j].isRevealed = True
                        grid[i][j].updateGrid(grid)
            # get time differences, format them, and draw them to the screen
            currentTime = time.time()
            timeDifference = int(currentTime - startTime)
            timeDisplay.update(format(timeDifference, 3))
            mineDisplay.update(format(flags, 3))
            timeDisplay.draw()
            mineDisplay.draw()
            # draw the grid
            for i in range(0, len(grid)):
                for j in range(0, len(grid[i])):
                    grid[i][j].updateGrid(grid)
                    grid[i][j].draw(isAlive)
            drawGridOutline(rows, cols)
            # draw outline for when the squares are mined
            # check to see if the player has won
            checkGameWin()
        elif state == 'game over':
            # game over display
            WIN.blit(MAIN_GUI, (0, 0))
            timeDisplay.update(format(timeDifference, 3))
            mineDisplay.update(format(flags, 3))
            timeDisplay.draw()
            mineDisplay.draw()
            for i in range(0, len(grid)):
                for j in range(0, len(grid[i])):
                    grid[i][j].draw(isAlive)
            drawGridOutline(rows, cols)
        elif state == 'win':
            # win screen display with a start new game feature
            pass
        else:
            # if there is an invalid game state, then we stop running the application and print an error 
            print(f'Error: Invalid game state: {state}')
            run = False
            sys.exit()
        # update the actual display
        pygame.display.update()
    # quit if the main loop is killed
    pygame.quit()

if __name__ == '__main__':
    # only run if this is called main
    main()