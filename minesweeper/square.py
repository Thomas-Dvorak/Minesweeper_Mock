import pygame

# source images for the mines and revealed squares
cover_mine = pygame.image.load("imgs/mine_cover.png")
flag_cover = pygame.image.load("imgs/flag_cover.png")
flag_wrong = pygame.image.load("imgs/wrong_mine.png")
mine = pygame.image.load("imgs/mine.png")
mine_number = [
    pygame.image.load("imgs/1_mine.png"),
    pygame.image.load("imgs/2_mine.png"),
    pygame.image.load("imgs/3_mine.png"),
    pygame.image.load("imgs/4_mine.png"),
    pygame.image.load("imgs/5_mine.png"),
    pygame.image.load("imgs/6_mine.png"),
    pygame.image.load("imgs/7_mine.png"),
    pygame.image.load("imgs/8_mine.png"),
]
# for the number of mines around the square (1, 2, 3, 4, 5, 6, 7, 8), use i - 1 for iteration

class Square(pygame.sprite.Sprite):
    def __init__(self, pygame, window, grid, size: list[int], rows: int, cols: int, rowPos: int, colPos: int, isMine: bool):
        self.window = window
        self.pygame = pygame
        self.grid = grid
        self.size = size
        self.rows = rows - 1 
        self.cols = cols - 1
        self.row = rowPos
        self.col = colPos
        self.isMine = isMine
        self.isRevealed = False
        self.isFlagged = False
        self.wasWrongGuess = False
        self.rect = self.pygame.rect.Rect(self.getXYCoordinates(), (25, 25))
    
    def draw(self, isAlive: bool):
        # counts for hover effects
        # TODO: Re-write this draw method to work with images. 
        if not self.isRevealed: 
            if not self.isFlagged:
                # if it is not revealed and not flagged, then display the cover
                self.window.blit(cover_mine, self.getXYCoordinates())
            else: 
                # else it will draw the flag
                self.window.blit(flag_cover, self.getXYCoordinates())
        else:
            if self.isMine and self.isFlagged:
                self.window.blit(flag_cover, self.getXYCoordinates())
            if self.isMine:   
                self.window.blit(mine, self.getXYCoordinates())
            elif self.getNeighbors(self.grid, True) == 0:
                self.pygame.draw.rect(self.window, (160, 160, 160), self.pygame.rect.Rect(self.getXYCoordinates(), (25, 25)))
            elif self.wasWrongGuess or (not self.isMine and self.isFlagged):
                self.window.blit(flag_wrong, self.getXYCoordinates())
            else:
                self.window.blit(mine_number[self.getNeighbors(self.grid, True) - 1], self.getXYCoordinates())


    def getXYCoordinates(self):
        """Returns an (x, y) tuple[int, int] of the coordinates of the top left corner of the square."""
        return (self.row * 25, 50 + (self.col * 25))
    
    def updateGrid(self, grid: list):
        """Updates the grid according to the square."""
        self.grid = grid
    
    def getNeighbors(self, grid: list, countMines = False):
        """Counts the mines surrounding the square. Covers edge and corner cases. TODO: It counts squares on the other side. Fix that."""
        # * seems to roll over into the other side
        # * when one's on the right edge
        # * it'll count ones on the left side as well
        # covers ALL cases
        surroundingSquares = []
        if self.col == 0 and self.row == 0:
            surroundingSquares = [
                grid[self.row][self.col + 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col + 1]
            ]
        elif self.col == self.cols and self.row == 0:
            surroundingSquares = [
                grid[self.row][self.col - 1],
                grid[self.row + 1][self.col - 1],
                grid[self.row + 1][self.col]
            ]
        elif self.col == 0 and self.row == self.rows:
            surroundingSquares = [
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col + 1],
                grid[self.row][self.col + 1]
            ]
        elif self.col == self.cols and self.row == self.rows:
            surroundingSquares = [
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col - 1],
                grid[self.row][self.col - 1]
            ]
        elif self.col == 0: 
            surroundingSquares = [
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col + 1],
                grid[self.row][self.col + 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col + 1]
            ]
        elif self.col == self.cols:
            surroundingSquares = [
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col - 1],
                grid[self.row][self.col - 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col - 1]
            ]
        elif self.row == 0:
            surroundingSquares = [
                grid[self.row][self.col - 1],
                grid[self.row][self.col + 1],
                grid[self.row + 1][self.col - 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col + 1]
            ]
        elif self.row == self.rows:
            surroundingSquares = [
                grid[self.row][self.col - 1],
                grid[self.row][self.col + 1],
                grid[self.row - 1][self.col - 1],
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col + 1]
            ]
        else:
            surroundingSquares = [
                grid[self.row - 1][self.col - 1],  
                grid[self.row - 1][self.col],
                grid[self.row - 1][self.col + 1],
                grid[self.row][self.col - 1],
                grid[self.row][self.col + 1],
                grid[self.row + 1][self.col - 1],
                grid[self.row + 1][self.col],
                grid[self.row + 1][self.col + 1]
            ]
        if countMines:
            total = 0
            for i in range(0, len(surroundingSquares)):
                if surroundingSquares[i].isMine:
                    total += 1
            return total
        else:
            return surroundingSquares