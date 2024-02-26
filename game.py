import pygame
import pytmx
import pyscroll
from player import Player
from traps import Trap

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
        self.tmx_data = pytmx.util_pygame.load_pygame("maps/map-1.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom = 2
        # font
        self.font = pygame.font.Font(None, 36)
        # create player
        self.player_position = self.tmx_data.get_object_by_name("player_spawn")
        self.player = Player(self.player_position.x, self.player_position.y)
        # set level
        self.level = 1
        # set trap 
        self.trap = None
        # create map layers
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        self.group.add(self.player)
        # gravity zones
        self.gravity_zones = []
        self.collision_zones = []
        self.checkpoint_position = []
        for obj in self.tmx_data.objects:
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
    # Change level 
    def change_level(self, level):
        self.tmx_data = pytmx.util_pygame.load_pygame(f"./maps/map-{level}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)
        map_layer.zoom = 2
        # update collision zones 
        self.gravity_zones = []
        self.collision_zones = []
        self.checkpoint_position = []
        for obj in self.tmx_data.objects:
            if obj.type == "GravityZones":
                self.gravity_zones.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "collision":
                self.collision_zones.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
            if obj.type == "checkpoint":
                self.checkpoint_position = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
            if obj.type == "lava":
                self.lava = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
        # add player 
        self.player = Player(self.player_position.x, self.player_position.y)
        self.group.add(self.player)
    
    # Check if checkpoint is reached
    def checkpoint_reached(self, checkpoint_position):
        level_is_changed = False
        player_position = self.player.get_position()
        if player_position.colliderect(checkpoint_position):
            if level_is_changed == False:
                self.level = self.level + 1
                level_is_changed = True
            self.change_level(self.level)
    # trap
    def create_trap(self):
        if self.level > 1:
            trap_limit1_zone = []
            trap_limit2_zone = []
            for obj in self.tmx_data.objects:
                if obj.type == "trap1_limit1":
                    trap_limit1_zone.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                if obj.type == "trap1_limit2":
                    trap_limit2_zone.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

            trap1_spawn = self.tmx_data.get_object_by_name("trap1_spawn")
            # lava_rect = lava.rect
            self.trap = Trap(trap1_spawn.x, trap1_spawn.y)
            self.group.add(self.trap)
            player_rect = self.player.get_position()
            trap_rect = self.trap.get_position()
            for limit in trap_limit1_zone:
                limit1_rect = pygame.Rect(limit.x, limit.y, limit.width, limit.height)
                if trap_rect.colliderect(limit1_rect):
                    self.trap.move_left()
                    break
            for limit in trap_limit2_zone:
                limit2_rect = pygame.Rect(limit.x, limit.y, limit.width, limit.height)
                if trap_rect.colliderect(limit2_rect):
                    self.trap.move_right()
                    break
                # If trap is not colliding with either limit, move right
                else:
                    self.trap.move_left()
            # if the player touches the trap or the lava, the player will go back to the spawn
            if trap_rect.colliderect(player_rect) or player_rect.colliderect(self.lava):
               self.player.back_to_spawn(self.player_position.x, self.player_position.y)
    # update
    def update(self):
        self.group.update()
        self.player.gravity(self.gravity_zones)
        for sprite in self.group.sprites():
            if self.player.feet.collidelist(self.collision_zones) > -1:
                self.player.move_back()
        self.checkpoint_reached(self.checkpoint_position)
        if self.trap:
            self.trap.update()
    # Run until the user asks to quit
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            self.player.save_location()
            self.handle_input()
            self.update()
            self.create_trap()
            # the camera will keep the player centered
            self.group.center(self.player.rect.center)
            self.group.draw(self.screen)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)
        pygame.quit()

