from pygame import Rect
import pygame
import math
from building import Building
from button import Button
from unit import Unit

class Map:
    def __init__(self, window, blockSize, res_w, res_h):
        self.blockSize = blockSize
        self.window = window
        self.res_w = res_w
        self.res_h = res_h
        self.new_build_pos_x = None
        self.new_build_pos_y = None
        self.object_selected = 0
        self.active_troop_button = None
        self.troops = []
        self.gridmap = self.grid()
        self.active_building = None

    'Create grid from blocks'
    def grid(self):
        gridmap = []
        for x in range(0, self.res_w, self.blockSize):
            grid_map_line = []
            for y in range(0, self.res_h, self.blockSize):
                # Create panels to screen, which are 3 blocks large from the bottom, and
                # right side of the screen.
                if (self.res_h - y) <= (4 * self.blockSize):
                    rect = Rect(x, y, self.blockSize, self.blockSize)
                    pygame.draw.rect(self.window, (110, 110, 110), rect)
                    grid_map_line.append('p')

                elif (self.res_h - y) <= (5 * self.blockSize):
                    grid_map_line.append('pe')

                elif ((x / self.blockSize) == 10 and (y / self.blockSize) == 10) or ((x / self.blockSize) == 3 and (y / self.blockSize) == 3)\
                        or ((x / self.blockSize) == 10 and (y / self.blockSize) == 11)\
                    or ((x / self.blockSize) == 11 and (y / self.blockSize) == 11):
                    rect = Rect(x, y, self.blockSize, self.blockSize)
                    pygame.draw.rect(self.window, (0, 110, 0), rect)
                    grid_map_line.append('r')

                # Create grid blocks.
                else:
                    rect = Rect(x, y, self.blockSize, self.blockSize)
                    pygame.draw.rect(self.window, (110, 110, 110), rect, 1)
                    grid_map_line.append(0)
            gridmap.append(grid_map_line)

        print(gridmap)

        return gridmap

    'Returns object that is located in gridmap position.'
    def get_grid_object(self, x, y):
        return self.gridmap[x][y]

    'Changes object in gridmap.'
    def change_grid_object(self, x, y, obj):
        self.gridmap[x][y] = obj

    def get_grid_dimensions(self):
        w = self.res_w / self.blockSize
        h = self.res_h / self.blockSize
        return [int(w), int(h)]


    'Converts pixels coordinates to grid coordinates.'
    def get_pos_in_grid(self, pos):
        x = math.floor(pos[0] / self.blockSize)
        y = math.floor(pos[1] / self.blockSize)
        return x,y

    'Checks if clicked grid is empty.'
    def position_empty(self, pos):
        x_pos_block, y_pos_block = self.get_pos_in_grid(pos)
        try:
            if self.gridmap[x_pos_block][y_pos_block] == 0:
                self.new_build_pos_x = x_pos_block
                self.new_build_pos_y = y_pos_block
                return 1
            return 0
        except IndexError:
            print("Outside of grid.")

    'Creates new building object and sets it to map.'
    def create_building(self):
        new_building = Building((self.new_build_pos_x, self.new_build_pos_y),
                                self.window,
                                self.blockSize,
                                self.res_w,
                                self.res_h
                                )
        self.change_grid_object(self.new_build_pos_x, self.new_build_pos_y, new_building)


    def troop_list_update(self, troop):
        lista = self.troops
        lista.append(troop)
        self.troops = lista


    'Sets building to select-position.'
    def select_building(self, pos):
        x, y = self.get_pos_in_grid(pos)
        # If IndexError occurs, it means that player clicked outside gridmap.
        try:
            grid_object = self.get_grid_object(x, y)
            if str(type(grid_object)) == "<class 'building.Building'>" and (self.object_selected == 0):
                self.object_selected = 1
                grid_object.select(1)
                dim = self.get_grid_dimensions()
                self.active_troop_button = Button(3, dim[1] - 2, 30, 2, "Troop", self.window)

                # Show button for user

                self.change_grid_object(3, dim[1] - 2, 'b')
                self.change_grid_object(4, dim[1] - 2, 'b')
                self.change_grid_object(3, dim[1] - 1, 'b')
                self.change_grid_object(4, dim[1] - 1, 'b')


                self.active_building = grid_object
                return

            if str(type(grid_object)) == "<class 'building.Building'>" and self.object_selected and grid_object.selected:
                self.object_selected = 0
                grid_object.select(0)

                # Remove button
                self.active_troop_button.remove_button()
                self.active_troop_button = None

                dim = self.get_grid_dimensions()
                self.change_grid_object(3, dim[1] - 2, 'p')
                self.change_grid_object(4, dim[1] - 2, 'p')
                self.change_grid_object(3, dim[1] - 1, 'p')
                self.change_grid_object(4, dim[1] - 1, 'p')
                self.active_building = None

            # Create troop
            if str(type(self.active_troop_button)) == "<class 'button.Button'>" and grid_object == 'b':
                troop = Unit(self.active_building.get_position(), self.window, self.blockSize, self.gridmap)
                self.troop_list_update(troop)

        except IndexError:
            print("Not active block at the moment.")
            return

    def update_troops(self):
        if self.troops != 0:
            for i in self.troops:
                i.move()

    'Draws lines to GUI.'
    def draw_line(self, x1, y1, x2, y2, col):
        pygame.draw.lines(self.window, col, True,
                          [(x1, y1), (x2, y2)], 1)


    'Update map in every iteration'
    def update(self):
        self.window.fill((255, 255, 204))
        for index_i, i in enumerate(self.gridmap):
            for index_j, j in enumerate(i):

                # Grid object empty.
                if j == 0:
                    rect = Rect(index_i * self.blockSize, index_j * self.blockSize, self.blockSize, self.blockSize)
                    pygame.draw.rect(self.window, ((255, 255, 204)), rect, 1)

                # Grid object building and not active.
                if str(type(j)) == "<class 'building.Building'>":

                    myimage = pygame.image.load("./sprites/tent.png")
                    imagerect = Rect(index_i * self.blockSize,
                                               index_j * self.blockSize,
                                               self.blockSize,
                                               self.blockSize
                                               )

                    self.window.blit(myimage, imagerect)

                # Grid object button.
                if j == 'b':
                    dim = self.get_grid_dimensions()
                    myimage = pygame.image.load("./sprites/miner_face.png")
                    imagerect = Rect(3 * self.blockSize,
                                     (dim[1] - 2) * self.blockSize,
                                     self.blockSize,
                                     self.blockSize
                                     )

                    self.window.blit(myimage, imagerect)

                # Resource
                if j == 'r':
                    myimage = pygame.image.load("./sprites/resource_1.png")
                    imagerect = Rect(index_i * self.blockSize,
                                            index_j * self.blockSize,
                                            self.blockSize,
                                            self.blockSize
                                            )

                    self.window.blit(myimage, imagerect)

                # Grid object active building
                if str(type(j)) == "<class 'building.Building'>" and self.active_building == j:
                    myimage = pygame.image.load("./sprites/tent_selected.png")
                    imagerect = Rect(index_i * self.blockSize,
                                            index_j * self.blockSize,
                                            self.blockSize,
                                            self.blockSize
                                            )
                    self.window.blit(myimage, imagerect)

                # Draw panel
                if j == 'p':
                    myimage = pygame.image.load("./sprites/panel_3.png")
                    imagerect = Rect(index_i * self.blockSize,
                                     index_j * self.blockSize,
                                     self.blockSize,
                                     self.blockSize
                                     )
                    self.window.blit(myimage, imagerect)

                if j == 'pe':
                    myimage = pygame.image.load("./sprites/panel_edge.png")
                    imagerect = Rect(index_i * self.blockSize,
                                     index_j * self.blockSize,
                                     self.blockSize,
                                     self.blockSize
                                     )
                    self.window.blit(myimage, imagerect)

                if j == 'l':
                    myimage = pygame.image.load("./sprites/log.png")
                    imagerect = Rect(index_i * self.blockSize,
                                     index_j * self.blockSize,
                                     self.blockSize,
                                     self.blockSize
                                     )
                    self.window.blit(myimage, imagerect)

