from constants import *
from potentials import *
from helpers import *
from display import *
import numpy as np
from multiprocessing import Pool
# from numba import jit




def test_bfs():
    grid = np.zeros((3,3))
    for i, item in enumerate(grid_bfs(1,1,3)):
        print (item)
        grid[item] = i
    print (grid)

def get_bfs_sphere_slice(central_tile_index, tiles):
    sphere = np.zeros([SPHERE_WIDTH, SPHERE_WIDTH, SPHERE_WIDTH, len(tiles)])
    # print ("CENTRAL TILE", central_tile_index)
    visited = np.zeros([SPHERE_WIDTH, SPHERE_WIDTH, SPHERE_WIDTH]) 
    visited[SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, SPHERE_WIDTH // 2] = 1
    sphere[SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, :] = 0
    sphere[SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, central_tile_index] = 1 


    for query_i, query_j, query_l in grid_bfs(SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, SPHERE_WIDTH):
        # if central_tile_index == 2:    
        #     print (query_i, query_j)
        # if query_i == SPHERE_WIDTH // 2 and query_j == SPHERE_WIDTH // 2:
        #     continue
        # print ("  bfs to", i,j)
        for neighbor_i, neighbor_j, neighbor_l in neighbors(query_i,query_j, query_l, width = SPHERE_WIDTH):
            if visited[neighbor_i, neighbor_j, neighbor_l] == 1:
                prob_from = sphere[neighbor_i, neighbor_j, neighbor_l, :]
                # print ("==")
                # print (transition_matrix(neighbor_i - query_i, neighbor_j - query_j, neighbor_l - query_l).shape)
                # print (prob_from.shape)
                prob_to = transition_matrix(neighbor_i - query_i, neighbor_j - query_j, neighbor_l - query_l).dot(prob_from)
                sphere[query_i,query_j, query_l, :] += prob_to

        if np.sum(sphere[query_i,query_j, query_l, :]) != 0:
            sphere[query_i,query_j, query_l, :] = sphere[query_i,query_j, query_l, :] / np.sum(sphere[query_i,query_j, query_l, :])
        else:
            sphere[query_i,query_j, query_l, :] = 0
        visited[query_i,query_j, query_l] = 1

    return sphere


def get_ac3_arc_consistency_slice(central_tile_index, tiles):
    worklist = np.ones([SPHERE_WIDTH, SPHERE_WIDTH, SPHERE_WIDTH])
    sphere = np.ones([SPHERE_WIDTH, SPHERE_WIDTH, SPHERE_WIDTH, len(tiles)])
    print ("SPHERE_WIDTH", SPHERE_WIDTH / 2, sphere.shape)

    sphere[SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, :] = 0

    sphere[SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, central_tile_index] = 1

    while True:
        old_sphere = sphere.copy()
        # for query_i in range(SPHERE_WIDTH):
        #     for query_j in range(SPHERE_WIDTH):
        #         for query_k in range(SPHERE_WIDTH):
        work_indices = zip(*np.where(worklist==1))
        for indices in work_indices:
            query_i, query_j, query_k = indices
            # print (indices)
            for neighbor_i, neighbor_j, neighbor_k in neighbors(query_i, query_j, query_k, width = SPHERE_WIDTH):
                    prob_from = sphere[neighbor_i, neighbor_j, neighbor_k, :]
                    trans = transition_matrix(neighbor_i - query_i, neighbor_j - query_j, neighbor_k - query_k)
                    assert np.max(trans) <= 1
                    prob_to = trans.dot(prob_from)
                    prob_to = (prob_to > 0).astype(np.int32)
                    assert np.max(prob_to) <= 1

                    sphere[query_i,query_j, query_k, :] *= prob_to
            worklist = np.any(old_sphere != sphere, axis=-1)
            # print (worklist.shape)
        if np.all(sphere == old_sphere):
            break
    # print ("created sphere", central_tile_index)
    return sphere

def get_arc_consistency_slice(central_tile_index, tiles):
    sphere = np.ones([SPHERE_WIDTH, SPHERE_WIDTH, SPHERE_WIDTH, len(tiles)])
    sphere[SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, :] = 0
    sphere[SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, SPHERE_WIDTH // 2, central_tile_index] = 1

    while True:
        old_sphere = sphere.copy()
        for query_i in range(SPHERE_WIDTH):
            for query_j in range(SPHERE_WIDTH):
                for query_k in range(SPHERE_WIDTH):

                    for neighbor_i, neighbor_j, neighbor_k in neighbors(query_i, query_j, query_k, width = SPHERE_WIDTH):
                            prob_from = sphere[neighbor_i, neighbor_j, neighbor_k, :]
                            trans = transition_matrix(neighbor_i - query_i, neighbor_j - query_j, neighbor_k - query_k)
                            assert np.max(trans) <= 1
                            prob_to = trans.dot(prob_from)
                            prob_to = (prob_to > 0).astype(np.int32)
                            assert np.max(prob_to) <= 1

                            sphere[query_i,query_j, query_k, :] *= prob_to
        if np.all(sphere == old_sphere):
            break
    # print ("created sphere", central_tile_index)
    return sphere




def f(a):
    central_tile_index, tiles = a
    # return get_bfs_sphere_slice(central_tile_index, tiles)
    return get_arc_consistency_slice(central_tile_index, tiles)
    # return get_bfs_sphere_slice(central_tile_index, tiles) * get_arc_consistency_slice(central_tile_index, tiles)

# def create_spheres(tiles):
#     p = Pool(7)
#     spheres = p.map(f, zip(range(len(tiles)), [tiles] * len(tiles)))
#     spheres = np.array(spheres)
#     return spheres

def create_spheres(tiles):
    spheres = []
    for i in range(len(tiles)):
        # s1 = get_ac3_arc_consistency_slice(i, tiles)
        # s2 = get_arc_consistency_slice(i, tiles)
        # assert len(set(s1.flatten())) == 2
        # assert len(set(s2.flatten())) == 2
        # # assert np.all(s1 == s2), (np.sum(s1), np.sum(s2)) 
        # if not np.all(s1 == s2):
        #     print ("")
        #     print (s1[s1 != s2])
        #     print (np.sum(s1))
        #     print (s2[s1 != s2])
        #     print (np.sum(s2))

        # spheres.append(get_arc_consistency_slice(i, tiles))
        spheres.append(get_ac3_arc_consistency_slice(i, tiles))

        # print ("made sphere", i)
    return np.array(spheres)


