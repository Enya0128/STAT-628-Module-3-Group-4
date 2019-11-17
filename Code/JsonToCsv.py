import os
import json
import pandas as pd

os.getcwd()
os.chdir('C:\\MyStuff\\Files\\UW\\STAT628\Module3')

### Convert to csv
### Business

with open('Data\\json\\business.json', encoding = 'utf-8') as f:
    json_str = f.read()
    json_list = json_str.split('\n')
    del json_list[-1]

del json_str
print('Num of samples: '+str(len(json_list)))
dict_business = {"business_id":[], 
                 "name":[],
                 "address":[], 
                 "city":[], 
                 "postal_code":[],
                 "latitude":[],
                 "longitude":[], 
                 "stars":[],
                 "review_count":[],
                 "is_open":[],
                 "attributes":[],
                 "categories":[],
                 "hours":[]}

for item in json_list:
    json_bus_line = json.loads(item)
    dict_business["business_id"].append(json_bus_line["business_id"])
    dict_business["name"].append(json_bus_line["name"])
    dict_business["address"].append(json_bus_line["address"])
    dict_business["city"].append(json_bus_line["city"])
    dict_business["postal_code"].append(json_bus_line["postal_code"])
    dict_business["latitude"].append(json_bus_line["latitude"])
    dict_business["longitude"].append(json_bus_line["longitude"])
    dict_business["stars"].append(json_bus_line["stars"])
    dict_business["review_count"].append(json_bus_line["review_count"])
    dict_business["is_open"].append(json_bus_line["is_open"])
    dict_business["attributes"].append(str(json_bus_line["attributes"]))
    dict_business["categories"].append(json_bus_line["categories"])
    dict_business["hours"].append(str(json_bus_line["hours"]))

del json_list
df_business = pd.DataFrame(dict_business)
del dict_business
df_business.to_csv('Data\\csv\\business.csv')
del df_business

### reviews

with open('Data\\json\\review.json', encoding = 'utf-8') as f:
    json_str = f.read()
    json_list = json_str.split('\n')
    del json_list[-1]

del json_str
print('Num of samples: '+str(len(json_list)))
dict_review = {"review_id":[], 
                 "user_id":[],
                 "business_id":[], 
                 "stars":[], 
                 "date":[],
                 "text":[],
                 "useful":[], 
                 "funny":[],
                 "cool":[]}

for item in json_list:
    json_review_line = json.loads(item)
    dict_review["review_id"].append(json_review_line["review_id"])
    dict_review["user_id"].append(json_review_line["user_id"])
    dict_review["business_id"].append(json_review_line["business_id"])
    dict_review["stars"].append(json_review_line["stars"])
    dict_review["date"].append(json_review_line["date"])
    dict_review["text"].append(json_review_line["text"])
    dict_review["useful"].append(json_review_line["useful"])
    dict_review["funny"].append(json_review_line["funny"])
    dict_review["cool"].append(json_review_line["cool"])

del json_list
df_review = pd.DataFrame(dict_review)
del dict_review
df_review.to_csv('Data\\csv\\review.csv')
del df_review

### tip

with open('Data\\json\\tip.json', encoding = 'utf-8') as f:
    json_str = f.read()
    json_list = json_str.split('\n')
    del json_list[-1]

del json_str
print('Num of samples: '+str(len(json_list)))
dict_tip = {"text":[], 
            "date":[],
            "compliment_count":[], 
            "business_id":[], 
            "user_id":[]}

for item in json_list:
    json_tip_line = json.loads(item)
    dict_tip["text"].append(json_tip_line["text"])
    dict_tip["date"].append(json_tip_line["date"])
    dict_tip["compliment_count"].append(json_tip_line["compliment_count"])
    dict_tip["business_id"].append(json_tip_line["business_id"])
    dict_tip["user_id"].append(json_tip_line["user_id"])

del json_tip_line
del json_list
df_tip = pd.DataFrame(dict_tip)
del dict_tip
df_tip.to_csv('Data\\csv\\tip.csv')
del df_tip

### merge data

df_business = pd.read_csv('Data\\csv\\business.csv')
df_review = pd.read_csv('Data\\csv\\review.csv')

categories = []
for i in range(df_business.shape[0]):
    cate_line = df_business.iloc[i,12]
    if isinstance(cate_line, str):
        cate_line = cate_line.replace(', ', ',')
        cate_line = cate_line.split(',')
        for cate in cate_line:
            if cate not in categories:
                categories.append(cate)

categories_count = []
for i in range(len(categories)):
    categories_count.append(0)

df_review_2 = pd.merge(df_review[['review_id', 'business_id']], 
                       df_business[['business_id', 'categories']],
                       on = ['business_id'], how = 'left')
del df_business
del df_review
for i in range(df_review_2.shape[0]):
    cate_line = df_review_2.iloc[i,2]
    if isinstance(cate_line, str):
        cate_line = cate_line.replace(', ', ',')
        cate_line = cate_line.split(',')
        for cate in cate_line:
            index = categories.index(cate)
            categories_count[index] += 1

df_cate_count = pd.DataFrame({"category":categories, 
                              "review count": categories_count})
df_cate_count.sort_values("review count", inplace = True, ascending = False)
df_cate_count.head()
df_cate_count.to_csv('Data\\csv\\category_count.csv', index=False)

### extract data

# mexican info

mexican_id = []
df_business = pd.read_csv('Data\\csv\\business.csv')
del df_business['Unnamed: 0']
df_mexican = pd.DataFrame(columns = ['business_id', 'name', 'city', 
                                    'latitude', 'longitude', 'star',
                                    'review_count', 'attribute'])
for i in range(df_business.shape[0]):
    cate_line = df_business.iloc[i,11]
    if isinstance(cate_line, str):
        cate_line = cate_line.replace(', ', ',')
        cate_line = cate_line.split(',')
        if 'Mexican' in cate_line:
            insert_row = df_business.iloc[i, [0, 1, 3, 5, 6, 7, 8, 10]]
            df_mexican.loc[df_mexican.shape[0]] = insert_row.to_list()
            mexican_id.append(df_business.iloc[i, 0])            

df_mexican.to_csv('Data\\csv\\mexican_info.csv', index = False)


df_mexican = pd.read_csv('Data\\csv\\mexican_info.csv')
for i in range(df_mexican.shape[0]):
    attr_str = df_mexican.iloc[i, 7]
    attrs = []
    print(i)
    if isinstance(attr_str, str):
        if attr_str == 'None':
            df_mexican.iloc[i, 7] = ''
        else:
            attr_dict = eval(attr_str)
            keys = list(attr_dict.keys())
            for key in keys:
                if attr_dict[key] == 'True':
                    attrs.append(key)
            df_mexican.iloc[i, 7] = ','.join(attrs)
    else:
        df_mexican.iloc[i, 7] = ''


df_mexican.to_csv('Data\\csv\\mexican_info.csv', index = False)
del df_mexican




























