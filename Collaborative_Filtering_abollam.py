#Collaborative Filtering
import math
import numpy as np
import pandas as pd
ratings = pd.read_csv('ratings_train_85.csv', names = ['user','movie','rating','timestamp'])
test_file = pd.read_csv('ratings_test_15_v2.csv',names =['user','movie','rating','timestamp'] )
movie = ratings.movie.unique()
movie.sort()
user = ratings.user.unique()
user.sort()

index_col = [] 
for i in range(len(movie)):
    index_col.append(i)

index_movie ={}
for i in range(len(movie)):
    index_movie[movie[i]] = index_col[i]

index_row = [] 
for i in range(671):
    index_row.append(i)

index_user ={}
for i in range(671):
    index_user[user[i]] = index_row[i]


movie_user_matrix = np.zeros((len(movie),671))
for i in range(len(ratings)):
    movieId = ratings.ix[i,1]
    userId = ratings.ix[i,0]
    mid = index_movie[movieId]
    uid = index_user[userId]
    movie_user_matrix[mid,uid]=ratings.ix[i,2]



def predict(u,i):
	weighted_sum = 0
	sim_sum = 0
	N = []
	S = []
	J = []
	for p in range(len(movie)):
		if (int(movie_user_matrix[i,u]) | int(movie_user_matrix[p,u])) != 0:
			J.append(p)
	for k in range(len(J)):
		if similarity_matrix[i,J[k]] != -2:
			S.append(similarity_matrix[i,J[k]])
		else:
			similarity_matrix[i,J[k]] = similarity(i,J[k])
			similarity_matrix[J[k],i] = similarity_matrix[i,J[k]]
			S.append(similarity_matrix[i,J[k]])

	for n in range(len(J)):
		if(S[n] > 0):
			N.append(J[n])
	if len(N) >0:
		for n in range(len(N)):
			a = similarity_matrix[i,N[n]]
			b = movie_user_matrix[N[n],u]
			weighted_sum = weighted_sum + (a*b)
			sim_sum = sim_sum+ a
		predicted = round((weighted_sum / sim_sum),1)
	else:
		predicted = 0
	return predicted

def similarity(i,j):
	if similarity_matrix[i,j] != -2:
		sim = similarity_matrix[i,j]
	else:
		numerator = 0
		denominator = 0
		sim = 0
		users = 671
		iusers = np.nonzero(movie_user_matrix[i,:])
		jusers = np.nonzero(movie_user_matrix[j,:])
		X = np.intersect1d(iusers,jusers)
		for p in range(len(X)):
			u = X[p]
			Rbar = sum(movie_user_matrix[:,u])/np.count_nonzero(movie_user_matrix[:,u])
			a = movie_user_matrix[i,u] - Rbar
			b = movie_user_matrix[j,u] - Rbar
			c = (math.sqrt(math.pow(a,2)) * math.sqrt(math.pow(b,2)))
			numerator = numerator + (a*b)
			denominator = denominator + c
			
		if numerator != 0:
			sim = numerator/denominator
	similarity_matrix[i,j] =sim
	similarity_matrix[j,i] =sim
	return sim

similarity_matrix = np.full((len(movie),len(movie)),-2)
l = len(test_file)
results_15 = []
for k in range(l) :
	m = test_file.ix[k,0]
	n = test_file.ix[k,1]
	i= index_movie[n]
	u = index_user[m]
	x = predict(u,i)
	results_15.append(x)
	print(k,x)