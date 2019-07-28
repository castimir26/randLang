
import random
from itertools import product


def con_select_all(vowel_list,consonant_list):

    '''
    Input: the hard-coded vowel_list and an empty list for consonants
    Process:
        1. Initialize the alphabet list
        2. Add vowels to the vowel_list
        3. Add consonants to the consonant_list
    Output: a list of consonants
    '''
    alphabet_list = create_alphabet()
    for letter in alphabet_list:
        if letter not in vowel_list:
            consonant_list.append((random.SystemRandom().randint(0,100), letter))
    return consonant_list


def enum_dict(dictionary):

    '''
	Abstract method for enumerate dictionary and returning values I want in this situation
	Input: an object
	Process:
		1. Use enumerate to pare away the keys. They should all be the same anyway
		2. Instantiate some lists
		3. Splice the original list to weed out the former key of the nested dictionary Note: this is all a strong, hence the need for this method
		4. Find where the former value of the nested dictionary ends and get an index
		5. Iterate up to the index, appending the values as you go
		6. Join it all together into a string
		7. Append and return a list of all strings
	Output: A list of strings
	'''
    return_list = []
    for key,value in enumerate(dictionary):
        instance_word = ""
        instance = value.word
        new_instance = instance[10:]
        index = new_instance.find("'")
        for x in range(0,index):
            instance_word+=new_instance[x]
        return_list.append(instance_word)
    return return_list


def assemble_list(sound,weight):

    '''
    Input: a sound and a weight
    Process:
        1. Store ipa_sound and weight in a tuple
        2. Add tuple to list
    return: a list
    '''
    assembled_list = []
    tuple = (sound, weight)
    assembled_list.append(tuple)
    return assembled_list


def weighted_random(pairs):

    '''
    weighted_random transforms tuples with weighted values into randomly chosen values.
    Meant to be generic
    Input: a list of tuples
    Process:
        1. Sum the numerical first part of all tuples
        2. Choose a weighting seed based on the interval 1 to total
        3. For each pair, decrement r by weight
        4. Once r is below 0, return
    Output: the randomly selected value
    '''
    try:
        total = sum(pair[0] for pair in pairs)
        r = random.SystemRandom().randint(1, total)
        for (weight, value) in pairs:
            r -= weight
            if r <= 0: return value
    except TypeError:
        print(pairs)


def assemble_syllable(pattern, vowels, consonants):

    '''
    Input: The current pattern of syllables
    Process:
        1. Choose vowels or consonants based on letters in the pattern
        2. Call a weighted_random function on the global vowel and consonant lists
        3. return created syllable
    Output: a list
    '''
    syllable = []
    try:
        for letter in pattern:
            if letter == "v":
                letter = weighted_random(vowels)
            if letter == "c":
                letter = weighted_random(consonants)
            letter = "".join(letter)
            syllable.append(letter)
    except Exception as e:
        print(e)
    return syllable


def assemble_word(length, patterns, vowels, consonants):

    '''
    Input: the number of syllables required,patterns,vowels, and consonants
    Process:
        1. Feed the patterns parameter into weighted_random
        2. Feed chosen pattern into the assemble_syllable
        3. Join it all together
    Output: a list, with join called on the elements
    '''

    word = []
    try:
        for x in range(length):
            pattern = weighted_random(patterns)
            syllable = "".join(assemble_syllable(pattern, vowels, consonants))
            word.append(syllable)
        word = "".join(word)
    except Exception as e:
        print(e)
        print("word: ", word)
        print("length: ", length)
        print("patterns: ", patterns)
        print("pattern: ", pattern)
        print("vowels: ", vowels)
        print("consonants: ", consonants)
    return word


def create_alphabet():

    '''
    Input: none
    Process: Use map and range to generate the entire alphabet.
    Output: a map (key-value pair)

    Meant to be generic if it is needed elsewhere
    '''
    alphabet = map(chr, range(ord('a'), ord('z')+1))
    return alphabet


def create_syllables():

    '''
    Input: none
    Process:
        1. Create a seed for the product function later on
        2. Create a list to exclude invalid syllables with only consonants
        3. Use map and product to generate all possible syllable combinations
    Output: a list with all possible syllable combinations

    It's worth noting that you can have repeat patterns, or functionally repeat
    patterns. The difference between cvvc and vvc is really, really small.
    However, real languages are messy like this. This is by design.
    '''
    syllable_frag = "cv"
    invalid_list = ["cc", "ccc", "cccc"]
    four_letters = list(map(''.join, product(syllable_frag, repeat=4)))
    three_letters = list(map(''.join, product(syllable_frag, repeat=3)))
    two_letters = list(map(''.join, product(syllable_frag, repeat=2)))
    four_letters.extend(three_letters)
    four_letters.extend(two_letters)
    for syllable in four_letters:
        if syllable in invalid_list:
            four_letters.remove(syllable)
    return four_letters
