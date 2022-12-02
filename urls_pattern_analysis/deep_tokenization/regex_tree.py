from enum import IntEnum

import networkx as nx

class RegExTree(IntEnum):
    all_chars = 0
    non_space_chars = 1
    space_chars = 2
    alphanumeric = 3
    special_chars = 4
    alpha_chars = 5
    digits = 6

REGEX_EXPRESSION = {
    RegExTree.all_chars: ".",
    RegExTree.non_space_chars: "\S",
    RegExTree.space_chars: "\s",
    RegExTree.alphanumeric: "[a-zA-Z0-9]",
    RegExTree.special_chars: "[^a-zA-Z0-9]",
    RegExTree.alpha_chars: "[a-zA-Z]",
    RegExTree.digits: "[0-9]"
}

elist = [
    (RegExTree.all_chars, RegExTree.non_space_chars),
    (RegExTree.all_chars, RegExTree.space_chars),
    (RegExTree.non_space_chars, RegExTree.alphanumeric),
    (RegExTree.non_space_chars, RegExTree.special_chars),
    (RegExTree.alphanumeric, RegExTree.alpha_chars),
    (RegExTree.alphanumeric, RegExTree.digits)
]

def initialize_regex_tree():
    G = nx.DiGraph()
    G.add_edges_from(elist)
    return G