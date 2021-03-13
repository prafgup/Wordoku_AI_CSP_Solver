import itertools
import time
import argparse
from copy import deepcopy
from CSP import Wordoku_CSP


def min_conflict(csp: Wordoku_CSP):

    max_c_val = 21 # can have at max 20 conflicts for any cell 
    min_conflict_allowed = max_c_val

    # generate a random wordoku
    csp.create_wordoku_random_copy()

    wordoku_grid_conflict_count = csp.get_total_grid_conflict()

    consistency_checks = 0
    max_consistency_checks = (10**5) # will run of this many maximum iteration else stop
    
    while consistency_checks < max_consistency_checks and wordoku_grid_conflict_count > 0:

        # get a valid random cell which is not pre set by input
        row , col = csp.get_random_row_col()
        if len(csp.domains[csp.encode_cell(row,col)]) == 1:
            continue
        csp.nodes_generated+=1

        # if current cell has conflicts remaining iterate over every possible element and set it to the one having lowest conflict
        if csp.get_cell_conflict_count(row, col, csp.wordoku[row][col]) > 0:
            for elem in range(len(csp.wordoku)):
                wordoku_cell_conflict_count = csp.get_cell_conflict_count(row, col, elem+1)
                if wordoku_cell_conflict_count < min_conflict_allowed: #this number has least conflict so setting current cell to this
                    min_conflict_allowed = wordoku_cell_conflict_count
                    csp.wordoku[row][col] = elem + 1
        
        # updating variables for iteration
        wordoku_grid_conflict_count = csp.get_total_grid_conflict()
        consistency_checks+=1
        min_conflict_allowed = max_c_val
    return csp




if __name__ == "__main__":
    current_wordoku_path = "./input.txt"
    print("Loading Wordoku From: {}".format(current_wordoku_path))
    start = time.time()
    wordoku = Wordoku_CSP(current_wordoku_path)
    search_time = time.time()
    solution = min_conflict(wordoku)
    search_end_time = time.time()
    wordoku.print_output_wordoku()
    end = time.time()
    print("Total Clock Time : {} seconds".format(end-start))
    print("Total Search Time : {} seconds".format(search_end_time-search_time))
    print("Conflicts Remaining : {}".format(solution.get_total_grid_conflict()))
    print("Nodes Generated : {}".format(solution.nodes_generated))
    print("Words Found : {}".format(solution.find_words_in_wordoku()))
    