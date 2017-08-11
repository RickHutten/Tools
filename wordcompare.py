import time

def timed(f):
    """ Decoration function to time functions """
    def inner(*args, **kwargs):
        start = time.clock()
        ans = f(*args, **kwargs)
        print "%s() time: %f s" %(f.__name__, time.clock() - start)
        return ans
    return inner


@timed
def find_close_words(word, word_list):
    """
    Find the max 5 closest words to the word given.
    return: list of close words [('word_1', 0.995), ('word_2', 0.9040),...]
    """
    word = word.lower()
    close_words = []
    levenshtein = []
    for i, w in enumerate(word_list):
        # Quick but sometimes inaccurate
        score = compare_words(word, w, i)
        close_words.append((w, score))
        # Slower but usually more accurate
        score = levenshtein_distance(word, w, i)
        levenshtein.append((w, score))
    return [ sorted(close_words, key=lambda a: -a[1])[:5],
             sorted(levenshtein, key=lambda a: -a[1])[:5] ]


def compare_words(w1, w2, i=0):
    """
    Checks how much w1 compares to w2 by checking the number of letters that are
    the same with different shifts (max 2). Is inaccurate when a letter in the center
    of the word is exta or missing (different distance between beginning and end of word).
    return: float between 0 (completely different) and 1 (exactly the same)
    """
    if w1 == w2:
        return 1
    
    point_list = []
    # Check points for different shifts
    for shift in [1, 2]:
        points = 0
        for z in zip(w1, w2[shift:]):
            if z[0] == z[1]:
                points += 1
        point_list.append(points)
    for shift in [0, 1, 2]:
        points = 0
        for z in zip(w1[shift:], w2):
            if z[0] == z[1]:
                points += 1
        point_list.append(points)
    frequency_penalty = i / 200000.0
    return max(0, max(point_list) / float(max(len(w1), len(w2))) - frequency_penalty)

def levenshtein_distance(w1, w2, index=0):
    """
    Calculates the Levenshtein distance using Hirschberg's algorithm
    and calculates a 
    return: float between 0 (completely different) and 1 (exactly the same)
    """
    if w1 == w2:
        return 1
    
    v0 = range(len(w2) + 1)
    v1 = [0] * (len(w2) + 1)
    
    for i in xrange(1, len(w1) + 1):
        v1[0] = i
        for j in xrange(1, len(w2) + 1):
            if w1[i-1] != w2[j-1]:
                v1[j] = 1 + min(v1[j-1], v0[j], v0[j-1])
            else:
                v1[j] = min(v1[j-1] + 1, v0[j] + 1, v0[j-1])
        v0 = [i for i in v1]
        
    frequency_penalty = index / 200000.0
    return max(0, 1 - v1[len(w2)] / float(max(len(w1), len(w2))) - frequency_penalty)
        

if __name__ == "__main__" and 1:
    # Load file with most common words
    with open("english_10000.txt") as f:
        word_list = f.readlines()
    word_list = [word.strip() for word in word_list]

    # Keep asking for words until the word 'stop', 'exit' or 'quit' is written
    while True:
        word = raw_input("Check this word: ")
        if word in ["stop", "exit", "quit"]:
            break
        close_words = find_close_words(word, word_list)
        print "Closest words found own algorithm:"
        print close_words[0]
        print "Closest words found Hirschberg's algorithm:"
        print close_words[1]
        print ""
