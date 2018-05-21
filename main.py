import pygame
import random
import time
from config import *
from sprites import *
from os import path
from level_list import *

class Game:
    def __init__(self):
        pygame.init()
        #pygame.mixer.init()#############
        self.game_display = pygame.display.set_mode((game_width, game_height))
        pygame.display.set_icon(game_icon)
        pygame.display.set_caption(game_name)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(font_type)
        self.load_data()

    def load_data(self):
        #############
        self.dir = path.dirname(__file__)
        with open(path.join(self.dir, highscore_file), 'r') as hs:
            try:
                self.highscore = int(hs.read())
            except:
                self.highscore = 0
        #################
        img_dir = path.join(self.dir, 'img')
        self.spritesheet = Spritesheet(path.join(img_dir, spritesheet_image))
        self.spritesheet_bg = Spritesheet_bg(path.join(img_dir, spritesheet_image_background))
        # cloud images
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pygame.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())
        # load sounds
        self.sound_dir = path.join(self.dir, 'sound')
        ############################
        #self.jump_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'Jump33.wav'))
        #self.boost_sound = pygame.mixer.Sound(path.join(self.sound_dir, 'Boost16.wav'))

    def new(self):
        # start a new game
        self.score = 0
        self.distance = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        self.bg_structures = pygame.sprite.Group()
        self.bg_structurestree = pygame.sprite.Group()
        self.bg_structurestree2 = pygame.sprite.Group() ########################## Groups
        self.shrooms = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.signs = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()
        self.player = Player(self)
        for plat in platform_array:
            Platform(self, *plat)
        for water in water_array:
            Water(self, *water)
        for bridge in bridge_array:
            Bridge(self, *bridge)
        for shroom in mushroom_array: ########################### draw things
            Shroom(self, *shroom)
        for sign in sign_array:
            Sign(self, *sign)
        for spike in spike_array:
            Spikes(self, *spike)
        for rock in rock_array:
            Rocks(self, *rock)
        self.mob_timer = 0
        #pygame.mixer.music.load(path.join(self.sound_dir, 'Happy Tune.ogg')) ##################### Main Music
        for object in range(8):
            c = Cloud(self)
            c.rect.y += 500
        for object in range(2):
            c = BgStructures_castle(self)
            c.rect.y += 700
        for object in range(2):
            c = BgStructures_tree(self)
            c.rect.y += 700
        for object in range(1):
            c = BgStructures_tree2(self)
            c.rect.y += 700
        self.run()
    def run(self):
        # Game Loop
        #pygame.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()
        #pygame.mixer.music.fadeout(500)

    def update(self):
        # Game Loop - Update
        self.all_sprites.update()

        # spawn a mob?
        now = pygame.time.get_ticks()
        if now - self.mob_timer > 3000 + random.choice([0, 500, 1000]):
            self.mob_timer = now
            Mob(self)
            MobBee(self)
        # hit mobs?
        mob_hits = pygame.sprite.spritecollide(self.player, self.mobs, False, pygame.sprite.collide_mask)
        if mob_hits:
            self.playing = False
        bullet_hits = pygame.sprite.groupcollide(self.mobs, self.bullets, True, True)
        if bullet_hits:
            self.score += 10
        spike_hits = pygame.sprite.spritecollide(self.player, self.spikes, False, pygame.sprite.collide_mask)
        if spike_hits:
            self.playing = False
        if now > 1:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            for hit in hits:
                if hit.rect.bottom > self.player.rect.bottom:
                    if self.player.pos.x < hit.rect.right and self.player.pos.x > hit.rect.left:
                        if self.player.pos.y < hit.rect.centery:
                            self.player.pos.y = hit.rect.top
                            self.player.vel.y = 0
                            self.player.jumping = False
        if self.player.rect.right >= 300:
            self.distance += 0.1
            self.player.pos.x -= max(abs(self.player.vel.x), 2)
            for cloud in self.clouds:
                cloud.rect.x -= max(abs(self.player.vel.x / 2), 4)
            for struct in self.bg_structures:
                struct.rect.x -= max(abs(self.player.vel.x / 2), 5)
            for struct in self.bg_structurestree:
                struct.rect.x -= max(abs(self.player.vel.x / 2), 5)
            for struct in self.bg_structurestree2:
                struct.rect.x -= max(abs(self.player.vel.x / 2), 5)
            for sign in self.signs:
                sign.rect.x = sign.rect.x - max(abs(self.player.vel.x / 2), 7)
            for shroom in self.shrooms:
                shroom.rect.x = shroom.rect.x - max(abs(self.player.vel.x / 2), 7)
            for mob in self.mobs:
                mob.rect.x -= max(abs(self.player.vel.x), 2)
            for spike in self.spikes:
                spike.rect.x -= max(abs(self.player.vel.x), 2)
            for plat in self.platforms:
                plat.rect.x -= max(abs(self.player.vel.x), 2)
            for rock in self.rocks:
                rock.rect.x -= max(abs(self.player.vel.x), 7)
            for coin in self.coins:
                coin.rect.x -= max(abs(self.player.vel.x), 5)
            pygame.display.update()
        #move world up

        coin_hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in coin_hits:
            if coin.type == 'gold':
                self.score += 50
            if coin.type == 'silver':
                self.score += 10
            if coin.type == 'bronze':
                self.score += 1
        # Die
        if self.player.rect.bottom > game_height:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False
        while len(self.clouds) < 8:
            c = Cloud(self)
            c.rect.y += 500
            c.rect.x += 800
        if randrange(100) < 1:
            c = BgStructures_castle(self)
            c.rect.x += 100
        while len(self.bg_structurestree) < 2:
            c = BgStructures_tree(self)
            c.rect.x += 600
        while len(self.bg_structurestree2) < 2:
            c = BgStructures_tree2(self)
            c.rect.x += 600

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self.player.jump_cut()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
                if event.key == pygame.K_w:
                    self.player.jump()

    def draw(self):
        # Game Loop - draw
        self.game_display.fill(background_colour)
        #self.bg = pygame.image.load("background1.png") ###########################
        #self.game_display.blit(self.bg, (0, 0))
        self.all_sprites.draw(self.game_display)
        self.text_on_screen(str(self.score), 22, white, game_width / 2, 15)
        self.text_on_screen("Distance: " + str(round(self.distance, 1)) + 'm', 22, white, game_width - 60, 15)
        # *after* drawing everything, flip the display
        pygame.display.flip()

    def test_button(self, msg, x, y, w, h, ic, ac, action=None):
        MOUSE = pygame.mouse.get_pos()
        CLICK = pygame.mouse.get_pressed()
        if x + w > MOUSE[0] > x and y + h > MOUSE[1] > y:
            pygame.draw.rect(self.game_display, ac, (x, y, w, h))
            if CLICK[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(self.game_display, ic, (x, y, w, h))
        smallText = pygame  .font.SysFont("comicsansms", 20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ((x + (w / 2)), (y + (h / 2)))
        self.game_display.blit(textSurf, textRect)


    def show_start_game_display(self):
        # game splash/start game_display
        #pygame.mixer.music.load(path.join(self.sound_dir, 'Yippee.ogg'))
        #pygame.mixer.music.play(loops=-1)
        self.game_display.fill(background_colour)
        self.text_on_screen(game_name, 48, white, game_width / 2, game_height / 4)
        self.text_on_screen("Test Level Made Using Engine", 22, white, game_width / 2, game_height / 2)
        self.text_on_screen("Press a key to play", 22, white, game_width / 2, game_height * 3 / 4)
        self.text_on_screen("High Score: " + str(self.highscore), 22, white, game_width / 2, 15)
        #self.test_button("Play", 150, 450, 100, 50, green, light_blue)
        pygame.display.flip()
        self.any_key_press()
        #pygame.mixer.music.fadeout(500)

    def show_go_game_display(self):
        # game over/continue
        if not self.running:
            return
        #pygame.mixer.music.load(path.join(self.sound_dir, 'Yippee.ogg'))
        #pygame.mixer.music.play(loops=-1)
        self.game_display.fill(background_colour)
        self.text_on_screen("GAME OVER", 48, white, game_width / 2, game_height / 4)
        self.text_on_screen("Score: " + str(self.score), 22, white, game_width / 2, game_height / 2)
        self.text_on_screen("Press a key to play again", 22, white, game_width / 2, game_height * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.text_on_screen("NEW HIGH SCORE!", 22, white, game_width / 2, game_height / 2 + 40)
            with open(path.join(self.dir, highscore_file), 'w') as f:
                f.write(str(self.score))
        else:
            self.text_on_screen("High Score: " + str(self.highscore), 22, white, game_width / 2, game_height / 2 + 40)
        pygame.display.flip()
        self.any_key_press()
        pygame.mixer.music.fadeout(500)

    def any_key_press(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False
    def text_objects(self, text, font):
        textsurface = font.render(text, True, white)
        return textsurface, textsurface.get_rect()
    def text_on_screen(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.game_display.blit(text_surface, text_rect)
g_start = Game()
g_start.show_start_game_display()
while g_start.running:
    g_start.new()
    g_start.show_go_game_display()

pygame.quit()
