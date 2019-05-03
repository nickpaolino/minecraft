from mcpi.minecraft import Minecraft
import shelve

mc = Minecraft.create()


def save(name, structure):
    shelve_dict = shelve.open('locationsFile.db')
    shelve_dict[name] = structure


def place(structure, distance_x=0, distance_y=0, distance_z=0):
    x, y, z = mc.player.getPos()
    buildStructure(x + distance_x, y + distance_y, z + distance_z, structure)


def sortPair(val1, val2):
    if val1 > val2:
        return val2, val1
    else:
        return val1, val2


def copyStructure(x1, y1, z1, x2, y2, z2):
    x1, x2 = sortPair(x1, x2)
    y1, y2 = sortPair(y1, y2)
    z1, z2 = sortPair(z1, z2)
    width = x2 - x1 or 1
    height = y2 - y1 or 1
    length = z2 - z1 or 1
    total = width * height * length
    count = 0
    structure = []
    print("Please wait...")
    # Copy the structure
    for row in range(height):
        structure.append([])
        for column in range(width):
            structure[row].append([])
            for depth in range(length):
                count += 1
                print(count, ' / ', total)
                block = mc.getBlock(x1 + column, y1 + row, z1 + depth)
                structure[row][column].append(block)
    return structure


def buildStructure(x, y, z, structure):
    xStart = x
    zStart = z
    for row in structure:
        for column in row:
            for block in column:
                mc.setBlock(x, y, z, block)
                z += 1
            x += 1
            z = zStart
        y += 1
        x = xStart


def setup():
    name = raw_input("What is the name of the structure you'd like to build?")
    place(name)


def initiate_copy():
    # Get the position of the first corner
    raw_input("Move to the first corner and press enter in this window")
    pos = mc.player.getTilePos()
    x1, y1, z1 = pos.x, pos.y, pos.z
    print(pos)
    # Get the position of the second corner
    raw_input("Move to the opposite corner and press enter in this window")
    pos = mc.player.getTilePos()
    x2, y2, z2 = pos.x, pos.y, pos.z
    print(pos)
    # Copy the building
    structure = copyStructure(x1, y1, z1, x2, y2, z2)
    # Set the position for the copy
    name = raw_input("What do you want to call it?")
    save(name, structure)
