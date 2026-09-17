import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S
NP -> N | Det N | Det AP N
AP -> Adj | Adj Adj | Adj Adj Adj
PP -> P NP
VP -> V | V NP | VP PP | Adv VP | VP Adv | VP Conj VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))

    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    nltk.download('punkt_tab')
    sentence = sentence.casefold()
    tokenized_words = nltk.tokenize.word_tokenize(sentence)
    tokenized_sen = []
    for word in tokenized_words:
        if any(letter.isalpha() for letter in word):
            tokenized_sen.append(word)

    return tokenized_sen


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    tree_sort = list()
    np_chunks = list()
    # np_strings = list()
    # print(tree.pretty_print())
    tree_pos = tree.treepositions()
    for index, pos in enumerate(tree_pos):
        tree_sort.append((pos, tree[pos], index))

    for item in tree_sort:
        if isinstance(item[1], nltk.tree.tree.Tree):
            if item[1].label() == 'NP':
                np_chunks.append(item[1])

    for tree in np_chunks:
        for tree2 in np_chunks:
            if tree2 != tree:
                if any(subtree == tree for subtree in tree2.subtrees()):
                    np_chunks.remove(tree2)

    return np_chunks

    """for pos in np_chunks:
        strings = str()
        for string in tree[pos].leaves():
            if string is None:
                strings = string
            else:
                strings += ' ' + string
        np_strings.append(strings)"""
    # print(np_strings)


if __name__ == "__main__":
    main()
