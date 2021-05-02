import pygame
import os
from PIL import Image, ImageDraw


WIDTH = 750
HEIGHT = 500
FPS = 40

PLAYER_SIZE = (50,) * 2
ORD_SIZE = (50,) * 2

BLOCK_SIZE = 100

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (225, 225, 0)

FORWARD = 0
BACKWARD = 1
RIGHT = 2
LEFT = 3

PLAYER_SPEED = 10

BACKGROUND_COLOR = (204, 51, 51)


class Block(pygame.sprite.Sprite):
    def __init__(self, coord, color):
        super(Block, self).__init__()
        self.image = pygame.Surface((BLOCK_SIZE,)*2)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = coord[0] * BLOCK_SIZE
        self.rect.y = coord[1] * BLOCK_SIZE


class Connect:
    @staticmethod
    def get_data():
        coord = [{'type': 'player', 'coord': [100, 100], 'parameters': RED},
                 {'type': 'ore', 'coord': [150, 150]},
                 {'type': 'block', 'coord': [0, 0], 'parameters': GREEN},
                 {'type': 'block', 'coord': [1, 0], 'parameters': RED}
                 ]
        return coord

    @staticmethod
    def send(*flags):
        pass


class Game:
    def __init__(self):
        self.connect = Connect()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("My Game")
        self.clock = pygame.time.Clock()
        self.game_loop()

    def load(self):
        load = self.connect.get_data()
        return load

    def draw_sprites(self):
        sprites = pygame.sprite.Group()
        ores = pygame.sprite.Group()
        blocks = pygame.sprite.Group()
        loaded_sprites = self.load()
        for i in loaded_sprites:
            if i['type'] == 'player':
                sprites.add(Player(i['coord'], i['parameters']))
            if i['type'] == 'ore':
                ores.add(Ore(i['coord']))
            if i['type'] == 'block':
                blocks.add(Block(i['coord'], i['parameters']))
        sprites.update()
        ores.update()
        blocks.update()
        blocks.draw(self.screen)
        ores.draw(self.screen)
        sprites.draw(self.screen)

    def game_loop(self):
        forward = False
        backward = False
        right = False
        left = False
        running = True
        while running:
            self.screen.fill(WHITE)
            self.draw_sprites()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        left = True
                    if event.key == pygame.K_UP:
                        backward = True
                    if event.key == pygame.K_DOWN:
                        forward = True
                    if event.key == pygame.K_RIGHT:
                        right = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        left = False
                    if event.key == pygame.K_UP:
                        backward = False
                    if event.key == pygame.K_DOWN:
                        forward = False
                    if event.key == pygame.K_RIGHT:
                        right = False
            self.connect.send(forward, backward, left, right)
            pygame.display.flip()
            self.clock.tick(FPS)


class CircleMaker:
    @staticmethod
    def make(color, player_number: int):
        img = Image.new('RGB', PLAYER_SIZE, color=BACKGROUND_COLOR)
        drawer = ImageDraw.Draw(img)
        drawer.ellipse((0, 0, *PLAYER_SIZE), fill=color)
        if not os.path.isdir("res"):
            os.mkdir("res")
        if not os.path.isdir("res/images"):
            os.mkdir("res/images")
        img.save(f'res/images/circle{player_number}.png')
        return f'res/images/circle{player_number}.png'


class PlayerTexture:
    def __init__(self, color):
        self.color = color

    def get(self):
        return pygame.image.load(CircleMaker.make(self.color, 1))


class Player(pygame.sprite.Sprite):
    def __init__(self, coord, color):
        super().__init__()
        self.image = PlayerTexture(color).get()
        self.image.set_colorkey(BACKGROUND_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = coord[0]
        self.rect.y = coord[1]


class OreTexture:
    def __init__(self, color):
        self.color = color

    def get(self):
        return pygame.image.load(CircleMaker.make(self.color, 100))


class Ore(pygame.sprite.Sprite):
    def __init__(self, coord):
        super().__init__()
        self.image = OreTexture(YELLOW).get()
        self.image.set_colorkey(BACKGROUND_COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.rect.x = coord[0]
        self.rect.y = coord[1]


def main(name):
    print('starting game with name:', name)
    Game()
