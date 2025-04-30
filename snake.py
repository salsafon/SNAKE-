import pygame
import random
import time
import sys

screenX = 800
screenY = 600

snakeSpeed = 10

#colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
green = pygame.Color(11, 218, 81)
purple = pygame.Color(128, 0, 128)
darkGreen = pygame.Color(80, 200, 120)

fruitImage = pygame.image.load('snakeFruit.png')
fruitImage = pygame.transform.scale(fruitImage, (20, 20))


# Initialize pygame
pygame.init()
pygame.display.set_caption('Cobra Game')
gameWindow = pygame.display.set_mode((screenX, screenY))
fps = pygame.time.Clock()

snake_position = [200, 200]
snake_body = [[200, 100], [180, 100], [160, 100]]
fruit_position = [random.randrange(1, (screenX // 20)) * 20,
                   random.randrange(1, (screenY // 20)) * 20]
fruit_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0

#score function
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    gameWindow.blit(score_surface, score_rect)


#grid function
def draw_grid():
    for x in range(0, screenX, 20):
        pygame.draw.line(gameWindow, darkGreen, (x, 0), (x, screenY))
    for y in range(0, screenY, 20):
        pygame.draw.line(gameWindow, darkGreen, (0, y), (screenX, y))


#game over function
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, white)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (screenX / 2, screenY / 4)
    gameWindow.fill(green)
    gameWindow.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# Main Function
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # If two keys pressed simultaneously
    # don't want the snake to move into two directions simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 20
    if direction == 'DOWN':
        snake_position[1] += 20
    if direction == 'LEFT':
        snake_position[0] -= 20
    if direction == 'RIGHT':
        snake_position[0] += 20

    # Snake body growing mechanism
    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        fruit_spawn = False
    else:
        snake_body.pop()
    if not fruit_spawn:
        fruit_position = [random.randrange(1, (screenX // 20)) * 20,
                           random.randrange(1, (screenY // 20)) * 20]
    fruit_spawn = True

    # GFX
    gameWindow.fill(green)
    draw_grid()
    for pos in snake_body:
        pygame.draw.rect(gameWindow, purple, pygame.Rect(pos[0], pos[1], 20, 20))
    
    # Fruit Image
    gameWindow.blit(fruitImage, (fruit_position[0], fruit_position[1]))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > screenX - 10:
        game_over()
    if snake_position[0] < 0 or snake_position[0] >= screenX or snake_position[1] < 0 or snake_position[1] >= screenY:
        game_over()

    # Check if the snake has hit itself
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()
    
    # Display score continuously
    show_score(1, white, 'times new roman', 20)

    # Refresh game screen
    pygame.display.update()

    # Frame Per Second /Refresh Rate
    fps.tick(snakeSpeed)


