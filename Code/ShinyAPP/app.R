#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)
library(DT)
library(leaflet)

#load data

data_attri_all<- read.csv("data/mexican_attributes_all.csv")
data_id<- as.character(data_attri_all$business_id)
data_adrs<- as.character(data_attri_all$address)
data_star<-as.numeric(data_attri_all$star)
data_city<- as.character(data_attri_all$city)
data_name<- as.character(data_attri_all$name)
data_ad<- as.character(data_attri_all$all_advice)
data_lat<- as.numeric(data_attri_all$latitude)
data_lon<- as.numeric(data_attri_all$longitude)
data_city_rc<- as.character(data_attri_all$recommendation)
data_city_pos<- as.character(data_attri_all$positive)
data_city_neg<- as.character(data_attri_all$negative)

#Some self-defined function
Drawtrend <- function(business_id,city_name){
  city_trend <- read.csv(paste("data/",city_name,'_trend.csv',sep = ''),header = TRUE)####Set your owen path
  city_count <- read.csv(paste("data/",city_name,'_count.csv',sep = ''),header = FALSE)
  business_id=business_id
  i=which(city_trend[,1]==business_id)  
  xaxislab=gsub('X','',colnames(city_trend)[2:ncol(city_trend)])
  yvalue=unlist(c(city_trend[i,2:ncol(city_trend)]))
  notnarange=which(!is.na(yvalue))######Drop the date when business has not started or already closed
  notnarange=notnarange[c(1,length(notnarange))]
  yvalue=yvalue[c(notnarange[1]:notnarange[2])]
  xaxislab=xaxislab[c(notnarange[1]:notnarange[2])]
  xvalue=1:length(yvalue)
  notna <- which(!is.na(yvalue))
  obscount <- unlist(c(city_count[i,2:ncol(city_count)]))[c(notnarange[1]:notnarange[2])]
  plot(xvalue,yvalue,bty='n',type = 'n',yaxt='n',xaxt='n',ylim = c(0,120),xlab='',ylab='Percentile Score In The City')
  abline(h=c(0,20,40,60,80,100),col='gray')
  if (length(xaxislab)>30){
    for (i in 1:length(xaxislab)){
      if(i%%2==0){xaxislab[i]=NA}  ##########Reduce the dense date labels
    }
  }
  axis(1,at=1:length(yvalue),label=xaxislab,las=3)  
  axis(2,at=c(0,20,40,60,80,100),labels = c(0,20,40,60,80,100))
  lines(xvalue[notna],yvalue[notna],type='b',col='red')
  lines(xvalue,yvalue,type = 'b',col='#00008b')
  text(xvalue[notna],yvalue[notna],obscount[notna],pos=1)
  legend('top',c('Actual Score Based On # Reviews', 'No Reviews Period'),cex=0.7, pch = c(1,NA), lty = c(1,1),col=c('#145b7d','red'),bty='n')
}


##########################      USAGE     ############################
#########################      Drawtrend  ###########################
#####################################################################

get_sentence = function(city, business_id){
  table = read.csv(paste('data/sentence_', city, '.csv', sep=''))
  sen_list = as.character(table$important_sentence[table$business_id==business_id])
  sens = strsplit(sen_list, "\\|")
  sens = sens[[1]]
  return(sens)
}
##########################      USAGE     ############################
#########################      ImportantSent  ###########################
#####################################################################
# Define UI for application that draws a histogram
ui <- fluidPage(
   
   # Application title
   titlePanel("YELP ADVICE"),
   sidebarPanel(
     img(src = "Yelp.jpg", height = 100, width = 250),
    # Input Information
    selectInput("City", "Choose your CITY:", 
                choices = c("Las Vegas","Phoenix","Scottsdale","Toronto","Charlotte",
                            "Mesa","Henderson","Tempe","Pittsburgh","Chandler")), 
     textInput(inputId = "Restaurant_Name",label = "NAME OF RESTAURANT"),
     helpText("NOTE: CLICK your restaurant from the MAP, then GET the ADVICE to you.")
   ),
  
    mainPanel(
      # Map for click
        fluidRow(column(width = 12,
                        leafletOutput('map', height = 550))),
        
        fluidRow(verbatimTextOutput("Click_text")),
        
        h3("RECOMMENDATION FROM CITY"),
        dataTableOutput("pos_neg_city"),
        textOutput("rc_city"),
        
        h3("ATTRIBUTES YOU HAVE"),
        fluidRow(column(width = 12,
          dataTableOutput("view_attri")
        )
        ),

       h3("ADVICE FROM ATTRIBUTES"),
        textOutput("advice"),
       
       h3("TREND OF RATINGS"),
       plotOutput("TrendPlot"),

       h3("NOTICED MESSAGES"),
       dataTableOutput("reviews")
      )
)


# Define server logic required to draw a histogram
server <- function(input, output,session) {
   map <- createLeafletMap(session, 'map')
   session$onFlushed(once=T,function(){
     output$map <- renderLeaflet({
       m <- leaflet() %>%
         addTiles() %>%  # Add default OpenStreetMap map tiles
         addMarkers(lng=data_lon[which(data_city==input$City& data_name==toupper(input$Restaurant_Name))], 
                    lat=data_lat[which(data_city==input$City& data_name==toupper(input$Restaurant_Name))], 
                    popup=data_adrs[which(data_city==input$City& data_name==toupper(input$Restaurant_Name))])
       
     })
     
   })
   observe({
     click<- input$map_marker_click
     if(is.null(click))
       return()
     target_id<- data_id[which(data_lat==click$lat & data_lon == click$lng & data_name==toupper(input$Restaurant_Name))]
     target_num<- which(data_lat==click$lat & data_lon == click$lng & data_name==toupper(input$Restaurant_Name))
     city_num<- which(data_name==input$City & data_city == input$City)
     attri_col<- c(which(data_attri_all[city_num,]=="GOOD"),which(data_attri_all[city_num,]=="BAD"))
     text<- paste("Lattitude ",click$lat,"Longtitude ",click$lng)
     map$clearPopups()
     map$showPopup(click$lat,click$lng,text)
     
     output$Click_text<- renderText({
       text
     })
     
     output$pos_neg_city<- renderDataTable({
       p_n_city<- rbind(c("POSITIVE ATTITUDE",data_city_pos[city_num]),c("NEGATIVE ATTITUDE",data_city_neg[city_num]))
       colnames(p_n_city)<- c(paste("In ",input$City)," ")
       p_n_city
     })
     
     output$rc_city<- renderText({
       paste("In ",input$City,", ",data_city_rc[city_num])
     })
    
     output$view_attri<- renderDataTable({
       data_attri_all[c(city_num,target_num),c(2,attri_col)]
     },options = list(scrollX = TRUE)
     )
     
     output$advice<- renderText({
       data_ad[which(data_lat==click$lat & data_lon == click$lng & data_name==toupper(input$Restaurant_Name))]
     })

     output$TrendPlot<- renderPlot({
       Drawtrend(target_id,input$City)
     })
     
     output$reviews<- renderDataTable({
       sentence<- get_sentence(input$City,target_id)
       n<- length(sentence)
       result<- matrix(rep("a",2*n),nrow = n)
       for(i in 1:n){
         result[i,]<- c(paste("Review ",i),sentence[i])
       }
       colnames(result)<- c(" ","Reviews") 
       result
     })
   })
}

# Run the application 
shinyApp(ui = ui, server = server)

