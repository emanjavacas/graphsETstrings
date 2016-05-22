# coding: utf-8

import codecs
import argparse
import signal
import sys

from collections import defaultdict

from src.digraph import Digraph, DirectedCycle
from programming.wordnet.sap import SAP


def check_csv(fname):
    with codecs.open(fname, 'r', 'utf-8') as f:
        fields = None
        for l in f:
            line = l.strip().split(',')
            if fields and fields != len(line):
                print(l.encode('utf-8'))
            fields = len(line)


def read_synsets(fname):
    with codecs.open(fname, 'r', 'utf-8') as f:
        for l in f:
            line = l.strip().split(',')
            synset_id, synsets, gloss = line[0], line[1], line[2:]
            synsets = synsets.split(' ')
            yield int(synset_id), synsets, ",".join(gloss)


def read_hypernyms(fname):
    with open(fname, 'r') as f:
        for l in f:
            line = l.split(',')
            hypopnym, hypernyms = line[0], line[1:]
            yield int(hypopnym), [int(h) for h in hypernyms]


class SynsetNode(object):
    def __init__(self, synset_id, synsets, gloss=None):
        self.synset_id = synset_id
        self.synsets = synsets
        self.gloss = gloss

    def __str__(self):
        return "<Synset id=%d, synsets=%s, gloss=%s>" % \
            (self.synset_id, "; ".join(self.synsets), self.gloss)


class WordNet(object):
    def __init__(self, synsets, hypernyms):
        hypernyms = {h: hs for h, hs in read_hypernyms(hypernyms)}
        self.synsets = [None] * len(hypernyms)
        self.graph = Digraph(len(self.synsets))
        self.noun2synsets = defaultdict(list)
        for synset_id, synsets, gloss in read_synsets(synsets):
            self.synsets[synset_id] = SynsetNode(synset_id, synsets, gloss)
            for synset in synsets:
                self.noun2synsets[synset].append(synset_id)
            try:
                for hyp in hypernyms[synset_id]:
                    self.graph.add_edge(synset_id, hyp)
            except KeyError:
                continue
        self._sap = SAP(self.graph)

    def is_rooted_dag(self):
        cycles = DirectedCycle(self.graph)
        if cycles.has_cycle():
            return False
        roots = 0
        for v in range(self.graph.V):
            if len(self.graph.adj(v) == 0):
                roots += 1
        return roots == 1       # there can only be one

    def nouns(self):
        return self.noun2synsets.keys()

    def is_noun(self, word):
        return word in self.noun2synsets

    def dist(self, noun_a, noun_b):
        synsets_a = self.noun2synsets[noun_a]
        synsets_b = self.noun2synsets[noun_b]
        return self._sap.length(synsets_a, synsets_b)

    def sap(self, noun_a, noun_b):
        if not self.noun2synsets[noun_a] or not self.noun2synsets[noun_b]:
            return "Ancestor not found"
        synsets_a = self.noun2synsets[noun_a]
        synsets_b = self.noun2synsets[noun_b]
        ancestor = self._sap.ancestor(synsets_a, synsets_b)
        return self.synsets[ancestor]

if __name__ == '__main__':
    signal.signal(signal.SIGINT, lambda s, frame: sys.exit(0))

    parser = argparse.ArgumentParser(description='WordNet')
    parser.add_argument('-s', '--synsets')
    parser.add_argument('-H', '--hypernyms')
    args = vars(parser.parse_args())

    wordnet = WordNet(args['synsets'], args['hypernyms'])

    def process_input(prompt):
        words = prompt.strip().split(' ')
        if len(words) > 1:
            return words
        else:
            return words[0]

    while True:
        word_a = process_input(raw_input("Insert a word or words\n"))
        word_b = process_input(raw_input("Insert a word or words\n"))
        dist = wordnet.dist(word_a, word_b)
        ancestor = wordnet.sap(word_a, word_b)
        print("\nDistance between `%s` and `%s` = %d;\nAncestor is:\n\t %s\n"
              % (word_a, word_b, dist, ancestor))
