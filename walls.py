from block_types import *


def defenses(size, base, height, material, battlements, walkway, mc):
    mc.setBlocks(-size, base+1, -size, size, base + height, -size, material)
    mc.setBlocks(-size, base+1, -size, -size, base + height, size, material)
    mc.setBlocks(size, base+1, size, -size, base + height, size, material)
    mc.setBlocks(size, base+1, size, size, base + height, -size, material)

    for x in range(0, (2 * size) + 1, 2):
        mc.setBlock(size, base + height+1,(x - size), material)
        mc.setBlock(-size, base + height+1,(x - size), material)
        mc.setBlock((x-size), base + height+1, size, material)
        mc.setBlock((x-size), base + height+1, -size, material)
        mc.setBlocks(-size+1, base + height-1, size - 1, size - 1, base + height-1, size - 1, WOOD_PLANKS)
        mc.setBlocks(-size+1, base + height-1, -size + 1, size - 1, base + height-1, -size + 1, WOOD_PLANKS)
        mc.setBlocks(-size+1, base + height-1, -size+1, -size + 1, base + height-1, size - 1, WOOD_PLANKS)
        mc.setBlocks(size-1, base + height-1, -size + 1, size - 1, base + height-1, size - 1, WOOD_PLANKS)
