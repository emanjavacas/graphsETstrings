# coding: utf-8

import argparse
import signal
import sys
from collections import defaultdict

from programming.wordnet.wdgraph import WordNet


class Outcast(object):
    def __init__(self, wordnet):
        self.wordnet = wordnet

    def outcast(self, nouns):
        "find out which noun is least to related to the bunch"
        dists = defaultdict(int)
        for n in nouns:
            for m in nouns:
                if n != m:
                    dists[n] += self.wordnet.dist(n, m)
        print(sorted(dists.items(), key=lambda x: x[1]))
        return max(dists.items(), key=lambda x: x[1])[0]


if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda s, frame: sys.exit(0))
    parser = argparse.ArgumentParser(description='WordNet')
    parser.add_argument('-s', '--synsets')
    parser.add_argument('-H', '--hypernyms')
    args = vars(parser.parse_args())

    wordnet = WordNet(args['synsets'], args['hypernyms'])
    outcast = Outcast(wordnet)

    while True:
        words = raw_input("Insert words:\n").strip().split(" ")
        print("Outcast=%s\n" % outcast.outcast(words))
