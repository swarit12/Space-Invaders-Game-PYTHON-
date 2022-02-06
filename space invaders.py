import sys
import pygame
import random
from pygame import mixer
from pygame.constants import QUIT

pygame.init()

# COLOURS
green = (0, 250, 0)
black = (0,0,0)
white = (250,250,250)
yellow = (255, 255, 0)

# Game Specific Variables
screen_width = 850
screen_height = 680
screen = pygame.display.set_mode((screen_width, screen_height))
title = pygame.display.set_caption("SPACE INVADERS")
icon_img = pygame.image.load("C:\\Users\Shashank-dt\Desktop\game sprites\Space Invaders\\ship.png")
icon_img = pygame.transform.scale(icon_img, (150, 150))
icon = pygame.display.set_icon(icon_img)
alien_img = pygame.image.load("C:\\Users\Shashank-dt\Desktop\game sprites\Space Invaders\enemy1.png")
alien_img = pygame.transform.scale(alien_img, (80, 80))
alien_img2 = pygame.image.load("C:\\Users\Shashank-dt\Desktop\game sprites\Space Invaders\enemy2.png")
alien_img2 = pygame.transform.scale(alien_img2, (80, 80))
alien_img3 = pygame.image.load("C:\\Users\Shashank-dt\Desktop\game sprites\Space Invaders\enemy3.png")
alien_img3 = pygame.transform.scale(alien_img3, (80, 80))
welcome_img = pygame.image.load("C:\\Users\Shashank-dt\Desktop\game sprites\Space Invaders\welcome_screen.jpg")
welcome_img = pygame.transform.scale(welcome_img, (700, 700))
background = pygame.image.load("C:\\Users\Shashank-dt\Desktop\game sprites\Space Invaders\\background.png")
background = pygame.transform.scale(background, (screen_width, screen_height))
font= pygame.font.SysFont("Comic Sans MS", 20)
font2= pygame.font.SysFont("Comic Sans MS", 30)
font3= pygame.font.SysFont("Comic Sans MS", 25)
exit = False
game_over = False
player_x= screen_width/2
player_y= 530
enemy_row= 4
enemy_col = 10
player_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
alien_bulet_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
level_group = pygame.sprite.Group()
fps =  60
clock = pygame.time.Clock()
lives = 3
score = 0
level = 1
btn_color = (255, 255, 255)
btn_color2= (100, 100, 100)

def display_text(text, color, x, y):
    screen_text=font.render(text, True, color)
    screen.blit(screen_text, [x,y])

def display_text2(text, color, x, y):
    screen_text=font2.render(text, True, color)
    screen.blit(screen_text, [x,y])

def display_text3(text, color, x, y):
    screen_text=font3.render(text, True, color)
    screen.blit(screen_text, [x,y])

def main_menu():
    with open("C:\\Users\Shashank-dt\Desktop\Game files\high score(for space invaders).txt", "r")as f:
        highscore = f.read()

    with open("C:\\Users\Shashank-dt\Desktop\Game files\highest level.txt", "r")as j:
        highest_level = j.read()

    def button(x, y):
        mouse = pygame.mouse.get_pos()

        if x <= mouse[0] <= x + 150 and y <= mouse[1] <= y + 60:
            pygame.draw.rect(screen, btn_color2, [x, y, 150, 60])
            display_text2("Play", white, 390, 410)

        else:
            pygame.draw.rect(screen, btn_color, [x, y, 150, 60])
            display_text2("Play", black, 390, 410)

    global exit
    while not exit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if screen_width/2.5 <= mouse[0] <= screen_width/2.5 + 150 and 405 <= mouse[1] <= 405 + 60:
                    main_game()

        mouse = pygame.mouse.get_pos()
        screen.fill(black)
        screen.blit(welcome_img, (80,-150))
        button(screen_width/2.5, 405)
        screen.blit(icon_img, (100, 400))
        screen.blit(alien_img, (550, 420))
        screen.blit(alien_img2, (650, 420))
        screen.blit(alien_img3, (750, 420))
        display_text3("HIGHSCORE: "+str(highscore), white, 160, 600)
        display_text3('HIGHEST LEVEL: '+ str(highest_level),white,  500, 600)
        pygame.display.update()

def main_game():
    start_time = pygame.time.get_ticks()
    alien_cooldown = 800

    with open("C:\\Users\Shashank-dt\Desktop\Game files\high score(for space invaders).txt")as f:
        highscore = f.read()
    
    with open("C:\\Users\Shashank-dt\Desktop\Game files\highest level.txt", "r")as j:
        highest_level = j.read()

    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(f"C:\\Users\Shashank-dt\Desktop\game sprites"
                                           f"\Space Invaders\ship.png")
            self.image = pygame.transform.scale(self.image, (90,90)).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.start_time = pygame.time.get_ticks()

        def update(self):
            speed = 8

            cooldown = 500

            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and self.rect.left > 10:
                self.rect.x -= speed
            if key[pygame.K_RIGHT] and self.rect.right  < screen_width-10:
                self.rect.x += speed
            current_time = pygame.time.get_ticks()

            if key[pygame.K_SPACE] and current_time-self.start_time > cooldown:
                bullet = Bullets(self.rect.centerx, self.rect.top)
                bullet_group.add(bullet)
                bullet_sound = mixer.Sound("C:\\Users\Shashank-dt\Desktop\game sprites\Space Invaders\img_laser.wav")
                bullet_sound.play()
                self.start_time = current_time

            self.mask = pygame.mask.from_surface(self.image)

            if lives == 0:
                game_over = True
                sound = mixer.Sound("C:\\Users\Shashank-dt\Desktop\game sprites\Space Invaders\img_explosion2.wav")
                mixer.Sound.play(sound)
                self.kill()
    player = Player(player_x, player_y)
    player_group.add(player)

    class enemies(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(f"C:\\Users\Shashank-dt\Desktop\game sprites"
                                 f"\Space Invaders\enemy{str(random.randint(1,3))}.png")
            self.image = pygame.transform.scale(self.image, (25 ,25)).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = [x ,y]
            self.move_counter = 0
            self.move_direct = 1

        def update(self):
            self.rect.x += self.move_direct
            self.move_counter += 1
            if abs(self.move_counter)>150:
                self.move_direct *= -1
                self.move_counter *= self.move_direct
            self.mask = pygame.mask.from_surface(self.image)


    class Alien_Bullets(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(f"C:\\Users\Shashank-dt\Desktop\game sprites"
                                 f"\Space Invaders\\alien_bullet.png")
            self.image = pygame.transform.scale(self.image, (15, 15)).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]

        def update(self):
            if self.rect.y >= screen_height-50:
                self.kill()
            self.rect.y += 5
            if pygame.sprite.spritecollide(self, player_group, False, pygame.sprite.collide_mask):
                self.kill()
                global lives
                lives -= 1
                explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
                explosion_group.add(explosion)
            if pygame.sprite.spritecollide(self, wall_group, True):
                self.kill()

    class Bullets(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(f"C:\\Users\Shashank-dt\Desktop\game sprites"
                                 f"\Space Invaders\\bullet.png")
            self.image = pygame.transform.scale(self.image, (20 ,22)).convert_alpha()
            self.rect = self.image.get_rect()
            self.rect.center = [x ,y]

        def update(self):
            if self.rect.y <= 0:
                self.kill()
            self.rect.y -= 6
            if pygame.sprite.spritecollide(self, enemy_group, True, pygame.sprite.collide_mask):
                sound = mixer.Sound("C:\\Users\Shashank-dt\Desktop\game sprites\Space Invaders\img_explosion.wav")
                mixer.Sound.play(sound)
                self.kill()
                explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
                explosion_group.add(explosion)
                global score
                score += 10

            if pygame.sprite.spritecollide(self, wall_group, True):
                self.kill()
            self.mask = pygame.mask.from_surface(self.image)


    class Explosion(pygame.sprite.Sprite):
        def __init__(self, x, y, size):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load(f"C:\\Users\Shashank-dt\Desktop\game sprites"
                                           f"\Space Invaders\\explosion.png")
            if size== 1:
                self.image = pygame.transform.scale(self.image, (40, 40))
            if size==2:
                self.image = pygame.transform.scale(self.image, (50, 50))
            if size==3:
                self.image = pygame.transform.scale(self.image, (100, 100))
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]
            self.counter = 0

        def update(self, explosion):
            explosion_speed = explosion

            self.counter += 1

            if self.counter>= explosion_speed:
                self.counter = 0
                self.kill()
    

    class walls(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface([8,8])
            self.image.fill(green)
            self.rect = self.image.get_rect()
            self.rect.center = [x, y]


    def create_enemy():
        for row in range(enemy_row):
            for col in range(enemy_col):
                green_enemy = enemies(200+col*50, 90 + row * 60)
                enemy_group.add(green_enemy)

    def create_walls():
        for i in range(3):
            for row in range(6):
                for column in range(13):
                    wall = walls((90+(275*i))+(10*column), 360 + (10*row))
                    wall_group.add(wall)
    
    def next_level():
        enemy_group.empty()
        bullet_group.empty()
        alien_bulet_group.empty()
        explosion_group.empty()
        display_text2("NEXT LEVEL +", white, 350, 200)
        pygame.display.update()
        pygame.time.delay(3000)
        create_enemy()        

    create_walls()
    create_enemy()
    global exit, game_over
    while exit== False :
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                exit = True

        current_time = pygame.time.get_ticks()

        if current_time - start_time > alien_cooldown:
            if len(enemy_group)>0:
                selected_alien = random.choice(enemy_group.sprites())
                shoot_bullet = Alien_Bullets(selected_alien.rect.centerx, selected_alien.rect.bottom)
                alien_bulet_group.add(shoot_bullet)
                start_time = current_time

        if lives == 0:
            player_group.empty()
            game_over = True
        

        if len(enemy_group) == 0:

            global level
            level += 1
            screen.fill(black)
            level_group.update()
            screen.blit(background, (0,0))
            player_group.draw(screen)
            enemy_group.draw(screen)
            wall_group.draw(screen)
            level_group.draw(screen)
            display_text("LEVEL: "+ str(level), white, 400, 20)
            display_text("SCORE: "+str(score), white, 40, 600)
            display_text("SPACE INVADERS", white, 350, 600)
            display_text("LIVES: "+str(lives), white, 720, 600)
            next_level()
        
        if score > int(highscore):
            highscore = score
        
        if level > int(highest_level):
            highest_level = level
    
        explosion_group.update(10)
        level_group.update()
        screen.fill(black)
        screen.blit(background, (0,0))
        player_group.draw(screen)
        enemy_group.draw(screen)
        explosion_group.draw(screen)
        wall_group.draw(screen)
        level_group.draw(screen)
        display_text("LEVEL: "+ str(level), white, 400, 20)
        display_text("SCORE: "+str(score), white, 40, 600)
        display_text("SPACE INVADERS", white, 350, 600)
        display_text("LIVES: "+str(lives), white, 720, 600)

        if not game_over:
            player_group.update()
            bullet_group.update()
            enemy_group.update()
            alien_bulet_group.update()
            alien_bulet_group.draw(screen)
            bullet_group.draw(screen)

        if game_over:
            display_text("GAME OVER!! YOU LOST", white, screen_width/3, screen_height/2.2)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    with open("C:\\Users\Shashank-dt\Desktop\Game files\high score(for space invaders).txt", "w")as f:
        f.write(str(highscore))
    with open("C:\\Users\Shashank-dt\Desktop\Game files\highest level.txt", "w")as j:
        j.write(str(highest_level))
    sys.exit()
    
main_menu()