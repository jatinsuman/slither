import pygame
import math
import random

pygame.init()

screen = pygame.display.set_mode((620, 620))
screen.fill((20, 20, 20))
pygame.display.set_caption("Slither IO")
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)

run = True
temp_speed = 0.3
player_x_coords, player_y_coords = 310, 310

CYAN = (0, 200, 200)
GREEN = (50, 255, 50)
YELLOW = (200,200,0)
ORANGE = (255,165,0)
RED = (255, 100, 100)
MAGENTA = (255,0,255)

color_list = [CYAN, GREEN, YELLOW, ORANGE, RED, MAGENTA]
blob_list = []

for i in range(250):
    blob_list.append([random.choice(color_list), random.randrange(0, 5000),\
         random.randrange(0, 5000), random.randrange(8, 15)])

class Snake:
    def __init__(self, x_coord, y_coord, size):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.size = size
        self.segments = [[self.x_coord, self.y_coord]] * size
        self.head_segment = None
        self.cursor_head_length = None
        self.head_tail_length = 0
        self.head_rect = pygame.Rect(self.x_coord, self.y_coord, 40, 40)
        self.temp_speed = 0.3

    def movement(self, current_x, current_y, target_x, target_y, speed):
        global length
        length = math.sqrt((target_x - current_x) ** 2 + (target_y - current_y) ** 2)
        try:
            new_x = current_x + ((target_x - current_x) / length) * speed
            new_y = current_y + ((target_y - current_y) / length) * speed
        except:
            return [current_x, current_y]
        return [new_x, new_y]

snake_group = []
player_snake = Snake(310, 310, 5)
other_snake = Snake(310, 310, 10)

snake_group.append(player_snake)

target_blob_x, target_blob_y = other_snake.x_coord + random.randrange(-100, 100), \
                               other_snake.y_coord + random.randrange(-100, 100)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for snake in snake_group:
        if snake != player_snake:
            if random.choice([0, 1]) == 1:
                target_blob_x += random.randrange(-30, -10)
            else:
                target_blob_x += random.randrange(10, 30)
            if random.choice([0, 1]) == 1:
                target_blob_y += random.randrange(-30, -10)
            else:
                target_blob_y += random.randrange(10, 30)

    cursor_pos = pygame.mouse.get_pos()

    player_x_coords, player_y_coords = player_snake.movement(
            player_x_coords, player_y_coords, cursor_pos[0], cursor_pos[1], 0.006
        ) 
        
    if round(length) == 0:
        player_x_coords, player_y_coords = 310, 310
    
    for snake in snake_group:
        if snake == player_snake:
            snake.head_segment = snake.movement(
                snake.x_coord, snake.y_coord, cursor_pos[0], cursor_pos[1], 0.3) 
        else:
            snake.head_segment = snake.movement(
                snake.x_coord, snake.y_coord, target_blob_x, target_blob_y, 0.3) 

        snake.segments[0] = snake.head_segment
        snake.head_rect = pygame.Rect(snake.head_segment[0], snake.head_segment[1], 40, 40)
        if snake == player_snake:
            snake.cursor_head_length = math.sqrt(
                (cursor_pos[0] - snake.x_coord) ** 2 + (cursor_pos[1] - snake.y_coord) ** 2
            )
        else:
            snake.cursor_head_length = math.sqrt(
                (target_blob_x - snake.x_coord) ** 2 + (target_blob_y - snake.y_coord) ** 2
            )            

    for snake in snake_group:
        for i in range(1, len(snake.segments)):
            snake.head_tail_length += math.sqrt(
                (snake.segments[i - 1][0] - snake.segments[i][0]) ** 2 +
                (snake.segments[i - 1][1] - snake.segments[i][1]) ** 2
            )

    screen.fill((20, 20, 20))

    offset_x = player_x_coords - 310
    offset_y = player_y_coords - 310

    for i in range(len(blob_list)):
        blob_list[i][1] -= offset_x * 50
        blob_list[i][2] -= offset_y * 50
        if 0 < blob_list[i][1] < 620 and 0 < blob_list[i][1] < 620:
            pygame.draw.circle(screen, blob_list[i][0], (int(blob_list[i][1]), int(blob_list[i][2])), blob_list[i][3])

    player_x_coords, player_y_coords = 310, 310
    
    for snake in snake_group:
        if snake == player_snake:
            snake_diff = [snake.head_segment[0] - 310, \
            snake.head_segment[1] - 310]        
            for piece in snake.segments:
                piece[0] -= snake_diff[0] 
                piece[1] -= snake_diff[1] 
        
    for snake in snake_group:
        if snake == player_snake:
            pygame.draw.circle(
                screen, (255, 255, 255), (int(snake.head_segment[0]), int(snake.head_segment[1])), 20, 20
            )
        snake.x_coord, snake.y_coord = snake.head_segment

    for snake in snake_group:
        if round(snake.cursor_head_length) != 0:
            for i in range(1, len(snake.segments)):
                if snake.head_tail_length < 15 * len(snake.segments) and snake == player_snake:
                    snake.temp_speed -= 0.01
                elif snake.head_tail_length > 15 * len(snake.segments) and snake == player_snake:
                    snake.temp_speed += 0.01
                elif snake != player_snake:
                    snake.temp_speed -= 0.008

                other_segment = snake.movement(
                    snake.segments[i][0], snake.segments[i][1],
                    snake.segments[i - 1][0], snake.segments[i - 1][1], snake.temp_speed
                )
                pygame.draw.circle(
                    screen, (255, 255, 255), (int(other_segment[0]), int(other_segment[1])), 20, 20
                )
                snake.segments[i] = other_segment
        else:
            for segment in snake.segments:
                pygame.draw.circle(
                    screen, (255, 255, 255), (int(segment[0]), int(segment[1])), 20, 20
                )
    for snake in snake_group:
        snake.temp_speed = 0.3

    for snake in snake_group:
        snake.head_tail_length = 0
        new_blob_list = []
        for ele in blob_list:
            if 620 > ele[1] > 0 and 620 > ele[2] > 0 and 0 < abs(snake.head_segment[0] - ele[1]) < 20 and 0 < abs(snake.head_segment[1] - ele[2]) < 20:
                snake.size += 1
                snake.segments.append([snake.segments[-1][0], snake.segments[-1][1]])
                continue
            new_blob_list.append(ele)
        blob_list = new_blob_list
    pygame.display.update()
