#!/usr/bin/python
import sys
#from mpi4py import MPI
debugMode = 0
def main(argv):
    filename = argv[0]
    num_cores = int(argv[1])
    
    with open(filename) as f:
        # read in lines from input file
        lines = f.readlines()

    # parse number of generations from input file
    num_iter = int(lines.pop(0))
    # parse board size from input file
    board_dim = int(lines.pop(0))

    # build the game board
    board = build_board(lines, board_dim)

    pretty_print_board(board, board_dim, board_dim)
    print ""

    #comm = MPI.COMM_WORLD

    # run the simulation
    for i in range(num_iter):
        board = run_iter(i, board, board_dim, num_cores)
        pretty_print_board(board, board_dim, board_dim)
        print ""

    # done; print the output
    #print_board(board, board_dim)


# takes the input file format and converts to 2d array for iterating
def build_board(lines, dim):
    # initialize 2d array for board
    board = [["0" for x in range(dim)] for x in range(dim)]

    for l in lines:
        # strip trailing whitespace
        l = l.strip()
        # split the line into the two coordinates
        tokens = l.split(',')
        # fill game board with starting live cells
        board[int(tokens[0])][int(tokens[1])] = "1"
    return board


def run_iter(comm, board, dim, num_cores):
    # divide board into num_cores subsections
    # have subsections include overlapping edge with other subsections
    # send subsection to be processed / updated for next iteration
    # merge output back into full board
    new_board = list(board)
    new_board.insert(0, board[dim-1])
    new_board.append(board[0])
    
    if(debugMode):
    	print "Matrix with ghost rows is..."
    	pretty_print_board(new_board, dim+2, dim)
    	print ""
	
    rank = 0
    #rank = comm.Get_rank()
    if (rank == 0):
        
        num_divisions = dim / num_cores
        if(debugMode):
        	print "Dividing input..."
        	print "Snipped boards are...\n"
        next_board = []
    	for row in range(1, num_cores*num_divisions, num_divisions):
    		rows = list(new_board[row-1:row+num_divisions+1])
		if(debugMode):
			pretty_print_board(rows,num_divisions+2,dim)
			print ""
		rsize = num_divisions + 2;
		csize = dim;
		processed_rows = process_section(rows, rsize, csize)
		if(debugMode):
			print("Processed snippet is...")
			pretty_print_board(processed_rows,num_divisions,csize)
			print ""
		for i in range(num_divisions):
			next_board.append(processed_rows[i])
	# divide and send
    else:
        pass
        # run divisions

    # return new board (result of iteration)
    return next_board


def process_section(section, dim):
    # declare next iteration board
    new_board = [["0" for x in range(dim)] for x in range(dim)]
    # process section; return section updated for next iteration
    for row in range(dim):
        for col in range(dim):
            result = check_cell(section, row, col, dim)
            # if cell should be dead, set to 0 in next iteration board
            if result == "die":
                new_board[row][col] = "0"
            # if cell reproduced or still lives, set to 1 in next board
            elif result == "reproduce" or result == "live":
                new_board[row][col] = "1"
    return new_board

def process_section(section, rsize, csize):
    # declare next iteration board
    if(debugMode):
    	print "rsize:" + str(rsize)
    	print "csize:" + str(csize)
    new_board = [["0" for x in range(csize)] for x in range(rsize-2)]
    # process section; return section updated for next iteration
    for row in range(0,rsize-2):
        for col in range(csize):
            result = check_cell(section, row, col, rsize,csize)
            # if cell should be dead, set to 0 in next iteration board
            if result == "die":
                new_board[row][col] = "0"
            # if cell reproduced or still lives, set to 1 in next board
            elif result == "reproduce" or result == "live":
                new_board[row][col] = "1"
    return new_board

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

def check_cell(board, row, col, rsize, csize):
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
    # merge processed sections back into full board
    # remove section overlap
    pass


# prints the board in the input file format
def print_board(board, dim):
    for row in range(dim):
        for col in range(dim):
            if(board[row][col] == "1"):
                print '%s,%s'%(row,col)


def pretty_print_board(board, col, row):
    print_str = ""
    for c in range(col):
        for r in range(row):
            print_str += str(board[c][r])
        print print_str
        print_str = ""


if __name__ == '__main__': main(sys.argv[1:])