import itertools
import random
from copy import deepcopy
import enchant

class Wordoku_CSP:
    def __init__(self,input_path):
        self.wordoku = self.parse_input(input_path)
        self.decoder = self.encode_characters()
        self.id_row = "ABCDEFGHI"#A
        self.id_col = "123456789"
        self.variables = [a + b for a in self.id_row for b in self.id_col]
        self.variables_set = set(self.variables)
        self.domains = self.get_domains()
        self.constraints = self.get_constraints()
        self.assignment = {}
        self.nodes_generated = 0
        #self.prune_domain()

    def check_solved(self):
        for var in self.variables:
            if len(self.domains[var]) != 1:
                return False
        print("Solved")
        return True

    def get_constraints(self):
        tied_together = list()
        for row_elem in self.id_row:
            in_row = [row_elem + col_elem for col_elem in self.id_col]
            tied_together += list(itertools.combinations(in_row, 2))
        for col_elem in self.id_col:
            in_col = [row_elem + col_elem for row_elem in self.id_row]
            tied_together += list(itertools.combinations(in_col, 2))

        for row_elem in [self.id_row[0:3],self.id_row[3:6],self.id_row[6:9]]:
            for col_elem in [self.id_col[0:3],self.id_col[3:6],self.id_col[6:9]]:
                box_3x3 = [ r+c for c in col_elem for r in row_elem]
                tied_together += list(itertools.combinations(box_3x3, 2))
        constraints = {}

        for var in self.variables:
            var_constraint = set()
            for rule in tied_together:
                if var in rule:
                    var_constraint.add(rule[0] if var == rule[1] else rule[1])
            constraints[var] = var_constraint
        return constraints


    def get_domains(self):
        domains = {}
        for row in range(len(self.wordoku)):
            for col in range(len(self.wordoku[0])):
                if self.wordoku[row][col] == 0:
                    domains[self.id_row[row] + self.id_col[col]] = { x + 1 for x in range(len(self.wordoku))}
                else:
                    domains[self.id_row[row] + self.id_col[col]] = {self.wordoku[row][col]}
        return domains

    # def prune_domain(self):
    #     for i in range(len(self.wordoku)):
    #         for j in range(len(self.wordoku[0])):
    #             if len(self.domains[self.encode_cell(i,j)]) == 1:
    #                 for elem in self.constraints[self.encode_cell(i,j)]:
    #                     val = self.wordoku[i][j]
    #                     row, col = self.decode_cell(elem)
    #                     if val in self.domains[self.encode_cell(row,col)]:
    #                         self.domains[self.encode_cell(row,col)].remove(val)




    def parse_input(self,input_path):
        parsed_matrix = []
        with open(input_path) as file:
            for line in file:
                parsed_matrix.append([0 if curr == "*" else curr for curr in line.strip().replace(" ", "")])
        return parsed_matrix

    def encode_characters(self):
        encoder = {}
        for row in range(len(self.wordoku)):
            for col in range(len(self.wordoku[0])):
                if self.wordoku[row][col] in encoder.keys():
                    self.wordoku[row][col] = encoder[self.wordoku[row][col]]  
                elif self.wordoku[row][col] != 0:
                    encoder[self.wordoku[row][col]] = len(encoder) + 1
                    self.wordoku[row][col] = encoder[self.wordoku[row][col]]
        decoder = {encoder[key]: key for key in encoder.keys()}
        return decoder
        
    def output_wordoku(self):
        out_file =  open("output.txt", "w")
        out_file.writelines([" ".join([ self.decoder[x] if x in self.decoder else "*" for x in row]) + "\n" for row in self.wordoku])
        out_file.close()

    def decode_cell(self,cell):
        return self.id_row.index(cell[0]), self.id_col.index(cell[1])

    def encode_cell(self,i,j):
        return self.id_row[i] + self.id_col[j]
    
    def print_output_wordoku(self):
        for cell in self.assignment.keys():
            row,col = self.decode_cell(cell)
            self.wordoku[row][col] = self.assignment[cell]
        self.output_wordoku()

    def create_wordoku_random_copy(self):
        for i in range(len(self.wordoku)):
            for j in range(len(self.wordoku[0])):
                if self.wordoku[i][j] == 0:
                    self.wordoku[i][j] = random.randint(1,len(self.wordoku))

    def get_cell_conflict_count(self,row,col,val):
        total_conflict = 0
        cell_id = self.encode_cell(row,col)
        for cell in self.constraints[cell_id]:
            i , j  = self.decode_cell(cell)
            if self.wordoku[i][j] == val:
                total_conflict += 1
        return total_conflict


    def get_total_grid_conflict(self):
        total_conflict = 0
        for i in range(len(self.wordoku)):
            for j in range(len(self.wordoku[0])):
                if self.get_cell_conflict_count(i,j,self.wordoku[i][j]) > 0 :
                    total_conflict += 1
        return total_conflict

    def get_random_row_col(self):
        return random.randint(0,len(self.wordoku) -1),random.randint(0,len(self.wordoku) -1)
    

    def find_words_in_wordoku(self):
        all_words = []
        wordoku = ["".join([ self.decoder[x] if x in self.decoder else "*" for x in row]) for row in self.wordoku]

        for row in wordoku:
            all_words.append(row)

        for i in range(len(wordoku[0])):
            curr_word = []
            for j in range(len(wordoku)):
                curr_word.append(wordoku[j][i])
            all_words.append("".join(curr_word))

        all_words.append("".join([wordoku[i][i] for i in range(len(wordoku))]))
        all_words.append("".join([wordoku[i][len(wordoku) -1 - i] for i in range(len(wordoku))]))
        
        d = enchant.Dict("en_US")


        real_words = []
        for word in all_words:
            if d.check(word):
                real_words.append(word)
            if d.check(word[::-1]):
                real_words.append(word[::-1])

        if len(real_words) == 0:
            real_words.append("NONE")
        out_file =  open("output.txt", "a")
        out_file.writelines(["\nWords Found\n"] + real_words)
        out_file.close()
        return real_words






