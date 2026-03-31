import pygame.font


class Button:
    """Class to build the startbutton."""

    def __init__(self, game, msg):
        """Initialize button attributes."""
        self.game = game
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()
        self.width = 160
        self.height = 80

        self.msg = msg

        # Set the dimensions, color and font of the button.
        self.width, self.height = 180, 70
        self.button_color = (184, 105, 98)
        self.text_color = (245, 238, 155)
    
        self.font = pygame.font.SysFont(None, 60)

        # Build the button's rect object and set position.
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = 320
        self.rect.y = 30

        self.load_positions()
        self.prep_msg(msg)

    def load_positions(self):
        if self.msg == "Play!":
            self.width, self.height = 160, 80     
            self.rect.x = 320
            self.rect.y = 30
        elif self.msg == "Replay?":
            self.width, self.height = 200, 80
            self.rect.x = 160
            self.rect.y = 500

    def prep_msg(self, msg):
        # Get a rendered image of the buttontext.
        self.msg_image = self.font.render(msg, True, self.text_color,
                self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # Draw the button to the screen.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect) 
        pygame.draw.rect(self.screen, self.game.color_set[8],
                         self.rect, width=3)