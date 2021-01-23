import numpy as np #if not install use "pip install numpy"
import pandas as pd
from sklearn.metrics.pairwise import pairwise_distances
from load_dataset_module import Load_data
import streamlit as st
import warnings
warnings.simplefilter(action='ignore')

#Created the load data Class to collect data 
ld =  Load_data()
class Similarity_comp():
    def ___init___(self):
        pass

    def _compute_similar(self, types ,iden , similarity_func, n):
        """
        type : type of dataframe needed for method
        similarity_func : Similarity algorithm to use
        iden: unique identifier for the Music or Artist. 
        n: number of most similar values to return 

        This method take an id and the a similarity metric
        then carries out mathematical computation using the numerical values of the ids
        using the similarity metric pass and return the top n result, .
        """
        #we use the different type of methods to determine 
        #the data we would collect from the load_dataset Class
        if types == "music":
            data, data_dict = ld.music_features_func()
           
        elif types == "artist":
            data, data_dict = ld.artist_music_func()
            
        elif types == "music for artist":
            data, data_dict, music_data_dict = ld.music_for_artist_func()
        
        if types == "music":
            first = data[data.index == iden]
            first = first.values

        elif types == "artist" :
            first = data[data.index == iden]
            first = first.groupby(by=first.index).mean()
           
            first = first.values
        elif types == "music for artist":
            data = data[data["artists_cat"] == iden]
            first = data.groupby(by="artists_cat").mean()
            data = data.drop(["artists_cat"], axis=1)
            first = first.values
        
        second = data.values
     
        arr = pairwise_distances(first, second, metric=similarity_func)
        arr = arr.reshape(-1, 1)
        preds = pd.DataFrame(arr,index=data.index, columns=["similarity"])
        if types == "artist":
            preds["artist"] = preds.index.map(data_dict)
            preds = preds.reset_index(drop=True)
            preds = preds[1:]
        if types == "music for artist" or types == "music" :
            preds["music"] = preds.index.map(data_dict)
            preds = preds.reset_index(drop=True)
        if types == "music for artist":
            preds["music"] = preds.index.map(data_dict)
            data_dict = music_data_dict
            preds = preds.reset_index(drop=True)
             

        preds = preds.sort_values(by="similarity")
        preds= preds.reset_index(drop=True)
        return preds.head(n)


    def compute_similar_music(self, music_id,  similarity_func, n):
        """
        music_id : the song id
        similarity_func =the similarity function 
        n : number of similar values to return 

        this method takes the music name, the similarity_metrics and number of similar 
        music to return. This values are then feed to the compute similar method and return result gotten from 
        the compute_similar method. 
        """

        return self._compute_similar(types="music",iden=music_id, similarity_func=similarity_func, n=n)
    
    def compute_similar_artist(self, artist_id, similarity_func, n):
        """
        artist_id : the artist id
        similarity_func =the similarity function 
        n : number of similar values to return 

        this method takes the artist name, the similarity_metrics and number of similar 
        music to return. This values are then feed to the compute similar method and return result gotten from 
        the compute_similar method. 
        """
        return self._compute_similar(types="artist", iden=artist_id, similarity_func=similarity_func, n=n)

    def compute_similar_music_for_artist(self, artist_id, similarity_func,n):
        """
        artist_id : the artist id
        similarity_func =the similarity function 
        n : number of similar values to return 

        this method takes the artist name, the similarity_metrics and number of similar 
        music to return. This values are then feed to the compute similar method and return result gotten from 
        the compute_similar method.
        
        """
        return self._compute_similar(types="music for artist", iden=artist_id, similarity_func=similarity_func, n=n)

def main(query1, query2, query3, query4):
    """
    query1 : This represent the kind of service you want
    query2 : This represent the id of the music or artist 
    query3 : This represent the kind of similarity metrics you want to use
    query4 : This represent the number of values to return 

    This is the main function and it takes different values and return the result as a dataframe 
    """

    query4 = int(query4)
    query2 = int(query2)
    simil = Similarity_comp()
    similar_dict = {1: "euclidean", 2 :"cosine", 3 :"correlation", 4 :"hamming",5 : "manhattan"}
    if query1 == 1:
        return simil.compute_similar_music(music_id=query2, similarity_func=similar_dict[query3], n=query4)
    if query1 == 2:
        return simil.compute_similar_artist(artist_id=query2, similarity_func=similar_dict[query3], n=query4)
    if query1 == 3:
        return simil.compute_similar_music_for_artist(artist_id=query2, similarity_func=similar_dict[query3], n=query4)

        
    


                
if __name__ == "__main__":
    st.title("Music Recommendation Engine")
    st.subheader("This application helps you find the most similar music or artist to an already selected music or artist")
    query1 = st.number_input("We offer three different services please choose?\n\
                    Enter 1 for finding top similar music\n\
                    Enter 2 for finding top similar artist\n\
                    Enter 3 for finding top similar music based on a particular artist\n",
                     min_value= 1, max_value= 3)
    if query1 == 1:
        query2 = st.number_input("Enter the music id: ", min_value= 1, max_value=150000)
    elif query1 == 2 or query1 == 3:
        query2 = st.number_input("Enter the artist id: ", min_value = 1, max_value= 30000)
    query3 = st.number_input("What similarity metric should we use?\n\
                          Enter 1 for euclidean\n\
                              Enter 2 for cosine\n\
                                  Enter 3 for correlation\n\
                                      Enter 4 for jaccard coefficient\n\
                                          Enter 5 for manhattan\n",
                    min_value= 1, max_value=5)
    if query1 == 1:
        query4 = st.number_input("How many similar music should we return ", min_value= 1, max_value=1000)
    elif query1 == 2:
        query4 = st.number_input("How many similar artist should we return ", min_value= 1, max_value=1000)
    elif query1 == 3:
        query4 = st.number_input(f"How many similar music should we return", min_value=1, max_value=1000)
    data  = main(query1, query2, query3, query4)
    similar_dict = {1: "music", 2 :"artist", 3 :"music for artist"}
    st.write(f"Top {query4} number of similar {similar_dict[query1]} are\n")
    st.dataframe(data)
