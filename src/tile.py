import pygame


class Tile:
    """This class contains the tile-related attributes like tile positions and
    methods to create and update a tile, made of blocks."""

    def __init__(self, game, x, y, tile):
        self.game = game
        self.x = x
        self.y = y
        self.tile = tile
        self.side_len = 40

        self.drop_speed = game.drop_speed
        self.counter = 0
        self.posture = 0
        self.test_posture = 0
        
        self.tile_positions = self.get_tile_position(self.tile)

        self.moving_right = False
        self.moving_left = False
        self.fast_drop_possible = True
        self.fast_drop = False
        self.moving = True
    
    def get_tile_position(self, tile):
        # Tile positions for any possible posture.
        if tile == "L":
            positions = [
                        [(0, 0),
                        (0, 40),
                        (0, 80),
                        (40, 80)],
                    
                        [(-40, 40),
                        (0, 40),
                        (40, 40),
                        (-40, 80)],
                    
                        [(-40, 0),
                        (0, 0),
                        (0, 40),
                        (0, 80)],
                        
                        [(-40, 40),
                        (0, 40),
                        (40, 40),
                        (40, 0)]     
                        ]
            return positions
            
        elif tile == "Rev_L":
            positions = [[
                        (0, 0),
                        (0, 40),
                        (0, 80),
                        (-40, 80)],
                    
                        [(-40, 0),
                        (-40, 40),
                        (0, 40),
                        (40, 40)],
                    
                        [(-40, 0),
                        (0, 0),
                        (-40, 40),
                        (-40, 80)],
                        
                        [(-40, 40),
                        (0, 40),
                        (40, 40),
                        (40, 80)]     
                        ]
            return positions
        
        elif tile == "Bloc":
            positions = [[
                        (0, 0),
                        (40, 0),
                        (0, 40),
                        (40, 40)]
                        ] 
            return positions
            
        elif tile == "Z":
            positions = [[
                        (-40, 0),
                        (0, 0),
                        (0, 40),
                        (40, 40)],
                    
                        [(40, 0),
                        (40, 40),
                        (0, 40),
                        (0, 80)]
                        ]
            return positions
            
        elif tile == "Rev_Z":
            positions = [
                        [(0, 0),
                        (40, 0),
                        (-40, 40),
                        (0, 40)],
                    
                        [(0, 0),
                        (0, 40),
                        (40, 40),
                        (40, 80)]
                        ]
            return positions
            
        elif tile == "Tri":
            positions = [
                        [(0, 0),
                        (0, 40),
                        (40, 40),
                        (0, 80)],
                    
                        [(-40, 40),
                        (0, 40),
                        (40, 40),
                        (0, 80)],
                    
                        [(0, 0),
                        (-40, 40),
                        (0, 40),
                        (0, 80)],
                        
                        [(0, 0),
                        (-40, 40),
                        (0, 40),
                        (40, 40)]     
                        ]
            return positions

        elif tile == "Bar":
            positions = [
                        [(-40, 0),
                        (-40, 40),
                        (-40, 80),
                        (-40, 120)],
                    
                        [(-80, 80),
                        (-40, 80),
                        (0, 80),
                        (40, 80)]
                        ]
            return positions

    def create_tile_blocks(self):
        self.x = 160
        self.y = 0
        # Create tile in standard position.
        for i in self.tile_positions[0]:
            block = Block(self.game, self.x + i[0], self.y + i[1], 
                          self.side_len, self.tile)
            self.game.moving_blocks.append(block)
            self.game.tile_posture = 0

        self.moving = True
    
    def update_tile_blocks(self):
        # Recreate tile, if rotated.
        if not self.posture == self.game.tile_posture:
            self.posture = self.game.tile_posture

            if self.moving:
                self.game.moving_blocks = []

                for i in self.tile_positions[self.posture]:
                    block = Block(self.game, self.x + i[0], self.y + i[1], 
                                  self.side_len, self.tile)
                    self.game.moving_blocks.append(block)

    def check_fast_drop(self):  
        if self.fast_drop_possible and self.fast_drop and self.moving:
            self.game.y += 40
            
            for i in self.game.moving_blocks:
                i.rect.y += 40

    def update(self): 
        self.x = self.game.x
        self.y = self.game.y  
        self.check_fast_drop()   
        self.update_tile_blocks()


class Block:
    """This class create the block-rects to build a tile with its correct
    color. """

    def __init__(self, game, x, y, side, tile):
        self.game = game
        self.piece = tile
        self.color = self.get_color()
        # self.border_color = self.game.color_set[9]
        self.rect = pygame.Rect((x, y, side, side))

    def get_color(self):
        if self.piece == "L":
            color = self.game.color_set[1]
            return color
        
        elif self.piece == "Rev_L":
            color = self.game.color_set[2]
            return color
        
        elif self.piece == "Bloc":
            color = self.game.color_set[3]
            return color
        
        elif self.piece == "Z":
            color = self.game.color_set[4]
            return color
        
        elif self.piece == "Rev_Z":
            color = self.game.color_set[5]
            return color
        
        elif self.piece == "Tri":
            color = self.game.color_set[6]
            return color
        
        elif self.piece == "Bar":
            color = self.game.color_set[7]
            return color
        
        