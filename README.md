# Snake-Game
This is a pretty simple snake game which works in an efficient, but also understandable way. That is accomplished by decomposing the game into 3 parts:
1. moving the snake
2. checking if the snake is dead
3. eating the food

Let's simplify the UI into a grid, in which each segment of the snake is a cell. The snake has a head and body cells, and ends with its tail. Splitting the UI into a grid helps simplify the process because of the way pygame uses pixel coordinates to draw shapes.

Moving the snake is quite simple, as when the snake moves, notice how most of its body appears to stay exactly where it is as each cell of the snake follows the next cell. We can utilise this by only changing the head and tail of the snake and leaving the rest of the body cells where they are, giving the illusion of movement.

There are 2 ways in which our snake can die: either it wanders off the screen or it collides with its own body. So, before each movement, we can check if each condition is met so we know when to end our game. To check whether the snake goes off the screen, we can use some simple modular arithmitic, that is the use of integer division, as if the snake's coordinate's are less than 0, then 'coordinate // gridlength' would be negative and if it were greater than the gridlength it would be positive. This means that when 'coordinate // gridlength != 0', the snake has wandered off the screen. To check if the next move by the player has caused the snake to collide onto itself, we can simply check whether the new coordinates are the same as any of the coordinates of cells in the snake (list).

Lastly, when handling the food, we first need to check whether the snake's new coordinates are the same as the food's as this would mean the snake will touch and therefore eat the food. When this happens, we can move our current food into a new, random location in the grid (as long as this isn't on the snake), to make it look as if it were eaten nd some new food has appeared. When the snake eats the food, it grows one cell longer. Dealing with this is simple as to simulate movement, we were going to delete the last cell of the snake anyways, so instead of deleting it, we can simply keep it when the snake eats food.
