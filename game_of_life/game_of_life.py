import random
import time

def dead_state(width, height):
    state = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(0)
        state.append(row)
    return state

def random_state(width, height):
    state = dead_state(width, height)
    for y in range(height):
        for x in range(width):
            random_number = random.random()
            if random_number >= 0.5:
                cell_state = 0
            else:
                cell_state = 1
            state[y][x] = cell_state
    return state

def load_state(filename):
    state = []
    file = open(filename, 'r')
    for line in file:
        stripped_line = line.rstrip()
        row = []
        for entry in stripped_line:
            row.append(int(entry))
        state.append(row)
    file.close()
    return state
            

def next_cell_state(coordinates, state):
    height = len(state)
    width = len(state[0])
    neighbors = 0
    y, x = coordinates
    for y1 in range((y-1), (y+1)+1):
        if y1 < 0 or y1 >= height:
            continue
        for x1 in range((x-1), (x+1)+1):
            if x1 < 0 or x1 >= width:
                continue
            if x1 == x and y1 == y:
                continue
            if state[y1][x1] == 1:
                neighbors += 1
                
    if state[y][x] == 1:
        if neighbors <= 1:
            return 0
        elif neighbors <= 3:
            return 1
        else:
            return 0
    else:
        if neighbors == 3:
            return 1
        else:
            return 0

def next_board_state(state):
    height = len(state)
    width = len(state[0])
    next_state = dead_state(width, height)
    for y in range(height):
        for x in range(width):
            next_state[y][x] = next_cell_state((y, x), state)
    return next_state
    
def render(state):
    print(' ' + '-' * len(state[0]))
    for y in state:
        print('|', end='')
        for x in y:
            if x == 1:
                print('Y', end='')
            else:
                print(' ', end='')
        print('|')
    print(' ' + '-' * len(state[0]))

#state = load_state('gosper_glider_gun.txt')
state = random_state(30,20)

while True:
    render(state)
    state = next_board_state(state)
    time.sleep(.1)
