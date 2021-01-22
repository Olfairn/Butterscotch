"""
Visualization of a MCMC simulation of a supermarket.
"""
import time
import numpy as np
import cv2
from helper_funcs import move_step, get_target_coordinates, get_time
import test2

PROBS = test2.create_prob_mat()
CUS_FIRST_START_TIME = test2.cus_first_stat_time
STATES= test2.first_state_prop

MARKET = """
##################
##..............##
##..PY..MF..FB..##
##..PY..MF..FB..##
##..PY..MF..FB..##
##..PY..MF..FB..##
##..PY..MF..FB..##
##...............#
##..C#..C#..C#...#
##..##..##..##...#
##...............#
##############GG##
""".strip()

#STATES = [0.288, 0.154, 0.377, 0.181]
# PROBS = {'dairy': [ 0.103,  0.737,  0.059,  0.049,  0.052],
#         'drinks': [0.211,  0.086,  0.065,  0.587,  0.051],
#         'fruit': [0.201,  0.096,  0.055,  0.597,  0.051],
#         'spices': [0.150,  0.193,  0.163,  0.091,  0.403]}
TILE_SIZE = 32
OFS = 50
SIMULATE_DAY = 60*14


class SupermarketMap:
    """Maps the supermarket background"""
    def __init__(self, layout, tiles_options):
        """
        layout : a string with each character representing a tile
        tile   : a numpy array containing the tile image
        """
        self.tiles = tiles_options
        self.contents = [list(row) for row in layout.split('\n')]
        self.xsize =  len(self.contents[0])
        self.ysize = len(self.contents)
        self.image = np.zeros((self.ysize * TILE_SIZE, self.xsize * TILE_SIZE, 3), dtype=np.uint8)
        self.prepare_map()

    def get_tiles(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.tiles[0 : TILE_SIZE, 0 : TILE_SIZE]
        elif char == "G":
            return self.tiles[7 * TILE_SIZE : 8 * TILE_SIZE, 3 * TILE_SIZE : 4 * TILE_SIZE]
        elif char == "C":
            return self.tiles[2 * TILE_SIZE : 3 * TILE_SIZE, 8 * TILE_SIZE : 9 * TILE_SIZE]
        elif char == "B":
            return self.tiles[1 * TILE_SIZE : 2 * TILE_SIZE,  10 * TILE_SIZE: 11 * TILE_SIZE]
        elif char == "P":
            return self.tiles[6 * TILE_SIZE : 7 * TILE_SIZE, 13 * TILE_SIZE : 14 * TILE_SIZE]
        elif char == "M":
            return self.tiles[6 * TILE_SIZE : 7 * TILE_SIZE, 11 * TILE_SIZE : 12 * TILE_SIZE]
        elif char == "F":
            return self.tiles[7 * TILE_SIZE : 8 * TILE_SIZE, 12 * TILE_SIZE : 13 * TILE_SIZE]
        elif char == "Y":
            return self.tiles[1 * TILE_SIZE : 2 * TILE_SIZE, 3 * TILE_SIZE : 4 * TILE_SIZE]
        else:
            return self.tiles[TILE_SIZE : TILE_SIZE * 2, TILE_SIZE * 2:TILE_SIZE * 3]

    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for y, row in enumerate(self.contents):
            for x, tile in enumerate(row):
                all_tiles = self.get_tiles(tile)
                self.image[y * TILE_SIZE:(y+1)*TILE_SIZE,
                      x * TILE_SIZE:(x+1)*TILE_SIZE] = all_tiles

    def draw(self, s_frame):
        """draws the image into a bigger frame
        offset pixels from the top left corner"""
        s_frame[OFS:OFS+self.image.shape[0], OFS:OFS+self.image.shape[1]] = self.image


class Customer:
    """Class to create customers."""

    def __init__(self, image,cus_id):
        self.image = image
        self.x = 14
        self.y = 11
        self.target = np.random.choice(STATES.index.values, p=STATES)
        self.tx = get_target_coordinates(self.target)[0]
        self.ty = get_target_coordinates(self.target)[1]
        self.current = 'entrance'
        self.active = True
        self.journey = [self.current]
        self.cus_id = cus_id

    def move(self):
        """moves the customer around, aka updates x and y."""
        if self.x == self.tx and self.y == self.ty:
            self.current = self.target
            if self.current == 'exit':
                self.active = False
                print(self)
            else:
                self.next_state()
        new_x, new_y = move_step(self.x, self.y, self.tx, self.ty, self.current, self.target)
        self.x, self.y = new_x, new_y


    def next_state(self):
        """ Updates the target locations using a weighted random choice from the
        transition probabilities conditional on the current state."""
        if self.current == 'checkout':
                self.target = 'exit'
                self.tx, self.ty = 14, 11
        elif self.current != 'exit':
            probs = PROBS[self.current]
            self.target = np.random.choice(PROBS.index.values,
                                            p=probs)
            self.tx, self.ty = get_target_coordinates(self.target)
        self.journey.append(self.target)

    def draw(self, s_frame):
        """draws the customer into the market"""
        xpos = OFS + self.x * TILE_SIZE
        ypos = OFS + self.y * TILE_SIZE
        s_frame[ypos:ypos+self.image.shape[0], xpos:xpos+self.image.shape[1]] = self.image

    def __repr__(self):
        return f'The journey of {self.cus_id} was: {self.journey}'


class SupermarketVisualization:
    """Simulates and visualizes multiple customers"""

    def __init__(self):
        self.customers = []

    def move(self):
        """move each customer"""
        for customer in self.customers:
            customer.move()

    def draw(self, frame):
        """draws each customer"""
        for customer in self.customers:
            customer.draw(frame)

    def add_new_customers(self):
        """new customers enter the shop so there are 5 at all times."""
        if len(self.customers) < 5:
            for cus_id in range(len(CUS_FIRST_START_TIME)):
                self.customers.append(Customer(c_image, cus_id))

    def remove_exited_customers(self):
        """removes customers that are done shopping"""
        self.customers = [customer for customer in self.customers if customer.active]



if __name__ == '__main__':
    background = np.zeros((700, 1000, 3), np.uint8)
    tiles = cv2.imread('tiles.png')
    c_image = tiles[8 * TILE_SIZE : 9 * TILE_SIZE, 2 * TILE_SIZE : 3 * TILE_SIZE]
    tmap = SupermarketMap(MARKET, tiles)
    vis = SupermarketVisualization()

    minutes = 0 
    # FIXME: use the entrance time from the real data

    for _ in range(SIMULATE_DAY):
        minutes += 1
        frame = background.copy()
        tmap.draw(frame)
        vis.move()
        vis.draw(frame)
        vis.add_new_customers()
        vis.remove_exited_customers()
        current_time = get_time(minutes)
        cv2.putText(frame, current_time, (50, 430), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255))
        cv2.imshow('frame', frame)

        key = chr(cv2.waitKey(1) & 0xFF)
        if key == 'q':
            break

        time.sleep(0.1)

    cv2.destroyAllWindows()
