
import pygame
from sys import exit
from random import randint,choice

def display_Score():
    score_surf = test_font.render(f"Score: {score}", False, "White")
    score_rect = score_surf.get_rect(center = (WIDTH // 2, 80))
    window.blit(score_surf,score_rect)

def enemy_movement(enemy_list):
    if enemy_list:
        for obs_rect in enemy_list:
            obs_rect.x += 8
            if obs_rect.y == 540:
                window.blit(enemy_surf,obs_rect)
            else:
                window.blit(enemy2_surf,obs_rect)

            enemy_list = [enemy for enemy in enemy_list if (enemy.x > -100) or (enemy.x < WIDTH)]
        
        return enemy_list
    else:
        return []
    
def collisions(player,enemies,bullets):
    global score
    if enemies:
        for enemy_rect in enemies:
            if player.colliderect(enemy_rect):
                return False
            if bullets:
                for bullet_rect in bullets:
                    if enemy_rect.colliderect(bullet_rect):
                        if enemy_rect.y == 540: score += 1
                        else: score += 5
                        enemies.remove(enemy_rect)
                        bullets.remove(bullet_rect)
    return True

def shootBullet(bullet_list):
    if bullet_list:
        for bullet_rect in bullet_list:
            bullet_rect.x += 20
            window.blit(bullet_surf,bullet_rect)
            bullet_list = [bullet for bullet in bullet_list if bullet.x < WIDTH]
        
        return bullet_list
    else:
        return []

WIDTH = 1280
HEIGHT = 720
FRAME_RATE = 60
running = True

pygame.init()
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Square Game")
clock = pygame.time.Clock()
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_active = False

PLAYER_WIDTH = 60
PLAYER_HEIGHT = 60
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50

ground_surf = pygame.Surface((WIDTH,10))
ground_surf.fill("White")
ground_rect = ground_surf.get_rect(midbottom = (WIDTH // 2, HEIGHT - 120))

player_surf = pygame.Surface((PLAYER_WIDTH,PLAYER_HEIGHT))
player_surf.fill("Lime")
player_rect = player_surf.get_rect(center = (WIDTH // 2,HEIGHT // 2))
player_gravity = 0
start_time = 0
score = 0

enemy_rect_list = []
bullet_rect_list = []

enemy_surf = pygame.Surface((ENEMY_WIDTH,ENEMY_HEIGHT))
enemy_surf.fill("Red")

enemy2_surf = pygame.Surface((ENEMY_WIDTH,ENEMY_HEIGHT))
enemy2_surf.fill("Cyan")

bullet_surf = pygame.Surface((20,20))
bullet_surf.fill("Yellow")

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,900)

while running:
    window.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
            exit()

        if game_active:
            if event.type == obstacle_timer:
                if choice([0,1,1,1]):
                    enemy_rect_list.append(enemy_surf.get_rect(midbottom = (randint(-340,-20),590)))
                else:
                    enemy_rect_list.append(enemy2_surf.get_rect(midbottom = (randint(-340,-20),490)))

            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                bullet_rect_list.append(bullet_surf.get_rect(midbottom = (player_rect.x,player_rect.y + 40)))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_active = True
                score = 0

    if game_active:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            if player_rect.x > 0:
                player_rect.x -= 5
        if keys[pygame.K_d]:
            if player_rect.x < (WIDTH - PLAYER_WIDTH):
                player_rect.x += 5
        if keys[pygame.K_SPACE]:
            if player_rect.bottom >= ground_rect.top:
                player_gravity = -20

        player_gravity += 1
        player_rect.y += player_gravity

        if player_rect.bottom >= ground_rect.top:
            player_rect.bottom = ground_rect.top

        enemy_rect_list = enemy_movement(enemy_rect_list)
        bullet_rect_list = shootBullet(bullet_rect_list)

        window.blit(player_surf,player_rect)
        window.blit(ground_surf,ground_rect)

        display_Score()

        game_active = collisions(player_rect,enemy_rect_list,bullet_rect_list)

    else:
        window.fill("black")
        enemy_rect_list.clear()
        bullet_rect_list.clear()
        player_rect.center = (WIDTH // 2,HEIGHT // 2)
        player_gravity = 0

        if score == 0:
            message_disp = test_font.render("Press ENTER to Start",False,"White")
            message_disp_rect = message_disp.get_rect(center = (WIDTH // 2, HEIGHT - 130))
            window.blit(message_disp,message_disp_rect)
        else:
            score_display = test_font.render(f"Score: {score}",False,"White")
            score_display_rect = score_display.get_rect(center = (WIDTH // 2, HEIGHT - 130))
            window.blit(score_display,score_display_rect)

        game_title = test_font.render("Square Jump",False,"White")
        game_title_rect = game_title.get_rect(center = (WIDTH // 2, 80))
        window.blit(game_title,game_title_rect)

        player_stand_surf = pygame.Surface((PLAYER_WIDTH,PLAYER_HEIGHT))
        player_stand_surf.fill("Lime")
        player_stand_rect = player_stand_surf.get_rect(center = (WIDTH // 2,HEIGHT // 2))
        window.blit(player_stand_surf,player_stand_rect)

    pygame.display.update()
    clock.tick(FRAME_RATE)