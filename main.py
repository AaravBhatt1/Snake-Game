import pygame
import sys
import numpy as np

pygame.init()

# Define dimensions of the screen and frame rate as contstants
gridlength = 20
squarelength = 20
fps = 10

clock = pygame.time.Clock()
screen = pygame.display.set_mode(
    (gridlength * squarelength, gridlength * squarelength))
pygame.display.set_caption('Snake')

up = np.array([0, -1])
down = np.array([0, 1])
left = np.array([-1, 0])
right = np.array([1, 0])


class SnakeCell:
    def __init__(self, coordinates, head):
        self.coordinates = coordinates  # Coordinates of the snake body cell as an np.array
        self.head = head  # a boolean whether this cell is the head of the snake

    def draw(self, screen):
        if self.head:
            # the head of the snake is darker so we know which way the snake is facing
            color = (0, 100, 0)
        else:
            color = (0, 255, 0)
        pygame.draw.rect(screen, color, (self.coordinates[0] * squarelength,
                         self.coordinates[1] * squarelength, squarelength, squarelength))


class Food:

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (
            self.coordinates[0] * squarelength, self.coordinates[1] * squarelength, squarelength, squarelength))

    # Moves the food to a new random location
    def create(self, snake_coordinates):
        self.coordinates = np.array(
            [np.random.randint(0, gridlength), np.random.randint(0, gridlength)])
        if self.coordinates.tolist() in snake_coordinates:
            self.create(snake_coordinates)


# The snake is initially a single cell
snake = [SnakeCell(np.array([gridlength // 2, gridlength // 2]), True)]
food = Food()
food.create(map(lambda cell: cell.coordinates.tolist(), snake))
direction = right  # The snake initially faces right

while True:
    for event in pygame.event.get():  # This checks if the user has quit the game
        if event.type == pygame.QUIT:
            sys.exit()

    # Check if the user has pressed a key to move the snake
    key = pygame.key.get_pressed()
    if key[pygame.K_UP]:
        direction = up
    elif key[pygame.K_DOWN]:
        direction = down
    elif key[pygame.K_LEFT]:
        direction = left
    elif key[pygame.K_RIGHT]:
        direction = right

    # Check if the snake has hit the wall or itself
    head_coordinates = snake[0].coordinates + direction
    if ((head_coordinates // gridlength).tolist() != [0, 0]) or (head_coordinates.tolist() in map(lambda cell: cell.coordinates.tolist(), snake)):
        print('Score:', len(snake) - 1)
        sys.exit()
    # Add a new cell to the snake
    snake.insert(0, SnakeCell(head_coordinates, True))
    snake[1].head = False  # The old head is not the head anymore
    if (snake[0].coordinates == food.coordinates).all():  # Check if the snake has eaten the food
        food.create(map(lambda cell: cell.coordinates.tolist(), snake))
    else:
        # If the snake has not eaten the food, remove the last cell of the snake
        del(snake[-1])

    screen.fill((0, 0, 0))
    food.draw(screen)
    for cell in snake:
        cell.draw(screen)

    pygame.display.update()
    clock.tick(fps)
