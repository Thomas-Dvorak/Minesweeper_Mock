import pygame

# source images for the time display
negate = pygame.image.load("imgs/nums/negative.png")
empty = pygame.image.load("imgs/nums/empty.png")
# numbers are an array for easy access, i.e. numbers[0] is 0, numbers[1] is 1 and so on...
numbers = [
    pygame.transform.scale(pygame.image.load("imgs/nums/0.png"), (13, 24)),
    pygame.transform.scale(pygame.image.load("imgs/nums/1.png"), (13, 24)),
    pygame.transform.scale(pygame.image.load("imgs/nums/2.png"), (13, 24)),
    pygame.transform.scale(pygame.image.load("imgs/nums/3.png"), (13, 24)),
    pygame.transform.scale(pygame.image.load("imgs/nums/4.png"), (13, 24)),
    pygame.transform.scale(pygame.image.load("imgs/nums/5.png"), (13, 24)),
    pygame.transform.scale(pygame.image.load("imgs/nums/6.png"), (13, 24)),
    pygame.transform.scale(pygame.image.load("imgs/nums/7.png"), (13, 24)),
    pygame.transform.scale(pygame.image.load("imgs/nums/8.png"), (13, 24)),
    pygame.transform.scale(pygame.image.load("imgs/nums/9.png"), (13, 24)),
]

class NumberDisplay():
    def __init__(self, window, num: str, coordinates: tuple[int, int]):
        # need how long the display will be in digits
        # store the formatted number
        # window for displaying
        # coordinates for placement -> coordinate is the top-left
        self.display_count = len(num)
        self.num = num
        self.window = window
        self.coords = coordinates

    def draw(self):
        # draw them in rapid succession
        # 13 is there because that's how wide the image is by default
        for i in range(0, self.display_count):
            self.window.blit(numbers[int(self.num[i])], (self.coords[0] + (13 * i), self.coords[1]))

    def update(self, num: str):
        # just change the number, it makes more sense to do it this way
        self.num = num

    