import pygame


class Highscore:
    """The highscore class creates the leaderboard. It pops up if the game is 
    lost, shows the top 3 ranks and a button to restart the game."""

    def __init__(self, game):
        self.game = game

        # Font and color settings.
        self.color = self.game.color_set[4]
        self.frame_color = self.game.color_set[8]

        self.text_label_color = self.color
        self.text_color = self.frame_color

        self.font = pygame.font.SysFont(None, 32)
        self.number_font = pygame.font.SysFont(None, 32)

        self.load_positions()
        self.prep_title()
        self.prep_entries()
        
    def load_positions(self):
        # Main rect positions
        self.width =  400
        self.height = 600
        self.x = 60
        self.y = 50
        
        self.img = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Title rect positions
        self.title_x = self.x + 100
        self.title_y = self.y + 20
        self.title_img = pygame.Surface((1, 1))

        # Entries rect positions
        self.entry_1_x = self.x + 50
        self.entry_1_y = self.y + 20
        self.entry_1_img = pygame.Surface((1, 1))

        self.entry_2_x = self.x + 50
        self.entry_2_y = self.y + 20
        self.entry_2_img = pygame.Surface((1, 1))

        self.entry_3_x = self.x + 50
        self.entry_3_y = self.y + 20
        self.entry_3_img = pygame.Surface((1, 1))
        
    def prep_title(self):
        # Get a rendered image with the level.
        title_str = "!HIGH - SCORES!"
        self.title_img = self.font.render(title_str, True, self.text_color,
                                            self.color)   
           
        self.title_rect = self.title_img.get_rect()
        self.title_rect.center = self.rect.center
        self.title_rect.top = self.title_rect.y + 30

    def prep_entries(self):
        # Get rendered images with the names and points.
        self.rank_1_name = self.game.rank_1_name
        self.rank_1_val = self.game.rank_1_val       
        self.rank_pos_1 = f"1. {self.rank_1_name}: {self.rank_1_val} pts."
        self.rank_pos_1_img = self.font.render(
            self.rank_pos_1, True, self.text_color, self.color)   
        
        self.rank_pos_1_rect = self.rank_pos_1_img.get_rect()
        self.rank_pos_1_rect.center = self.rect.center
        self.rank_pos_1_rect.top = self.y + 120

        self.rank_2_name = self.game.rank_2_name
        self.rank_2_val = self.game.rank_2_val
        self.rank_pos_2 = f"2. {self.rank_2_name}: {self.rank_2_val} pts."
        self.rank_pos_2_img = self.font.render(
            self.rank_pos_2, True, self.text_color, self.color)   
        
        self.rank_pos_2_rect = self.rank_pos_2_img.get_rect()
        self.rank_pos_2_rect.center = self.rect.center
        self.rank_pos_2_rect.top = self.y + 220

        self.rank_3_name = self.game.rank_3_name
        self.rank_3_val = self.game.rank_3_val
        self.rank_pos_3 = f"3. {self.rank_3_name}: {self.rank_3_val} pts."
        self.rank_pos_3_img = self.font.render(
            self.rank_pos_3, True, self.text_color, self.color)   
        
        self.rank_pos_3_rect = self.rank_pos_3_img.get_rect()
        self.rank_pos_3_rect.center = self.rect.center
        self.rank_pos_3_rect.top = self.y + 320

    def drawme(self):
        # Draw leaderboard.
        pygame.draw.rect(self.game.screen, self.color, self.rect)
        pygame.draw.rect(self.game.screen, self.frame_color, self.rect, 
                         width=5)
      
        self.game.screen.blit(
            self.title_img, (self.title_x, self.title_y))
        self.game.screen.blit(self.rank_pos_1_img,
                              (self.rank_pos_1_rect.x, self.rank_pos_1_rect.y))
        self.game.screen.blit(self.rank_pos_2_img,
                              (self.rank_pos_2_rect.x, self.rank_pos_2_rect.y))
        self.game.screen.blit(self.rank_pos_3_img,
                              (self.rank_pos_3_rect.x, self.rank_pos_3_rect.y))
