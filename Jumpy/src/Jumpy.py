import pygame
from pygame.locals import *
from pygame import mixer
import random
import os

from Player import Player
from Platform import Platform
from SpriteSheet import SpriteSheet
from Bird import Bird

mixer.init()
pygame.init()

clock = pygame.time.Clock()
FPS = 60

MAX_PLATFORM = 10
SCROLL_THRESH = 275
IMAGE_SIZE = 32
scroll = 0
bg_scroll = 0
game_over = False
score = 0
jump_vel = -7
chance_broken = 0
chance_moving = 0
chance_enemies = 0
e_chance = 11 #chance is 1-10 so by putting it as 11 it'll prevent the game from spawning enemy at the beginning
platform_width_min = 100
platform_width_max = 120
increase_player_vel = -0.1
increase_gravity = 0.006
old_score = 0
e_pos_y = 100
dead_from_bird = False

if os.path.exists('score.txt'):
    with open('score.txt', 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 750
WHITE = (255,255,255)
BLACK = (0,0,0)

font_small = pygame.font.SysFont('Comic Sans MS', 20)
font_big = pygame.font.SysFont('Comic Sans MS', 24)

# font_small = pygame.font.SysFont('Bradley Hand', 20)
# font_big = pygame.font.SysFont('Bradley Hand', 24)

# initiate screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Jumpy')

# load music and sound
pygame.mixer.music.load('../assets/bg.mp3')
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play(-1, 0.0)
death_sfx = pygame.mixer.Sound('../assets/death.mp3')
death_sfx.set_volume(0.8)
jump_sfx = pygame.mixer.Sound('../assets/jump.mp3')
jump_sfx.set_volume(0.7)


# load images
bg_img = pygame.image.load('../assets/bg.png').convert()
player_img = pygame.image.load('../assets/left.png').convert_alpha()
platform_img = pygame.image.load('../assets/platform.png').convert_alpha()
broken_platform_img = pygame.image.load('../assets/platform-broken.png').convert_alpha()
bird_sheet_img = pygame.image.load('../assets/bird.png').convert_alpha()
bird_sheet = SpriteSheet(bird_sheet_img, IMAGE_SIZE, IMAGE_SIZE, 1, BLACK)
# crab_sheet_img = pygame.image.load('../assets/crab.png').convert_alpha()

# function to draw text
def draw_text(text, font, col, x, y):
    img = font.render(text, True, col)
    screen.blit(img, (x, y))

# function to draw bg to scroll
def draw_bg(bg_scroll):
    screen.blit(bg_img, (0, bg_scroll))
    screen.blit(bg_img, (0, -SCREEN_HEIGHT + bg_scroll))

# player
player = Player(player_img, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)

# sprite group
platform_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

# starting platform
platform = Platform(platform_img, SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 100, 300, 1, 11, chance_moving)
platform_group.add(platform)



run = True
while run: 

    clock.tick(FPS)
    if game_over == False:
        bg_scroll += scroll
        if bg_scroll >= SCREEN_HEIGHT:
            bg_scroll = 0
        draw_bg(bg_scroll)

        # update all variables to increase difficulties
        if score < 3000:
            chance_broken = 0
            chance_moving = 0
            platform_width_min = 100
            platform_width_max = 120
            chance_enemies = 0
        elif 3000 < score < 8000:
            chance_broken = 0
            chance_moving = 2
            platform_width_min = 100
            platform_width_max = 120
            chance_enemies = 0
        elif 8000 < score < 16000:
            chance_broken = 1
            chance_moving = 3
            platform_width_min = 80
            platform_width_max = 100
            chance_enemies = 0
        elif 16000 < score < 26000:
            chance_broken = 3
            chance_moving = 3
            platform_width_min = 60
            platform_width_max = 100
            chance_enemies = 1
        elif 26000 < score < 40000:
            chance_broken = 4
            chance_moving = 4
            platform_width_min = 60
            platform_width_max = 80
            chance_enemies = 2
        elif score > 40000:
            chance_broken = 5
            chance_moving = 5
            platform_width_min = 40
            platform_width_max = 60
            chance_enemies = 3
        
        # for p in platform_group.sprites():
        #     draw_text(str(p.type)+ ' ' + str(chance_broken), font_small, BLACK, p.rect.right, p.rect.y)

        # generate platforms
        if len(platform_group) < MAX_PLATFORM:
            p_w = random.randint(platform_width_min, platform_width_max)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = platform.rect.y - random.randint(80, 120)
            p_type = random.randint(1,10)
            p_move = random.randint(1,10)
            if p_type <= chance_broken: # percent chance of getting a broken platform
                p_temp_type = 2
                platform = Platform(broken_platform_img, p_x, p_y, p_w, p_temp_type, p_move, chance_moving)
            else:
                p_temp_type = 1
                platform = Platform(platform_img, p_x, p_y, p_w, p_temp_type, p_move, chance_moving)
            platform_group.add(platform)

        # update/scroll platforms
        platform_group.update(scroll)

        # generate enemies
        if e_chance <= chance_enemies:
            if len(bird_group) == 0:
                bird = Bird(SCREEN_WIDTH, e_pos_y, bird_sheet, 3)
                bird_group.add(bird)
            
        bird_group.update(scroll, SCREEN_WIDTH)

        # score
        if scroll >= 0:
            score = int(score + scroll)

        # highscore line
        pygame.draw.line(screen, BLACK, (0, score - high_score + SCROLL_THRESH), (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 3)
        draw_text('HIGHSCORE', font_small, BLACK, 5, score - high_score + SCROLL_THRESH - 30)

        # draw platforms and enemies
        platform_group.draw(screen)
        bird_group.draw(screen)

        # draw player with hitbox
        screen.blit(pygame.transform.flip(player.image, player.flipped, False), (player.rect.x - player.hitbox_offset, player.rect.y))
        
        # check collision with bird
        if pygame.sprite.spritecollide(player, bird_group, False):
            if pygame.sprite.spritecollide(player, bird_group, False, pygame.sprite.collide_mask):
                death_sfx.play()
                dead_from_bird = True
                game_over = True
        
        # UNCOMMENT TO SHOW PLAYER HITBOX
        # pygame.draw.rect(screen, BLACK, player.rect, 2) 

        # reset scroll before making new scroll from SCROLL_THRESHOLD
        scroll = 0

        # move
        player.move()
        
        # draw the score
        draw_text(str(score), font_big, BLACK, 15, 5)

        # check for player is top of screen
        if player.rect.top <= SCROLL_THRESH:
            if player.vel_y < 0:
                scroll = -player.vel_y
                #player.vel_y = 0

        # limit player jump to only SCROLL_THRESHOLD
        player.rect.y += scroll

        # check for collision with platform
        for p in platform_group:
            if p.rect.colliderect(player.rect.x, player.rect.y + player.vel_y, player.rect_w, player.rect_h):
                if player.rect.bottom < p.rect.centery:
                    if player.vel_y > 0:
                        player.rect.bottom = p.rect.top
                        player.vel_y = jump_vel
                        jump_sfx.play()

                        # get random enemies encounter chance every time player hits platform
                        e_chance = random.randint(1,10)
                        #e_pos_y = random.randint(-100, int(SCREEN_WIDTH*(3/4)))
                        e_pos_y = SCREEN_HEIGHT - 500

                        # increase speed every time player hits platform and only when score increases
                        if score > old_score:
                            if player.gravity <= 1:
                                player.gravity += increase_gravity
                            if jump_vel >= -18:
                                jump_vel += increase_player_vel
                            old_score = score

                        # check if the platform collision is a broken one so it falls
                        if p.type == 2:
                            if p.first_jump == True:
                                p.falling = True
                            else:
                                p.first_jump = True

        # UNCOMMENT TO SHOW SCROLL_THRESHOLD
        # pygame.draw.line(screen, BLACK, (0, SCROLL_THRESH), (SCREEN_WIDTH, SCROLL_THRESH))
        
        # check game over
        if player.rect.top > SCREEN_HEIGHT:
            death_sfx.play()
            game_over = True

    else:
        draw_bg(bg_scroll)
        platform_group.update(scroll)
        platform_group.draw(screen)
        bird_group.draw(screen)
        bird_group.update(scroll, SCREEN_WIDTH)
        screen.blit(pygame.transform.flip(player.image, player.flipped, False), (player.rect.x - player.hitbox_offset, player.rect.y))
        player.grav()
        jump_vel = -7
        player.gravity = 0.2
        if dead_from_bird == True:
            player.vel_y = jump_vel
            dead_from_bird = False
        # record highscore
        draw_text('GAME OVER', font_big, BLACK, 225, 300)
        draw_text('SCORE: ' + str(score), font_big, BLACK, 225, 350)
        draw_text('HIGHSCORE: ' + str(high_score), font_big, BLACK, 225, 400)
        draw_text('PRESS SPACE TO PLAY AGAIN', font_big, BLACK, 120, 450)
        if score > high_score:
            high_score = score
            with open('score.txt', 'w') as file:
                file.write(str(high_score))
                file.close()
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            # reset variables
            game_over = False
            score = 0
            scroll = 0
            bg_scroll = 0
            dead_from_bird = False

            # reset player
            player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)
            jump_vel = -7
            player.gravity = 0.2

            # reset enemies
            bird_group.empty()

            # reset platforms
            platform_group.empty()
            platform = Platform(platform_img, SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 100, 300, 1, 11, chance_moving)
            platform_group.add(platform)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            # record highscore
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
                    file.close()

            # close
            run = False
    
    pygame.display.update()

pygame.quit()