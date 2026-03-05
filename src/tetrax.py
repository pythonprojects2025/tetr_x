import pygame
import sys
from random import choice, randint
from time import sleep
import csv

from tile import Tile, Block
from score_field import Scorefield
from button import Button
from highscore import Highscore
from name import Name


class Game:
    """This is the main game class for tetrx, containing the main loop:
    detecting user input, update game objects, draw game objects to screen."""

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.screen = pygame.display.set_mode((520, 720))
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("Tetr_x")

        self.color_sets = [
            # pos_0: playfield, pos_1 - pos_7: blocks, pos_8: blockborder

                            [
                            (27, 36, 71), (144, 82, 188), (238, 181, 156),
                            (212, 128, 187), (226, 178, 126), (180, 117, 56),
                            (114, 75, 44), (39, 137, 205), (250, 214, 255),
                            ], 

                            [
                            (73, 65, 130), (246, 162, 168), (178, 82, 102),
                            (138, 196, 195), (178, 139, 120), (150, 104, 136),
                            (246, 216, 150), (236, 225, 231), (201, 212, 253),
                            ], 
                        
                            [
                            (23, 21, 22), (94, 113, 142), (178, 139, 120),
                            (114, 75, 44), (100, 54, 75), (105, 91, 89),
                            (239, 221, 145), (178, 82, 102), (196, 241, 41)
                            ], 
                        
                            [
                            (144, 82, 188), (71, 114, 56), (97, 165, 63), 
                            (143, 208, 50), (196, 241, 41), (252, 247, 190), 
                            (151, 237, 202), (70, 84, 86), (238, 181, 156)
                            ], 
                        
                            [
                            (136, 163, 188), (40, 44, 60), (105, 102, 130),
                            (184, 204, 216), (138, 196, 195), (70, 84, 86),
                            (72, 104, 89), (134, 198, 154),(241, 242, 255),
                            ], 
                        
                            [
                            (76, 61, 46), (236, 235, 231), (166, 158, 154), 
                            (89, 87, 87), (40, 44, 60), (86, 79, 91), 
                            (101, 73, 86), (136, 110, 106), (66, 191, 232),
                            ], 
                        
                            [
                            (101, 73, 86), (27, 36, 71), (39, 137, 205), 
                            (66, 191, 232), (230, 231, 240), (138, 161, 246),
                            (73, 65, 130), (206, 170, 237), (246, 122, 168),
                            ], 

                            [
                            (42, 30, 35), (255, 240, 137), (211, 151, 65), 
                            (76, 61, 46), (198 , 133, 86), (246, 162, 168), 
                            (100, 54, 75), (238, 230, 234), (252, 247, 190),
                            ], 
                        ] 
        self.color_set = self.color_sets[randint(0, 7)]

        self.play_field = pygame.Surface((400, 720))
        self.play_field_rect = pygame.Rect(0, 0, 400, 720)
        self.play_field_color = self.color_set[0]
        self.play_field.fill(self.play_field_color)

        self.title_screen = self.load_title_image()

        self.played_sounds = []
        # self.play_sound()
        pygame.mixer.Channel(0).play(pygame.mixer.Sound("sound/intro.mp3")) 

        self.drop_speed = 60
        # Counter for dropping the tile one step.
        self.counter = 0
        # Counter to detect the amount of destroyed lines.
        self.tetrx_counter = 0

        self.x = 160
        self.y = 0
        self.tile_posture = 0

        self.moving_blocks = []
        self.static_blocks = []

        self.all_rects = self.create_all_rects()
        self.rects = []

        self.tile_pool = ["L", "Rev_L", "Bloc", "Z", "Rev_Z", "Tri", "Bar"]

        self.line_counter = 0
        self.level = 1
        self.points = 0

        self.winner = ""
        self.rank_1_name = ""
        self.rank_1_val = 0
        self.rank_2_name = ""
        self.rank_2_val = 0
        self.rank_3_name = ""
        self.rank_3_val = 0

        self.game_active = False
        self.game_over = False
        self.new_highscore = False

        self.rightmove_possible = True
        self.leftmove_possible = True
        self.rightturn_possible = True
        self.leftturn_possible = True
        self.step_active = True
        self.waiting = False

        self.current_tile = self.get_next_tile()
        self.next_tile = self.get_next_tile()

        self.tile = Tile(self, self.x, self.y, self.current_tile)
        self.tile.create_tile_blocks()

        self.scorefield = Scorefield(self)
        self.button = Button(self, "Play!")
        self.savegame = self.load_savefile()
        self.set_hiscores()
        self.highscore = Highscore(self)
        self.name = Name(self)

    def run_game(self):     
        # Main game loop.
        while True:
            self.check_events()

            if self.game_over and self.new_highscore:
                self.name.update()
               
            if self.game_over and not self.new_highscore:
                self.ask_replay()

            if self.game_active:                     
                self.tile_step()
                self.tile.update()
                self.check_max_heigth()
                self.check_borders(self.play_field_rect)
                
                if self.waiting:
                    self.wait_to_lock()
                
                self.check_full_lines()
                self.check_drop_collision()
                self.check_bottom()
                self.check_tile_sides()   

                if not self.game_over:
                    if not self.moving_blocks and not self.waiting:
                        self.create_new_tile()

                self.scorefield.update()

            self.update_screen()
            self.clock.tick(self.fps)

    def check_events(self):
        # Check for user input.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()     
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self.check_play_button(mouse_pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if self.game_over and self.new_highscore:
                        self.name.enter = True
                        continue

                    if self.rightmove_possible and self.tile.moving:
                        self.move_right()
                           
                if event.key == pygame.K_LEFT:
                    if self.game_over and self.new_highscore:
                        self.name.delete = True
                        continue

                    if self.leftmove_possible and self.tile.moving:
                        self.move_left()
                
                if event.key == pygame.K_DOWN:
                    if self.game_over and self.new_highscore:
                        self.name.cursor += 1
                        continue

                    on_block = self.block_true()

                    if self.tile.moving and not on_block:
                        self.step_active = False
                        self.tile.fast_drop = True
                
                if event.key == pygame.K_UP:
                    if self.game_over and self.new_highscore:
                        self.name.cursor -= 1
                        continue

                if event.key == pygame.K_m:
                    self.turn_right()

                if event.key == pygame.K_n:
                    self.turn_left()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.tile.fast_drop = False
                    self.step_active = True

    def check_play_button(self, mouse_pos):
        # Start game when button is clicked and reset game stats.
        if not self.game_active or self.game_over:
            if not self.new_highscore:
                if self.button.rect.collidepoint(mouse_pos):
                    
                    pygame.mixer.Channel(6).play(
                        pygame.mixer.Sound("sound/beep.mp3"))  
                    
                    pygame.time.wait(500)
                    self.reset_stats()  
                    pygame.mouse.set_visible(False)
                    self.game_active = True  
                    self.new_highscore = False
                    self.play_sound()
    
    def ask_replay(self):
        self.game_active = False
        pygame.mouse.set_visible(True)
        self.button.__init__(self, "Replay?")

    def reset_stats(self):
        self.color_set = self.color_sets[randint(0, 7)]
        self.play_field_color = self.color_set[0]
        self.play_field.fill(self.play_field_color)

        self.drop_speed = 60
        self.counter = 0
        self.tetrx_counter = 0

        self.x = 160
        self.y = 0
        self.tile_posture = 0

        self.moving_blocks = []
        self.static_blocks = []
        self.rects = []

        self.line_counter = 0
        self.level = 1
        self.points = 0

        self.winner = ""
        self.rank_1_name = ""
        self.rank_1_val = 0
        self.rank_2_name = ""
        self.rank_2_val = 0
        self.rank_3_name = ""
        self.rank_3_val = 0

        self.game_active = False
        self.game_over = False
        self.new_highscore = False

        self.rightmove_possible = True
        self.leftmove_possible = True
        self.rightturn_possible = True
        self.leftturn_possible = True
        self.step_active = True
        self.waiting = False

        self.current_tile = self.get_next_tile()
        self.next_tile = self.get_next_tile()

        self.tile = Tile(self, self.x, self.y, self.current_tile)
        self.tile.create_tile_blocks()

        self.scorefield = Scorefield(self)
        self.button = Button(self, "Play!")
        self.savegame = self.load_savefile()
        self.set_hiscores()
        self.highscore = Highscore(self)
        self.name = Name(self)

    def play_sound(self):
        if len(self.played_sounds) == 4:
            self.played_sounds = []

        sound = choice(["1", "2", "3", "4", "5"])

        if not sound in self.played_sounds:
            if sound == "1":
                self.played_sounds.append("1")
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound("sound/level_1.mp3"), loops=4) 
            elif sound == "2":
                self.played_sounds.append("2")
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound("sound/level_2.mp3"), loops=4) 
            elif sound == "3":
                self.played_sounds.append("3")
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound("sound/level_3.mp3"), loops=4)
            elif sound == "4":
                self.played_sounds.append("4")
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound("sound/level_4.mp3"), loops=4) 
            elif sound == "5":
                self.played_sounds.append("5")
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound("sound/level_5.mp3"), loops=4)
            return
        else:
            self.play_sound()
        
    def load_title_image(self):
        image = randint(1, 8)
        if image == 1:
            return pygame.image.load("images/title_col_1.png")
        elif image == 2:
            return pygame.image.load("images/title_col_2.png")
        elif image == 3:
            return pygame.image.load("images/title_col_3.png")
        elif image == 4:
            return pygame.image.load("images/title_col_4.png")
        elif image == 5:
            return pygame.image.load("images/title_col_5.png")
        elif image == 6:
            return pygame.image.load("images/title_col_6.png")
        elif image == 7:
            return pygame.image.load("images/title_col_7.png")
        elif image == 8:
            return pygame.image.load("images/title_col_8.png")

    def load_savefile(self):
        file_name = "save_file.csv"
        with open(file_name, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                return row

    def set_hiscores(self):
        self.rank_1_name = self.savegame[0]
        self.rank_1_val = int(self.savegame[1])
        self.rank_2_name = self.savegame[2]
        self.rank_2_val = int(self.savegame[3])
        self.rank_3_name = self.savegame[4]
        self.rank_3_val = int(self.savegame[5])
        
    def save_savefile(self):
        csv_file = "save_file.csv"
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            data = (
                    [self.rank_1_name, self.rank_1_val, self.rank_2_name,
                    self.rank_2_val, self.rank_3_name, self.rank_3_val]
                    )
            writer.writerow(data)

    def get_next_tile(self):
        next_tile = choice(self.tile_pool)
        return next_tile

    def create_new_tile(self):
        self.x = 160
        self.y = 40
        self.current_tile = self.next_tile
        self.next_tile = self.get_next_tile()
        self.counter = 0
        self.tile_posture = 0
        self.tile = Tile(self, self.x, self.y, self.current_tile)
        self.tile.create_tile_blocks()
        self.rightmove_possible = True
        self.leftmove_possible = True
        self.rightturn_possible = True
        self.leftturn_possible = True
        self.waiting = False
        self.tile.fast_drop_possible = True
        self.step_active = True

    def wait_to_lock(self):
        if self.counter == self.drop_speed-1:
            # lock tile, if ground is reached.
            for i in self.moving_blocks:
                if i.rect.bottom == self.screen_rect.bottom:
                    self.lock_tile()

            # lock tile, if on top of other tile.
            for block in self.moving_blocks:
                test_x = block.rect.x
                test_y = block.rect.y + 40
                testrect = pygame.Rect(test_x, test_y, 40, 40)

                for i in self.static_blocks:
                    if testrect.colliderect(i.rect):
                        self.lock_tile()
    
    def lock_tile(self):
        # Pass moving blocks to static blocks and reset list of moving blocks.
        for j in self.moving_blocks:
            self.static_blocks.append(j)
        self.scorefield.prev_blocks = []
        self.moving_blocks = [] 
        self.x = 160
        self.y = 0
        self.waiting = False

        pygame.mixer.Channel(1).play(pygame.mixer.Sound("sound/lock.mp3")) 

    def bottom_true(self):
        for i in self.moving_blocks:
            if i.rect.bottom == self.screen_rect.bottom:
                return True
        return False
    
    def check_bottom(self):
        # Check collision tile/bottom.
        bottom_reached = self.bottom_true()
        if bottom_reached:
            self.check_right_turn()
            self.check_left_turn()

            if self.tile.fast_drop and self.tile.fast_drop_possible:
                # locking tile immediately, if dropped fast.
                self.step_active = False
                self.tile.fast_drop_possible = False
                self.lock_tile()
                self.create_new_tile()
                return
            
            else:   
                # Keeping tile movable for one step.
                self.tile.fast_drop_possible = False
                self.step_active = False
                self.waiting = True
                return
        
        self.tile.fast_drop_possible = True
        self.step_active = True

    def block_true(self):
        for i in self.moving_blocks:
            test_x = i.rect.x
            test_y = i.rect.y + 40
            testrect = pygame.Rect(test_x, test_y, 40, 40)

            for j in self.static_blocks:
                if testrect.colliderect(j.rect):
                    return True
        return False

    def check_drop_collision(self):
        # Check collision tile/tile.
        block_reached = self.block_true()

        if block_reached:
            self.check_right_turn()
            self.check_left_turn()

            if self.tile.fast_drop:
                # locking tile immediately, if dropped fast.
                self.lock_tile()
                self.create_new_tile()
                return       
              
            else:
                # Keeping tile movable for one step.
                self.tile.fast_drop_possible = False
                self.step_active = False
                self.waiting = True
                return 
                
        self.tile.fast_drop_possible = True
        self.step_active = True

    def check_max_heigth(self):
        # set the game over attribute to true, if max height is reached.
        for block in self.static_blocks:
            if block.rect.y <= 0:
                pygame.mixer.Channel(0).play(
                    pygame.mixer.Sound("sound/gameover.mp3")) 
                
                self.check_win()
                self.game_active = False
                self.game_over = True
                return

    def check_win(self):
        # Check if new record happened.
        if (
            self.points >= self.rank_1_val or 
            self.points >= self.rank_2_val and self.points <= self.rank_1_val
            or self.points > self.rank_3_val and self.points <= self.rank_2_val
            ):
            self.new_highscore = True

            pygame.time.wait(2000)
            pygame.mixer.Channel(1).play(
                pygame.mixer.Sound("sound/newrecord.mp3"))
            return

    def check_points(self):
        # Check ranking, initialize highscore view and save the scores.
        if self.points >= self.rank_1_val:
            self.rank_3_val = self.rank_2_val
            self.rank_3_name = self.rank_2_name
            if self.points == self.rank_1_val:
                self.rank_2_val = self.points
                self.rank_2_name = self.winner
                self.rank_1_val = self.rank_1_val
                self.rank_1_name = self.rank_1_name
            elif self.points > self.rank_1_val:
                self.rank_2_val = self.rank_1_val
                self.rank_2_name = self.rank_1_name
                self.rank_1_val = self.points
                self.rank_1_name = self.winner
        
        elif self.points >= self.rank_2_val and self.points <= self.rank_1_val:
            if self.points == self.rank_2_val:
                self.rank_3_val = self.points
                self.rank_3_name = self.winner
            elif self.points > self.rank_2_val:
                self.rank_3_val = self.rank_2_val
                self.rank_3_name = self.rank_2_name
                self.rank_2_val = self.points
                self.rank_2_name = self.winner
        
        elif self.points >= self.rank_3_val and self.points <= self.rank_2_val:
            if self.points > self.rank_3_val:
                self.rank_3_val = self.points
                self.rank_3_name = self.winner

        self.highscore.__init__(self)
        self.save_savefile()
        return
        
    def tile_step(self):
        # Increase the drop-counter.
        if self.tile.moving: 
            self.counter += 1
            if self.counter > self.drop_speed:
                self.counter = self.drop_speed
            if self.counter == self.drop_speed:
                self.counter = 0
                if self.step_active:          
                    self.y += 40
                    for i in self.moving_blocks:  
                        i.rect.y += 40               

    def check_borders(self, field_rect):
        # Check if left/right border is reached.
        for block in self.moving_blocks:
            if block.rect.left <= field_rect.left:
                self.leftmove_possible = False  
                return
            
            if block.rect.right >= field_rect.right:
                self.rightmove_possible = False  
                return  
                       
            if (block.rect.left >= field_rect.left or
                block.rect.right <= field_rect.right):
                self.rightmove_possible = True
                self.leftmove_possible = True
        
    def check_tile_sides(self):
        self.check_right_move()  
        self.check_left_move()

    def check_right_move(self):
        # Check if a tile blocks the right side.
        testblocks = []  
        for i in self.moving_blocks:
            testblock = Block(self, i.rect.x + 40, i.rect.y,
                              self.tile.side_len, self.tile)
            testblocks.append(testblock)
   
        for i in testblocks:
            for j in self.static_blocks:
                collision = pygame.Rect.colliderect(i.rect, j.rect)
                if collision:
                    self.rightmove_possible = False
                    return
        if not self.rightmove_possible == False:
            self.rightmove_possible = True
        
    def check_left_move(self):
        # Check if a tile blocks the left side.
        testblocks = []       
        for i in self.moving_blocks:
            testblock = Block(self, i.rect.x - 40, i.rect.y,
                              self.tile.side_len, self.tile)
            testblocks.append(testblock)

        for i in testblocks:
            for j in self.static_blocks:   
                collision = pygame.Rect.colliderect(i.rect, j.rect)
                if collision:
                    self.leftmove_possible = False
                    return
        if not self.leftmove_possible == False:
            self.leftmove_possible = True
                
    def move_right(self):
        self.x += 40
        for i in self.moving_blocks:
            i.rect.x += 40

        pygame.mixer.Channel(6).play(pygame.mixer.Sound("sound/beep.mp3")) 

    def move_left(self):
        self.x -= 40
        for i in self.moving_blocks:
            i.rect.x -= 40

        pygame.mixer.Channel(6).play(pygame.mixer.Sound("sound/beep.mp3")) 

    def check_right_turn(self):
        testrects = []
        testblocks = []
        testposture = 0
        
        # Create the posture to get position for test-tile.
        if len(self.tile.tile_positions) == 1:
            return True
        
        elif len(self.tile.tile_positions) == 4:     
            if not self.tile_posture == 3:
                testposture = self.tile_posture + 1 
            if self.tile_posture == 3:
                testposture = 0

        elif len(self.tile.tile_positions) == 2:
            if not self.tile_posture == 1:
                testposture = self.tile_posture + 1 
            if self.tile_posture == 1:
                testposture = 0

        # Create Rect objects with origin side length.        
        for i in self.tile.tile_positions[testposture]:
            testrect = pygame.Rect(self.x + i[0], self.y + i[1], 40, 40)
            testrects.append(testrect)
        
        # Testing play-field borders.
        for i in testrects:          
            if (i.left < self.play_field_rect.left or
                i.right > self.play_field_rect.right):
                return False
            
         #  Checking for collision with ground.
        for i in testrects:
            if i.bottom > self.screen_rect.bottom:
                return False
            
        # Create Rect objects with smaller side length.
        for i in self.tile.tile_positions[testposture]:
            testblock = pygame.Rect(self.x + i[0]+1, self.y + i[1]+1, 38, 38)
            testblocks.append(testblock)
        
        # Checking for collision with other tiles when turning right.
        for i in testblocks:
            for j in self.static_blocks:
                collision = pygame.Rect.colliderect(i, j.rect)
                if collision:
                    return False
                
        return True
            
    def check_left_turn(self):
        testrects = []
        testblocks = []
        testposture = 0

        # Create the posture to get position for test-tile.
        if len(self.tile.tile_positions) == 4:     
            if not self.tile_posture == 0:
                testposture = self.tile_posture - 1 
            if self.tile_posture == 0:
                testposture = 3
                
        elif len(self.tile.tile_positions) == 2:
            if not self.tile_posture == 0:
                testposture = self.tile_posture - 1 
            if self.tile_posture == 0:
                testposture = 1
            
        # Create Rect objects with origin side length.
        for i in self.tile.tile_positions[testposture]:
            testrect = pygame.Rect(self.x + i[0], self.y + i[1], 40, 40)
            testrects.append(testrect)
        
        # Testing play-field borders.
        for i in testrects:
            if (i.left < self.play_field_rect.left or
                i.right > self.play_field_rect.right):
                return False
        
        #  Checking for collision with ground.
        for i in testrects:
            if i.bottom > self.screen_rect.bottom:
                return False
            
        # Create Rect objects with smaller side length.
        for i in self.tile.tile_positions[testposture]:
            testblock = pygame.Rect(self.x + i[0]+1, self.y + i[1]+1, 38, 38)
            testblocks.append(testblock)
        
        # Checking for collision with other tiles when turning left.
        for i in testblocks:
            for j in self.static_blocks:
                collision = pygame.Rect.colliderect(i, j.rect)
                if collision:
                    return False

        return True 
            
    def turn_right(self):
        right_turn_possible = self.check_right_turn()
        if right_turn_possible:

            pygame.mixer.Channel(2).play(pygame.mixer.Sound("sound/turnr.mp3")) 
            
            if len(self.tile.tile_positions) == 4:     
                if self.tile_posture >= 0:
                    self.tile_posture += 1 
                if self.tile_posture > 3:
                    self.tile_posture = 0

            elif len(self.tile.tile_positions) == 2:
                if self.tile_posture >= 0:
                    self.tile_posture += 1 
                if self.tile_posture > 1:
                    self.tile_posture = 0

    def turn_left(self):
        left_turn_possible = self.check_left_turn()
        if left_turn_possible:

            pygame.mixer.Channel(2).play(pygame.mixer.Sound("sound/turnl.mp3")) 
            
            if len(self.tile.tile_positions) == 4:     
                if self.tile_posture >= 0:
                    self.tile_posture -= 1 
                if self.tile_posture < 0:
                    self.tile_posture = 3
                
            elif len(self.tile.tile_positions) == 2:
                if self.tile_posture >= 0:
                    self.tile_posture -= 1 
                if self.tile_posture < 0:
                    self.tile_posture = 1

    def raise_level(self):
        # levelup for 10 destroyed lines.
        pygame.mixer.Channel(3).play(pygame.mixer.Sound("sound/levelup.mp3")) 
        self.level += 1

        if self.drop_speed > 5:
            if self.level <= 10:
                self.drop_speed -= 5
            elif self.level > 10:
                self.drop_speed -= 2
        else:
            self.drop_speed = 6

        self.update_block_colors()

    def update_block_colors(self):  
        # Get a new colorset, if levelup is reached.
        self.color_set = self.color_sets[randint(0, 7)]        
        self.play_field_color = self.color_set[0]
        self.play_field.fill(self.play_field_color)

        self.scorefield.color = self.play_field_color
        self.scorefield.frame_color = self.color_set[8]
        self.scorefield.text_color = self.color_set[8]

        for i in self.static_blocks:
            i.color = i.get_color()

    def remove_line(self, rects):
        # Remove the static blcks, when a line is cleared.
        remove_rects = rects
        y = remove_rects[0].y

        for i in remove_rects:
            for j in self.static_blocks:
                if i == j.rect:
                    self.static_blocks.remove(j)

        self.line_counter += 1

        if self.line_counter % 10 == 0:
            self.raise_level()
      
        self.drop_restblocks(y)

    def drop_restblocks(self, y):
        # Dropping the blocks above a destroyed line.
        for i in self.static_blocks:
            if i.rect.y < y:
                i.rect.y += 40

    def check_full_lines(self):
        # Check if there's a full line.
        x = 17
        static_rects = self.create_static_rects()
        for i in range(17):
            testline = []
            for j in self.all_rects[x]:
                if j in static_rects and not j in testline:
                    testline.append(j)

            if len(testline) < 10:
                x -= 1
                continue

            if len(testline) == 10:
                self.tetrx_counter += 1
                self.remove_line(testline)  
                testline = [] 
                x -= 1
        
        if self.counter == 6:
            # Checking the amount of destroyed lines, if counter is at 6:
            # 3 frames are needed to have the destroyed lines counted correct.
            self.play_linesound()
            self.add_points()
            self.tetrx_counter = 0

    def play_linesound(self):
        if self.tetrx_counter > 0 and self.tetrx_counter < 4:
            pygame.mixer.Channel(4).play(
                pygame.mixer.Sound("sound/linedown.mp3"))
                
        if self.tetrx_counter == 4:
            pygame.mixer.Channel(4).play(
                pygame.mixer.Sound("sound/tetrx.mp3"))
    
    def add_points(self):
        # Extra points for 4 simultanously destroyed lines.
        if self.tetrx_counter == 4:
            self.points += 1000 * self.tetrx_counter * self.level
            return      
        else:
            self.points += 100 * self.tetrx_counter * self.level
            return
                
    def create_all_rects(self):
        # Create the grid with rect objects to check full lines.
        testrects = []
        linerects = []
        x = 0
        y = 0

        for i in range(18):
            for i in range(10):
                testrect = pygame.Rect(x, y, 40, 40)
                linerects.append(testrect)
                x += 40
            testrects.append(linerects)
            linerects = []
            x = 0
            y += 40

        return testrects

    def create_static_rects(self):
        # Copy the static rect objects to check full lines.
        rects = []
        for i in self.static_blocks:
            rects.append(i.rect)
        return rects
       
    def update_screen(self):
        # Draw the game objects to screen.
        self.screen.fill(self.color_set[0])

        if self.game_over and self.new_highscore:
            self.name.drawme()

        if self.game_over and not self.new_highscore:
            self.highscore.drawme()
            self.button.draw_button() 

        if not self.game_active and not self.game_over:
            self.screen.blit(self.title_screen, (0, 0))
            self.button.draw_button() 

        if self.game_active:
            self.screen.blit(self.play_field, (0, 0))
            self.scorefield.drawme()
            for block in self.moving_blocks:      
                pygame.draw.rect(self.screen, block.color, block)
                pygame.draw.rect(self.screen, self.color_set[8], block,
                                 width=3)
            for block in self.static_blocks:
                pygame.draw.rect(self.screen, block.color, block)
                pygame.draw.rect(self.screen, self.color_set[8], block,
                                 width=3)

        pygame.display.flip()

pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run_game()