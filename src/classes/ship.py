import pygame
import os
from classes.laser import Laser, collide

ship_h, ship_w = 100, 150
alien_h, alien_w = 80, 120
asteroid_h, asteroid_w = 200, 200

# Load images
RED_SPACE_SHIP = pygame.image.load(
    os.path.join("../assets", "pixel_ship_red_small.png")
)
RED_SPACE_SHIP = pygame.transform.scale(RED_SPACE_SHIP, (alien_h, alien_w))
GREEN_SPACE_SHIP = pygame.image.load(
    os.path.join("../assets", "pixel_ship_green_small.png")
)
GREEN_SPACE_SHIP = pygame.transform.scale(GREEN_SPACE_SHIP, (alien_h, alien_w))
BLUE_SPACE_SHIP = pygame.image.load(
    os.path.join("../assets", "pixel_ship_blue_small.png")
)
BLUE_SPACE_SHIP = pygame.transform.scale(BLUE_SPACE_SHIP, (alien_h, alien_w))
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join("../assets", "pixel_ship_yellow.png")
)
YELLOW_SPACE_SHIP = pygame.transform.scale(YELLOW_SPACE_SHIP, (ship_h, ship_w))
ASTEROID = pygame.image.load(os.path.join("../assets", "asteroid.png"))
ASTEROID = pygame.transform.scale(ASTEROID, (asteroid_h, asteroid_w))

pygame.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
info = pygame.display.Info()

WIDTH, HEIGHT = info.current_w, info.current_h
WIN = pygame.display.set_mode((WIDTH-10, HEIGHT-50), pygame.RESIZABLE)
BG = pygame.transform.scale(
    pygame.image.load(os.path.join("../assets", "main_menu.jpg")),
    (WIDTH, HEIGHT),
)

# ... (other images)

# Lasers
RED_LASER = pygame.image.load(os.path.join("../assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("../assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("../assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("../assets", "pixel_laser_yellow.png"))


class Ship:
    '''
    This class defines the characteristics of ships within the game world.
    '''
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    '''
    This class defines the characteristics of the player's ship.
    '''
    def __init__(self, x, y, health=100, laser_power=1):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score = 0
        self.laser_power = 0
        
    def increase_laser_power(self):
        #self.laser_power += 1
        """
        Overpowered version
        """
        if self.cool_down_counter == 0:
            laser1 = Laser(self.x - 50, self.y, self.laser_img)
            self.lasers.append(laser1)
            laser2 = Laser(self.x - 100, self.y, self.laser_img)
            self.lasers.append(laser2)
            laser3 = Laser(self.x - 150, self.y, self.laser_img)
            self.lasers.append(laser3)
            laser4 = Laser(self.x - 200, self.y, self.laser_img)
            self.lasers.append(laser4)
            laser5 = Laser(self.x - 250, self.y, self.laser_img)
            self.lasers.append(laser5)
            laser6 = Laser(self.x - 300, self.y, self.laser_img)
            self.lasers.append(laser6)
            laser7 = Laser(self.x - 350, self.y, self.laser_img)
            self.lasers.append(laser7)
            laser8 = Laser(self.x - 400, self.y, self.laser_img)
            self.lasers.append(laser8)
            laser9 = Laser(self.x - 450, self.y, self.laser_img)
            self.lasers.append(laser9)
            laser10 = Laser(self.x - 500, self.y, self.laser_img)
            self.lasers.append(laser10)
            laser11 = Laser(self.x + 50, self.y, self.laser_img)
            self.lasers.append(laser11)
            laser12 = Laser(self.x + 100, self.y, self.laser_img)
            self.lasers.append(laser12)
            laser13 = Laser(self.x + 150, self.y, self.laser_img)
            self.lasers.append(laser13)
            laser14 = Laser(self.x + 200, self.y, self.laser_img)
            self.lasers.append(laser14)
            laser15 = Laser(self.x + 250, self.y, self.laser_img)
            self.lasers.append(laser15)
            laser16 = Laser(self.x + 300, self.y, self.laser_img)
            self.lasers.append(laser16)
            laser17 = Laser(self.x + 350, self.y, self.laser_img)
            self.lasers.append(laser17)
            laser18 = Laser(self.x + 400, self.y, self.laser_img)
            self.lasers.append(laser18)
            laser19 = Laser(self.x + 450, self.y, self.laser_img)
            self.lasers.append(laser19)
            laser20 = Laser(self.x + 500, self.y, self.laser_img)
            self.lasers.append(laser20)
        

    def reset_laser_power(self):
        self.laser_power = 1
          
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers[:]:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.score += 10
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                            
                            if self.laser_power > 1:
                                for _ in range(self.laser_power - 1):
                                    extra_laser = Laser(self.x + self.ship_img.get_width() // 2, self.y, self.laser_img)
                                    extra_laser.move(vel)
                                    self.lasers.append(extra_laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(
            window,
            (255, 0, 0),
            (
                self.x,
                self.y + self.ship_img.get_height() + 10,
                self.ship_img.get_width(),
                10,
            ),
        )
        pygame.draw.rect(
            window,
            (0, 255, 0),
            (
                self.x,
                self.y + self.ship_img.get_height() + 10,
                self.ship_img.get_width() * (self.health / self.max_health),
                10,
            ),
        )
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x + self.ship_img.get_width() // 26, self.y, self.laser_img)
            self.lasers.append(laser)

            # Adjust the number of lasers based on laser power
            for i in range(1, self.laser_power):
                extra_laser = Laser(self.x + self.ship_img.get_width() // 26 - i * 10, self.y -16 * 10, self.laser_img)
                self.lasers.append(extra_laser)

            self.cool_down_counter = 1


class Enemy(Ship):
    '''
    This class defines the characteristics of the enemy's ship.
    '''
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Asteroid(Ship):
    '''
    This class defines the characteristics of asteroids that appear within the game world.
    '''
    COLOR_MAP = {
        "asteroid": ASTEROID,
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel
        
class Gift:
    def __init__(self, x, y, img_path, width, height, identifier):
        self.x = x
        self.y = y

        self.img = pygame.transform.scale(pygame.image.load(img_path), (width, height))
        self.mask = pygame.mask.from_surface(self.img)
        self.identifier = identifier

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel
