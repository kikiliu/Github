#! usr/bin/env python

__author__ = 'Qi Liu'
__email__ = 'kikiliu@ischool.berkeley.edu'
__python_version = '2.7.3'
__can_anonymously_use_as_example = True

scores_file_path = "D:\\SkyDrive\\Berkeley\\206\\A4\\AFINN-111.txt"
tweets_file_path = "D:\\SkyDrive\\Berkeley\\206\\A4\\tweets.txt"


import string

#store sentiment scores words in dictionary store_dic
score_dic = {}
def load_scores(scores_file_path):
    with open(scores_file_path,"r") as scores_file:
        for line in scores_file:
            if line !="":
                line = line.rstrip("\n")
                columns = line.split("\t")
                score_dic[columns[0]] = columns[1]
                
#calculate the average sentiment score for each tweet
def calc_tweets(tweets_file_path):
    with open(tweets_file_path, "r") as tweets_file:
        for line in tweets_file:
            if line != "":
                tweet_words = line.split()
                tweet_score = 0.0
                count = 0.0
                for word in tweet_words:
                    word = word.strip(string.punctuation)
                    word = word.lower()
                    if word in score_dic:
                        tweet_score += float(score_dic[word])
                        count += 1.0
            if count != 0.0:
                print("%.2f" % (tweet_score/count))
            else:
                print("0.00")

def main():
    load_scores(scores_file_path)
    calc_tweets(tweets_file_path)

if __name__ == '__main__':
    main()