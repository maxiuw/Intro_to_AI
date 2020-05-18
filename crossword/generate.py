import sys
import pandas as pd
from copy import deepcopy
from crossword import *
import pdb
from time import sleep


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """

        self.enforce_node_consistency()
        for i in self.crossword.variables:
            print(self.domains[i])
        self.ac3()
        print('variables after ac3')
        for i in self.crossword.variables:
            print(self.domains[i])
        # creating dictionary of variables and available domains
        assigment = {
            var: self.domains[var]

            for var in self.crossword.variables
        }
        return self.backtrack(assigment)

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        copy_domain = deepcopy(self.domains)
        for v in self.crossword.variables:
            for word in copy_domain[v]:
                if len(word) != list(self.crossword.variables)[list(self.crossword.variables).index(v)].length:
                    self.domains[v].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        counter = 0
        overlap = self.crossword.overlaps[x, y]
        if overlap == None:
            return False
        else:
            copy_domain_x = deepcopy(self.domains[x])
            # jezeli litera na pozycji ktora satanowi wspolna pozycje dla w1,w2
            # nie jest taka sama, slowo nie spelnia wygomow i usowaym z domeny
            # copy cause size will change during the loop
            for w1 in copy_domain_x:
                # at the end not if any of the 2nd domain's letters is the same as 1st word specific letter,
                # del the word, otherwise continue
                w2_letters = [i[overlap[1]] for i in self.domains[y]]  # common letters for 2 positions
                if any(i == w1[overlap[0]] for i in w2_letters):
                    continue
                else:
                    self.domains[x].remove(w1)
                    counter += 1

        if counter > 0:
            return True
        else:
            return False

    def ac3(self):
        """
        makes sure that all the variables are arc consistant
        if looping over revision leaves any of the domains empty - return false
        else return true
        """
        for i in self.crossword.variables:
            for j in self.crossword.variables:
                # making sure we dont check arc const for itself
                if i == j:
                    continue

                self.revise(i, j)
                if len(self.domains[i]) == 0:
                    raise AttributeError(f'empy set of {i}')

                # check if change of the domain, did not influence any of previous constraints
                for k in self.crossword.variables:
                    if k == j or k == i or list(self.crossword.variables).index(k) > list(
                            self.crossword.variables).index(j):
                        continue

                    self.revise(k, i)
                    if len(self.domains[i]) == 0:
                        raise AttributeError(f'empy set of {i}')
                        # return False
            # if it has already assigned value, checking if any other var still has that val in the domain
            # if yes, del it from 2nd val's domain
            if len(self.domains[i]) == 1:
                for var in self.crossword.variables:
                    if var == i:
                        continue
                    self.domains[var] -= self.domains[i]

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in assignment:
            if len(assignment[var]) > 1:
                return False
        else:
            return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for var in assignment:
            # checkign just for the ones which have jsut one solution
            if len(assignment[var]) != 1:
                continue
            if var.length != len(list(assignment[var])[0]):
                return False
            else:
                for variable in assignment:

                    if variable == var or len(assignment[variable]) != 1:
                        continue
                    elif self.crossword.overlaps[var, variable] is not None:
                        overlap = self.crossword.overlaps[var, variable]
                        # checking if it s consistant with the other variables
                        if list(assignment[var])[0][overlap[0]] != list(assignment[variable])[0][overlap[1]]:
                            print('ovelaping letters are not the same')
                            return False
                    elif assignment[var] == assignment[variable]:
                        print('same words')
                        return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # TODO!!!!
        # dictionary of ammount of overlaping var for each var
        # index = [i for i in range(0, len(assignment[var]))]
        # df = pd.DataFrame(data=list(assignment[var]))

        return assignment[var]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        d = None
        for var in assignment:
            if len(assignment[var]) == 1:
                continue
            elif d is None:
                d = var
                continue
            elif len(assignment[d]) > len(assignment[var]):
                d = var
                continue
                # if their domains are equal, choosing the one with higher number of neighbours
            # elif len(assignment[d])==len(assignment[var]):
            #     d_n = len([i for i in [self.crossword.overlaps[d,i] for i in self.crossword.variables]])
            #     var_n = len([i for i in [self.crossword.overlaps[var,i] and i!=var for i in self.crossword.variables]])
            #     if var_n>d_n:
            #         d = var
        return d

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to  (values).

        If no assignment is possible, return None.
        """

        # 1 take variable
        # 2 take 1st word from its domain and check if its workign >>> for the first on it should work!!!
        # 3 check if this combination is wocking for the next combination or not
        # 4 if not come back one step, try different combination (up to all possible combinations
        # 5 if it doesn't work, go on and come one more back
        # 6 when error was found come back to the beginning of the loop

        assignment_copy = deepcopy(assignment)
        modify_vars = []
        while True:
            # pdb.set_trace()
            print(assignment_copy)
            print(f"variables {modify_vars}")
            # 0 - check if assigment is true
            if self.assignment_complete(assignment_copy) and self.consistent(assignment_copy):
                for var in assignment_copy:
                    assignment_copy[var] = list(assignment_copy[var])[0]
                print(assignment_copy)
                return assignment_copy

            # 1 #
            var = self.select_unassigned_variable(assignment_copy)
            assignment[var] = self.order_domain_values(var, assignment_copy)

            # 2,3 #
            for word in assignment[var]:
                assignment_copy[var] = {word}

                if self.consistent(assignment_copy):
                    break
                else:
                    print(f'not consistent for {word}')
                    continue
            # make sure it is arc const

            if self.consistent(assignment_copy):
                modify_vars.append(var)
                continue

            elif not self.consistent(assignment_copy) and len(modify_vars) == 0:
                raise ValueError('no solution')

            else:
                # 4,5 #
                print('trying to solve even more ')
                copy = deepcopy(assignment_copy)
                while not self.consistent(copy) or len(modify_vars) != 0:
                    recheck = modify_vars[-1]
                    modify_vars.remove(recheck)
                    for i in assignment[recheck]:
                        if i == assignment_copy[recheck]:
                            continue
                        copy[recheck] = i
                        if self.consistent(copy):
                            break
                    if self.consistent(copy):
                        break
                    else:
                        copy[recheck]=assignment[recheck]



def main():
    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
