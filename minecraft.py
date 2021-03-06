from mcpi import minecraft
from mcpi import block
from block_types import *
from time import sleep
from random import randint
from walls import defenses
from write import write
from mcpi.vec3 import Vec3
import objects
from copy_functions import *

mc = minecraft.Minecraft.create()

class Player:
    def __init__(self, mc):
        self.mc = mc
        self.mc.player.setPos(0, 2, 4)
        self.check_player_pos()

    def get_player_pos(self):
        return self.x, self.y, self.z

    def set_player_pos(self, x, y, z):
        self.mc.player.setPos(x, y, z)

    def check_player_pos(self):
        if hasattr(self, 'x') and hasattr(self, 'y') and hasattr(self, 'z'):
            self.lastX, self.lastY, self.lastZ = self.x, self.y, self.z
        self.x, self.y, self.z = self.mc.player.getPos()

    def draw(self, time=100, block_type=FLOWER_CYAN):
        for x in range(time):
            self.check_player_pos()
            if round(self.lastX, 1) != round(self.x, 1) or round(self.lastY, 1) != round(self.y, 1) or round(self.lastZ, 1) != round(self.z, 1):
                self.mc.setBlock(self.lastX, self.lastY, self.lastZ, block_type)
            sleep(0.1)

    def shower(self, num, block_type=FLOWER_CYAN):
        for x in range(num):
            self.mc.setBlock(self.x + randint(-50, 50), self.y + randint(1, 50), self.z + randint(-50, 50), block_type)

    def forward(self, steps):
        x, y, z = mc.player.getDirection()
        greaterThan = abs(x) > abs(z)
        x = round(x)
        z = round(z)
        if greaterThan:
            mc.player.setPos(self.x + (steps * x), self.y, self.z)
        else:
            mc.player.setPos(self.x, self.y, self.z + (steps * z))

    def up(self, steps):
        mc.player.setPos(self.x, self.y + steps, self.z)

    def save(self):
        return mc.player.getPos()

    def teleport(self, location):
        self.mc.player.setPos(location)

    def goto(self, x, y, z):
        self.mc.player.setPos(x, y, z)


class World:
    def __init__(self):
        self.mc = minecraft.Minecraft.create()
        self.create_landscape(33, 10, 23)
        self.player = Player(self.mc)

    def get_mc(self):
        return self.mc

    def get_player(self):
        return self.player

    def create_landscape(self, moatwidth, moatdepth, islandwidth):
        # Set upper half to air
        self.mc.setBlocks(-128, 1, -128, 128, 128, 128, block.AIR)

        # Set lower half of world to dirt with a layer of grass
        self.mc.setBlocks(-128, -1, -128, 128, -128, 128, block.DIRT)
        self.mc.setBlocks(-128, 0, -128, 128, 0, 128, block.GRASS)


world = World()
player = world.player


class Entity:
    def __init__(self, type, size, x=0, y=0, z=0):
        self.mc = world.get_mc()
        self.player = world.get_player()
        self.set_player_pos()
        self.x = x
        self.y = y
        self.z = z
        self.build(type, size, x, y, z)

    def set_player_pos(self):
        pos = self.player.get_player_pos()
        self.pos = pos
        self.x, self. y, self.z = pos

    def set_blocks(self, block_type=4, size=None, width=None, height=None, length=None, x_distance=1, y_distance=0, z_distance=1):
        if not width and not height and not length:
            width, height, length = size, size, size

        self.mc.setBlocks(self.x + x_distance, self.y + y_distance, self.z + z_distance, self.x + + x_distance + width, self.y + + y_distance + height, self.z + z_distance + length, block_type)

    def build(self, type, size, x=0, y=0, z=0):
        if type == 'cube':
            self.cube(size, x, y, z)
        elif type == 'tree':
            self.tree(size, x, y, z)

    def cube(self, size, x=0, y=0, z=0, doorway=True, block_type=4):
        self.set_blocks(size=size, block_type=block_type, x_distance=x, y_distance=y, z_distance=z)

        # creates hollow interior
        self.set_blocks(size=(size - 1), x_distance=2, z_distance=2, block_type=0)

        if doorway:
            self.mc.setBlocks(self.x + (size / 2), self.y, self.z + 1, self.x + (size / 2), self.y + (size / 4), self.z + 1, 0)

    def tree(self, x=0, y=0, z=0, size=5):
        wood = 17
        leaves = 18

        # Trunk
        self.mc.setBlocks(self.x + x, self.y + y, self.z + z, self.x + x, self.y + y + size, self.z + z, wood)
        # Leaves
        self.mc.setBlocks(self.x + x - 2, self.y + y + size + 1, self.z + z - 2, self.x + 2 + x, self.y + y + size + 1, self.z + z + 2, leaves)
        self.mc.setBlocks(self.x + x - 1, self.y + y + size + 2, self.z + z - 1, self.x + 1 + x, self.y + y + size + 2, self.z + z + 1, leaves)


def cube(size, x=0, y=0, z=0, type='cube'):
    player.check_player_pos()
    Entity(type, size, x, y, z)


# def tree(size=5, x=0, y=0, z=0, type='tree'):
#     player.check_player_pos()
#     Entity(type, size, x, y, z)


def walls(height=6):
    defenses(13, 1, height, STONE_BRICK, True, True, world.mc)


def text(text, material=STONE_BRICK):
    write(world.mc, text, material)


def starting_text(text, material=GOLD_BLOCK):
    write(world.mc, text, material, starting_pos=Vec3(46, 15, 35))


def water_flowing(text, material=WATER_FLOWING):
    write(world.mc, text, material, starting_pos=Vec3(46, 10, 35))


def list():
    for item in ['house', 'tree', 'temple', 'mansion', 'pool', 'office', 'tunnel']:
        print(item)


def house(x=1, y=0, z=1):
    place(objects.house, x, y, z)


def tree(x=1, y=0, z=1):
    place(objects.tree, x, y, z)


def temple(x=1, y=0, z=1):
    place(objects.temple, x, y, z)


def office(x=1, y=0, z=1):
    place(objects.office, x, y, z)


def mansion(x=1, y=0, z=1):
    place(objects.mansion, x, y, z)


def pavilion(x=1, y=0, z=1):
    place(objects.pavilion, x, y, z)


def water(x=1, y=0, z=1):
    place(objects.water, x, y, z)


def tunnel(x=1, y=0, z=1):
    place(objects.tunnel, x, y, z)


def building(x=1, y=0, z=1):
    place(objects.center, x, y, z)


def pool(x=1, y=0, z=1):
    place(objects.pool_with_slide, x, y, z)


def pool_with_lava(x=1, y=0, z=1):
    place(objects.pool_with_lava, x, y, z)


starting_text('RENAISSANCE YOUTH CENTER')
water_flowing('RENAISSANCE YOUTH CENTER')
