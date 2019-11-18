getwd()
data<- read.csv("~/Desktop/628_module3/mexican_data/mexican_info.csv",na.strings = "")
attribute_m<- as.character(data$attribute)
attribute_split<- strsplit(attribute_m,",")

#============================================================================
#Find all existed attributes

all_attri<- character()
for(i in 1:4618){
  all_attri<- c(all_attri,as.vector(attribute_split[[i]]))
}
all_attri<- as.factor(all_attri)
attri_names<- levels(all_attri) #21 attributes in mexican restaurants


#assign 0:no 1:yes to to all restaurants with their attributes

attri_table<- matrix(rep(0,21*4618),ncol = 21)

for(i in 1:4618){
  attri_i<- as.vector(attribute_split[[i]])
  for(j in 1:length(attri_names)){
    if(attri_names[j]%in%attri_i == TRUE){
      attri_table[i,j]<- 1
    }else{
      attri_table[i,j]<- 0
    }
  }
}

colnames(attri_table)<- attri_names
attri_table[which(is.na(attribute_m)),]<- NA
data_new<- cbind(data,attri_table)
write.csv(data_new,"~/Desktop/628_module3/mexican_data/mexican_attributes.csv")


#================================================================================

#For 10 Cities with most reviews, give each one its significant attributes

City<- as.character(data_new$city)
star<- data_new$star

Find_sign_attri<- function(star,attri_table,city,allcity,attri){
  attri_pval<- numeric()
  city_num<- which(allcity == city)
  n<- length(attri)
  for(i in 1:n){
   anova_i<- anova(lm(star[city_num] ~ attri_table[city_num,i]))
   attri_pval[i]<- anova_i$`Pr(>F)`[1]
  }
  attri_sign<- attri[which(attri_pval<=0.05)]
  return(attri_sign)
}

#Las Vegas,Phoenix,Scottsdale,Toronto,Charlotte,
#Mesa,Henderson,Tempe,Pittsburgh,Chandler

LasVegas_sign<- Find_sign_attri(star,attri_table,"Las Vegas",City,attri_names)
Phoenix_sign<- Find_sign_attri(star,attri_table,"Phoenix",City,attri_names)
Scottsdale_sign<- Find_sign_attri(star,attri_table,"Scottsdale",City,attri_names)
Toronto_sign<- Find_sign_attri(star,attri_table,"Toronto",City,attri_names)
Charlotte_sign<- Find_sign_attri(star,attri_table,"Charlotte",City,attri_names)
Mesa_sign<- Find_sign_attri(star,attri_table,"Mesa",City,attri_names)
Henderson_sign<- Find_sign_attri(star,attri_table,"Henderson",City,attri_names)
Tempe_sign<- Find_sign_attri(star,attri_table,"Tempe",City,attri_names)
Pittsburgh_sign<- Find_sign_attri(star,attri_table,"Pittsburgh",City,attri_names)
Chandler_sign<- Find_sign_attri(star,attri_table,"Chandler",City,attri_names)

LasVegas_o<- LasVegas_sign[-which(LasVegas_sign%in%c("DriveThru","HappyHour")==TRUE)]
Phoenix_o<- Phoenix_sign[-which(Phoenix_sign%in%c("DriveThru")==TRUE)]
Scottsdale_o<- Scottsdale_sign[-which(Scottsdale_sign%in%c("DriveThru","HappyHour")==TRUE)]
Toronto_o<- Toronto_sign
Charlotte_o<- Charlotte_sign[-which(Charlotte_sign%in%c("DriveThru")==TRUE)]
Mesa_o<- Mesa_sign[-which(Mesa_sign%in%c("DriveThru")==TRUE)]
Henderson_o<- Henderson_sign[-which(Henderson_sign%in%c("DriveThru")==TRUE)]
Tempe_o<- Tempe_sign[-which(Tempe_sign%in%c("DriveThru")==TRUE)]
Pittsburgh_o<- Pittsburgh_sign[-which(Pittsburgh_sign%in%c("DriveThru")==TRUE)]
Chandler_o<- Chandler_sign[-which(Chandler_sign%in%c("DriveThru")==TRUE)]

LasVegas<- attribute_split[which(City == 'Las Vegas')]
Phoenix<- attribute_split[which(City == 'Phoenix')]
Scottsdale<- attribute_split[which(City == 'Scottsdale')]
Mesa<- attribute_split[which(City == 'Mesa')]
Henderson<- attribute_split[which(City == 'Henderson')]
Toronto<- attribute_split[which(City == 'Toronto')]
Charlotte<- attribute_split[which(City == 'Charlotte')]
Tempe<- attribute_split[which(City == 'Tempe')]
Pittsburgh<- attribute_split[which(City == 'Pittsburgh')]
Chandler<- attribute_split[which(City == 'Chandler')]

#================================================================================
#Find significant attributes critical to star ratings
#Build regression model using significant attributes

#we will build model: 
#star ~ BikeParking + Caters + DogsAllowed+ DriveThru +HappyHour
#       +HasTV+RestaurantsDelivery+RestaurantsReservations+RestaurantsTableService+RestaurantsTakeOut+WheelchairAccessible

model_attri<- lm(star ~ BikeParking + Caters + DogsAllowed+ 
                   DriveThru +HappyHour+HasTV+
                   RestaurantsDelivery+RestaurantsReservations+
                   RestaurantsTableService+RestaurantsTakeOut+WheelchairAccessible,data = data_new)
summary(model_attri)

model_attri_2<- lm(star ~ Caters + DogsAllowed+ 
                     DriveThru +HappyHour+HasTV+
                     RestaurantsDelivery+
                     RestaurantsTableService+WheelchairAccessible,data = data_new)
summary(model_attri_2)

layout(matrix(1:4,nrow=2))
plot(model_attri_2)

#===============================================================================
#Give advice of attributes by City
#Defined function

Give_Advice<- function(city_attri,city_sign_o){
  n<- length(city_attri)
  advice<- character()
  bad_attri<- c("DriveThru","HappyHour")
  for(i in 1:n){
    if(all(city_sign_o %in% city_attri[[i]])==TRUE &&  any(bad_attri %in% city_attri[[i]])==FALSE){
      advice[i]<- paste("You are excellent with all your attributes!")
    }else if(all(city_sign_o %in% city_attri[[i]])==FALSE &&  any(bad_attri %in% city_attri[[i]])==FALSE){
      good<- paste(city_sign_o[which(city_sign_o %in% city_attri[[i]] ==FALSE)], 
                   sep = "",collapse=", ")
      advice[i]<- paste("To improve your business, you should better have: ",
                        good,".")
    }else if(all(city_sign_o %in% city_attri[[i]])==FALSE &&  any(bad_attri %in% city_attri[[i]])==TRUE){
      good<- paste(city_sign_o[which(city_sign_o %in% city_attri[[i]] ==FALSE)], 
                   sep = "",collapse=",")
      not<- paste(bad_attri[which(bad_attri %in% city_attri[[i]] ==TRUE)], 
                  sep = "",collapse=", ")
      advice[i]<- paste("To improve your business, you should better have: ",
                        good,";","However,you should better NOT have ",not," in your restaurant.")
    }else{
      not<- paste(bad_attri[which(bad_attri %in% city_attri[[i]] ==TRUE)], 
                  sep = "",collapse=",")
      advice[i]<- paste("You are good with your attributes. However, you should better NOT have ",not," in your restaurant.")
    }
  }
  return(advice)
}

#===============================================================================
#Advice for 10 cities

LasVegas_ad<- Give_Advice(LasVegas,LasVegas_o)
Phoenix_ad<- Give_Advice(Phoenix,Phoenix_o)
Scottsdale_ad<- Give_Advice(Scottsdale,Scottsdale_o)
Toronto_ad<- Give_Advice(Toronto,Toronto_o)
Charlotte_ad<- Give_Advice(Charlotte,Charlotte_o)
Mesa_ad<- Give_Advice(Mesa,Mesa_o)
Henderson_ad<- Give_Advice(Henderson,Henderson_o)
Tempe_ad<- Give_Advice(Tempe,Tempe_o)
Pittsburgh_ad<- Give_Advice(Pittsburgh,Pittsburgh_o)
Chandler_ad<- Give_Advice(Chandler,Chandler_o)
others<- attribute_split[City%in%c('Las Vegas','Phoenix','Scottsdale','Mesa','Henderson',
                                   'Toronto','Charlotte','Tempe','Pittsburgh','Chandler')==FALSE]
general_sign_o<- c("BikeParking","Caters","DogsAllowed", 
  "HasTV","RestaurantsDelivery","RestaurantsReservations",
  "RestaurantsTableService","RestaurantsTakeOut","WheelchairAccessible")
others_ad<- Give_Advice(others,general_sign_o)

all_advice<- character()
all_advice[which(City == 'Las Vegas')]<- LasVegas_ad
all_advice[which(City == 'Phoenix')]<- Phoenix_ad
all_advice[which(City == 'Scottsdale')]<- Scottsdale_ad
all_advice[which(City == 'Mesa')]<- Mesa_ad
all_advice[which(City == 'Henderson')]<- Henderson_ad
all_advice[which(City == 'Toronto')]<- Toronto_ad
all_advice[which(City == 'Charlotte')]<- Charlotte_ad
all_advice[which(City == 'Tempe')]<- Tempe_ad
all_advice[which(City == 'Pittsburgh')]<- Pittsburgh_ad
all_advice[which(City == 'Chandler')]<- Chandler_ad
all_advice[City%in%c('Las Vegas','Phoenix','Scottsdale','Mesa','Henderson',
                     'Toronto','Charlotte','Tempe','Pittsburgh','Chandler')==FALSE]<- others_ad

data_advice<- cbind(data,all_advice)
write.csv(data_advice,"~/Desktop/628_module3/mexican_data/mexican_attributes_ad.csv")


