

import sys



def populate_map():
    grid = dict()
    grid[(0,0)] = 22
    grid[(1,0)] = '-'
    grid[(2,0)] = 9
    grid[(3,0)] = '*'
    grid[(0,1)] = '+'
    grid[(1,1)] = 4
    grid[(2,1)] = '-'
    grid[(3,1)] = 18
    grid[(0,2)] = 4
    grid[(1,2)] = '*'
    grid[(2,2)] = 11
    grid[(3,2)] = '*'
    grid[(0,3)] = '*'
    grid[(1,3)] = 8
    grid[(2,3)] = '-'
    grid[(3,3)] = 1
    return grid


def next_positions(current_position, grid):
    p = current_position
    ret = []

    if p == (3,3):
        return None


    if (p[0] + 1, p[1]) in grid:
        ret += [(p[0] + 1, p[1])]

    if (p[0] - 1, p[1]) in grid:
        ret += [(p[0] - 1, p[1])]

    if (p[0], p[1] + 1) in grid:
        ret += [(p[0] , p[1] + 1)]

    if (p[0], p[1] - 1) in grid:
        ret += [(p[0] , p[1] - 1)]

    return ret


def calculate_path_value(path, grid):
    value = grid[path[0]]
    next_op = None
    for loc in path[1:]:

        if next_op == None:
            next_op = grid[loc]
        else:
            if next_op == '-':
                value -= grid[loc]
            elif next_op == '+':
                value += grid[loc]
            elif next_op == '*':
                value *= grid[loc]
            else: 
                print("SOMETHING IS SCREWED UP")
            next_op = None
    return value

def dist(loc):
    return 3-loc[0] + 3-loc[1]

if __name__ == '__main__':
    grid = populate_map()

    paths_by_distance = {}

    paths_to_extend = [[(0,0)]]

    start_path = [(0,0)]

    paths_by_distance[len(start_path) + dist(start_path[-1])] = [start_path]


    while True:
        
        for i in sorted(paths_by_distance.keys()):
            if len(paths_by_distance[i]) > 0:
                this_path = paths_by_distance[i][0]
                paths_by_distance[i] = paths_by_distance[i][1:]
                break
        

        print("Investigating path of len:",len(this_path))
        neighbors = next_positions(this_path[-1],grid)

        for n in neighbors:
            if n == (3,3):
                if calculate_path_value(this_path + [n],grid) == 30:
                    print(this_path + [n])
                    sys.exit()
            elif n != (0,0):
                p = this_path + [n]
                expected_len = dist(p[-1]) + len(p)
                if expected_len < 14:
                    if expected_len not in paths_by_distance:
                        paths_by_distance[expected_len] = []
                    paths_by_distance[expected_len] += [p]
         





