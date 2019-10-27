# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 00:38:30 2019

@author: yong
"""

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
os.chdir('E:\\downloadslib\\628Module3')
os.listdir()


import nltk, urllib.request
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
from string import punctuation
from collections import Counter
mexican_info = pd.read_csv("mexican_info.csv") 
mexican_review = pd.read_csv("mexican_review.csv") 
mexican_tip = pd.read_csv("mexican_tip.csv") 
mexican_review_p = pd.read_csv("mexican_review_p.csv") 

def draw_wordcloud(texts,stop_words,path_img,a=50):
    Freq_dist={}
    for onereview in texts:
        word_tokens = word_tokenize(onereview.lower()) 
        filtered_sentence = [w for w in word_tokens if not w in stop_words]  
        Freq_dist_add=nltk.FreqDist(filtered_sentence)
        Freq_dist=dict(Counter(Freq_dist)+Counter(Freq_dist_add))
    
    result=dict(list(sorted(Freq_dist.items(),key=lambda x:x[1],reverse=1))[:a])
    path_img = path_img#"C://Users/Administrator/Desktop/timg.jpg"
    background_image = np.array(Image.open(path_img))
    image_colors = ImageColorGenerator(background_image)
    wordcloud = WordCloud(
            background_color='white', #设置背景为白色，默认为黑色
            width=2000, #设置图片的宽度
            height=2000, #设置图片的高度
            margin=0, #设置图片的边缘
            mask=background_image
            ).generate_from_frequencies(result)
    plt.figure(figsize=(15,10),facecolor='k')
    plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
    plt.axis("off")
    plt.show()

stop_words = set(stopwords.words('english')+list(punctuation)+['want','include','great','good','think','nothing','use',\
                 'family','people','one','many','50','go','make','years','add','like','see','non','come',\
                 'take','pull','well','look','get','ask','even','...',"''",'``','=/','also','live',\
                 'much','something','2','tell','back','say','58','3','9','40','around'])
draw_wordcloud(mexican_review_p[mexican_review.stars==1].text.head(),stop_words,'1star.jpg',500)
draw_wordcloud(mexican_review_p[mexican_review.stars==2].text.head(),stop_words,'2star.png',500)
draw_wordcloud(mexican_review_p[mexican_review.stars==3].text.head(),stop_words,'3star.jpg',500)
draw_wordcloud(mexican_review_p[mexican_review.stars==4].text.head(),stop_words,'4star.jpg',500)
draw_wordcloud(mexican_review_p[mexican_review.stars==5].text.head(),stop_words,'5star.jpg',500)











