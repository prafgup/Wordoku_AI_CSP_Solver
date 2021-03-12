import itertools
import time
import argparse
from copy import deepcopy
from CSP import Wordoku_CSP


def check_consistent(assignment, constraints, value, var):
    for rule in constraints:
        if rule in assignment.keys() and assignment[rule] == value:
            return False
    return True


def backtracking_csp(csp):
    return backtracking(csp.assignment,csp)

def backtracking(assignment, csp : Wordoku_CSP):
    csp.nodes_generated+=1
    #print(csp.nodes_generated)
    if set(assignment.keys()) == csp.variables_set:
        return csp

    curr = select_new_unassigned_value_mrv(assignment, csp)
    curr_domain = deepcopy(csp.domains)

    for value in csp.domains[curr]:
        if check_consistent(assignment,csp.constraints[curr], value, curr):
            assignment[curr] = value

            domain_shortened = remove_possibilities_from_others(assignment, csp, curr, {value})
            if domain_shortened!= False:
                result = backtracking(assignment, csp)
                if result!=False:
                    return result
            del assignment[curr]
            csp.domains = curr_domain
    return False

def select_new_unassigned_value_mrv(assignment, csp):
    
    unassigned_cells = []
    for cell in csp.domains:
        if cell not in assignment.keys():
            unassigned_cells.append([csp.domains[cell],cell])
    unassigned_cells.sort()
    min_remaining_value = min(unassigned_cells)
    return min_remaining_value[1]

def remove_possibilities_from_others(assignment, csp, curr, value):
    

    for neighbor in csp.constraints[curr]:
        
        if neighbor not in assignment and value in csp.domains[neighbor]:
            if len(csp.domains[neighbor])==1:
                return False
            csp.domains[neighbor].remove(value)

            if len(csp.domains[neighbor])==1:
                result = remove_possibilities_from_others(assignment, csp, neighbor, csp.domains[neighbor])
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
    