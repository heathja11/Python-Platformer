import pygame
from config import *
from random import choice, randrange, uniform
vec = pygame.math.Vector2

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()
    def image_retrieve(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width // 2, height // 2))
        return image

class Spritesheet_bg:
    # utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet_bg = pygame.image.load(filename).convert()

    def image_retrieve(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet_bg, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width, height ))
        return image
class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = player_layer
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.current_frame = 0
        self.last_update = 0
        self.player_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (200, game_width / 2)
        self.pos = vec(200, game_width / 2)
        self.vel = vec(5, 0)
        self.acc = vec(0, 0)
    def player_images(self):
        self.standing_frames = [self.game.spritesheet.image_retrieve(0, 1032, 128, 256),
                                self.game.spritesheet.image_retrieve(130, 0, 128, 256)]
        for frame in self.standing_frames:
            frame.set_colorkey(black)
        self.walk_frames_r = [self.game.spritesheet.image_retrieve(0, 258, 128, 256),
                              self.game.spritesheet.image_retrieve(0, 0, 128, 256)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(black)
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.image_retrieve(0, 1290, 128, 256)
        self.jump_frame.set_colorkey(black)
    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
    def jump(self):
        # jump only if standing on a platform
        self.rect.y += 2
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.y -= 2
        if hits and not self.jumping:
            #self.game.jump_sound.play()
            self.jumping = True
            self.vel.y = -player_jump_speed
    def update(self):
        self.animate()
        self.acc = vec(0, player_gravity)
        key_press = pygame.key.get_pressed()
        # Player Physics
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the game_display
        '''if self.pos.x > game_width + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = game_width + self.rect.width / 2'''
        self.rect.midbottom = self.pos
        # if key_press[pygame.K_a]:
        # self.acc.x = -player_acceleration
        # if key_press[pygame.K_d]:
        # self.acc.x = player_acceleration
        # apply friction
        '''self.acc.x += self.vel.x * player_friction'''

    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        '''if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom'''
        self.mask = pygame.mask.from_surface(self.image)
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        self.mask = pygame.mask.from_surface(self.image)

    def shoot(self):
        bullet = Bullet(self.game, self.rect.centerx + 50, self.rect.centery +50)
        self.game.all_sprites.add(bullet)
        self.game.bullets.add(bullet)


class Cloud(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = cloud_layer
        self.groups = game.all_sprites, game.clouds
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        scale = randrange(50, 101) / 100
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * scale),
                                                     int(self.rect.height * scale)))
        self.rect.x = randrange(800 - self.rect.width)
        self.rect.y = randrange(-600, -50)

    def update(self):
        if self.rect.right < game_width - game_width:
            self.kill()

class Sign(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = sign_layer
        self.groups = game.all_sprites, game.signs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.image_retrieve(1950, 1820, 128, 128)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = bullet_layer
        self.groups = game.all_sprites, game.bullets
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((20, 10))
        self.image.fill(yellow)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedx = +10
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        self.rect.x += self.speedx
        if self.rect.left > 800:
            self.kill()



class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = platform_layer
        self.groups = game.all_sprites, game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        round_rock = self.game.spritesheet.image_retrieve(1170, 1040, 128, 128)
        square_rock = self.game.spritesheet.image_retrieve(1560, 390, 128, 128)
        #blocks = [round_rock, square_rock]
        self.image = square_rock
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < coin_percent_gold:
            CoinGold(self.game, self)
        if randrange(100) < coin_percent_silver:
            CoinSilver(self.game, self)
        if randrange(100) < coin_percent_bronze:
            CoinBronze(self.game, self)
        self.mask = pygame.mask.from_surface(self.image)
        if self.rect.right < 0:
            self.kill()

class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = platform_layer
        self.groups = game.all_sprites, game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game


        #blocks = [round_rock, square_rock]
        self.image = self.game.spritesheet.image_retrieve(1820, 1430, 128, 128)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if self.rect.right < 0:
            self.kill()

class Bridge(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = platform_layer
        self.groups = game.all_sprites, game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game


        #blocks = [round_rock, square_rock]
        self.image = self.game.spritesheet.image_retrieve(2340, 0, 128, 128)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if self.rect.right < 0:
            self.kill()
class BgStructures_castle(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = structure_layer
        self.groups = game.all_sprites, game.bg_structures
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet_bg.image_retrieve(743, 1174, 204, 182),
                  self.game.spritesheet_bg.image_retrieve(745, 886, 204, 182),




                   ]
        self.image = choice(images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        #scale = randrange(50, 101) / 100
        #self.image = pygame.transform.scale(self.image, (int(self.rect.width * scale),
                                                     #int(self.rect.height * scale)))
        self.rect.x = randrange(game_width - 1000, game_width + 1000)
        self.rect.y = -340
        if self.rect.x < 0:
            self.kill()

    def update(self):
        if self.rect.right < game_width - game_width:
            self.kill()

class BgStructures_tree(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = structure_layer
        self.groups = game.all_sprites, game.bg_structurestree
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet_bg.image_retrieve(1285, 901, 136, 293),
                  self.game.spritesheet_bg.image_retrieve(1275, 606, 136, 293),





                   ]
        self.image = choice(images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        #scale = randrange(50, 101) / 100
        #self.image = pygame.transform.scale(self.image, (int(self.rect.width * scale),
                                                     #int(self.rect.height * scale)))
        self.rect.x = randrange(game_width - 1000, game_width + 1000)

        self.rect.y = -450
        if self.rect.x < 0:
            self.kill()

    def update(self):
        if self.rect.right < game_width - game_width:
            self.kill()

class BgStructures_tree2(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = structure_layer
        self.groups = game.all_sprites, game.bg_structurestree2
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet_bg.image_retrieve(1322, 0, 129, 230),
                  self.game.spritesheet_bg.image_retrieve(1322, 0, 129, 230),





                   ]
        self.image = choice(images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        #scale = randrange(50, 101) / 100
        #self.image = pygame.transform.scale(self.image, (int(self.rect.width * scale),
                                                     #int(self.rect.height * scale)))
        self.rect.x = randrange(game_width - 1000, game_width + 1000)

        self.rect.y = -380
        if self.rect.x < 0:
            self.kill()

    def update(self):
        if self.rect.right < game_width - game_width:
            self.kill()

class BgStructures_tower(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = background_layer
        self.groups = game.all_sprites, game.bg_structures
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet_bg.image_retrieve(1647, 262, 66, 227),
                  self.game.spritesheet_bg.image_retrieve(1641, 1164, 66, 227),





                   ]
        self.image = choice(images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        #scale = randrange(50, 101) / 100
        #self.image = pygame.transform.scale(self.image, (int(self.rect.width * scale),
                                                     #int(self.rect.height * scale)))
        self.rect.x = randrange(game_width - 1000, game_width + 1000)

        self.rect.y = -380
        if self.rect.x < 0:
            self.kill()

    def update(self):
        if self.rect.right < game_width - game_width:
            self.kill()
class CoinGold(pygame.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = coin_layer
        self.groups = game.all_sprites, game.coins
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = 'gold'
        self.image = self.game.spritesheet.image_retrieve(2730, 0, 128, 128)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()


class CoinSilver(pygame.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = coin_layer
        self.groups = game.all_sprites, game.coins
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = 'silver'
        self.image = self.game.spritesheet.image_retrieve(2600, 1820, 128, 128)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()


class CoinBronze(pygame.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = coin_layer
        self.groups = game.all_sprites, game.coins
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = 'bronze'
        self.image = self.game.spritesheet.image_retrieve(2730, 130, 128, 128)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()
class Mob(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = mob_layer
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image_up = self.game.spritesheet.image_retrieve(260, 258, 128, 256)
        self.image_up.set_colorkey(black)
        self.image_down = self.game.spritesheet.image_retrieve(260 ,0, 128 ,256)
        self.image_down.set_colorkey(black)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, game_width + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > game_width:
            self.vx *= -1
        self.rect.y = randrange(game_height /4, game_height / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > game_width + 100 or self.rect.right < -100:
            self.kill()


class MobBee(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = mob_layer
        self.groups = game.all_sprites, game.mobs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game

        self.image_up = self.game.spritesheet.image_retrieve(3510, 130, 128, 128)
        self.image_up.set_colorkey(black)
        self.image_down = self.game.spritesheet.image_retrieve(3380, 1820, 128, 128)
        self.image_down.set_colorkey(black)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, game_width + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > game_width:
            self.vx *= -1
        self.rect.y = randrange(game_height / 4, game_height / 2)
        self.vy = 0
        self.dy = 0.5

    def update(self):
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > game_width + 100 or self.rect.right < -100:
            self.kill()

class Shroom(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = mushroom_layer
        self.groups = game.all_sprites, game.shrooms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet.image_retrieve(2080, 780, 128, 128),
                  self.game.spritesheet.image_retrieve(2080, 650, 128, 128)
                  ]
        self.image = choice(images)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)


class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Spikes(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = spike_layer
        self.groups = game.all_sprites, game.spikes
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.image_retrieve(1950, 1560, 128, 128)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)

class Rocks(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = spike_layer
        self.groups = game.all_sprites, game.rocks
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = self.game.spritesheet.image_retrieve(2080, 390, 128, 128)
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)