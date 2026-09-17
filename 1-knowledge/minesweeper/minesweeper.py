import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    # implement a function to find adjacent cells to the target

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count and self.count > 0:
            return self.cells
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0 and len(self.cells) >= 1:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            cell_cover = {cell}
            self.cells = self.cells - cell_cover
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            cell_cover = {cell}
            self.cells = self.cells - cell_cover


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # since ai made a random move and game still on then mark that move as move made and mark cell as safe
        self.moves_made.add(cell)
        self.mark_safe(cell)

        # generate actual neighbors
        i, j = cell
        possible_neighbors = []
        for h in range(-1, 2):
            for w in range(-1, 2):
                possible_neighbors.append((i + h, w+j))
        actual_neighbors = set()
        # if the generated is not in self.move_made and doesnt breach the boudnaries of the board then
        for neighbor in possible_neighbors:
            if neighbor != cell and neighbor not in self.moves_made:
                i, j = neighbor
                if 0 <= i < self.height and 0 <= j < self.width:
                    actual_neighbors.add(neighbor)

        # make sure to eliminate mines and safes form actual neighbours before feeding to sentence
        for cell in actual_neighbors:
            if cell in self.safes:
                cell = {cell}
                actual_neighbors = actual_neighbors - cell

            if cell in self.mines:
                cell = {cell}
                actual_neighbors = actual_neighbors - cell
                count -= 1

        # inference segment
        inference = Sentence(actual_neighbors, count)

        # mark cells as safes or mines
        if inference.known_mines():
            for mine in inference.known_mines():
                self.mark_mine(mine)

        if inference.known_safes():
            for safe in inference.known_safes():
                self.mark_safe(safe)

        # append sentence
        self.knowledge.append(inference)

        # Additional inference over sentences

        # if sentence {a,b,c} = 2 and we know c is safe (as in c is in self.safes) we can conclude that a,b is a mine
        # After marking current cell as safe
        for sentence in self.knowledge:
            # Direct inference from the sentence counts
            if sentence.count == 0:
                for cell in sentence.cells:
                    self.mark_safe(cell)
            elif sentence.count == len(sentence.cells):
                for cell in sentence.cells:
                    self.mark_mine(cell)

        # Subset logic
        for sentence in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence.cells.issubset(sentence2.cells) and sentence != sentence2:
                    new_cells = sentence2.cells - sentence.cells
                    new_count = sentence2.count - sentence.count
                    new_sentence = Sentence(new_cells, new_count)
                    if new_sentence.known_mines():
                        for cell in new_sentence.known_mines():
                            self.mark_mine(cell)
                    if new_sentence.known_safes():
                        for cell in new_sentence.known_safes():
                            self.mark_safe(cell)

        """if len(self.knowledge) > 0:
            for sentence in self.knowledge:
                for cell in sentence.cells:
                    if cell in self.safes:
                        cell = {cell}
                        new_sentence = Sentence(sentence.cells - cell, sentence.count)
                        if new_sentence.known_mines():
                            for cell in new_sentence.cells:
                                self.mark_mine(cell)
                            self.knowledge.append(new_sentence)
                    if cell in self.mines:
                        cell = {cell}
                        new_sentence = Sentence(sentence.cells -cell, sentence.count - len(cell))
                        if new_sentence.known_safes():
                            for cell in new_sentences.cells:
                                self.mark_safe(cell)
                        self.knowledge.append(new_sentence)"""

        """for sentence in self.knowledge:
                # if cell in actual neighbors is in sentence and is safe
                if sentence.known_mines():
                        if sentence.cells.issubset(inference.cells) and sentence.cells != inference.cells:
                            new_sentence = Sentence(inference.cells-sentence.cells, inference.count-sentence.count)

                            if new_sentence.known_safes():
                                for cell in new_sentence.known_safes():
                                    self.mark_safe(cell)


                if sentence.known_safes():
                        if sentence.cells.issubset(inference.cells) and sentence.cells != inference.cells:
                            new_sentence = Sentence(inference.cells-sentence.cells, inference.count-sentence.count)

                            if new_sentence.known_mines():
                                for cell in new_sentence.known_mines():
                                    self.mark_mine(cell)"""

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        row = []
        for i in range(self.width):
            row.append(i)
        col = []
        for j in range(self.height):
            col.append(j)

        cells = []
        for i in row:
            for j in row:
                cells.append((i, j))
        for cell in cells:
            if (cell not in self.moves_made and cell in self.safes):
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # cell generator segment
        row = []
        for i in range(self.width):
            row.append(i)
        col = []
        for j in range(self.height):
            col.append(j)

        cells = set()
        for i in row:
            for j in col:
                cells.add((i, j))

        cells = cells - self.moves_made
        cells = cells - self.mines
        # random move segment
        rnd_pool = list(cells)
        rnd_mv = random.choice(rnd_pool)
        return rnd_mv
