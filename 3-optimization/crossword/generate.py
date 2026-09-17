import sys

from crossword import *


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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        to_remove_dict = {variable: set(
        ) for variable in self.domains}  # create a dict of keys from self.domains with empty sets
        for variable in self.domains:  # for each key
            for value in self.domains[variable]:  # for the values in the keys
                if len(value) != variable.length:  # if value not same string length as unary constraint
                    # add it to the to_remove_dict to be removed later
                    to_remove_dict[variable].add(value)

        for variable in self.domains:  # for keys in self.domain
            # set subtract the to remove sets from the original sets
            self.domains[variable] -= to_remove_dict[variable]

        # print(self.domains)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # to remove any values in the domain of x, if the overlap does not fit, then return true if remove or false if not
        # print(x, y)
        # if x and y has overlapping cells
        revised_domain = set()
        overlap_check = self.crossword.overlaps.get((x, y))
        if overlap_check:
            x_index, y_index = overlap_check
            # option 1 any()
            for x_values in self.domains[x]:
                if any(x_values[x_index] == y_values[y_index] for y_values in self.domains[y]):
                    revised_domain.add(x_values)

            # option 2 manual nested loops
            """for x_values in self.domains[x]:
                match_found= False
                for y_values in self.domains[y]:
                    if x_values[x_index] == y_values[y_index]:
                        match_found = True
                    if match_found:
                        revised_domain.add(x_values)"""
        else:
            return False

        if len(revised_domain) < len(self.domains[x]):
            self.domains[x] = revised_domain
            return True
        else:
            return False

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        if arcs is None:
            # default arc list
            queue = []
            # build all combinations of (x, not x) as y
            for variable_x in self.domains:
                x = variable_x
                for variable_y in self.domains:
                    if variable_y != x:
                        y = variable_y
                        queue.append((x, y))
        else:
            queue = list(arcs)
            # queue = arcs

        while queue:
            x, y = queue.pop(0)
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for neighbor in (self.crossword.neighbors(x) - {y}):
                    queue.append((neighbor, x))
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.domains:
            if variable not in assignment or type(assignment[variable]) is not str:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        distinct_values = [values for values in assignment.values()]
        if len(distinct_values) != len(set(distinct_values)):
            return False
        for variable in assignment:
            if any(len(assignment[variable]) != variable2.length for variable2 in self.domains if variable2 == variable):
                return False
        for variable in assignment:
            neighbors = self.crossword.neighbors(variable)
            if neighbors:
                neighbors = list(neighbors)
                for neighbor in neighbors:
                    x_index, y_index = self.crossword.overlaps.get((variable, neighbor))
                    if neighbor in assignment:
                        if assignment[variable][x_index] != assignment[neighbor][y_index]:
                            return False
                    else:
                        break
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # feature to extract heuristic from var regarding the lowest n number of elimination to possible neighbors
        # get neighbors of var
        neighbors = list(self.crossword.neighbors(var))
        # find heuristic for each value in domain of var in relation to other neighbors
        heuristic_dict = {}

        for value_x in self.domains[var]:
            n = 0
            for neighbor in neighbors:
                x_index, y_index = self.crossword.overlaps.get((var, neighbor))
                if x_index is None or y_index is None:
                    continue
                # neighbors values
                for value_y in self.domains[neighbor]:
                    if value_x[x_index] != value_y[y_index]:
                        n += 1

            # elimination count for each value in domain
            heuristic_dict.update({value_x: n})
        # lambda sort
        sorted_values = sorted(self.domains[var], key=lambda v: heuristic_dict[v])
        return sorted_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Collect unassigned variables with their heuristics and degrees
        unassigned_variables = []

        for variable in self.domains:
            if variable not in assignment:
                heuristic = len(self.domains[variable])  # Remaining values
                degree = len(self.crossword.neighbors(variable))  # Number of neighbors
                # Store (variable, heuristic, degree) tuples for sorting
                unassigned_variables.append((variable, heuristic, degree))

        # Sort by heuristic (ascending), then by degree (descending)
        unassigned_variables = sorted(unassigned_variables, key=lambda x: (x[1], -x[2]))

        # Return the first variable (best choice)
        return unassigned_variables[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """

        if len(self.domains) == len(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            copy_assign = assignment.copy()
            copy_assign[var] = value
            if self.consistent(copy_assign):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result is not None:
                    return result
            assignment[var].pop()
        return None


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

    # for variables in creator.crossword.overlaps:
    # if creator.crossword.overlaps[variables] is (0,0):
    # print(f"variables: {variables}, overlap cell: {creator.crossword.overlaps[variables]} \n")

    x, y = Variable(0, 1, 'down', 5), Variable(0, 1, 'across', 3)

    # creator.revise(x, y)

    # creator.ac3()

    print(creator.crossword.neighbors(x))

    """assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)"""


if __name__ == "__main__":
    main()
