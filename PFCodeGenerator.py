from HuffmanTree import *
from Encode import *
import codecs

'''
Prefix Free code
Want to use a Huffman tree

1) Read through input text file, create dictionaries for each symbol to get
   a letter count for each symbol. Store each symbol in a list for reference
2) Create a Huffman tree (min 3 bits) to convert each symbol to a code word
'''

input_file_name = "input.txt"
code_lookup_table_file_name = "code_lookup_table.txt"
saved_huffman_tree_file_name = "saved_huffman_tree.txt"
compressed_asci_text_file_name = "compressed_asci_text_file.txt"
restored_input_file_name = "restored_input_file_name.txt"
approach = 0

def tally_freq(input_file_name, char_dict, char_list):
    ''' Fill a dictionary (and iterable list) of all symbols that appear in the
    input text file, and count the number of appearances each one makes. This
    is for calculating the code word length from the entropy function based on
    their appearance frequency.

    In: file name to read through
    Out: dictionary and iterable list of symbols and their appearance frequencies
    '''
    fp = open(input_file_name, 'r')
    contents = fp.read()
    #print("\nInput file contents:\n'''\n{}\n'''\n".format(contents))
    for character in contents:
        try:
            char_dict[character] += 1
        except:
            char_dict[character] = 1
            char_list.append(character)
    fp.close()
    return char_dict, char_list


def print_table(char_dict, char_list):
    print("Char dict:")
    print(char_dict)
    print("\nChar LIST:")
    print(char_list)

    print("\nchar\tfreq\tASCII")
    for char in char_list:
        print("'{}'\t{}\t{}".format(char, char_dict[char], ord(char)))


def save_tree_to_file(huffman_tree):

    fp = open(saved_huffman_tree_file_name, 'w')
    fp.write(str(huffman_tree.write_tree_to_str(huffman_tree.root)))
    fp.close()


def compress_output_file(char_codes):
    ''' Write a hex file that is the compressed version of the input file.
    '''
    
    fp_input = open(input_file_name, 'r')
    contents = fp_input.read()
    fp_input.close()

    total_write = ""
    code = ""
    for char in contents:
        try:
            code = char_codes[char]
            total_write += str(code)
        except:
            print("Should never get here!\nChar:", char, "does not exist in table.")

    ascii_write = ""
    final_write = ""
    i = 0
    while i < len(total_write):
        ascii_write += total_write[i]
        i += 1
        if i%8 == 0:
            final_write += chr(int(ascii_write,2))
            ascii_write = ""

    # Non-aligned with 8-bit ASCII codes
    if ascii_write != "":
        ascii_write += "0"*(8 - len(ascii_write))
        final_write += chr(int(ascii_write,2))

    #print("\nCompressed output file contents:\n'''\n{}\n'''\n".format(final_write))

    fp = codecs.open(compressed_asci_text_file_name, 'w', encoding='utf8')
    fp.write(final_write)
    fp.close()


def main():
    print("Starting to encode \"" + input_file_name + "\"...")
    char_dict = {}
    char_list = []
    char_dict, char_list = tally_freq(input_file_name, char_dict, char_list)

    print("Constructing the Huffman Encoding tree...")
    #Get codes from tree
    char_codes, huffman_tree = Encode(char_dict, char_list)

    print("Writing codes to a code lookup table file: \"" + code_lookup_table_file_name + "\"...")
    #Write codes to code_lookup_table.txt file
    fp = open(code_lookup_table_file_name, 'w')
    for i in char_list:
        temp = i + " " + char_codes[i] + "\n"
        fp.write(temp)
    fp.close()

    print("Writing encoded output to \"" + compressed_asci_text_file_name + "\"...")
    #Use codes to write compressed output file
    compress_output_file(char_codes)
    print("Encoding completed!")
    
main()
