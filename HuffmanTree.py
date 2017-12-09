from collections import OrderedDict
'''
Create a Huffman tree to generate the code words for each symbol.
Create a dictionary of symbol-codeword key-value pairs and return the dictionary
back to the PFCodeGenerator module.
Note: Code word assignment order does not matter since it is a dictionary.

Store each dictionary entry value as a node object when it is being assigned a
codeword in the tree navigation. It is very important that a checking method
be implemented in order to ensure that all codes remain prefix-free

Will need to keep at least 2 rows (depth) in the tree void Nodes since otherwise
it won't be able to accomodate enough Nodes (cause of Prefix-free code).

Needs:
    - if Node symbol == None, it is a void (placeholder) Node
    - instantiate tree with 2 depth rows of void Nodes
    - (possibly?) pointers/counter for sibbling Nodes
    - Simplicity approach:
      -> try finding the biggest power of 2 that is greater than the number of
         occupied Nodes, and leave all of the nodes on the bottom row
    - Ideal approach:
      -> algorithm to optimize minimum void/empty Nodes needed to fill the tree,
         then fill it accordingly in order of shortest code
'''

class Node:
    def __init__(self, symbol, freq=0, left=None, right=None, parent = None, code_word = None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right
        self.parent = parent
        self.code_word = code_word

    def assign_parent(self, parent):
        self.parent = parent
        return self.parent

    def print_symbol(self):
        print(self.symbol)

    def print_ASCII(self):
        ''' Prints the symbol's ASCII code - all None until the node has been
        added to the tree
        '''
        print(ord(symbol))

    def print_code_word(self):
        ''' Prints the code word assigned - all None until the node has been
        added to the tree
        '''
        print(self.code_word)



class Tree:
    def __init__(self, approach):
        self.root = None
        self.approach = approach
        self.depth = None
    
    def get_root(self):
        return self.root

    def print_root(self):
        if self.root:
            return self.root.symbol
        return None

    def assign_depth(self, depth):
        self.depth = depth
        return self.depth

    def add_node(self, Node):
        ''' Enter node into the tree
        '''
        #If tree is empty
        if not self.get_root():
            self.root = Node
            return self.__assign_code_word(Node)
        #Else find spot in the tree by approach
        if self.approach == 0:
            self.simple_add_node(self.root, Node, self.depth, 0, False)
        elif self.approach == 1:
            self.ideal_add_node(Node)
        return self.__assign_code_word(Node)

    def rebuild_tree(self, root, char, code, i):
        if i == len(code):
            root.symbol = char
            return
        if code[i] == '0':
            if root.left == None: root.left = Node(None, -1, None, None, root, root.code_word + '0')
            self.rebuild_tree(root.left, char, code, i+1)
        elif code[i] == '1':
            if root.right == None: root.right = Node(None, -1, None, None, root, root.code_word + '1')
            self.rebuild_tree(root.right, char, code, i+1)
        else:
            print("Should never get here!")

    def search_tree(self, root, search_code, i):
        if i == len(search_code):
            if root == None or root.code_word == None or root.code_word != search_code:
                return None
            return root.symbol
        if search_code[i] == '0':
            if root.left == None:
                return None
            return self.search_tree(root.left, search_code, i+1)
        if search_code[i] == '1':
            if root.right == None:
                return None
            return self.search_tree(root.right, search_code, i+1)

    def __get_symbol_from_hash(self, hash_codes, code):
        for char in hash_codes.keys():
            if hash_codes[char] == code:
                return char
        return None

    def simple_add_node(self, current_node, node, depth, current_depth, flag):
        ''' Keep adding nodes until the bottom depth is reached, then add the
            real Nodes and call helper fcn to assign code words.
        '''
        
        # Note: None of the occupied nodes can have children (prefix-free)
        # Iterate down the tree to that depth, allocating void Nodes along the way
        # Once at that depth, if no node is already there then place the Node
        # Call to assign the code word
        
        if flag: return 
        if depth == current_depth + 1:
            # At depth where the child of this node would be in the right row
            #if current_node.left == None:
            if current_node.left == None and current_node.code_word != "0"*len(current_node.code_word):
                current_node.left = node
                node.parent = current_node
                node.code_word = current_node.code_word + "0"
                flag = True
            elif current_node.right == None:
                current_node.right = node
                node.parent = current_node
                node.code_word = current_node.code_word + "1"
                flag = True

        elif depth > current_depth + 1:
            # Still > 1 row above target - allocate void nodes if it is void also
            if current_node.left == None:
                current_node.left = Node(None, -1, None, None, current_node, current_node.code_word + "0")
            if current_node.right == None:
                current_node.right = Node(None, -1, None, None, current_node, current_node.code_word + "1")

            flag = flag or self.simple_add_node(current_node.left, node, depth, current_depth + 1, flag)
            flag = flag or self.simple_add_node(current_node.right, node, depth, current_depth + 1, flag)
        return flag

    def ideal_add_node(self, Node):
        #IMPLETMENT
        
        # Note: None of the occupied nodes can have children (prefix-free)
        
        return

    def print_tree(self, head):
        '''Prints the tree in LCR order'''
        if not head:
            return
        self.print_tree(head.left)
        print(head.symbol, head.code_word)
        self.print_tree(head.right)
        return

    def __assign_code_word(self, Node):
        ''' Internal helper function that assigns a code word to a node that has
        just been added to the tree without having its code already generated.
        This is for void nodes mainly.
        '''
        if Node.symbol == None:
            Node.code_word = None
            return Node.code_word
        if Node.code_word == None:
            Node.code_word = "0xDEADBEEF"
        return Node.code_word
