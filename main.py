import pygame
import sys
import numpy as np

pygame.init()

# Define dimensions of the screen and frame rate as contstants
gridlength = 50
squarelength = 10
fps = 20

clock = pygame.time.Clock()
screen = pygame.display.set_mode((gridlength * squarelength, gridlength * squarelength))

class SnakeBody:
    def __init__(self, coordinates, direction, trailing):
        self.coordinates = coordinates # Coordinates of the snake body cell as an np.array
        self.direction = direction # Direction of the snake as an np.array representing a vector
        self.trailing = trailing # The next cell on the snake

    def move(self, direction):
        self.coordinates += direction # Move the snake one cell in the given direction
        self.trailing.move(self.direction) # Moves the next cells too recursively
        self.direction = direction # Updates the direction
        
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.coordinates[0] * squarelength, self.coordinates[1] * squarelength, squarelength, squarelength))
        self.trailing.draw(screen) # Draws the next cells recursively

    # This returns all the coordinates of the whole snake when called from the head using recursion to check for collisions
    def get_coordinates(self):
        return [self.coordinates.tolist()] + self.trailing.get_coordinates()

class SnakeHead(SnakeBody):
    def __init__(self):
        coordinates = np.array([gridlength // 2, gridlength // 2]) # The head starts in the middle of the grid
        direction = np.array([1, 0]) # The head starts moving right
        start_trailing = SnakeTail(coordinates - direction, direction) # The tail starts behind the head
        super().__init__(coordinates, direction, start_trailing)

    def move(self, direction, food):
        self.coordinates += direction
        # The head checks if the snake is dead when it moves
        if snake.check_dead():
            print ("Game Over")
            score = len(snake.get_coordinates()) - 2 # The score is the length of the snake minus 2 because the head and tail exist at the start
            print (f'Score: {score}')
            sys.exit()
        # The head checks if the snake has eaten the food when it moves
        elif self.coordinates.tolist() == food.coordinates.tolist():
            self.trailing = SnakeBody(self.coordinates - direction, self.direction, self.trailing) # This adds a new cell to the snake behind the head
            food.create() # This moves the food to a new location
        else:
            self.trailing.move(self.direction)

        self.direction = direction
        return food

    # This draws the cell with a dark green color so we know which side the head is
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 150, 0), (self.coordinates[0] * squarelength, self.coordinates[1] * squarelength, squarelength, squarelength))
        self.trailing.draw(screen)

    def check_dead(self):
        # Checks if the head is outside the grid
        x_off_screen = self.coordinates[0] // gridlength
        y_off_screen = self.coordinates[1] // gridlength
        # Check if the head is in the body of the snake
        collision = self.coordinates.tolist() in self.get_coordinates()[1:]
        if x_off_screen != 0 or y_off_screen != 0 or collision: return True

# This is like SnakeBody but it is the tail so it ends the recursion        
class SnakeTail(SnakeBody):
    def __init__(self, coordinates, direction):
        super().__init__(coordinates, direction, None)

    def move(self, direction):
        self.coordinates += direction
        self.direction = direction

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), (self.coordinates[0] * squarelength, self.coordinates[1] * squarelength, squarelength, squarelength))


    def get_coordinates(self):
        return [self.coordinates.tolist()]

class Food:
    def __init__(self):
        self.create()

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.coordinates[0] * squarelength, self.coordinates[1] * squarelength, squarelength, squarelength))
    
    # Moves the food to a new random location
    def create(self):
        self.coordinates = np.array([np.random.randint(0, gridlength), np.random.randint(0, gridlength)])

snake = SnakeHead()
food = Food()

while True:
    for event in pygame.event.get(): # This checks if the user has quit the game
        if event.type == pygame.QUIT:
            sys.exit()

    # Check if the user has pressed a key to move the snake
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        food = snake.move(np.array([0, -1]), food)
    elif key[pygame.K_DOWN]:
        food = snake.move(np.array([0, 1]), food)
    elif key[pygame.K_LEFT]:
        food = snake.move(np.array([-1, 0]), food)
    elif key[pygame.K_RIGHT]:
        food = snake.move(np.array([1, 0]), food)
    else:
        food = snake.move(snake.direction, food) # if the user doesn't move the snake, it continues in the same direction
    
    screen.fill((0, 0, 0))
    food.draw(screen)
    snake.draw(screen)
    
    pygame.display.update()
    clock.tick(fps)

