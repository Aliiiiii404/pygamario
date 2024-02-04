from time import sleep
import pygame

class Player(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.sprite_sheet = pygame.image.load('./maps/adventure/main-characters/mask-dude/run.png')
            self.image = self.get_image(0, 0)
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect()
            self.position = [x, y]
            self.images = {
                'down' : self.get_image(4, 0),
                'left' : pygame.transform.flip(self.get_image(0, 0), True, False),
                'right' : self.get_image(0, 0),
                'up' : self.get_image(4, 0),
            }
            self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12)
            self.old_position = self.position.copy()
            self.speed = 3
            self.jump_height = 6
            self.jump_count = 0
            self.jumping = False
            self.jump_in_progress = False
        def save_location(self):
            self.old_position = self.position.copy()
        
        def change_image(self, name):
            self.image = self.images[name]
            self.image.set_colorkey((0, 0, 0))
        # Movement methods
        def move_right(self): self.position[0] += self.speed
        def move_left(self): self.position[0] -= self.speed
        def move_up(self): self.position[1] -= self.speed
        def jump(self):
            if not self.jumping:
                self.jumping = True
                self.jump_count = self.jump_height
                self.jump_in_progress = True

            if self.jump_in_progress:
                neg = 1
                if self.jump_count < 0:
                    neg = -1

                self.position[1] -= (self.jump_count ** 2) * 0.8 * neg
                self.jump_count -= 1
                print("Jumping")
                if self.jump_count < -self.jump_height:
                    self.jumping = False
                    self.jump_in_progress = False
                    self.jump_count = self.jump_height
        
        def move_down(self): self.position[1] += self.speed
        
        def update(self):
            self.rect.topleft = self.position
            self.feet.midbottom = self.rect.midbottom
        def move_back(self):
            self.position = self.old_position
            self.rect.topleft = self.position
            self.feet.midbottom = self.rect.midbottom
        def get_image(self, x, y):
            image = pygame.Surface([32, 32])
            image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
            return image

