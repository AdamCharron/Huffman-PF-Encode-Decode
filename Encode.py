from HuffmanTree import *
from collections import OrderedDict
from operator import itemgetter


def simple_approach_depth(number_nodes):
    ''' Return the biggest power of 2 that is greater than the number of
        occupied Nodes. Will be used to add all nodes to bottom row of the tree.
    '''
    depth = 0
    while 2**depth < number_nodes + 1:
    #The + 1 is for the offset fix that prevents code words that are only 0
        depth += 1
    if depth < 2:
        depth = 2
    return depth


def ideal_approach_depth():
    ''' Algorithm to optimize minimum void/empty Nodes needed to fill the tree,
        then fill it accordingly in order of shortest code
    '''
    # IMPLEMENT
    
    return


def Encode(char_dict, char_list):
    ''' Takes in as input the character list and frequency dictionary
    '''
    approach = 0     #Simple
    #approach = 1     #Ideal
    
    char_codes = {}
    huffman_tree = Tree(approach)

    #Sort the dictionary by descending values
    sorted_char_dict = OrderedDict(sorted(char_dict.items(), key=itemgetter(1), reverse=True))

    #Initialize void root, and 2nd row voids Nodes. Will never have <= 2 chars
    void_root = Node(None, -1, None, None, None, "")
    void_left = Node(None, -1, None, None, void_root, void_root.code_word + "0")
    void_right = Node(None, -1, None, None, void_root, void_root.code_word + "1")

    #Bypass adding them into the tree by instantly setting them as roots children
    void_root.left = void_left
    void_root.right = void_right    
    huffman_tree.add_node(void_root)

    #Define approach and go to approach_encode helper functions
    if approach == 0: #Simple
        depth = simple_approach_depth(len(char_list))
    elif approach == 1: #Ideal
        depth = ideal_approach_depth()
    else:
        print("INVALID APPROACH. NEEDS TO BE 0 OR 1")
    temp = huffman_tree.assign_depth(depth)
    if temp <= 2:
        print("\nDepth issue encountered! Exiting.\n")
        return

    #Add each char in order of descending values into the tree
    #Get and return PF code dict
    for i in sorted_char_dict:
        char_code = huffman_tree.add_node(Node(i, char_dict[i]))
        char_codes[i] = char_code
        
    return char_codes, huffman_tree
