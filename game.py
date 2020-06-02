# Creating a space invaders game with pygame

import sys
import pygame
from pygame.locals import *
import random
pygame.init()

# Setting the window and the window's name
WIDTH = 750
HEIGHT = 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load background
BG = pygame.transform.scale(pygame.image.load("assets/Background.png"), (WIDTH, HEIGHT))

# Load enemy ships
RED_SHIP = pygame.image.load("assets/Red_Ship.png")
GREEN_SHIP = pygame.image.load("assets/Green_Ship.png")
BLUE_SHIP = pygame.image.load("assets/Blue_Ship.png")

# Load enemy lasers
RED_LASER = pygame.image.load("assets/Red_Laser.png")
GREEN_LASER = pygame.image.load("assets/Green_Laser.png")
BLUE_LASER = pygame.image.load("assets/Blue_Laser.png")

# Load player's ship
YELLOW_SHIP = pygame.image.load("assets/Yellow_Ship.png")

# Load player's laser
YELLOW_LASER = pygame.image.load("assets/Yellow_Laser.png")


# Creating a Laser class
class Laser():
	def __init__(self, x, y, image):
		self.x = x
		self.y = y
		self.image = image
		self.mask = pygame.mask.from_surface(self.image)
	
	# Method for drawing lasers to window
	def draw(self, window):
		window.blit(self.image, (self.x, self.y))
	
	# Method for moving laser
	def move(self, speed):
		self.y += speed
	
	# Method to check if laser is off the screen		
	def off_screen(self, height):
		return not (self.y <= HEIGHT and self.y >= 0)
	
	# Method that checks for collision by invoking the collide function
	def collision(self, obj):
		return collide(obj, self)


# Creating a Ship superclass from which player ship and enemy ships will inherit from
class Ship():
	def __init__(self, x, y, health = 100):
		self.x = x
		self.y = y
		self.health = health
		self.ship_image = None
		self.laser_image = None
		self.lasers = []
		
	# Method for drawing ships to window and that also invokes the Method for drawing lasers to window	
	def draw(self, window):
		window.blit(self.ship_image, (self.x, self.y))
		for laser in self.lasers:
			laser.draw(window)
	
	# Method for defining the movement and action of enemy laser		
	def move_laser(self, speed, obj):
		for laser in self.lasers:
			laser.move(speed)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			elif laser.collision(obj):
				obj.health -= 5
				self.lasers.remove(laser)
	
	# Method for Creating a laser	
	def shoot(self):
		laser = Laser(self.x, self.y, self.laser_image)
		self.lasers.append(laser)
	
	# Method for checking width of ship	
	def get_width(self):
		return self.ship_image.get_width()
	
	# Method for checking height of ship	
	def get_height(self):
		return self.ship_image.get_height()


# Creating the Player subclass		
class Player(Ship):
	def __init__(self, x, y, health = 100):
		super().__init__(x, y, health)
		self.ship_image = YELLOW_SHIP
		self.mask = pygame.mask.from_surface(self.ship_image)
		self.laser_image = YELLOW_LASER
		self.max_health = health
	
	# Defining the player laser movement and action	
	def move_laser(self, speed, objs):
		for laser in self.lasers:
			laser.move(speed)
			if laser.off_screen(HEIGHT):
				self.lasers.remove(laser)
			else:
				for obj in objs:
					if laser.collision(obj):
						objs.remove(obj)
						if laser in self.lasers:
							self.lasers.remove(laser)
	
	# Drawing the health bar to window
	def draw(self, window):
		super().draw(window)
		self.health_bar(window)
	
	# Creating a health bar for the player ship
	def health_bar(self, window):
		pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_image.get_height() + 10, self.ship_image.get_width(), 10))
		pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_image.get_height() + 10, self.ship_image.get_width() * (self.health/self.max_health), 10))


# Creating the Enemy subclass		
class Enemy(Ship):
	COLOR_MATCH = {
	"red": (RED_SHIP, RED_LASER),
	"green": (GREEN_SHIP, GREEN_LASER),
	"blue": (BLUE_SHIP, BLUE_LASER)
	}
	def __init__(self, x, y, color, health = 100):
		super().__init__(x, y, health)
		self.ship_image, self.laser_image = self.COLOR_MATCH[color]
		self.mask = pygame.mask.from_surface(self.ship_image)
	
	# Defining enemy ship movement
	def move(self, speed):
		self.y += speed

#Collide function that checks collision between ship and laser or between ships
def collide(obj1, obj2):
	offset_x = obj2.x - obj1.x
	offset_y = obj2.y - obj1.y
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


# Main loop
def main():
	run = True
	lost = False
	lost_count = 0
	FPS = 60
	clock = pygame.time.Clock()
	lives = 7
	level = 0
	enemies = []
	number_of_enemies = 20
	enemy_speed = 1
	player = Player(375, 625)	
	player_speed = 20
	laser_speed = 5
	
	def update_window():
		# Loading main font
		main_font = pygame.font.SysFont("comicsans", 50)
		
		# Creating lives and level labels
		lives_label = main_font.render(f"lives: {lives}", 1, (255, 255, 255))
		level_label = main_font.render(f"level: {level}", 1, (255, 255, 255))
		
		# Loading lost font
		lost_font = pygame.font.SysFont("comicsans", 100, bold = True)
		
		# Creating lost label
		lost_label = lost_font.render("GAME OVER", 1, (255, 255, 255))
		
		# Drawing background to window
		WIN.blit(BG, (0, 0))
		
		#Drawing lives and level labels to window
		WIN.blit(lives_label, (50, 50))
		WIN.blit(level_label, (WIDTH - level_label.get_width() - 50, 50))
	
		# Drawing enemy ships to window	
		for enemy in enemies:
			enemy.draw(WIN)
	
		# Drawing player ship to window	
		player.draw(WIN)
	
		# Drawing lost label to window 		
		if lost:
			WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 600))
		
		pygame.display.update()
	
	while run:
		clock.tick(FPS)
		update_window()
		
		# Stating condition for game lost
		if lives <= 0 or player.health <= 0:
			lost = True
			lost_count += 1
		
		# Setting how long "GAME OVER" displays
		if lost:
			if lost_count > FPS * 0.5:
				run = False
			else:
				continue
			
		# Creating enemy ships, stating condition for increasing level & number of enemy ships, and positioning & selecting enemy ships at random
		if len(enemies) == 0:
			level += 1
			number_of_enemies += 3		
			for ship in range(number_of_enemies):
				enemy = Enemy(random.randrange(150, WIDTH-150), random.randrange(-1000, -300), random.choice(["red", "blue", "green"]))
				enemies.append(enemy)
				
		for enemy in enemies:
			# Moving the enemy laser
			enemy.move_laser(laser_speed, player)
			
			# Making the enemy shoot with a 100% probability that it would be every 2 secs
			if random.randrange(0, 3*FPS) == 1:
				enemy.shoot()
				
			# Moving the enemy ship move and stating when the player loses health and life
			enemy.move(enemy_speed)
			if collide(enemy, player):
				player.health -= 2
				enemies.remove(enemy)
			if enemy.y + enemy.get_height() > HEIGHT:
				lives -= 1
				enemies.remove(enemy)
			
		# Moving the player laser
		player.move_laser(-laser_speed, enemies)

		# Setting player movement and shooting buttons
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				if event.key == K_RIGHT and player.x + player_speed + player.get_width() < WIDTH:
					player.x += player_speed
				elif event.key == K_LEFT and player.x > player_speed:
					player.x -= player_speed
				elif event.key == K_UP and player.y > player_speed:
					player.y -= player_speed
				elif event.key == K_DOWN and player.y + player_speed + player.get_height() + 15 < HEIGHT:
					player.y += player_speed
				elif event.key == K_SPACE:
					player.shoot()
			
			elif event.type == pygame.QUIT:
				run = False
				quit()
				
def main_menu():
	# Loading menu font
    menu_font = pygame.font.SysFont("comicsans", 70)
    
    run = True
    while run:
        WIN.blit(BG, (0,0))
        
        # Creating menu label and drawing it to window
        menu_label = menu_font.render("Click Mouse To Begin", 1, (255,255,255))
        WIN.blit(menu_label, (WIDTH/2 - menu_label.get_width()/2, 375))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:         
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main()
                del menu_label
 
main_menu()