import itertools
import time
import argparse
from copy import deepcopy
from CSP import Wordoku_CSP


# checks if current solution is consistent with constraints
def check_consistent(assignment, constraints, value, var):
    for rule in constraints:
        if rule in assignment.keys() and assignment[rule] == value:
            return False
    return True

# backtracking entry point
def backtracking_csp(csp):
    return backtracking(csp.assignment,csp)


# main baccktracking function
def backtracking(assignment, csp : Wordoku_CSP):
    csp.nodes_generated+=1
    #print(csp.nodes_generated)

    # end if assignment is complete
    if set(assignment.keys()) == csp.variables_set:
        return csp

    # get new unassigned mrv cell
    curr = select_new_unassigned_value_mrv(assignment, csp)
    # create a deep copy of current domain in case there is a need for backtracking
    curr_domain = deepcopy(csp.domains)

    # try every value in current domain
    for value in csp.domains[curr]:
        if check_consistent(assignment,csp.constraints[curr], value, curr):
            assignment[curr] = value
            #remove current value from domains of other which have constraints with current cell
            domain_shortened = remove_possibilities_from_others(assignment, csp, curr, {value})
            if domain_shortened!= False:
                # move forward if current shortning domain passed
                result = backtracking(assignment, csp)
                if result!=False:
                    return result
            # backtrack if this assignment failed, remove current added assignment and set domain to old value
            del assignment[curr]
            csp.domains = curr_domain
    return False


# returns the cell with least size of its possible domain 
def select_new_unassigned_value_mrv(assignment, csp):
    unassigned_cells = []
    # for every cell in its variables add (length_domai,cell) in array to be sorted
    for cell in csp.variables:
        if cell not in assignment.keys():
            unassigned_cells.append([len(csp.domains[cell]),cell])
    # sort and return minimum domain length value
    unassigned_cells.sort()
    min_remaining_value = min(unassigned_cells)
    return min_remaining_value[1]


#remove current value from domains of other which have constraints with current cell using recusrion
def remove_possibilities_from_others(assignment, csp, curr, value):

    # for every cell in its constraint
    for cell in csp.constraints[curr]:
        # if cell is not already assigned then remove that value from its domain
        if cell not in assignment and value in csp.domains[cell]:
            if len(csp.domains[cell])==1:
                return False
            csp.domains[cell].remove(value)
            # if length of current domain is 1 the recursely shorten others domain again
            if len(csp.domains[cell])==1:
                result = remove_possibilities_from_others(assignment, csp, cell, csp.domains[cell])
                if flresultag == False:
                    return False

    return True




if __name__ == "__main__":
    current_wordoku_path = "./input.txt"
    print("Loading Wordoku From: {}".format(current_wordoku_path))
    start = time.time()
    wordoku = Wordoku_CSP(current_wordoku_path)
    search_time = time.time()
    solution = backtracking_csp(wordoku)
    search_end_time = time.time()
    wordoku.print_output_wordoku()
    end = time.time()
    print("Total Clock Time : {} seconds".format(end-start))
    print("Total Search Time : {} seconds".format(search_end_time-search_time))
    print("Conflicts Remaining : {}".format(solution.get_total_grid_conflict()))
    print("Nodes Generated : {}".format(solution.nodes_generated))
    print("Words Found : {}".format(solution.find_words_in_wordoku()))
    