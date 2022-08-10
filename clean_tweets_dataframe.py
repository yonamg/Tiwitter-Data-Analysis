from nltk.corpus import stopwords, words
from nltk.tokenize import word_tokenize
import pandas as pd
import re

class Clean_Tweets:
    """
    The PEP8 Standard AMAZING!!!
    """
    def __init__(self, df:pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')
        
    def drop_unwanted_column(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove rows that has column names. This error originated from
        the data collection stage.  
        """
        unwanted_rows = df[df['retweet_count'] == 'retweet_count' ].index
        self.df.drop(unwanted_rows , inplace=True)
        self.df = self.df[self.df['polarity'] != 'polarity']
        
        return self.df
    def drop_duplicate(self, df:pd.DataFrame)->pd.DataFrame:
        """
        drop duplicate rows
        """
        no_duplicate = self.df.drop_duplicates(subset="original_text")
        df = no_duplicate
        
        return df
    def convert_to_datetime(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert column to datetime
        """
        self.df['created_at'] = pd.to_datetime(self.df['created_at'], errors='coerce')
        return self.df

        df = df[df['created_at'] >= '2020-12-31' ]
        
        return df
    
    def convert_to_numbers(self, df:pd.DataFrame)->pd.DataFrame:
        """
        convert columns like polarity, subjectivity, retweet_count
        favorite_count etc to numbers
        """

        df['polarity'] = pd.to_numeric(df['polarity'], errors='coerce')
        df['subjectivity'] = pd.to_numeric(df['subjectivity'], errors='coerce')
        df['retweet_count'] = pd.to_numeric(df['retweet_count'], errors='coerce')
        df['favorite_count'] = pd.to_numeric(df['favorite_count'], errors='coerce')
        df["friends_count"] = pd.to_numeric(df["friends_count"], errors='coerce')
        df["followers_count"] = pd.to_numeric(df["followers_count"], errors='coerce')
        return df
    
    def remove_non_english_tweets(self, df:pd.DataFrame)->pd.DataFrame:
        """
        remove non english tweets from lang
        """
        
        df = df.drop(self.df[self.df['lang'] != 'en'].index)
        
        return df

    def tweet_preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        import numpy as np
        import string
        from nltk.corpus import stopwords
        from cleantext import clean

        self.df['original_text'] = self.df['original_text'].str.lower()
        self.df['original_text'] = self.df['original_text'].str.replace('(@\w+.*?)', "")
        self.df['original_text'] = self.df['original_text'].astype(str).apply(lambda x: x.encode('latin-1', 'ignore').decode('latin-1'))
        self.df['original_text'] = self.df['original_text'].str.replace('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ')
        self.df['original_text'] = self.df['original_text'].apply(lambda x: ''.join([i for i in x if i not in string.punctuation]))
        english_stopwords = stopwords.words('english')
        user_stop_words = ['2022', '2', 'rt', 'much', 'next', 'cant', 'wont', 'hadnt',
                           'havent', 'hasnt', 'isnt', 'shouldnt', 'couldnt', 'wasnt', 'werent',
                           'mustnt', 'amp', '10', '100', 'pm', '’', '...', '..', '.', '.....', '....', 'been…', 'one',
                           'two',
                           'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'aht',
                           've']
        stop = english_stopwords + user_stop_words
        self.df['original_text'] = self.df['original_text'].apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))
        self.df.drop(self.df[self.df['original_text'] == ''].index, inplace=True)

        return self.df

    if __name__ == "__main__":
        cleaned_df = pd.read_csv("data/processed_tweet_data.csv")
        clean_tweets = Clean_Tweets(cleaned_df)
        cleaned_df = clean_tweets.drop_duplicate(cleaned_df)
        cleaned_df = clean_tweets.remove_non_english_tweets(cleaned_df)
        cleaned_df = clean_tweets.convert_to_datetime(cleaned_df)
        cleaned_df = clean_tweets.drop_unwanted_column(cleaned_df)
        cleaned_df = clean_tweets.convert_to_numbers(cleaned_df)
        cleaned_df = clean_tweets.tweet_preprocessing(cleaned_df)

        print(cleaned_df['polarity'][0:5])

        cleaned_df.to_csv('data/clean_processed_tweet_data.csv')