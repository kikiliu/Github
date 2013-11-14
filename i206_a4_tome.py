#! usr/bin/env python

__author__ = 'Qi Liu'
__email__ = 'kikiliu@ischool.berkeley.edu'
__python_version = '2.7.3'
__can_anonymously_use_as_example = True 


import time
import string
import sys
import os

#Please find the tome file paths at main()
scores_file_path = os.path.relpath("AFINN-111.txt")

#store sentiment scores words in a dictionary with key of the word and value of the score
#store sentiment scores words in a list of tuple pair with first element of the word and second of the score
score_dic = {}
score_list = []
def load_scores(scores_file_path):
    with open(scores_file_path,"r") as scores_file:
        for line in scores_file:
            if line !="":
                line = line.rstrip("\n")
                columns = line.split("\t")
                score_dic[columns[0]] = columns[1]
                score_tuple = (columns[0], columns[1])
                score_list.append(score_tuple)

#store each word of tome in a list
def load_tome(tome_file_path):
    tome_list = []
    with open(tome_file_path, "r") as tome_file:
        for line in tome_file:            
            if line != "":                
                tome_words = line.split()
                for word in tome_words:
                    word = word.strip(string.punctuation)
                    word = word.lower()
                    tome_list.append(word)
    return tome_list

# list_of_words: all the words to be searched in score_list
# The following three functions are to calculate the average sentiment score of the list_of_words and return time elapsed          
def calc_dictionary_lookup(list_of_words):
    tome_score = 0.0
    count = 0.0
    t0 = time.clock()
    for word in list_of_words:
        if word in score_dic:
            tome_score += float(score_dic[word])
            count += 1.0
    t1 =time.clock()
    if count != 0.0:
        print "Sentiment score by Strategy 1 is %.2f" % (tome_score/count)
    else:
        print "0.00"
    return (t1-t0)

def calc_linear_search(list_of_words):
    tome_score = 0.0
    count = 0.0
    t0 = time.clock()
    for word in list_of_words:
        for i in range(len(score_list)):
            if word == score_list[i][0]:
                tome_score += float(score_list[i][1])
                count += 1.0
    t1 = time.clock()
    if count != 0.0:
        print "Sentiment score by Strategy 2 is %.2f" % (tome_score/count)
    else:
        print "0.00"
    return (t1-t0)        
        
def calc_binary_search(list_of_words):    
    tome_score = 0.0
    count = 0.0
    t0 = time.clock()
    for word in list_of_words:        
        search_result = binary_search(score_list, word, 0, len(score_list)-1)
        if search_result != sys.maxint:
            tome_score += float(search_result)
            count += 1.0
    t1 = time.clock()
    if count != 0.0:
        print "Sentiment score by Strategy 3 is %.2f" % (tome_score/count)
    else:
        print "0.00"
    return (t1-t0)  
                  
# score_list: a list of (word, score) pair sorted by word
# word: a word to search in score_list
# start: index of first element to search in score_list
# end: index of last element to search in score_list  
# personal notes: recursive function should have returned value!

def binary_search(score_list, word, start, end):
    if end < start:
        return sys.maxint        
    else:
        middle = int((end + start)/2)
        if word > score_list[middle][0]:
            return binary_search(score_list, word, middle + 1, end)            
        elif word < score_list[middle][0]:
            return binary_search(score_list, word, start, middle-1)            
        else:
            return score_list[middle][1]

#for each strategy, print its time elapsed            
def print_time(tome_file_path):
    tome_words_list = load_tome(tome_file_path)
    t_lookup = calc_dictionary_lookup(tome_words_list)
    t_linear = calc_linear_search(tome_words_list)
    t_binary = calc_binary_search(tome_words_list) 
    print "Time of Strategy 1, 2, 3: %f, %f, %f" % (t_lookup, t_linear, t_binary)   

def main():
    load_scores(scores_file_path)
    print_time(os.path.relpath("\\pg100.txt"))
    print_time(os.path.relpath("\\pg135.txt"))
    print_time(os.path.relpath("\\pg3160.txt"))
    print_time(os.path.relpath("\\pg19033.txt"))

    

if __name__ == '__main__':
    main()