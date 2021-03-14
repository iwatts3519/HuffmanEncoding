# Huffman Encoding seeks to encode a string or phrase by analysing the frequency of the letters in it and assigning
# them a shorter code than less frequent letters. In Ascii encoding every character is represented by 8 bits,
# which means that 200 characters would take 200 * 8 bits, meaning 1600 bits. With Huffman Encoding, each character
# is assigned a series of 0s and 1s, the most frequent possible only using one or two bits, and the less frequent
# using more bits. In the current example we have reduced the number of bits from 10280 bits to 5497 bits.

# The basic approach that I have taken follows a number of steps as follows:

# 1. Create a list of Tuples that hold the characters and their frequencies.

# 2. Create a Node Tree that slowly merges the tuples with the least values into a single object.

# 3. Use the node tree to build a dictionary of characters and their corresponding Huffman Code (I have chosen this
# solution because it only needs the tree to traversed once - after that the dictionary is used as a reference)

# 4. Use the dictionary to create the Huffman Coded string

# 5. Use the dictionary and the coded string to recreate the original phrase

# Limitations of my approach - my approach requires that the dictionary of all of the codes is present with the
# string, as it uses the dictionary, not the Node Tree, to compress and to uncompress the string, which adds to the
# overhead

# The following import allows us to sort lists using keys from tuples
from operator import itemgetter
import time


# The NodeTree class simply holds pointers to the next items in the tree, which are characters, and stores the nodes
# in a list of Tuples that gradually become a list with a single Tuple in, the first part being a single node tree,
# and the second part being the overall frequency for all the characters
class NodeTree:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

    def __str__(self):
        return f"{self.left}_{self.right}"

    def get_children(self):
        return self.left, self.right

    def get_right(self):
        return self.right

    def get_left(self):
        return self.left


def tally(phrase):
    # tally() is going to create a dictionary of characters and frequencies, by looping over each letter in the
    # phrase, and checking to see if the letter is already a key in the dictionary. If it isn't it creates it and
    # gives it a value of one, and if it is, it adds one to it's value. It has a time complexity of O(n).
    phrase_dict = {}
    for letter in phrase:
        if letter in phrase_dict:
            phrase_dict[letter] += 1
        else:
            phrase_dict[letter] = 1
    phrase_list = sorted(phrase_dict.items(), key=itemgetter(1), reverse=True)
    # Because we have sorted the dictionary, it is now turned into a list of tuples
    return phrase_list


def build_nodes(tally_list):
    # tally_list represents a list of tuples, where the first item in the tuple is the character and the second item
    # is the frequency. A loop is set up that loops over tally_list, taking the two lowest tuples, unpacking them
    # into the variables char and freq (char_1 and freq_1 for the last item in the list and char2, freq_2 for the
    # second to last item in the list). The list is then defined as the list minus the last two items in it,
    # a NodeTree is created from the characters and then that NodeTree is appended to the list with the combined
    # frequency of those characters. This continues until we have a single NodeTree with a frequency of all of the
    # letters in the phrase. This has a time complexity of O(n)
    while len(tally_list) > 1:
        char_1, freq_1 = tally_list[-1]
        char_2, freq_2 = tally_list[-2]
        tally_list = tally_list[:-2]
        node = NodeTree(char_1, char_2)
        tally_list.append((node, freq_1 + freq_2))

        tally_list = sorted(tally_list, key=itemgetter(1), reverse=True)

    return tally_list


def huffman_encode(node, left=True, bin_string=''):
    # the huffman_encode function is a recursive function that traverses the NodeTree object left, then right. As it
    # is recursive, it has to start with a base case, which is if the type of the node is a str (as opposed to an
    # object), then it has reached a leaf. It returns the string and the current value of bin_string (binary string)
    # back up the recursion stack until it reaches the final leaf, at which point we have a dictionary of each
    # character and it's huffman code, which we can use to print out a table of characters, codes and frequencies,
    # and, more importantly, use to create the coded version of the original phrase, and also to decode the
    # binary_string representation of the original phrase. Because this is a recursive function and has a branching
    # factor of 2, it has a Time Complexity of O(2^n)
    if type(node) is str:
        return {node: bin_string}
    # the get_children method returns a tuple of the left and right children of the node
    (left, right) = node.get_children()
    huffman_dict = {}
    # The encoding algorithm puts a 0 on the bin_string if it traverses to the left, and a 1 if it traverses to the
    # right. Once it reaches a leaf it moves back up the recursion stack to find the code for the next character. The
    # ultimate output is a dictionary of characters and their huffman code.
    huffman_dict.update(huffman_encode(left, True, bin_string + '0'))
    huffman_dict.update(huffman_encode(right, False, bin_string + '1'))
    return huffman_dict


def print_huffman_table(c_tally, n_tree):
    # This prints out a table of the characters, the Huffman Code assigned to those characters and the frequency that
    # they occur. It uses the frequency list of tuples - c_tally (character and frequency) produced by the tally
    # function. It also uses the dictionary produced by the huffman encode function - n_tree -  which contains the
    # characters and their huffman code. This is unnecessary for the encoding / decoding to work but does demonstrate
    # the logic that has gone before.
    print("\n*****************************************")
    print("************* Huffman Codes *************")
    print("*****************************************")
    print("\nCharacter    | Huffman Code | Frequency")
    print("_______________________________________")
    for (char, frequency) in c_tally:
        print(f"{char!r:12} | {n_tree[char]:12} | {frequency}")


def create_huffman_string(node, left=True, bin_string=''):
    if type(node) is str:
        return bin_string

    (left, right) = node.get_children()
    bin_string += create_huffman_string(left, True, bin_string + '0')
    bin_string += create_huffman_string(right, False, bin_string + '1')
    return bin_string


def decode(huffman_dict, huffman_string):
    # The decoding of the string requires the binary string representing the phrase and the dictionary of characters
    # and codes. It uses a nested loop, which traverses through the binary string one character at a time,
    # adding each 0 or 1 to the temp_huff variable. Each time another character is added, it moves to the inner loop
    # and traverses through the dictionary trying to find a code that matches. If it does, it adds that matching
    # character to the text variable, sets temp_huff back to an empty string, breaks out of the inner loop,
    # and carries on from the point in the binary string where it left off. This way it can build the original phrase
    # back up again. This method has a time complexity of O(n^2) which is the worst of all the functions, but doesn't
    # seem required for the assignment - I have added it for completeness.
    text = ""
    temp_huff = ""
    for char in huffman_string:
        temp_huff += char
        for h_char, h_code in huffman_dict.items():
            if h_code == temp_huff:
                text += h_char
                temp_huff = ""
                break
    return text


def size_of_original(phrase):
    # This function simply returns the size of the original phrase as ascii characters that require 8 bits per
    # character.
    return len(phrase) * 8


def size_of_coded(c_tally, n_tree):
    # This function returns the size of the encoded string, by unpacking each character and it's frequency in the
    # original tally list of tuples, and for each one it finds the length of the matching code in the huffman
    # dictionary and multiplies the length by the frequency. For example, the space character is used 238 times,
    # and is encoded as "00", which means it takes up 238 * 2 bits, which is 476 bits.
    ret_bits = 0
    for (char, frequency) in c_tally:
        ret_bits += len(n_tree[char]) * frequency
    return ret_bits


# Test Data -  First of all a phrase is assigned to the variable new_phrase (which happens to be the first few sentences
# from The Hobbit)

# new_phrase = "In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of " \
#              "worms and an oozy smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat: it " \
#              "was a hobbit-hole, and that means comfort. \nIt had a perfectly round door like a porthole, painted green, " \
#              "with a shiny yellow brass knob in the exact middle. The door opened on to a tube-shaped hall like a " \
#              "tunnel: a very comfortable tunnel without smoke, with panelled walls, and floors tiled and carpeted, " \
#              "provided with polished chairs, and lots and lots of pegs for hats and coats — the hobbit was fond of " \
#              "visitors. The tunnel wound on and on, going fairly but not quite straight into the side of the hill — " \
#              "The Hill, as all the people for many miles round called it — and many little round doors opened out of " \
#              "it, first on one side and then on another. No going upstairs for the hobbit: bedrooms, bathrooms, " \
#              "cellars, pantries (lots of these), wardrobes (he had whole rooms devoted to clothes), kitchens, " \
#              "dining-rooms, all were on the same floor, and indeed on the same passage. The best rooms were all on the " \
#              "left-hand side (going in), for these were the only ones to have windows, deep-set round windows looking " \
#              "over his garden, and meadows beyond, sloping down to the river. "
x = open("war_and_peace.txt", "r")
new_phrase = x.read()
# First of all we create a list of tuples, each tuple containing a character, and the frequency that character occurs
# in the original phrase
s1_start = time.time()
char_tally = tally(new_phrase)
s1_end = time.time()
print("\n**********************")
print("***** Tally List *****")
print("**********************")
print(char_tally)
# Next we create the node tree which results in a tuple (object, frequency) in a list. This process uses recursion so
# at the end we end up with just a single tuple in the list
s2_start = time.time()
node_tree = build_nodes(char_tally)
s2_end = time.time()
print("\n*********************")
print("***** Node Tree *****")
print("*********************")
print(node_tree)
# Now comes the part where we use the Node Tree to build a dictionary of characters and their huffman code. Because
# Node Tree ends up represented as a tuple in a list, and because we only need the object at this point, it is passed
# to the huffman_encode function using node_tree[0][0]
s3_start = time.time()
huffman_code = huffman_encode(node_tree[0][0])
s3_end = time.time()
print("\n********************************")
print("***** Coding of Characters *****")
print("********************************")
print(huffman_code)
# The next function simply prints out a user readable table of the character, it's huffman code, and the frequency
# that it occurs. This is ordered with the most frequent character at the top.
print_huffman_table(char_tally, huffman_code)
# Next we can view the encoded binary string representation of the original phrase
print("\n**********************************")
print("***** Huffman Encoded String *****")
print("**********************************")
s4_start = time.time()
encoded_string = create_huffman_string(node_tree[0][0])
s4_end = time.time()
print(encoded_string)
# Next we calculate the original length of the string, the encoded length, and the compression percentage achieved
original_size = size_of_original(new_phrase)
new_size = size_of_coded(char_tally, huffman_code)
compression_ratio = new_size / original_size * 100
print("\n*******************************")
print("***** Sizes and Reduction *****")
print("*******************************")

print(
    f"The original size of the phrase is {original_size} bits, while the new size of the phrase is {new_size} bits, "
    f"giving us {compression_ratio:0.2f}% reduction in size")

# Finally we will prove it works by decoding it using the decode function
print("\n***************************")
print("***** Original Phrase *****")
print("***************************")
s5_start = time.time()
print(decode(huffman_code, encoded_string))
s5_end = time.time()

print("\n********************")
print("***** Timings ******")
print("********************")
print("\n")
print(f"Time taken to create a list of the characters and their frequency is {s1_end - s1_start}")
print(f"Time taken to build a Node Tree is {s2_end - s2_start}")
print(
    f"Time taken to use the Node Tree to build a dictionary of characters and their huffman code is {s3_end - s3_start}")
print(f"Time taken to create the huffman encoded string {s4_end - s4_start}")
print(
    f"Time taken to decode the string using the dictionary and the original tally list from step 1 {s5_end - s5_start}")
# References

# [1] N. Gibson. "Huffman coding in Python - TechRepublic."
# https://www.techrepublic.com/article/huffman-coding-in-python/ (accessed 22/06/2020)

# [2] R. Rathi. "Huffman Encoding — Compression basics in Python - Hashtag by IECSE - Medium."
# https://medium.com/iecse-hashtag/huffman-coding-compression-basics-in-python-6653cdb4c476 (accessed 22/06/2020)

# [3] B. Srivastava. "Huffman Coding - Python Implementation."
# https://bhrigu.me/blog/2017/01/17/huffman-coding-python-implementation/ (accessed 22/06/2020)

# [4] Stackoverflow. "python - How can I create a tree for Huffman encoding and decoding? - Stack Overflow."
# https://stackoverflow.com/questions/11587044/how-can-i-create-a-tree-for-huffman-encoding-and-decoding (accessed
# 22/06/2020)

# [5] University of California. "Huffman Encoding."
# https://sites.cs.ucsb.edu/~franklin//20/assigns/prog6files/HuffmanEncoding.htm (accessed 22/06/2020)

# [6] Wikipedia. "Huffman coding." https://en.wikipedia.org/wiki/Huffman_coding (accessed 22/06/2020)
