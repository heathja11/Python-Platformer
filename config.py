import pygame

#Colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
light_blue = (0, 155, 155)

game_name = "Sample"
game_width = 800
game_height = 600
fps = 60
font_type = 'Comis Sans MS'
highscore_file = "highscore.txt"
spritesheet_image = "spritesheet_sample.png"
spritesheet_image_background = "spritesheet_bg.png"
game_icon = pygame.image.load('icon.png')
background_colour = light_blue
background_image = 'background1'




#Player Options
player_acceleration = 0
player_friction = -0.12
player_gravity = 0.8
player_jump_speed = 20


# Game Spawns
coin_percent_bronze = 10
coin_percent_silver = 1
coin_percent_gold = 0.9
mob_frequency = 0


# Game Layers
player_layer = 3
mushroom_layer = 2
sign_layer = 2
bullet_layer = 3
platform_layer = 2
coin_layer = 2
mob_layer = 3
cloud_layer = 0
structure_layer = 1
background_layer = 0
spike_layer = 2




# define colors


