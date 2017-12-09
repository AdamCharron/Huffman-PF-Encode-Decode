from HuffmanTree import *
from operator import itemgetter
import os.path
import codecs

input_file_name = "input.txt"
code_lookup_table_file_name = "code_lookup_table.txt"
restored_input_file_name = "restored_input_file.txt"
compressed_asci_text_file_name = "compressed_asci_text_file.txt"

def build_code_dict():

    fp = open(code_lookup_table_file_name, 'r')
    contents = fp.read()
    fp.close()

    code_dict = {}
    char_list = []
    temp_code = ""
    length = len(contents)
    i = 0
    while i < (length - 3):
        temp_code = contents[i]
        char_list.append(i)
        temp_write = ""
        i += 2
        #Now in the codeword part
        while contents[i] == '0' or contents[i] == '1':
            if i >= (length - 1): break 
            temp_write += contents[i]
            i += 1
        i += 1
        code_dict[temp_code] = temp_write 

    return char_list, code_dict



def build_tree_from_codes(char_list, code_dict):

    huffman_tree = Tree(0)
    void_root = Node(None, -1, None, None, None, "")
    void_left = Node(None, -1, None, None, void_root, void_root.code_word + "0")
    void_right = Node(None, -1, None, None, void_root, void_root.code_word + "1")
    void_root.left = void_left
    void_root.right = void_right    
    huffman_tree.add_node(void_root)
    huffman_tree.root = void_root
    
    for key in code_dict.keys():
        code = code_dict[key]
        huffman_tree.rebuild_tree(huffman_tree.root, key, code, 0)

    #huffman_tree.print_tree(huffman_tree.root)
    return huffman_tree


def get_encoded_file_contents():

    fp_encoded = codecs.open(compressed_asci_text_file_name, 'r', encoding='utf8')
    contents = fp_encoded.read()
    #print("Encoded:\n'''\n" + contents + "\n'''\n")
    fp_encoded.close()

    ascii_read = ""
    for char in contents:
        binary = "{0:b}".format(ord(char))
        binary = "0"*(8 - len(binary)) + binary
        ascii_read += binary

    return ascii_read

def Decode(code_tree):
    ''' Restore input file from compressed hex file.
        Return true for successful, false for unsuccesful.
    '''
    contents = get_encoded_file_contents()

    #Navigate tree, associating codes with chars and writing to a total_write str
    i = 0
    temp_write = ""
    total_write = ""
    while i < len(contents):
        temp_write += contents[i]
        search_result = code_tree.search_tree(code_tree.root, temp_write, 0)
        if search_result != None:
            total_write += search_result
            temp_write = ""
        i += 1
    
    #Write the decoded text to a reconstructed text file
    fp_restore = open(restored_input_file_name, 'w')
    fp_restore.write(total_write)
    fp_restore.close()

    #Compare reconstructed text to input text
    fp_input = open(input_file_name, 'r')
    contents = fp_input.read()
    fp_input.close()

    return contents == total_write


def main():

    if not os.path.exists(code_lookup_table_file_name) or not os.path.exists(compressed_asci_text_file_name):
        raise("Exception: One or more of the required files do not exist")
        return

    print("Starting to encode \"" + compressed_asci_text_file_name + "\"...")
    char_list, code_dict = build_code_dict()
    
    print("Reconstructing the Huffman Encoding tree...")
    code_tree = build_tree_from_codes(char_list, code_dict)
    print("Writing decoded output to \"" + restored_input_file_name + "\"...")

    if Decode(code_tree):
        print("Successfully decoded the input file!")
    else:
        print("Did not successfully decoded the input file!")
main()
