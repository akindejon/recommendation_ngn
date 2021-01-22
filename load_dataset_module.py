import csv
import pandas as pd

from zipfile import ZipFile
with ZipFile('data.zip', 'r') as zip:
    zip.extractall()



# list of features to retrive from the dataset
features_to_retrieve = ['acousticness', 'artists', 'danceability', 'energy', 'id', 'liveness',
                            'loudness', 'name', 'popularity', 'speechiness', 'tempo','valence']

class Load_data():
    def ___init___(self):
        pass

    def load_dataset(self):
        """
        This fuction loads the dataset.csv and stores it in a dictionary,
        the dataset column names and its values being used as key-value pair in dictionary
        return:
            a dictionary format of the dataset
        """
        csv_data = pd.read_csv("data.csv", encoding='utf-8')
        csv_data = csv_data.loc[:, features_to_retrieve]
        csv_data['name'] = csv_data['name'].astype('str')
        csv_data['artists'] = csv_data['artists'].astype('str')
        csv_data['artists'] = csv_data['artists'].str[1:-1]
        #csv_data['artists'] = csv_data['artists'].str.replace(",","")
        csv_data['artists'] = csv_data['artists'].str.replace("[","", regex=False)
        csv_data['artists'] = csv_data['artists'].str.replace("]","", regex=False)
        csv_data['artists'] = csv_data['artists'].str.replace("'","")
        return csv_data



    def artist_music_func(self):
        """
        This function returns artist music dataframe and a dictionary that
        contains artists name, music name, and corresponding features
        """
        
        features = ['artists', 'acousticness', 'danceability', 'energy', 'liveness',
                                'loudness', 'popularity', 'speechiness', 'tempo', 'valence']
        data = self.load_dataset()
        artist_music = data[features]
        artist_music['artists'] = artist_music['artists'].astype('category')
        artist_music['artists_cat'] = artist_music["artists"].cat.codes
        artist_music = artist_music.set_index("artists_cat")
        artist_music_dict = artist_music.to_dict()['artists']
        artist_music = artist_music.drop(['artists'], axis=1)
        artist_music = artist_music.groupby(artist_music.index).mean()
        return artist_music, artist_music_dict

    def music_features_func(self):
        """
        This fuction returns  music_features dataset and a  dictionary contains music id, and their respective features.
        """
        features = ['name', 'acousticness', 'danceability', 'energy', 'liveness',
                                'loudness', 'popularity', 'speechiness', 'tempo', 'valence']
        data = self.load_dataset()
        music_features = data[features]
        music_features_dict = music_features.to_dict()['name']
        music_features = music_features.drop(['name'], axis=1)
        return music_features, music_features_dict
    
    def music_for_artist_func(self):
        """
       This fuction returns  music_features dataset and a  dictionary contains music id, and their respective features.

        """
        features = ['name','artists' ,'acousticness', 'danceability', 'energy', 'liveness',
                                'loudness', 'popularity', 'speechiness', 'tempo', 'valence']
        data = self.load_dataset()
        music_for_artist = data[features]
        music_for_artist['artists'] = music_for_artist['artists'].astype('category')
        music_for_artist['artists_cat'] = music_for_artist["artists"].cat.codes
        music_dict = music_for_artist.to_dict()['name']
        music_data_dict = music_for_artist.set_index("artists_cat").to_dict()['artists']
        music_for_artist = music_for_artist.drop(['name', 'artists'], axis=1)
        return music_for_artist, music_dict, music_data_dict
