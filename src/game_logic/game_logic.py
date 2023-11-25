import pygame
import os
import random
from classes.ship import Player, Enemy, collide, Asteroid, WIDTH, HEIGHT, WIN, BG
import pygame.mixer
from classes.laser import Laser

pygame.init()
pygame.font.init()
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("../game_sounds/shoot.mp3")
explosion_sound = pygame.mixer.Sound("../game_sounds/explosion.mp3")

orbitron_font_path = os.path.join(os.path.dirname(__file__), '../../fonts/orbitron.ttf')
orbitron_font_size = 50
orbitron_font = pygame.font.Font(orbitron_font_path, orbitron_font_size)

background_images = [pygame.transform.scale(pygame.image.load(f"../assets/background_{i}.jpg"), (WIDTH, HEIGHT)) for i in range(1, 6)]

def redraw_window(level, lives, lost, enemies, asteroids, player):
    current_bg = background_images[level % len(background_images)]
    WIN.blit(current_bg, (0, 0))

    lives_label = orbitron_font.render(f"Lives: {lives}", 1, (255, 255, 255))
    level_label = orbitron_font.render(f"Level: {level}", 1, (255, 255, 255))
    score_label = orbitron_font.render(f"Score: {player.score}", 1, (255, 255, 255))

    WIN.blit(lives_label, (10, 10))
    WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
    WIN.blit(score_label, (WIDTH // 2 - score_label.get_width() // 2, 10))

    for enemy in enemies:
        enemy.draw(WIN)

    for asteroid in asteroids:
        asteroid.draw(WIN)

    player.draw(WIN)

    if lost:
        lost_label = orbitron_font.render("You Lost!!", 1, (255, 255, 255))
        WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

    pygame.display.update()

def main():
    run = True
    FPS = 60
    level = 0
    lives = 10

    enemies = []
    wave_length = 5
    enemy_vel = 1

    asteroids = []
    asteroid_vel = 1

    player = Player(300, 630)
    player_vel = 5
    laser_vel = 5

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0

    while run:
        clock.tick(FPS)
        redraw_window(level, lives, lost, enemies, asteroids, player)

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

            asteroid_wave_length = 5 + level * 2
            for i in range(asteroid_wave_length):
                asteroid = Asteroid(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), "asteroid")
                asteroids.append(asteroid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if keys[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_DOWN] and player.y + player_vel + player.get_height() + 15 < HEIGHT:
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
            shoot_sound.play()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                explosion_sound.play()
                enemies.remove(enemy)
                
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                explosion_sound.play()
                enemies.remove(enemy)

        for asteroid in asteroids[:]:
            asteroid.move(asteroid_vel)

            if collide(asteroid, player):
                player.health -= 10
                asteroids.remove(asteroid)
                explosion_sound.play()

        player.move_lasers(-laser_vel, enemies)

def main_menu():
    run = True
    while run:
        WIN.blit(BG, (0, 0))

        title_text = orbitron_font.render("STARDASH", 1, (0, 255, 0))
        title_font_size = 70
        orbitron_large_font = pygame.font.Font(orbitron_font_path, title_font_size)
        title_text = orbitron_font.render("STARDASH", 1, (0, 255, 0))
        title_font_size = 70
        orbitron_large_font = pygame.font.Font(orbitron_font_path, title_font_size)
        title_text = orbitron_large_font.render("STARDASH", 1, (0, 255, 0))
        title_x = WIDTH/2 - title_text.get_width()/2
        title_y = HEIGHT/2 - title_text.get_height() - 20
        WIN.blit(title_text, (title_x, title_y))

        subtitle_text = orbitron_font.render("Right click to begin...", 1, (255, 255, 255))
        subtitle_x = WIDTH/2 - subtitle_text.get_width()/2
        subtitle_y = HEIGHT/2 + 20
        WIN.blit(subtitle_text, (subtitle_x, subtitle_y))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for right-click
                main()

    pygame.quit()
