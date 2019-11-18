Drawtrend <- function(business_id,city_name,businessname){
  city_trend <- read.csv(paste(city_name,'_trend.csv',sep = ''),header = TRUE)####Set your owen path
  city_count <- read.csv(paste(city_name,'_count.csv',sep = ''),header = FALSE)
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
  plot(xvalue,yvalue,bty='n',type = 'n',main = businessname,yaxt='n',xaxt='n',ylim = c(0,120),xlab='',ylab='Percentile Score In The City')
  abline(h=c(0,20,40,60,80,100),col='gray')
  if (length(xaxislab)>30){
    for (i in 1:length(xaxislab)){
      if(i%%2==0){xaxislab[i]=NA}  ##########Reduce the dense date labels
    }
  }
  axis(1,at=1:length(yvalue),label=xaxislab,las=3)  
  axis(2,at=c(0,20,40,60,80,100),labels = c(0,20,40,60,80,100))
  lines(xvalue[notna],yvalue[notna],type='b',col='red')
  lines(xvalue,yvalue,type = 'b',col='#145b7d')
  text(xvalue[notna],yvalue[notna],obscount[notna],pos=1)
  legend('top',c('Actual Score Based On # Reviews', 'No Reviews Period'),cex=0.7, pch = c(1,NA), lty = c(1,1),col=c('#145b7d','red'),bty='n')
}


##########################      USAGE     ############################
#####      Drawtrend('frCxZS7lPhEnQRJ3UY6m7A','Phoenix')        #####
#####################################################################

####Plots in the Slides

y <- c('64dfRmMmUsOdLnkBOtzp4w', 'jsuUmIEefPjV__ads62Z5w', 'ElWzx5_fU8S2G45OnM-HpA', 'fbQaKW0Lte0JQ_opbnjdKg', 'P8IsTiHq5Hesa6UPL604ww', 'zJGtD3y-pAIGNId4codEEg', 'HGvNE87fvK5PwKMZBDkTbA', '_WtxQbDK7B-ExGdeG-2j6Q', '89uU51kOiQXbJHVA3C6XMQ', '2g4ZTD3ePNSbDAvh6qAOKQ', 'JfHXzulF6yIKgA22YYPedw', 'xZhNZb01n9b4e2X7bZdoVQ', 'jIzygnVmajEXYmfsBNY_Gw', '7Q2cYSl5NBYytJzgjX0oKw', '-bMZCfTK7fxFaURynKpBMA', 'T-KniGykrZ46ZC9plOTspw', 'Ns20WGWn6s6niKAGIQB4UQ')

info=read.csv('mexican_info.csv',header = T)
for (i in y){
  businessname=info[which(info[,1]==i),2]
  Drawtrend(i,'Phoenix',businessname)
  
}








