import numpy as np

from extract_tiles import *
from potentials import *
from create_sphere import *
from display import *




def p(i, j, t):
    p = 1.0
    for i2, j2 in neighbors(i,j):
        p *= potential(t, tiles[world[i2, j2]], i2-1, j2-j)
    return p

def get_all_valid(i,j):
    result = []
    for t in range(len(tiles)):
        ismatch = True
        for ni, nj in neighbors(i,j):
            ismatch = ismatch and match(tiles[t], tiles[world[ni,nj]], ni - i, nj - j)
        if ismatch:
            result.append(t)
    return result


            # else:
            #     world[i,j] = random.choice(tiles)



def logp(world):
    logp = 0
    for i in range(world.shape[0]):
        for j in range(world.shape[1]):
            logp += np.log(p(i,j,tiles[world[i,j]]))
    print logp





tile_file_content = get_lines("tiles.txt")
tile_file_content = np.array(tile_file_content)


print "===="
tiles = get_tiles(tile_file_content)
tile_index_to_prior = np.ones(len(tiles)) / len(tiles)

show_tiles(tiles)
spheres = create_spheres(tiles)
print spheres.shape
print spheres[0,:,:,0]
print spheres[0,:,:,1]

print "===="
print spheres[1,:,:,0]
print spheres[1,:,:,1]
# print spheres[1]

# show_tiles()
# print potential(tiles[1], tiles[1], 1,0)
# print potential(tiles[1], tiles[1], 0,1)
# print potential(tiles[0], tiles[1], 1,0)
# print potential(tiles[0], tiles[1], 0,1)
# quit()

world = np.zeros((WORLD_WIDTH,WORLD_WIDTH)).astype(np.int32)
world = np.random.randint(0,len(tiles),(WORLD_WIDTH,WORLD_WIDTH)).astype(np.int32)


all_coords = []

for i in range(world.shape[0]):
    for j in range(world.shape[1]):
        all_coords.append((i,j))
last_selection_time = np.zeros_like(np.array(all_coords)[:,0])

# for step in range(5000):
#     i,j = random.choice(all_coords)
#     if step % 500 == 0:
#         print 
#         draw_world(world)
#     v = get_all_valid(i,j)
#     if v:
#         world[i,j] = random.choice(v)

for step in range(1500 * 4):
    p_sample = (1-np.exp(-step + last_selection_time)) **33
    p_sample = np.ones_like(p_sample)
    # print p_sample
    coord_index = np.random.choice(range(len(all_coords)), 1, p=p_sample / np.sum(p_sample))[0]
    i,j = all_coords[coord_index]
    last_selection_time[coord_index] = step
    if step % 150 == 0:
        print 
        print
        draw_world(world, tiles)
        # logp(world)
    ts, ps = get_tiles_and_probs(i,j,tiles, p)
    world[i,j] = np.random.choice(ts, 1, p=np.array(ps))

print
print
draw_world(world, tiles)




# print match(tiles[2], tiles[0], 0, -1)