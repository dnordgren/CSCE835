#!/usr/bin/python
import sys
from mpi4py import MPI
import getopt
import numpy as np

debug = 0
def main(argv):
    comm = MPI.COMM_WORLD
    global debug
    filename = ''
    num_cores = comm.Get_size()

    try:
        opts, args = getopt.getopt(argv,'i:d')
    except getopt.GetoptError:
        help_string = ('gol.py -i <input_file>'
                             ' -d <if_debug>')
        print help_string
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-i':
            filename = arg
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
    # if debug:
    #     pretty_print_board(board)
    #     print ""

    rank = comm.Get_rank()
    # head
    if rank == 0:
        # deep-copy the new board to process
        new_board = list(board)
        # pad the by new board top row with the original board's bottom row
        new_board.insert(0, board[board_dim-1])
        # pad the new board bottom row the original board's top row
        new_board.append(board[0])

        # divide across number of workers (total cores - 1)
        num_divisions = board_dim / (num_cores-1)
        next_board = []
        # create a queue of rows to process
        rows_to_process = []
        for row in range(1, num_cores*num_divisions, num_divisions):
            rows = list(new_board[row-1:row+num_divisions+1])
            # add the new set of rows to the queue to be processed
            rows_to_process.append(rows)

        if debug:
            num_rows_to_process = len(rows_to_process)
            print "Number of chunks to process:" + str(num_rows_to_process)
            for i in range(num_rows_to_process):
                print rows_to_process[i]

        for i in range(0, len(rows_to_process)-1):
            worker_id = i+1
            if debug:
                print "sending data to worker: " + str(worker_id)
            # allocate array to send to workers
            data = np.array(rows_to_process[i], dtype='i')
            # send a row to some worker to process
            #comm.Send([data, MPI.INT], dest=i+1)
            comm.Isend([data, MPI.INT], dest=worker_id)

        processed_rows = []
        for i in range(0, len(rows_to_process)-1):
            # allocate space to receive processed row from worker
            recv = np.zeros((2,6), dtype='i')
            # receive processed row from worker
            comm.Recv([recv, MPI.INT], MPI.ANY_SOURCE)
            processed_rows.append([recv])
            if debug:
                print "received processed row from worker"
                print recv

        # declare space for the merged board
        merged_board = processed_rows[0]
        # merge the processed rows back together
        for sub_board in range(1, len(processed_rows)):
            #stack subsequent rows
            merged_board = np.vstack((merged_board, processed_rows[sub_board]))

        # remove numpy's formatting
        merged_board.flatten()
        # shape back to correct dimensions
        merged_board.shape = (board_dim, board_dim)

        if debug:
            print "finished iteration:"
            print merged_board



    # workers
    else:
        # allocate space to receive row to process from head
        data = np.zeros((4,6), dtype='i')
        # receive row to process from head
        comm.Recv([data, MPI.INT], source=0)
        # process the row
        processed_row = np.array(process_section(data, 4, 6), dtype='i')
        # send the processed row back to head
        comm.Send([processed_row, MPI.INT], dest=0)


# takes the input file format and converts to 2d array for iterating
def build_board(lines, dim):
    global debug
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


def process_section(section, rsize, csize):
    global debug
    # declare next iteration board
    new_board = [[0 for x in range(csize)] for x in range(rsize-2)]
    # process section; return section updated for next iteration
    for row in range(1, rsize-1):
        for col in range(csize):
            result = check_cell(section, row, col, rsize,csize)
            # if cell should be dead, set to 0 in next iteration board
            if result == "die":
                new_board[row-1][col] = 0
            # if cell reproduced or still lives, set to 1 in next board
            elif result == "reproduce" or result == "live":
                new_board[row-1][col] = 1
    return new_board


def check_cell(board, row, col, rsize, csize):
    global debug
    cell = board[row][col]

    # determine row index above cell
    up = row - 1
    if row == 0:
        up = rsize - 1
    # determine row index below cell
    down = row + 1
    if row == rsize-1:
        down = 0
    # determine col index left of cell
    left = col - 1
    if col == 0:
        left = csize - 1
    # determine col index right of cell
    right = col + 1
    if col == csize-1:
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
    #print "live neighbors = " + str(live_neighbors)
    if cell == 1:
        if live_neighbors < 2:
            return "die"
        elif live_neighbors > 3:
            return "die"
        else:
            return "live"
    elif cell == 0:
        if live_neighbors == 3:
            return "reproduce"
        else:
            return "NA"


# prints the board in the input file format
def print_board(board, dim):
    for row in range(dim):
        for col in range(dim):
            if(board[row][col] == 1):
                print '%s,%s'%(row,col)


def pretty_print_board(board):
    row = len(board)
    col = len(board[0])
    print_str = ""
    for r in range(row):
        for c in range(col):
            print_str += str(board[r][c])
        print print_str
        print_str = ""


if __name__ == '__main__': main(sys.argv[1:])
