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
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        # font
        self.font = pygame.font.Font(None, 36)
        # create player
        player_position = tmx_data.get_object_by_name("player_spawn")
        self.player = Player(player_position.x, player_position.y)
        # create map layers
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=1)
        self.group.add(self.player)
        # checkpoint text
        self.checkpoint_text = tmx_data.get_object_by_name("checkpointText")
        self.checkpoint_text.text = "test"
        self.checkpoint_text.visible = 1
        # gravity zones
        self.gravity_zones = []
        self.collision_zones = []
        self.checkpoint_position = []
        for obj in tmx_data.objects:
            if obj.type == "GravityZones":
                self.gravity_zones.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "collision":
                self.collision_zones.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "checkpoint":
                self.checkpoint_position = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
    # Handle input
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        # handle movement
        if pressed[pygame.K_SPACE]:
            self.player.jump(self.gravity_zones)
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()
        elif pressed[pygame.K_RETURN] or pressed[pygame.K_KP_ENTER]:
            # zoom on the player
            if self.map_layer.zoom != 2:
                self.map_layer.zoom = 2

    # Check if checkpoint is reached
    def checkpoint_reached(self, checkpoint_position):
        player_position = self.player.get_position()
        if player_position.colliderect(checkpoint_position):
            self.checkpoint_text.visible = 0
            print("ur here")
    # update
    def update(self):
        self.group.update()
        self.player.gravity(self.gravity_zones)
        for sprite in self.group.sprites():
            if sprite.feet.collidelist(self.collision_zones) > -1:
                self.player.move_back()
        self.checkpoint_reached(self.checkpoint_position)
    # Run until the user asks to quit
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            # the camera will keep the player centered
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
        pygame.quit()




