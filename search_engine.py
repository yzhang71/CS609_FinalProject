import pandas as pd
import sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def load_data(path):
	dataframe = pd.read_csv(path)
	return dataframe

def tf_idf(search_keys, dataframe, label):
  
	tfidf_vectorizer = TfidfVectorizer(stop_words='english')
	tfidf_weights_matrix = tfidf_vectorizer.fit_transform(dataframe.loc[:, label].values.astype('U'))
	search_query_weights = tfidf_vectorizer.transform([search_keys])
	
	return search_query_weights, tfidf_weights_matrix

def cos_similarity(search_query_weights, tfidf_weights_matrix):
	
	cosine_distance = cosine_similarity(search_query_weights, tfidf_weights_matrix)
	similarity_list = cosine_distance[0]

	return similarity_list

def most_similar(similarity_list, min_movies=5):
	
	most_similar= []
  
	while min_movies > 0:
		tmp_index = np.argmax(similarity_list)
		most_similar.append(tmp_index)
		similarity_list[tmp_index] = 0
		min_movies -= 1

	return most_similar

def main():
	if len(sys.argv) != 2:
		print("Wrong arguments")
		exit()

	data_base = sys.argv[1]

	dataframe = load_data(data_base)

	search_query_weights, tfidf_weights_matrix = tf_idf("science fiction", dataframe, "overview")

	similarity_list = cos_similarity(search_query_weights, tfidf_weights_matrix)

	movies_list = most_similar(similarity_list)

	for i in movies_list:
		print(dataframe['original_title'][i])

if __name__ == "__main__":
	main()