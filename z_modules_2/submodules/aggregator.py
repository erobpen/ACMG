

import sys
import os 
import jsonpickle
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, '..')

from modules.mc import mc
from modules.submodules.tree import node
from colorama import Back
from cmd2.ansi import style_aware_wcswidth as wcswidth
from PrettyPrint import PrettyPrintTree

class aggregator:

    def __init__(self, printer):
        self.tree = {}
        self.printer = printer
        pass

    def aggregate(self, parent_node : node, nodes, mc : mc):

        if self.tree == {}:
            self.tree = parent_node
        self.tree.add_nodes_to_tree(self.tree, parent_node.id, nodes)
        mc.store_progress(jsonpickle.encode(self.tree))
        PrettyPrintTree(lambda x: x.branches, lambda x: self.printer(x.task))(self.tree)
        print("\n\n")

        #this is very usefull to see the state of domains of the CSP for each individual node in the tree
        # PrettyPrintTree(lambda x: x.branches, lambda x: self.print_values(x))(self.tree)
        return True
    
    def print_values(self, x):
        string = ""
        counter = 0
        for key in x.domains:
            string += ''.join([str(x) for x in x.domains[key]]) + " "
            counter += 1
            if counter == 9:
                counter = 0
                string += '\n'
        return string
