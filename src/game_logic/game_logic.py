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
pause_music = pygame.mixer.Sound("../game_sounds/pause.mp3")

volume_level = 0.5
pause_music.set_volume(volume_level)

orbitron_font_path = os.path.join(os.path.dirname(__file__), '../../fonts/orbitron.ttf')
orbitron_font_size = 50
title_font_size = 85
orbitron_font = pygame.font.Font(orbitron_font_path, orbitron_font_size)
title_font = pygame.font.Font(orbitron_font_path, title_font_size)

background_images = [pygame.transform.scale(pygame.image.load(f"../assets/background_{i}.jpg"), (WIDTH, HEIGHT)) for i in range(1, 12)]

lives_h, lives_w = 50, 50

# Load images
LIVES = pygame.image.load(
    os.path.join("../assets", "lives.png")
)
LIVES = pygame.transform.scale(LIVES, (lives_h, lives_w))

TRANSPARENT_GREY = (128, 128, 128, 128)

def redraw_window(level, lives, lost, enemies, asteroids, player, gifts, paused):
    current_bg = background_images[level % len(background_images)]
    WIN.blit(current_bg, (0, 0))
    

    lives_label = orbitron_font.render(f"Lives: {lives}", 1, (255, 255, 255))
    level_label = orbitron_font.render(f"Level: {level}", 1, (255, 255, 255))
    score_label = orbitron_font.render(f"Score: {player.score}", 1, (255, 255, 255))

    WIN.blit(lives_label, (10, 10))

    lives_image_rect = LIVES.get_rect()
    WIN.blit(LIVES, (10 + lives_label.get_width() + 5, 10 + (lives_label.get_height() - lives_image_rect.height) // 2))

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
        #pause()
        #paused_label = orbitron_font.render("Paused: press 'p' to continue", 1, (0, 255, 0))
        #WIN.blit(paused_label, (WIDTH // 2 - paused_label.get_width() // 2, HEIGHT // 2 - paused_label.get_height() // 2))
        overlay_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay_surface.fill((128, 128, 128, 128))  # 128 is the alpha (transparency) value
        WIN.blit(overlay_surface, (0, 0))

        paused_label = orbitron_font.render("Paused: press 'p' to continue", 1, (0, 255, 0))
        WIN.blit(paused_label, (WIDTH // 2 - paused_label.get_width() // 2, HEIGHT // 2 - paused_label.get_height() // 2))
    elif lost:
        lost_label = orbitron_font.render("Game Over! Your score is " + str(player.score), 1, (255, 255, 255))
        WIN.blit(lost_label, (WIDTH / 2 - lost_label.get_width() / 2, 350))

    pygame.display.update()

def scores():
    pass

"""
def pause():
    #pass
    pygame.display.set_caption("Pause menu")
    
    run = True
    while run:
        tinted_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        tinted_surface.fill(TRANSPARENT_GREY)
        WIN.blit(tinted_surface, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = title_font.render("PAUSE MENU", True, "White")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 150))

        PLAY_BUTTON = Button(image=pygame.image.load("../assets/rectangle.png"), pos=(640, 300), 
                            text_input="BACK TO GAME", font=orbitron_font, base_color="White", hovering_color="#4CBB17")
        QUIT_BUTTON = Button(image=pygame.image.load("../assets/rectangle.png"), pos=(640, 450), 
                            text_input="QUIT GAME", font=orbitron_font, base_color="White", hovering_color="#4CBB17")

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    run = False
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()

        pygame.display.update()

        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
    pause()
"""    

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
        lives = 3

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

            if player.health <= 0:
                lives -= 1
                player.health = 100 

            if lives <= 0:
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
                    elif event.key == pygame.K_a:
                        player.x = 0
                    elif event.key == pygame.K_d:
                        player.x = WIDTH - player.get_width()

            if pause:
                # Pause the game music
                pygame.mixer.music.pause()

                # Play the pause music if it's not already playing
                if not pygame.mixer.get_busy():
                    pause_music.play()

                continue
            else:
                # Unpause the game music
                pygame.mixer.music.unpause()

                # Stop the pause music if it's playing
                if pygame.mixer.get_busy():
                    pause_music.stop()

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
        SCORES_BUTTON = Button(image=pygame.image.load("../assets/rectangle.png"), pos=(640, 375), 
                            text_input="SCORES", font=orbitron_font, base_color="White", hovering_color="#4CBB17")
        GUIDE_BUTTON = Button(image=pygame.image.load("../assets/rectangle.png"), pos=(640, 525), 
                            text_input="HOW TO PLAY", font=orbitron_font, base_color="White", hovering_color="#4CBB17")
        QUIT_BUTTON = Button(image=pygame.image.load("../assets/rectangle.png"), pos=(640, 675), 
                            text_input="QUIT GAME", font=orbitron_font, base_color="White", hovering_color="#4CBB17")

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, SCORES_BUTTON, GUIDE_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main()
                if SCORES_BUTTON.checkForInput(MENU_MOUSE_POS):
                    scores()
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




