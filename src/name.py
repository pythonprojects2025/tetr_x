import pygame


class Name:
    """The name class creates functionality to enter a name, if a new 
    highscore is set. The player is asked to chose characters using the
    arrow keys <up> or <down>. Use <right> key to confirm the previewed
    character or <left> key to delete, set your name with <end>."""

    def __init__(self, game):
        self.game = game

        # Font and color settings.
        self.color = self.game.color_set[4]
        self.frame_color = self.game.color_set[8]
        self.text_box_color = self.game.color_set[2]

        self.text_label_color = self.color
        self.text_color = self.frame_color

        self.font = pygame.font.SysFont(None, 40)
        self.preview_font = pygame.font.SysFont(None, 50)

        self.pool = [" ", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                     "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u",
                     "v", "w", "x", "y", "z","end"]
        
        self.display = ""
        self.cursor = 0
        self.char = ""
        self.chain = []
        self.entry = ""
        self.enter = False
        self.delete = False

        self.load_positions()
        self.prep_grats()
        self.prep_title()
        self.prep_hint_1()
        self.prep_hint_2()
        
    def load_positions(self):
        # Main rect positions
        self.width =  400
        self.height = 600
        self.x = 60
        self.y = 50
        
        self.img = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Grats rect positions
        self.grats_x = self.x + 75
        self.grats_y = self.y + 30
        self.grats_img = pygame.Surface((1, 1))

        # Title rect positions
        self.title_x = self.x + 75
        self.title_y = self.y + 90
        self.title_img = pygame.Surface((1, 1))

        # Hint rect positions
        self.hint_x_1 = self.x + 75
        self.hint_y_1 = self.y + 150
        self.hint_img_1 = pygame.Surface((1, 1))

        # Hint2 rect positions
        self.hint_x_2 = self.x + 75
        self.hint_y_2 = self.y + 200
        self.hint_img_2 = pygame.Surface((1, 1))

        # Display rect positions
        self.display_x = self.x + 75
        self.display_y = self.y + 320
        self.display_img = pygame.Surface((1, 1))

    def prep_grats(self):
        # Get a rendered image with the level.
        grats_str = "!!! NEW RECORD !!!"
        self.grats_img = self.font.render(grats_str, True, self.text_color,
                                            self.color)   
           
        self.grats_rect = self.grats_img.get_rect()
        self.grats_rect.center = self.rect.center
        self.grats_rect.top = self.grats_rect.y + 30

    def prep_title(self):
        # Get a rendered image with the level.
        title_str = "Enter your name:"
        self.title_img = self.font.render(title_str, True, self.text_color,
                                            self.color)   
           
        self.title_rect = self.title_img.get_rect()
        self.title_rect.center = self.rect.center
        self.title_rect.top = self.title_rect.y + 30

    def prep_hint_1(self):
        # Get a rendered image with the hint.
        self.hint_font = pygame.font.SysFont(None, 24)
        hint_str_1 = "Use up/down arrows to chose char."
        self.hint_img_1 = self.hint_font.render(
            hint_str_1, True, self.text_color, self.color)   
           
        self.hint_rect_1 = self.hint_img_1.get_rect()
        self.hint_rect_1.center = self.rect.center
        self.hint_rect_1.top = self.hint_y_1 + 30
    
    def prep_hint_2(self):
        # Get a rendered image with the hint.
        self.hint_font = pygame.font.SysFont(None, 24)
        hint_str_2 = "Use [->] to select or [<-] to delete."
        self.hint_img_2 = self.hint_font.render(
            hint_str_2, True, self.text_color, self.color)   
           
        self.hint_rect_2 = self.hint_img_2.get_rect()
        self.hint_rect_2.center = self.rect.center
        self.hint_rect_2.top = self.hint_y_2 + 30

    def prep_display(self):
        # Get a rendered image with the name characters.
        self.display_img = self.preview_font.render(
            self.display, True, self.text_color, self.text_box_color)   
           
        self.display_rect = self.display_img.get_rect()
        self.display_rect.x = self.display_x
        self.display_rect.y = self.display_y

    def check_cursor(self):
        if self.cursor == -1:
            self.cursor = 27
        if self.cursor == 28:
            self.cursor = 0
    
    def update_cursor(self):
        self.check_cursor()
        self.char = self.pool[self.cursor]
    
    def update_display(self):
        text = self.get_text()
        
        # save the chosen name to attribute.
        if (self.enter and self.char == "end" or 
            self.enter and len(self.chain) == 9):        
            text = self.get_text()
            self.game.winner = text
            self.game.new_highscore = False
            self.game.check_points()
            return
        
        # Check max length of name.
        if self.enter and len(self.chain) <= 8:
            self.chain.append(self.char)
            self.enter = False

        # Delete last character.
        if self.delete and len(self.chain) > 0:
            self.chain.pop()
            self.delete = False

        # shows "end" as only option to chose, if max length is reached.
        if len(self.chain) == 9:
            self.cursor = 27

        # Display the preview name and the 
        self.display = text + self.char

    def get_text(self):
        text = ""
        for i in self.chain:
            text = text + i
        return str(text)
    
    def update(self):
        self.update_cursor()
        self.update_display()
        self.prep_display()

    def drawme(self):
        # Draw the objects to screen.
        pygame.draw.rect(self.game.screen, self.color, self.rect)
        pygame.draw.rect(self.game.screen, self.frame_color, self.rect,
                         width=5)

        self.game.screen.blit(self.grats_img,
                              (self.grats_x, self.grats_y))
        self.game.screen.blit(self.title_img,
                              (self.title_x, self.title_y))
        self.game.screen.blit(self.display_img,
                              (self.display_x, self.display_y))
        self.game.screen.blit(self.hint_img_1,
                              (self.hint_x_1, self.hint_y_1))
        self.game.screen.blit(self.hint_img_2,
                              (self.hint_x_2, self.hint_y_2))
    
