import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    # corpus = crawl("corpus0")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # corpus is pages {'1.html': {'2.html'}, '2.html': {'1.html', '3.html'}, '3.html': {'4.html', '2.html'}, '4.html': {'2.html'}}
    # page with format {page : {set of pages}, ... }
    links = []  # list to store links
    n = 0
    default_options = []
    for keys in corpus:
        default_options.append(keys)
        if page == keys:
            n = len(corpus[keys])  # get len of links conencted to original page
            for elements in corpus[keys]:  # get values in set from key into list
                links.append(elements)
    if n > 0:
        # damping/ len(values)
        prob_key = damping_factor/n
        # create dict for key, and values
        # round to 2 places the 1 - 0.85/ len n + original page
        additional_prob = round((1-damping_factor)/len(corpus), 2)
        additional_subset = []
        for keys in default_options:
            if keys not in links:
                additional_subset.append(keys)
        answer = {}
        for items in additional_subset:
            answer.update({items: additional_prob})
        for element in links:
            # append new element to dict of d/len(n) + additional prob
            answer.update({element: additional_prob + (damping_factor/n)})
        return answer
    else:
        alt_link = []
        for keys in corpus:
            alt_link.append(keys)
        answer = {}
        rand_prob = round(1/len(alt_link), 2)
        for i in range(len(alt_link)):
            answer.update({alt_link[i]: rand_prob})
        return answer


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # whats n? samples
    # choose a page randomly from corpus to start
    corpus_random = []
    for key in corpus:
        corpus_random.append(key)
    random_page = random.choice(corpus_random)
    # use transition model to choose from that random page
    # extract key and probabilities into list and use random.choices to put in weights
    # think of a way to consider duplicate links as 1 and a loop link as none
    # dict to collect/track number of times a page is visited:
    tracking_dict = {}
    for keys in corpus:
        tracking_dict.update({keys: 0})
    for _ in range(n):
        # this will return the places to go for the samples
        sample_dict = transition_model(corpus, random_page, DAMPING)
        prob_dist = []
        for keys in sample_dict:
            prob_dist.append(sample_dict[keys])
        population = []
        for keys in sample_dict:
            population.append(keys)
        random_page = random.choices(population=population, weights=prob_dist)
        random_page = random_page[0]
        tracking_dict.update({random_page: tracking_dict[random_page]+1})
    for keys in tracking_dict:
        tracking_dict[keys] = round(tracking_dict[keys]/n, 4)
    return tracking_dict

    # i think do a random func with the probability dist from
    # transition model to choose a page based on the page

    # sample states randomly from the markov chain choose a page by random
    # then keep following links using transition model probabilities
    # keep track of how many times we have visted each page

    # i think somethings like loop for number of samples or 1 random_page per sample
    # run through algo and track total number for each page then scale to 0-1
    # return expected format of pank rank

    # return dict like {"1.html" : 0.}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # edit corpus if has no links then it should be treated as having a link to every page including itself

    # start by assuming the page rank of every page is 1/N

    # check corpus for key with empty set

    for key in corpus:
        if not corpus[key]:
            set_of_keys = {key1 for key1 in corpus}
            corpus[key].update(set_of_keys)

    answer = {}
    start_assumption_pr = {}
    key_list = []
    for keys in corpus:
        key_list.append(keys)
    N = len(key_list)

    for key in key_list:
        start_assumption_pr.update({key: round(1/N, 4)})

    # consider each possible source to page p
    # numlinks(i) is the number on link on i one of which is p
    # to do summation we add all this and plus begining structure to get pr(p)
    # return value is each key in corpus : pagerank sum to 1

    # if updated pagerank value within 0.001 then
    # return value if not loop endlessly

    # use sample page rank to get pr(i)

    # find list of i for p for every p in corpus

    # pr_i = # what links to p
    # how to get p? random i then random p
    permanent_answer = {}
    while True:
        # instead of random i then p too long just check and cut down keys in corpus as p, also scale answer to sum of 1
        # for i in range of len corpus p == len i then compare then reset

        for key in corpus:
            p = key

            # now find the i's for p
            i_for_p = []
            for key in corpus:
                if p in corpus[key]:
                    i_for_p.append(key)

            # summation part
            summation_list = []
            for i in i_for_p:
                numlinks_i = len(corpus[i])
                pr_i = start_assumption_pr[i]
                equation_p1 = pr_i/numlinks_i
                summation_list.append(equation_p1)

            summation_p = 0
            for value in summation_list:
                summation_p += value

            # pr(p) calc (put it together d + summation)
            pr_p = ((1-damping_factor)/N) + (damping_factor*summation_p)

            answer.update({p: pr_p})
            # fixed

            # the answer dict cant be compared every turn it has to be properly
            # accumlated to 4 then normalised before the next comaparison
            # also pls ponder if there are any updates for answer or is it new every turn
            # if answer has all the keys as corpus
        if len(answer.keys()) == len(corpus.keys()):
            # first convert the values to sum of 1
            sum_of_one_list = []
            for key in answer:
                sum_of_one_list.append(answer[key])

            sum_of_values = 0
            for values in sum_of_one_list:
                sum_of_values += values
            for key in answer:
                # need to scale answers tosum of 1 and update properly..
                answer.update({key: round(answer[key]/sum_of_values, 4)})
            # change to compare the answer with start assumption then update start assumption with answer if no
            # also no need all at once if one yes then save it to a permananent answer and return the answer if len is full
            for key in corpus:
                # need to debug this
                # print lens of corpus.keys and change i to j
                if start_assumption_pr[key] - 0.001 < answer[key] < start_assumption_pr[key] + 0.001:
                    # append answer value to permanent dict
                    permanent_answer.update({key: answer[key]})

            if len(permanent_answer.values()) == len(corpus.keys()):
                return permanent_answer
            # start assumption pr need to be updated to the values just calculated
            for key in corpus:
                start_assumption_pr.update({key: answer[key]})
            # comparison fixed but loop not ending i suspect there is an update element were missign
            # and were rewritting the values randomly instead

            # for now better clear answer before re looping
            answer = {}

        # condition that makes sure all keys have pr and
        #  the new prs are within 0.001
        # create a condition to alway fill 1 row first then check with the other
# the way youre calculating pr(p) must be wrong look into that
if __name__ == "__main__":
    main()
