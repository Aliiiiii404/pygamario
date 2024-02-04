import pygame
import pytmx
import pyscroll
from player import Player

# Game class
class Game:
    # Constructor
    def __init__(self):
        width = 800
        height = 800
        self.screen = pygame.display.set_mode([width, height])
        # the window title
        pygame.display.set_caption("PygaMario")
        # load data from pytmx
        tmx_data = pytmx.util_pygame.load_pygame("maps/map.tmx")
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        # create player
        player_position = tmx_data.get_object_by_name("player_spawn")
        self.player = Player(player_position.x, player_position.y)
        # collision detection
        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        # create map layers
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player)
    
    # Handle input
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        # handle movement
        if pressed[pygame.K_DOWN]:
            self.player.move_down()
            self.player.change_image('down')
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
            self.player.change_image('left')
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
            self.player.change_image('right')
        # handle jump
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                    self.player.change_image('up')
                    self.player.update()
    def update(self):
        self.group.update()
        # check for collision
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.walls) > -1:
                sprite.move_back()

    # Run until the user asks to quit
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.group.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
        pygame.quit()
