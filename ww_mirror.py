"""
Code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list. Key idea is, given an 
    element, search downwards from its position in the input list
    until we hit something different, and continue from there.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    new_list = []
    item_index = 0
    while item_index < len(list1):
        current_item = list1[item_index]
        new_list.append(current_item)
        next_index = item_index + 1
        while next_index < len(list1):
            if current_item != list1[next_index]:
                break
            else:
                next_index += 1
        item_index = next_index
    return new_list

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.
    
    If the lists are sorted by ascending order, then we can conclude the item
    is not in both if our search for it takes us past the point where this item
    would be in the other list. In case of ties, check the next character down, 
    since the lists are sorted in ascending order.

    This function can be iterative.
    """
    new_list = []
    index_one = 0
    index_two = 0
    while index_one < len(list1) and index_two < len(list2):
        item_one = list1[index_one]
        item_two = list2[index_two]
        if item_one == item_two:
            new_list.append(item_one)
            index_one += 1
            index_two += 1    
        elif isinstance(item_one, str) and isinstance(item_two, str):
            char_index = 0
            while char_index < min(len(item_one),len(item_two)):
                if ord(item_one[char_index]) < ord(item_two[char_index]):
                    index_one += 1
                    break
                elif ord(item_one[char_index]) > ord(item_two[char_index]):
                    index_two += 1
                    break
                else:
                    char_index += 1
            if char_index >= len(item_one):
                index_one += 1
            elif char_index >= len(item_two):
                index_two += 1
        elif isinstance(item_one, int) and isinstance(item_two, int):
            if item_one < item_two:
                index_one += 1
            elif item_one > item_two:
                index_two += 1
    return new_list            

# Functions to perform merge sort

def traverser(index, source_list, result_list):
    """
    Helper function to add items as-is from a sorted source list to a result list
    """
    while index < len(source_list):
        item_left = source_list[index]
        result_list.append(item_left)
        index += 1


def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.
    
    Idea here is to check, at the same index, which comes first.

    This function can be iterative.
    """   
    new_list = []
    index_one = 0
    index_two = 0
    while index_one < len(list1) and index_two < len(list2):
        item_one = list1[index_one]
        item_two = list2[index_two]
        if item_one == item_two:
            new_list.append(item_one)
            new_list.append(item_two)
            index_one += 1
            index_two += 1
        elif isinstance(item_one, str) and isinstance(item_two, str):
            char_index = 0
            while char_index < min(len(item_one),len(item_two)):
                if ord(item_one[char_index]) < ord(item_two[char_index]):
                    new_list.append(item_one)
                    index_one += 1
                    break
                elif ord(item_one[char_index]) > ord(item_two[char_index]):
                    new_list.append(item_two)
                    index_two += 1
                    break
                else:
                    char_index += 1
            if char_index >= len(item_one):
                new_list.append(item_one)
                index_one += 1
            elif char_index >= len(item_two):
                new_list.append(item_two)
                index_two += 1
        elif isinstance(item_one, int) and isinstance(item_two, int):
            if item_one < item_two:
                new_list.append(item_one)
                index_one += 1
            elif item_one > item_two:
                new_list.append(item_two)
                index_two += 1
    traverser(index_one, list1, new_list)            
    traverser(index_two, list2, new_list)
    return new_list                    
        
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.
    Idea is to split list into 2 lists of n/2 then call itself.
    Then merge them back together.

    This function should be recursive.
    """
    if len(list1) <= 1:
        return list1
    else:
        half_index = len(list1) // 2
        first_half = merge_sort(list1[:half_index])
        second_half = merge_sort(list1[half_index:])
        return merge(first_half, second_half)

# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    word_list = []
    word = str(word) #Sanity check
    if len(word) == 0:
        return [""]
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings(rest)
        for new_string in rest_strings:
            word_list.append(new_string)
            str_index = 0
            while str_index <= len(new_string):
                result_string = new_string[:str_index] + first + new_string[str_index:]
                word_list.append(result_string)
                str_index += 1
        return word_list

# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    word_list = []
    url = codeskulptor.file2url(filename)
    dictfile = urllib2.urlopen(url)
    for line in dictfile.readlines():
        word_list.append(line[:-1])
    return word_list

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()
