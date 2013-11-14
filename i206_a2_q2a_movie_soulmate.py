#! usr/bin/env python

__author__ = 'Qi Liu'
__email__ = 'kikiliu@ischool.berkeley.edu'
__python_version = '2.7.3'
__can_anonymously_use_as_example = True 

rating_file_path = "D:\\SkyDrive\\Berkeley\\206\\A2\\ratings.txt"
movie_file_path = "D:\\SkyDrive\\Berkeley\\206\\A2\\movies.txt"

#create movie object, including the properties of average rating,
#the name of movie and rating count for each movie.
class Movie:
    average_rating = 0.0
    watched_count = 0
    name = ""
    def __init__(self, name):
        self.name = name       
        

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
        
        return sorted(self.movies, key=lambda x: x.average_rating, reverse=True)

        


def main():
    rating_system = RatingSystem(rating_file_path, movie_file_path)
    rating_system.get_sorted_movies_by_avg_rating()
    user_id = raw_input("Pls enter a user id: ")
    
    if user_id in rating_system.users:
        unwatched_movies = rating_system.get_unwatched(user_id)
        
        print ("The user has %s unwatched movies" % len(unwatched_movies))
        for i in range(min(len(unwatched_movies),5)):
            print ("%d: %s, Avg Rating: %.2f, Num Ratings: %d" % (
            i+1,
            unwatched_movies[i].name,
            unwatched_movies[i].average_rating,
            unwatched_movies[i].watched_count))
    else:
        print ("User %s hasn't rated any movie" % user_id)            

main()