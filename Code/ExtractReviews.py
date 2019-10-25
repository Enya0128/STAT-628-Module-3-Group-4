import os
import pandas as pd

os.getcwd()
os.chdir('C:\\MyStuff\\Files\\UW\\STAT628\Module3')

df_business = pd.read_csv('Data\\csv\\business.csv')
df_review = pd.read_csv('Data\\csv\\review.csv')
df_mexican_info = pd.read_csv('Data\\csv\\mexican_info.csv')
df_mexican_info['mex'] =  1 # 加一列做标识

df_review_3 = pd.merge(df_review[['review_id', 'user_id', 'business_id', 
                                       'stars', 'date', 'text', 'useful', 
                                       'funny', 'cool']],
                       df_mexican_info[['business_id', 'mex']],
                       on = 'business_id', how = 'left')
del df_review
df_mexican_review = df_review_3[df_review_3['mex']==1]
del df_review_3
del df_mexican_review['mex']
df_mexican_review.to_csv('Data\\csv\\mexican_review.csv', index = False)
del df_mexican_review


df_tip = pd.read_csv('Data\\csv\\tip.csv')
del df_tip['Unnamed: 0']
df_tip_3 = pd.merge(df_tip, df_mexican_info[['business_id', 'mex']], on = 'business_id', how = 'left')
del df_tip
df_mexican_tip = df_tip_3[df_tip_3['mex']==1]
del df_tip_3
del df_mexican_tip['mex']
df_mexican_tip.to_csv('Data\\csv\\mexican_tip.csv', index = False)
del df_mexican_tip

del df_business
del item

df_mexican_info = pd.read_csv('Data\\csv\\mexican_info.csv')
df_mexican_review = pd.read_csv('Data\\csv\\mexican_review.csv')
df_mexican_tip = pd.read_csv('Data\\csv\\mexican_tip.csv')

