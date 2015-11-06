#!/usr/bin/python
import sys
import getopt
import numpy as np
#from mpi4py import MPI

debug = 0
def main(argv):
    global debug
    filename = ''
    num_cores = 0

    try:
        opts, args = getopt.getopt(argv,"i:c:d")
    except getopt.GetoptError:
        help_string = ('gol.py -i <input_file>'
                             ' -c <num_cores>'
                             ' -d <if_debug>')
        print help_string
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-i':
            filename = arg
        elif opt == '-c':
            num_cores = int(arg)
        elif opt == '-d':
            debug = 1

    with open(filename) as f:
        # read in lines from input file
        lines = f.readlines()

    # parse number of generations from input file
    num_iter = int(lines.pop(0))
    # parse board size from input file
    board_dim = int(lines.pop(0))

    # build the game board
    board = build_board(lines, board_dim)
    if debug:
        print board
        print ""

    #comm = MPI.COMM_WORLD

    # run the simulation
    for i in range(num_iter):
        board = run_iter(1, board, board_dim, num_cores)
        if debug:
            #print board
            print ""

    # done; print the output
    #print_board(board, board_dim)


# takes the input file format and converts to 2d array for iterating
def build_board(lines, dim):
    global debug
    # initialize 2d array for board
    board = np.array([["0" for x in range(dim)] for x in range(dim)])

    for l in lines:
        # strip trailing whitespace
        l = l.strip()
        # split the line into the two coordinates
        tokens = l.split(',')
        # fill game board with starting live cells
        board[int(tokens[0]), int(tokens[1])] = "1"
    return board


def run_iter(comm, board, dim, num_cores):
    global debug
    # divide board into num_cores subsections
    # have subsections include overlapping edge with other subsections
    # send subsection to be processed / updated for next iteration
    # merge output back into full board

    # deep-copy board
    new_board = np.array(board)
    # add the last row as the new first row as padding
    new_board = np.insert(new_board, 0, [board[dim-1]], axis=0)
    # add the old first row as the new last row as padding
    new_board = np.append(new_board, [board[0]], axis=0)

    if debug:
        print "new board:"
        print new_board
        print "new column:"
        #print new_board[:,dim-1]
        print np.array(new_board[:,0]).reshape((len(new_board),1))

    # add the last column as the new first column as padding
    new_board = np.concatenate(([new_board[:,dim-1]], new_board), axis=1)
    # add the first column as the new last column as padding
    new_board = np.concatenate((new_board, np.array(new_board[:,0]).reshape((len(new_board),1))), axis=1)

    if debug:
        print "new board:"
        print new_board

    num_divisions = dim / num_cores
    for row in range(1, num_cores, num_divisions):
        rows = board[row-1:row+num_divisions]

    #rank = comm.Get_rank()
    # if (rank == 0):
    #     pass
    #     # divide and send
    # else:
    #     pass
    #     # run divisions

    # return new board (result of iteration)
    return process_section(board, dim)


def process_section(section, dim):
    global debug
    # declare next iteration board
    new_board = np.array([["0" for x in range(dim)] for x in range(dim)])
    # process section; return section updated for next iteration
    for row in range(dim):
        for col in range(dim):
            result = check_cell(section, row, col, dim)
            # if cell should be dead, set to 0 in next iteration board
            if result == "die":
                new_board[row,col] = "0"
            # if cell reproduced or still lives, set to 1 in next board
            elif result == "reproduce" or result == "live":
                new_board[row,col] = "1"
    return new_board


def check_cell(board, row, col, dim):
    global debug
    cell = board[row,col]

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
    cell_neighbors.append(board[up,left])
    cell_neighbors.append(board[up,col])
    cell_neighbors.append(board[up,right])
    cell_neighbors.append(board[row,left])
    cell_neighbors.append(board[row,right])
    cell_neighbors.append(board[down,left])
    cell_neighbors.append(board[down,col])
    cell_neighbors.append(board[down,right])

    live_neighbors = cell_neighbors.count("1")
    #print "live neighbors = " + str(live_neighbors)
    if cell == "1":
        if live_neighbors < 2:
            return "die"
        elif live_neighbors > 3:
            return "die"
        else:
            return "live"
    elif cell == "0":
        if live_neighbors == 3:
            return "reproduce"
        else:
            return "NA"


def merge_sections(sections):
    global debug
    # merge processed sections back into full board
    # remove section overlap
    pass


# prints the board in the input file format
def print_board(board, dim):
    for row in range(dim):
        for col in range(dim):
            if(board[row,col] == "1"):
                print '%s,%s'%(row,col)


def pretty_print_board(board):
    # determine the number of rows
    row = len(board)
    # determine the number of columns
    col = len(board[0])

    print_str = ""
    for r in range(row):
        for c in range(col):
            print_str += str(board[r,c])
        print print_str
        print_str = ""


if __name__ == '__main__': main(sys.argv[1:])
