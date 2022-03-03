import random, time, os
try:
    import pygame
except ImportError:
    os.system('py3 -m pip install pygame')  # Automatically install PyGame


from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT
)

pygame.init()
pygame.mixer.init()

pusab = pygame.font.Font("pusab.otf", 25)

screenSize = SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

screen = pygame.display.set_mode(screenSize)

clock = pygame.time.Clock()

#"Generic Techno" by EnV
#Source: https://www.newgrounds.com/audio/listen/100400
pygame.mixer.music.load("generic_techno.mp3")
pygame.mixer.music.play(loops=-1)

#"Explosion, 8-bit, 01" by InspectorJ
#Source: https://freesound.org/people/InspectorJ/sounds/448226/
collision_sound = pygame.mixer.Sound("collision.wav")

#"Prop Plane" by Mozfoo
#Source: https://freesound.org/people/Mozfoo/sounds/440163/
engine_sound = pygame.mixer.Sound("engine.wav")
engine_sound.set_volume(0.3)

#Setup user events
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

#Setup "colors" class with all neccessary (and some unneccessary) colors
class colors:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    skyblue = (135, 206, 250)

#Initial screenfill
screen.fill(colors.blue)

#Setup Player class
class Player(pygame.sprite.Sprite):

    #Initialize sprite
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("plane.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.center = ( (SCREEN_WIDTH-self.surf.get_width())/2, (SCREEN_HEIGHT-self.surf.get_height())/2 )

    #Update sprite position with keypresses
    def update(self, pressed_keys):
        engine_sound.play()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        #The plane can't go off the edge of the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

#Setup Enemy class
class Enemy(pygame.sprite.Sprite):

    #Initialize sprite
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.image.load("missile.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)

    #Update sprite position
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

#Setup Cloud class, pretty much a clone of the Enemy class
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

#Setup player object
player = Player()

#Define a sprite master list and sublists for enemies and clouds
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#We're good to go!
running = True

#Initialize score
score = 0

#Main loop
while running:

    #Render score in the bottom-right of the screen
    text = pusab.render("Score: " + str(round(score/60)), True, colors.black)\

    #Update rect (IDK if this is really neccesary)
    textRect = text.get_rect()
    textRect.center = (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 15)

    #Fill the screen
    screen.fill(colors.skyblue)

    #Event loop
    for event in pygame.event.get():

        #Quit pygame if the escape key is used, the "x" button is clicked, or alt-F4 is pressed
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        #Handle the creation of new enemies
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        #Handle the creation of new clouds
        elif event.type == ADDCLOUD:
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    #Get pressed keys and pass to player.update()
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    #Update enemies and clouds
    enemies.update()
    clouds.update()

    #Blit all registered sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    #Blit score
    screen.blit(text, textRect)

    #Handle the collision between the player and a missile
    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()

        engine_sound.stop()
        collision_sound.play()

        screen.fill(colors.black)
        
        pygame.display.flip()
        
        time.sleep(.25)
        
        running = False    
    
    #Update the display
    pygame.display.flip()

    if (score/60) < 999:
        score += 1

    clock.tick(60)
    
print("Your score was: " + str(round(score/60)))

pygame.quit()
