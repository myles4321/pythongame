import pygame, os, sys, time, random
from classes.ship import Gift, Player, Enemy, collide, Asteroid, WIDTH, HEIGHT, WIN, BG
from classes.button import Button
import pygame.mixer
from classes.laser import Laser

pygame.init()
pygame.font.init()
pygame.mixer.init()
power_sound = pygame.mixer.Sound("../game_sounds/power.mp3")
health_sound = pygame.mixer.Sound("../game_sounds/health.mp3")
shoot_sound = pygame.mixer.Sound("../game_sounds/shoot.wav")
explosion_sound = pygame.mixer.Sound("../game_sounds/explosion.wav")
game_music = pygame.mixer.Sound("../game_sounds/game.mp3")

orbitron_font_path = os.path.join(os.path.dirname(__file__), '../../fonts/orbitron.ttf')
orbitron_font_size = 50
title_font_size = 85
orbitron_font = pygame.font.Font(orbitron_font_path, orbitron_font_size)
title_font = pygame.font.Font(orbitron_font_path, title_font_size)

background_images = [pygame.transform.scale(pygame.image.load(f"../assets/background_{i}.jpg"), (WIDTH, HEIGHT)) for i in range(1, 6)]

def redraw_window(level, lives, lost, enemies, asteroids, player, gifts, paused):
    current_bg = background_images[level % len(background_images)]
    WIN.blit(current_bg, (0, 0))
    

    lives_label = orbitron_font.render(f"Lives: {lives}", 1, (255, 255, 255))
    level_label = orbitron_font.render(f"Level: {level}", 1, (255, 255, 255))
    score_label = orbitron_font.render(f"Score: {player.score}", 1, (255, 255, 255))

    WIN.blit(lives_label, (10, 10))
    WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))
    WIN.blit(score_label, (WIDTH // 2 - score_label.get_width() // 2, 10))

    for gift in gifts:
        gift.draw(WIN)
        
    for enemy in enemies:
        enemy.draw(WIN)

    for asteroid in asteroids:
        asteroid.draw(WIN)

    player.draw(WIN)

    if paused:
        paused_label = orbitron_font.render("Paused: press 'p' to continue", 1, (255, 255, 255))
        WIN.blit(paused_label, (WIDTH // 2 - paused_label.get_width() // 2, HEIGHT // 2 - paused_label.get_height() // 2))
    elif lost:
        lost_label = orbitron_font.render("Game Over! Your score is " + str(player.score), 1, (255, 255, 255))
        WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

    pygame.display.update()

def profile():
    pass

def pause():
    pass

def guide():
    pass

def main():
    pygame.display.set_caption("Stardash")

    run = True
    while run:
        WIN.blit(BG, (0, 0))
        pygame.mixer.music.load("../game_sounds/game.mp3")
        pygame.mixer.music.play(-1)  
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
        
        gifts = []
        gift_vel = 3
        gift_images = ["../assets/gift.png", "../assets/laser_gift.png"]


        pause = False  # Reset pause to False at the start of each iteration 
        while run:
            clock.tick(FPS)
            redraw_window(level, lives, lost, enemies, asteroids, player, gifts, pause)

            if lives <= 0 or player.health <= 0:
                lost = True
                lost_count += 1

            if lost:
                if lost_count > FPS * 3:
                    run = False
                else:
                    continue    

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Press 'P' to pause/unpause
                        pause = not pause
                    elif event.key == pygame.K_q:  # Press 'Q' to quit
                        run = False

            if pause:
                continue  # Skip the rest of the loop if the game is paused
                pause()
        
            

            if len(enemies) == 0:
                level += 1
                wave_length += 5
                # Increase enemy velocity with each level
                enemy_vel += 0.2
                for i in range(wave_length):
                    enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                    enemies.append(enemy)

                # Increase asteroid velocity with each level
                asteroid_vel += 0.2
                asteroid_wave_length = 3 + level * 2
                for i in range(asteroid_wave_length):
                    asteroid = Asteroid(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), "asteroid")
                    asteroids.append(asteroid)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.mixer.music.stop()
                    
            if random.randrange(0, 10 * FPS) == 1:
                gift_path = random.choice(gift_images)
                gift_identifier = "laser" if "laser" in gift_path.lower() else "other"  # Identify the gift type
                gift = Gift(random.randrange(50, WIDTH - 100), random.randrange(-500, -100), gift_path, 40, 40, gift_identifier)
                gifts.append(gift)


            for gift in gifts[:]:
                gift.move(gift_vel)
                gift.draw(WIN)

                if collide(gift, player):
                    gifts.remove(gift)

                    if "laser" in gift.identifier.lower():
                        power_sound.play()
                        player.increase_laser_power()
                    else:
                        health_sound.play()
                        player.health = min(player.health + 20, 100)

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
                    player.reset_laser_power()
                    
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
                    player.reset_laser_power()

            player.move_lasers(-laser_vel, enemies)

    if not run:
        main_menu()
    
    
"""
#-----------------------previous main menu without GUI------------------------
def main_menu(current_user):

    print(f"Welcome, {current_user}!")

    print("1. Dash")
    print("2. Logout")

    choice = input("Enter your choice: ")
    
    if choice == "1":
        #play(current_user)
    elif choice == "2":
        #print("Logging out...")
    else:
        print("Invalid choice. Please try again.")

def play(current_user):
    print(f"{current_user}")
    #---------------continue code from here----------------
"""

def main_menu():
    pygame.display.set_caption("Main menu")
    pygame.mixer.init()
    pygame.mixer.music.load("../game_sounds/main_menu.mp3")
    pygame.mixer.music.play(-1) 
   
    run = True
    while run:
        WIN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = title_font.render("STARDASH", True, "#32CD32")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 75))

        PLAY_BUTTON = Button(image=pygame.image.load("../assets/rectangle.png"), pos=(640, 225), 
                            text_input="PLAY", font=orbitron_font, base_color="White", hovering_color="#4CBB17")
        PROFILE_BUTTON = Button(image=pygame.image.load("../assets/rectangle.png"), pos=(640, 375), 
                            text_input="MY PROFILE", font=orbitron_font, base_color="White", hovering_color="#4CBB17")
        GUIDE_BUTTON = Button(image=pygame.image.load("../assets/rectangle.png"), pos=(640, 525), 
                            text_input="HOW TO PLAY", font=orbitron_font, base_color="White", hovering_color="#4CBB17")
        QUIT_BUTTON = Button(image=pygame.image.load("../assets/rectangle.png"), pos=(640, 675), 
                            text_input="QUIT GAME", font=orbitron_font, base_color="White", hovering_color="#4CBB17")

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, PROFILE_BUTTON, GUIDE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()
                if PROFILE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    profile()
                if GUIDE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    guide()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
main_menu()    

"""
def play():    #can remove to implement sessions
    pygame.display.set_caption("Stardash")
    
    while True:
        pygame.mixer.music.load("../game_sounds/main_menu.mp3")
        pygame.mixer.music.play(-1)  

        run = True
        while run:
            WIN.blit(BG, (0, 0))

            title_text = orbitron_font.render("STARDASH", 1, (0, 255, 0))
            title_font_size = 100
            orbitron_large_font = pygame.font.Font(orbitron_font_path, title_font_size)
            title_text = orbitron_font.render("STARDASH", 1, (0, 255, 0))
            title_font_size = 70
            orbitron_large_font = pygame.font.Font(orbitron_font_path, title_font_size)
            title_text = orbitron_large_font.render("STARDASH", 1, (0, 255, 0))
            title_x = WIDTH / 2 - title_text.get_width() / 2
            title_y = HEIGHT / 2 - title_text.get_height() - 20
            WIN.blit(title_text, (title_x, title_y))

            subtitle_text = orbitron_font.render("Left click to begin...", 1, (255, 255, 255))
            subtitle_x = WIDTH / 2 - subtitle_text.get_width() / 2
            subtitle_y = HEIGHT / 2 + 20
            WIN.blit(subtitle_text, (subtitle_x, subtitle_y))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Check for right-click
                    pygame.mixer.music.stop()  
                    main()

        pygame.quit()
"""


