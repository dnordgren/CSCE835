#!/usr/bin/python
import sys

def main(argv):
    filename = argv[0]
    num_cores = argv[1]

    with open(filename) as f:
        # read in lines from input file
        lines = f.readlines()

    # parse number of generations from input file
    num_gens = int(lines.pop(0))
    # parse board size from input file
    board_dim = int(lines.pop(0))

    # build the game board
    board = build_board(lines, board_dim)

    # done; print the output
    print_board(board, board_dim)


# takes the input file format and converts to 2d array for iterating
def build_board(lines, dim):
    # initialize 2d array for board
    board = [[0 for x in range(dim)] for x in range(dim)]

    for l in lines:
        # strip trailing whitespace
        l = l.strip()
        # split the line into the two coordinates
        tokens = l.split(',')
        # fill game board with starting live cells
        board[int(tokens[0])][int(tokens[1])] = 1
    return board


def run_iter(board, dim):
    # divide board into num_cores subsections
    # have subsections include overlapping edge with other subsections
    # send subsection to be processed / updated for next iteration
    # merge output back into full board


def process_section(section, dim):
    # process section; return section updated for next iteration


def check_cell(board, row, col, dim):
    cell = board[row][col]

    # determine row index above cell
    up = row - 1
    if row == 0:
        up = dim - 1
    # determine row index below cell
    down = row + 1
    if row == dim-1:
        down = 0
    # determine col index left of cell
    left = col - 1
    if col == 0:
        left = dim - 1
    # determine col index right of cell
    right = col + 1
    if col == dim-1:
        right = 0

    # compute all neighbors
    cell_neighbors = []
    cell_neighbors.append(board[up][left])
    cell_neighbors.append(board[up][col])
    cell_neighbors.append(board[up][right])
    cell_neighbors.append(board[row][left])
    cell_neighbors.append(board[row][right])
    cell_neighbors.append(board[down][left])
    cell_neighbors.append(board[down][col])
    cell_neighbors.append(board[down][right])

    live_neighbors = cell_neighbors.count(1)

    if cell == 1:
        if live_neighbors < 2:
            return "die"
        elif live_neighbors > 3:
            return "die"
        else
            return "live"
    elif cell == 0:
        if live_neighbors == 3:
            return "reproduce"


def merge_sections(sections):
    # merge processed sections back into full board
    # remove section overlap


# prints the board in the input file format
def print_board(board, dim):
    for row in range(dim):
        for col in range(dim):
            if(board[row][col] == 1):
                print '%s,%s'%(row,col)
    

if __name__ == '__main__': main(sys.argv[1:])

