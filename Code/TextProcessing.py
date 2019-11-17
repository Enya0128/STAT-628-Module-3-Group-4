import pandas as pd
import os
import re
import nltk

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

os.chdir('C:\\MyStuff\\Files\\UW\\STAT628\Module3')

df_review = pd.read_csv('Data\\csv\\mexican_review.csv')
# df_mexican_tip =pd.read_csv('Data\\csv\\mexican_tip.csv')
# df_mexican_info = pd.read_csv('Data\\csv\\mexican_info.csv')

df_review = df_review.dropna()
df_review.shape
df_review.head()

# Text Processing Function

def text_processing(text):
    
    text = text.lower()
    text = re.sub(r'[^a-z0-9]', ' ', text)
    text = word_tokenize(text)
    text = [w for w in text if w not in stopwords.words('english')]
    text = [WordNetLemmatizer().lemmatize(w, pos = 'v') for w in text]
    text = ' '.join(text)
    
    return text

dict_review_p = {'index':[],
                 'review_id':[],
                 'user_id':[],
                 'business_id':[],
                 'stars':[],
                 'date':[],
                 'text':[],
                 'useful':[],
                 'funny':[],
                 'cool':[]}

for i in range(df_review.shape[0]):
    dict_review_p['index'].append(df_review.loc[i, 'index'])
    dict_review_p['review_id'].append(df_review.loc[i, 'review_id'])
    dict_review_p['user_id'].append(df_review.loc[i, 'user_id'])
    dict_review_p['business_id'].append(df_review.loc[i, 'business_id'])
    dict_review_p['stars'].append(df_review.loc[i, 'stars'])
    dict_review_p['date'].append(df_review.loc[i, 'date'])
    dict_review_p['text'].append(text_processing(df_review.loc[i, 'text']))
    dict_review_p['useful'].append(df_review.loc[i, 'useful'])
    dict_review_p['funny'].append(df_review.loc[i, 'funny'])
    dict_review_p['cool'].append(df_review.loc[i, 'cool'])
    
df_review_p = pd.DataFrame(dict_review_p)
df_review_p.to_csv('Data\\csv\\mexican_review_p.csv', index = False)
del df_review_p
del df_review

df_review_p = pd.read_csv('Data\\csv\\mexican_review_p.csv')
df_review_p.shape
df_review_p = df_review_p.dropna()
df_review_p.shape
df_review_p.to_csv('Data\\csv\\mexican_review_p.csv', index = False)

df_review_p = pd.read_csv('Data\\csv\\mexican_review_p.csv')
df_review_p.tail()