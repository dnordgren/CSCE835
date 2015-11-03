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

