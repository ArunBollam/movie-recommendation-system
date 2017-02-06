def predict(u,i):
	X = [] #list of nearest neighbor ratings
	i_users = [] #list of users who rated the movie i
	a = [] #list of the nearest neigbour keys
	for k in range(671):
		if user_movie_matrix[k,i] != 0: #filter the users who rated the movie
			i_users.append(k)
	dist_list = []  #dictionary to save the rated usersid and their distance from
	for p in i_users:
		dist_list.append([p ,distance_matrix[u,p]])
	dist_list.sort(key = lambda row: row[1:], reverse=False)
	
	if len(dist_list)< 5 :
		k = len(dist_list)
	else:
		k =5
	
	
	for b in range(k):
		c =dist_list[b][0]
		X.append(user_movie_matrix[c,i])
		
	predicted = round((sum(X)/k),1)
	return predicted
results_knn_5 = []	
test_file = pd.read_csv('ratings_test_10_v2.csv',names = ['userId','movieId','rating','timestamp'])
l = len(test_file)
for k in range(l):
	user = test_file.ix[k,0]
	movie = test_file.ix[k,1]
	u = index_user[user]
	i = index_movie[movie]
	x = predict(u,i)
	results_knn_5.append(x)
	print(x)
		
		
