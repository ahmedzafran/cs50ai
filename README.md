# CS50AI — Introduction to Artificial Intelligence with Python

Coursework from HarvardX's CS50AI, organized by the course's own conceptual chapters. Each project below implements a specific AI technique — search, logical inference, probabilistic reasoning, constraint satisfaction, machine learning, or natural language processing — applied to a small, self-contained problem. A top-level `certificate/` folder holds the course completion certificate.

Each project folder is runnable on its own (see each folder's `requirements.txt` where present); a couple of GUI projects (`minesweeper`, `tictactoe`) require `pygame`, and `traffic` requires a separately downloaded dataset (see its README).

## 0 - Search

- **degrees** — Finds the "degrees of separation" between two actors by running **breadth-first search (BFS)** over a bidirectional graph of actors and the movies they share, using an explicit FIFO `QueueFrontier` (from `util.py`) to guarantee the *shortest* path is found first.
- **tictactoe** — An unbeatable Tic-Tac-Toe AI implemented with the **minimax algorithm**: it recursively explores the full game tree via mutually-recursive `max_value`/`min_value` functions to compute exact win/lose/draw utilities. (Note: this implementation is a plain, exhaustive minimax search — it does not include alpha-beta pruning.)

## 1 - Knowledge

- **knights** — Solves "Knights and Knaves" logic puzzles via **propositional logic model checking**: puzzle premises are encoded as `And`/`Or`/`Not`/`Implication` formulas (`logic.py`), and `model_check()` recursively enumerates every possible true/false assignment over the symbols to test whether the knowledge base entails each candidate conclusion.
- **minesweeper** — An AI that plays Minesweeper by maintaining a **knowledge base of logical sentences** (`{cells} = count`), where each move adds a new sentence and the AI infers new safe cells/mines two ways: directly (a sentence with count 0 means all its cells are safe; count equal to the number of cells means all are mines) and by **subset inference** (if one known sentence's cells are a subset of another's, subtracting them yields a new, smaller inferred sentence).

## 2 - Uncertainty

- **pagerank** — Ranks web pages using **both PageRank formulations**: the random-surfer **Markov-chain sampling method** (`sample_pagerank`, which repeatedly samples the next page via `transition_model`'s damped-random-walk probabilities) and the closed-form **iterative update formula** (`iterate_pagerank`, which repeatedly recomputes each page's rank from its inbound links until values converge).
- **heredity** — Computes the probability that each person in a family carries 0, 1, or 2 copies of a gene (and expresses a trait) via **exact Bayesian network inference**: it enumerates every possible joint assignment of gene counts and trait outcomes across the family (using `powerset`), computes each joint probability from conditional inheritance/mutation probabilities, and normalizes to get each person's marginal distribution.

## 3 - Optimization

- **crossword** — Generates crossword puzzle solutions by modeling it as a **constraint satisfaction problem (CSP)**: unary constraints are enforced first (`enforce_node_consistency`), then **AC-3 arc consistency** (`ac3`/`revise`) prunes domains, and finally a **backtracking search** fills in the grid, ordering variable selection by the **minimum-remaining-values heuristic with a degree-heuristic tiebreak**, and ordering word choices with a least-constraining-value heuristic.

## 4 - Learning

- **nim** — Trains an AI to play Nim optimally through **reinforcement learning (Q-learning)**: the AI plays thousands of games against itself, updating action-value estimates via the Q-learning update rule with an **epsilon-greedy** action-selection strategy that balances exploration and exploitation.
- **shopping** — Predicts whether an online shopping session will result in a purchase using a **k-nearest-neighbors classifier** (scikit-learn's `KNeighborsClassifier`, k=1) trained on session features (page counts/durations, bounce/exit rates, visitor type, etc.), evaluated by sensitivity (true positive rate) and specificity (true negative rate).

## 5 - Neural Networks

- **traffic** — Classifies German traffic sign images into 43 categories with a **convolutional neural network (CNN)** built in TensorFlow/Keras: stacked `Conv2D` + pooling layers extract image features, feeding into dense hidden layers with dropout before a softmax output layer. Requires the GTSRB dataset, downloaded separately (see the project's README).

## 6 - Language

- **parser** — Parses English sentences according to a hand-written **context-free grammar (CFG)** using NLTK's `ChartParser`, then extracts noun-phrase chunks by walking the resulting parse tree for `NP` subtrees that don't themselves contain nested noun phrases.
- **attention** — Visualizes what a pretrained **BERT masked-language model** (`bert-base-uncased`, via Hugging Face `transformers`) attends to: it predicts the top candidate words for a `[MASK]` token, then renders a grayscale heatmap of the **self-attention weights for every layer and every attention head** to show which tokens the model focused on when making that prediction.

## Repository layout

```
0-search/{degrees, tictactoe}
1-knowledge/{knights, minesweeper}
2-uncertainty/{pagerank, heredity}
3-optimization/{crossword}
4-learning/{nim, shopping}
5-neural-networks/{traffic}
6-language/{parser, attention}
certificate/CS50AI.pdf
```
