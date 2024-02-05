from itertools import filterfalse
from time import sleep
import pygame


class Player(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            # set the sprite sheet to run animation
            self.set_sprite_sheet('run.png')
            self.frame_index = 0
            self.last_frame_time = pygame.time.get_ticks()
            # Set the duration for each frame
            self.duration = 50
            self.image = self.get_image(0, 0)
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect()
            self.position = [x, y]
            # the player's speed
            self.speed = 3
            self.jump_height = 5
            # the player's direction 1 is right, -1 is left
            self.direction = 1
            # the single jump
            self.singl_jump = 1
            # the player's feet to detect collision
            self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
            self.old_position = self.position.copy()
        # Set the sprite sheet
        def set_sprite_sheet(self, sheet_name):
            self.sprite_sheet = pygame.image.load(f'./maps/adventure/main-characters/mask-dude/{sheet_name}')
        # Movment
        def move_right(self):
            self.direction = 1
            self.position[0] += self.speed
            self.animate_run()
        def move_left(self): 
            self.direction = -1
            self.position[0] -= self.speed
            self.animate_run()
        def move_down(self):
            self.position[1] += self.speed
        def jump(self, gravity_zones):
            self.position[1] -= self.jump_height
            self.animate_jump()
                
        def double_jump(self):
            print("code for double jump didnt go brrrrrrrrr ;(")

        # Movment animation
        def animate_run(self):
            # Update frame index for animation
            self.set_sprite_sheet('run.png')
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time > self.duration:
                self.frame_index = (self.frame_index + 1) % 12
                self.last_frame_time = current_time
            # Update image based on frame index and direction
            frame_offset = self.frame_index * 32
            if self.direction == 1:
                self.image = self.get_image(frame_offset, 0)
            elif self.direction == -1:
                # Flip the image horizontally for left movement
                self.image = pygame.transform.flip(self.get_image(frame_offset, 0), True, False)
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect(topleft=self.position)

        def animate_jump(self):
            self.set_sprite_sheet('jump.png')
            self.frame_index = (self.frame_index + 1) % 1  # Assuming 6 frames for jumping animation
            frame_offset = 0
            if self.direction == 1:
                self.image = self.get_image(frame_offset, 0)
            elif self.direction == -1:
                self.image = pygame.transform.flip(self.get_image(frame_offset, 0), True, False)
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect(topleft=self.position)

        def animate_double_jump(self):
            self.set_sprite_sheet('double-jump.png')
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time > self.duration:
                self.frame_index = (self.frame_index + 1) % 6  # Assuming 6 frames for jumping animation
                self.last_frame_time = current_time
            frame_offset = self.frame_index * 32
            if self.direction == 1:
                self.image = self.get_image(frame_offset, 0)
            elif self.direction == -1:
                self.image = pygame.transform.flip(self.get_image(frame_offset, 0), True, False)
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect(topleft=self.position)

        def save_location(self): 
            self.old_position = self.position.copy()

        def move_back(self):
            self.position = self.old_position
            self.rect.topleft = self.position
            self.feet.midbottom = self.rect.midbottom

        def get_position(self):
            return self.rect

        def gravity(self, gravity_zones):
            default_gravity = 1.5
            gravity_applied = True
            # Check for gravity zones
            for zone in gravity_zones:
                zone_rect = pygame.Rect(zone.x, zone.y, zone.width, zone.height)
                if zone_rect.colliderect(self.rect):
                    gravity_applied = False
                    # whene the player touches the ground switch back to the run animation sprite sheet
                    self.set_sprite_sheet('run.png')
                    break
                else:
                    gravity_applied = True
            # if no collision with gravity zones, apply default gravity
            if gravity_applied:
                self.position[1] += default_gravity

        def update(self):
            self.rect.topleft = self.position
            self.feet.midbottom = self.rect.midbottom
            if self.frame_index == 7:  # Assuming 8 frames, so index 7 is the last frame
                self.is_jumping = False
                # Switch back to the run animation sprite sheet
                self.set_sprite_sheet('run.png')

        def get_image(self, x, y):
           image = pygame.Surface([32, 32])
           image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
           return image


