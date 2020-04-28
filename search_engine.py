import pandas as pd
import sys
import argparse
from tkinter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default=None, required = True, help='input file to search')
    parser.add_argument('--content', type=str, default=None, required = True, help='content used to search')
    options = parser.parse_args()
    return options


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

def main(keyword, content, input_file):


    dataframe = load_data(input_file)

    search_query_weights, tfidf_weights_matrix = tf_idf(keyword, dataframe, content)

    similarity_list = cos_similarity(search_query_weights, tfidf_weights_matrix)

    movies_list = most_similar(similarity_list)
    result = []
    for i in movies_list:
        #print(dataframe['original_title'][i])
        result.append(dataframe['original_title'][i])
    return result

def searchUrl(keyword, content, input_file):


    dataframe = load_data(input_file)

    search_query_weights, tfidf_weights_matrix = tf_idf(keyword, dataframe, content)

    similarity_list = cos_similarity(search_query_weights, tfidf_weights_matrix)

    movies_list = most_similar(similarity_list)
    result = []
    for i in movies_list:
        #print(dataframe['homepage'][i])
        result.append(dataframe['homepage'][i])
    return result

def get_me():
    global current
    entry_value = entry.get()
    result = main(entry_value, search_name, input_f)
    url = searchUrl(entry_value, search_name, input_f)
    for i in range(3):
        answer_value = result[i] + '\n'
        if url[i] == None:
            url_res = 'No URL \n'
        else:
            url_res = str(url[i]) + '\n'
        answer.insert(INSERT, answer_value)
        answer.insert(INSERT, url_res)



if __name__ == "__main__":
    options = parse_argument()
    search_name = options.content
    input_f = options.input

    root = Tk()
    topframe = Frame(root)
    topframe.pack(side = TOP)
    entry = Entry(topframe)
    entry.pack()
    
    button = Button(topframe, text='search', command=get_me)
    button.pack()
    bottomframe = Frame(root)
    scroll = Scrollbar(bottomframe)
    scroll.pack(side=RIGHT, fill=Y)
    answer = Text(bottomframe, width=30, height=10, yscrollcommand = scroll.set)
    scroll.config(command=answer.yview)
    answer.pack()
    bottomframe.pack()
    root.mainloop()





