import pygame

# ----- CONSTANTS
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (94, 243, 140)
WIDTH = 816
HEIGHT = 616
TITLE = "test subject"


# ----- Classes ------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.image = pygame.image.load()
        width = 40
        height = 60
        self.image = pygame.Surface([width, height])
        # ___Hitbox___
        self.rect = self.image.get_rect()
        self.image.fill(RED)

        # ___Speed of the player___
        self.vel_x = 0
        self.vel_y = 0

        # Added this cause plagiarism :D
        # Supposed to be list of things the sprites bump into
        self.level = None

    def update(self):
        """Player's movement"""
        self.calc_grav()

        # ___Hit Reg___
        # _Horizontal_
        self.rect.x += self.vel_x

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.vel_x > 0:
                self.rect.right = block.rect.left
            elif self.vel_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # _Vertical_
        self.rect.y += self.vel_y

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

            # Reset our position based on the top/bottom of the object.
            if self.vel_y > 0:
                self.rect.bottom = block.rect.top
            elif self.vel_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.vel_y = 0

    def calc_grav(self):
        """The Earth is flat things just fall"""
        if self.vel_y == 0:
            self.vel_y = 1
        else:
            self.vel_y += .35

        # See if we are on the ground.
        if self.rect.y >= HEIGHT - self.rect.height and self.vel_y >= 0:
            self.vel_y = 0
            self.rect.y = HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= HEIGHT:
            self.vel_y = -10

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.vel_x = -6

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.vel_x = 6

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.vel_x = 0


# TODO: platforms
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()


class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player

        # Background image
        self.background = None

    # Update everything on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(BLACK)

        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


class Field_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform 616 - 816 player 40 - 60
        level = [
            # ____border____
            # __sides__
            [8, 616, 0, 0],
            [8, 616, 808, 0],
            # __ top and bottom__
            [816, 8, 0, 0],
            [816, 8, 0, HEIGHT - 8],
            # __map platforms__
            [100, 8, 8, 88],
            [100, 8, 708, 88],
            [200, 8, WIDTH/2 - 100, 158],
            [100, 8, 108, 228],
            [100, 8, WIDTH - 208, 228],
            [100, 8, 8, 328],
            [100, 8, WIDTH - 108, 328],
            [100, 8, WIDTH/2 - 200, 412],
            [100, 8, WIDTH/2 + 100, 412],
            [100, 8, 8, HEIGHT - 120],
            [100, 8, WIDTH - 108, HEIGHT - 120],
            [50, 50, WIDTH/2 - 25, HEIGHT - 88],
            [200, 180, WIDTH/2 - 100, HEIGHT - 348]
        ]

        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)


# done players
# done walls
# TODO: player sprites
# TODO: bullet sprites
# TODO: menu
# TODO: animation
# TODO: Background
# TODO: sounds
# TODO: stages


def main():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()

    # ----- SPRITE GROUPS
    player_1 = Player()
    player_2 = Player()

    # -----  FIELD LIST (add more here)
    Field_list = []
    Field_list.append(Field_01(player_1))
    Field_list.append(Field_01(player_2))

    # ----- for field selection
    Field_selected_num = 0
    Field_selected = Field_list[Field_selected_num]
    player_1.level = Field_selected
    player_2.level = Field_selected

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player_1)
    all_sprites.add(player_2)

    # ----- Player's starting spawn point
    player_1.rect.x = 9
    player_1.rect.y = HEIGHT - player_1.rect.height - 10
    player_2.rect.x = 9
    player_2.rect.y = HEIGHT - player_2.rect.height - 10

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # _____Player 1 movement_____
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_1.go_left()
                if event.key == pygame.K_RIGHT:
                    player_1.go_right()
                if event.key == pygame.K_UP:
                    player_1.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player_1.vel_x < 0:
                    player_1.stop()
                if event.key == pygame.K_RIGHT and player_1.vel_x > 0:
                    player_1.stop()

            # _____Player 2 movement_____
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player_2.go_left()
                if event.key == pygame.K_d:
                    player_2.go_right()
                if event.key == pygame.K_w:
                    player_2.jump()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and player_2.vel_x < 0:
                    player_2.stop()
                if event.key == pygame.K_d and player_2.vel_x > 0:
                    player_2.stop()

        # ----- LOGIC
        all_sprites.update()
        Field_selected.update()

        # ----- DRAW
        screen.fill(BLACK)
        Field_selected.draw(screen)
        all_sprites.draw(screen)

        # ----- UPDATE
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
