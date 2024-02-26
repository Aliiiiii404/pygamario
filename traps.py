import pygame


class Trap(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            # set the sprite sheet to run animation
            self.set_sprite_sheet('trap-on-38.png')
            self.image = self.get_image(0, 0)
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect()
            self.position = [x, y]
            # the trap speed
            self.speed = 0.1
        # Set the sprite sheet
        def set_sprite_sheet(self, sheet_name):
            self.sprite_sheet = pygame.image.load(f'./maps/adventure/Traps/Saw/{sheet_name}')
        # the trap movement
        def move_right(self):
            self.position[0] += self.speed 
            self.rect.topleft = self.position
        def move_left(self):
            self.position[0] -= self.speed
            self.rect.topleft = self.position

        def get_image(self, x, y):
           image = pygame.Surface([32, 32])
           image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
           return image
        
        def get_position(self):
            return self.rect

        def update(self):
            pass

