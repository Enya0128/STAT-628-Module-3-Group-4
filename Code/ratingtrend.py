# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 16:35:17 2019

@author: yong
"""


########################################### Rating Rank
import datetime
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
os.chdir('E:\\downloadslib\\628Module3')
os.listdir()


mexican_info = pd.read_csv("mexican_info.csv") 
mexican_review = pd.read_csv("mexican_review.csv") 


###################### average rating for the center date

def sliding_window(x,targetdt,width=40):
   xt= (datetime.datetime.strptime(x[0], "%Y-%m-%d %H:%M:%S")).date() 
   return((xt <= targetdt + datetime.timedelta(days=width)) & (xt >= targetdt - datetime.timedelta(days=width)))


def movingaverage(centerdate,target_ratings,width=40):
    targetdt= (datetime.datetime.strptime(centerdate, "%Y-%m-%d")).date() 
    isinwindow=target_ratings.apply(lambda x : sliding_window(x,width=width,targetdt=targetdt),axis=1)
    r=target_ratings.loc[isinwindow,'stars'].mean()
    if np.isnan(r):
           isinwindow=target_ratings.apply(lambda x : sliding_window(x,width=width+10,targetdt=targetdt),axis=1)
           r=target_ratings.loc[isinwindow,'stars'].mean()
    if np.isnan(r):
           isinwindow=target_ratings.apply(lambda x : sliding_window(x,width=width+15,targetdt=targetdt),axis=1)
           r=target_ratings.loc[isinwindow,'stars'].mean()    
       
    return(r)

# usage : movingaverage('2015-10-10')    



###########datelist for a city

city_id=list(mexican_info[mexican_info.city=='Mesa'].business_id)#191 businesses

#isincity=mexican_review.business_id.apply(lambda x : 1 if x in city_id else 0)

city_ratings=mexican_review.loc[mexican_review['business_id'].isin(city_id),['date','stars']]####144 reviews
start_date=(datetime.datetime.strptime(city_ratings.date.min(), "%Y-%m-%d %H:%M:%S")).date()#######first review in the city
end_date=(datetime.datetime.strptime(city_ratings.date.max(), "%Y-%m-%d %H:%M:%S")).date()######last review in the city
date_list = [(start_date + datetime.timedelta(days=x)).strftime('%Y-%m-%d') for x in range(0,(end_date-start_date).days+60,60)]####measure every 60 days


###########caculate ratings for each business
#target_id=list(mexican_info[mexican_info.city=='Mesa'].business_id)[1]#191 businesses
#target_ratings=mexican_review.loc[mexican_review.business_id==target_id,['date','stars']]####144 reviews
#target_record=[]
#for centerdate in date_list :
#    target_record.append(movingaverage(centerdate=centerdate,target_ratings=target_ratings))
#target_record
#plt.plot(date_list,target_record, 'ro-', color='#4169E1', alpha=0.8, label='')


#############Chop the nan's in the beginning


##########################Rating Records for all business
#Rating_Records= pd.DataFrame(columns=['business_id']+date_list)
#
#for target_id in list(mexican_info[mexican_info.city=='Mesa'].business_id)[10:14] :
#    target_ratings=mexican_review.loc[mexican_review.business_id==target_id,['date','stars']]
#    target_records=[]
#    for centerdate in date_list :
#        target_records.append(movingaverage(centerdate=centerdate,target_ratings=target_ratings))
#    Rating_Records=np.concatenate((Rating_Records.values,pd.DataFrame([target_id]+target_records).T.values),axis=0)          
#         
#         
#np.concatenate( (df1.values, df2.values), axis=0 ) 
#df.loc['new_raw'] = '3'
Rating_Records= []

for target_id in list(mexican_info[mexican_info.city=='Mesa'].business_id) :
    target_ratings=mexican_review.loc[mexican_review.business_id==target_id,['date','stars']]
    target_records=[]
    for centerdate in date_list :
        target_records.append(movingaverage(centerdate=centerdate,target_ratings=target_ratings))
    Rating_Records.append([target_id]+target_records)       
         
  
Rating_Records=np.array(Rating_Records)

##########################Caculate percentile for business
from scipy import stats
#Rating_Records=np.load('Rating_Records.npy')

def findrank(col,business_id): 
    a=col[np.argwhere(Rating_Records[:,0]==business_id)]
    if str(a)=="[['nan']]":
        return(np.nan)
    a=float(a)
    col=[float(x) for x in col if x!='nan']
    if len(col)<=1:
        return(np.nan)
    return(stats.percentileofscore(col, a,kind='weak'))

Percentile_Score= []
for business_id in list(Rating_Records[:,0]) :
    Percentile_Score.append(np.apply_along_axis(findrank,0,Rating_Records[:,1:],business_id=business_id))                
Percentile_Score=np.array(Percentile_Score)


Result=np.row_stack((np.array(date_list),Percentile_Score))
pd.DataFrame(Result,index=['date']+list(Rating_Records[:,0])).to_csv("Mesa_trend.csv",index=True,header=False)

plotarg=np.argmax(np.apply_along_axis(lambda x : sum(~np.isnan(x)),1,Percentile_Score))   
plt.figure(figsize=(40,10))
plt.xticks(rotation=270)      
plt.plot(date_list,Percentile_Score[plotarg,:], 'ro-', color='#4169E1', alpha=0.8, label='')
plt.show()



#############################Output

cityname='Las Vegas'

city_id=list(mexican_info[mexican_info.city==cityname].business_id)#191 businesses
city_ratings=mexican_review.loc[mexican_review['business_id'].isin(city_id),['date','stars']]####144 reviews
start_date=(datetime.datetime.strptime(city_ratings.date.min(), "%Y-%m-%d %H:%M:%S")).date()#######first review in the city
end_date=(datetime.datetime.strptime(city_ratings.date.max(), "%Y-%m-%d %H:%M:%S")).date()######last review in the city
date_list = [(start_date + datetime.timedelta(days=x)).strftime('%Y-%m-%d') for x in range(0,(end_date-start_date).days+60,60)]####measure every 60 days


Rating_Records= []
for target_id in list(mexican_info[mexican_info.city==cityname].business_id) :
    target_ratings=mexican_review.loc[mexican_review.business_id==target_id,['date','stars']]
    target_records=[]
    for centerdate in date_list :
        target_records.append(movingaverage(centerdate=centerdate,target_ratings=target_ratings))
    Rating_Records.append([target_id]+target_records)                
Rating_Records=np.array(Rating_Records)


Percentile_Score= []
for business_id in list(Rating_Records[:,0]) :
    Percentile_Score.append(np.apply_along_axis(findrank,0,Rating_Records[:,1:],business_id=business_id))                
Percentile_Score=np.array(Percentile_Score)


Result=np.row_stack((np.array(date_list),Percentile_Score))
pd.DataFrame(Result,index=['date']+list(Rating_Records[:,0])).to_csv(cityname+"_trend.csv",index=True,header=False)


plotarg=np.argmax(np.apply_along_axis(lambda x : sum(~np.isnan(x)),1,Percentile_Score))   
plt.figure(figsize=(40,10))
plt.xticks(rotation=270)      
plt.plot(date_list,Percentile_Score[plotarg,:], 'ro-', color='#4169E1', alpha=0.8, label='')
plt.show()

###############################Point out not reliable ones

def movingcount(centerdate,target_ratings,width=40):
    targetdt= (datetime.datetime.strptime(centerdate, "%Y-%m-%d")).date() 
    isinwindow=target_ratings.apply(lambda x : sliding_window(x,width=width,targetdt=targetdt),axis=1)
    r=target_ratings.loc[isinwindow,'stars'].count()
    if r==0:
           isinwindow=target_ratings.apply(lambda x : sliding_window(x,width=width+10,targetdt=targetdt),axis=1)
           r=target_ratings.loc[isinwindow,'stars'].count()
    if r==0:
           isinwindow=target_ratings.apply(lambda x : sliding_window(x,width=width+15,targetdt=targetdt),axis=1)
           r=target_ratings.loc[isinwindow,'stars'].count()    
    return(r)




for cityname in ['Las Vegas','Phoenix','Scottsdale','Toronto','Charlotte','Mesa','Henderson','Tempe','Pittsburgh','Chandler']:
    city_id=list(mexican_info[mexican_info.city==cityname].business_id)#191 businesses
    city_ratings=mexican_review.loc[mexican_review['business_id'].isin(city_id),['date','stars']]####144 reviews
    start_date=(datetime.datetime.strptime(city_ratings.date.min(), "%Y-%m-%d %H:%M:%S")).date()#######first review in the city
    end_date=(datetime.datetime.strptime(city_ratings.date.max(), "%Y-%m-%d %H:%M:%S")).date()######last review in the city
    date_list = [(start_date + datetime.timedelta(days=x)).strftime('%Y-%m-%d') for x in range(0,(end_date-start_date).days+60,60)]####measure every 60 days
    Number_of_Reviews = []
    for target_id in list(mexican_info[mexican_info.city==cityname].business_id) :
        target_ratings=mexican_review.loc[mexican_review.business_id==target_id,['date','stars']]
        target_records = []
        for centerdate in date_list :
            target_records.append(movingcount(centerdate=centerdate,target_ratings=target_ratings))
        Number_of_Reviews.append([target_id]+target_records)                
    Number_of_Reviews=np.array(Number_of_Reviews)
    pd.DataFrame(Number_of_Reviews).to_csv(cityname+"_count.csv",index=False,header=False)
