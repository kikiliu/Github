#! usr/bin/env python

__author__ = 'Qi Liu'
__email__ = 'kikiliu@ischool.berkeley.edu'
__python_version = '2.7.3'
__can_anonymously_use_as_example = True 

rating_file_path = "D:\\SkyDrive\\Berkeley\\206\\A2\\ratings.txt"
movie_file_path = "D:\\SkyDrive\\Berkeley\\206\\A2\\movies.txt"


class Movie:
    average_rating = 0.0
    watched_count = 0
    name = ""
    def __init__(self, name):
        self.name = name       

class Soulmate:
    index = -1
    average_difference = 0.0
    matched_count = 0
               

class RatingSystem:
    movies = []
    ratings = []
    users = []
    
    def __init__(self, rating_file_path, movie_file_path):
        self.load_ratings(rating_file_path)
        self.load_movie_names(movie_file_path)
        
    #load rating.txt and parse into two lists. One is a list of user ids. 
    #The other is a matrix for user's ratings per movie.    
    def load_ratings(self, rating_file_path):
        with open(rating_file_path,"r") as rating_file:
            for line in rating_file:
                if line !="":                    
                    line = line.rstrip("\n")
                    columns = line.split(",")              
                    self.users.append(columns[0])
                    user_ratings = []
                    self.ratings.append(user_ratings)   
                    for i in range(1,len(columns)):
                        rating =  int(columns[i])
                        user_ratings.append(rating)


    #create a list with each element is a movie instance. 
    #assign each line of movie.txt as a movie's name
    def load_movie_names(self, movie_file_path):
        with open(movie_file_path,"r") as movie_names_file:
            for item in movie_names_file:
                item = item.rstrip("\n")
                movie = Movie(item)            
                self.movies.append(movie)

        
    #get movies not yet watched by given user id
    def get_unwatched(self, user):
        unwatched_list=[]
        index = self.users.index(user)
        for i in range(len(self.ratings[index])):
            if self.ratings[index][i] == 0:
                unwatched_list.append(self.movies[i])                
        return sorted(unwatched_list, key=lambda x:x.average_rating, reverse=True)
        
    def get_sorted_movies_by_avg_rating(self):    
        for movie in self.movies:
            movie.average_rating = 0.0
            movie.watched_count = 0 
            index = self.movies.index(movie)

            for user_ratings in self.ratings:
                if user_ratings[index] != 0:
                    movie.average_rating += user_ratings[index]
                    movie.watched_count += 1        
            if movie.watched_count != 0:
                movie.average_rating /= float(movie.watched_count)
            else:
                movie.average_rating = 0.0
        
        return sorted(self.movies, key=lambda x: x.average_rating*1000+x.watched_count, reverse=True)
    

   
    def find_soulmate(self, user):    
        user_index = self.users.index(user)
        soulmate = Soulmate()     
        for i in range(len(self.ratings)):  #iterate users
            if i != user_index:    
                matched_count = 0
                total_difference = 0
                for j in range(len(self.ratings[i])):  #iterate ratings per user
                    if self.ratings[user_index][j]!= 0 and self.ratings[i][j]!= 0:
                        matched_count += 1
                        total_difference += abs(self.ratings[user_index][j] 
                                                - self.ratings[i][j])
                if matched_count != 0:                    
                    average_difference = float(total_difference)/float(matched_count)   
        
                    if soulmate.index < 0 or soulmate.average_difference > average_difference or (soulmate.average_difference == average_difference and soulmate.matched_count < matched_count):
                        soulmate.index = i
                        soulmate.average_difference = average_difference
                        soulmate.matched_count = matched_count                            
        return soulmate.index    
            
    def recommend_soulmate_movies(self, user, soulmate_index):
        user_index = self.users.index(user)

        recommends=[]
        
        #build a recommended movie list, starting from 5 and then 4, rated by soulmate
        for i in range(len(self.ratings[user_index])):
            if self.ratings[user_index][i] == 0 and self.ratings[soulmate_index][i] == 5:
                recommends.append(i)
        for i in range(len(self.ratings[user_index])):
            if self.ratings[user_index][i] == 0 and self.ratings[soulmate_index][i] == 4:
                recommends.append(i)
        for k in range(min(len(recommends),5)):
            rating_index = recommends[k]
            print ("%d. %s, rating by %s: %d, Avg Rating: %.2f, Num Ratings: %d" % (
                    k+1,
                    self.movies[rating_index].name,
                    self.users[soulmate_index],
                    self.ratings[soulmate_index][rating_index],
                    self.movies[rating_index].average_rating,
                    self.movies[rating_index].watched_count)
                    )        


def main():
    rating_system = RatingSystem(rating_file_path, movie_file_path)
    sorted_movies = rating_system.get_sorted_movies_by_avg_rating()
    user_id = raw_input("Pls enter a user id: ")
    
    if user_id in rating_system.users:
        soulmate_index = rating_system.find_soulmate(user_id)
        print (rating_system.users[soulmate_index] + " is your movie soulmate")
        rating_system.recommend_soulmate_movies(user_id, soulmate_index)
    else:
        print ("This is a new users. Here are five movies we recommended:")
        for i in range(5):
            print ("%d. %s, Avg Rating: %.2f, Num Ratings: %d" % (
                      i+1,
                      sorted_movies[i].name,
                      sorted_movies[i].average_rating,
                      sorted_movies[i].watched_count)
                      )
                            

main()