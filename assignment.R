library(dplyr)    
library(readxl)
library(tidyr)
library(lubridate)
library(magrittr)
library(tidyverse)
library(readr)

df<-read_excel("C:/Users/ankur.kumar/Downloads/python/SaleData.xlsx")
#df1<-read.csv("C:/Users/ankur.kumar/Downloads/python/imdb.csv")
df5 <- read_delim("C:/Users/ankur.kumar/Downloads/python/imdb.csv",delim = ",", escape_backslash = T, escape_double = F)

df2<-read.csv("C:/Users/ankur.kumar/Downloads/python/movie_metadata.csv")
df3<-read.csv("C:/Users/ankur.kumar/Downloads/python/diamonds.csv")

#1
least_sales<- function(df){
  ty<-df %>%group_by(Item) %>% summarise(min_sale_amt=min(Sale_amt))
  return(ty)
}


#2
sales_year_region<- function(df){
  ye <-year(df$OrderDate)
  df$year <- ye
  second<- df %>% group_by(year,Region) %>% summarise(total_sales=sum(Sale_amt))
  return(second)
}


#3
days_diff<- function(df){
  cur<- as.Date(strptime(today(), "%Y-%m-%d"))
  diff_in_days<- cur-as.Date(df$OrderDate)
  df$days_diff<-diff_in_days
  return(df)
}
#df$diff_in_days<- cur_1-as.Date(df$OrderDate)

#4
mgr_slsmn <-function(df){
  ty<-df %>% group_by(Manager) %>% summarise(list_of_salesman = paste(unique(SalesMan), collapse = ', '))
  return(ty)
}

#5
slsmn_units<-function(df){
  agg <- aggregate(data=df, SalesMan ~ Region, function(x) length(unique(x)))
  agg_2<-df %>% group_by(Region) %>% summarise(total_sale=sum(Units))
  res<-merge(agg, agg_2, by="Region", all=TRUE)
  return(res)
}

#6
sales_pct<- function(df){
  agg_1<-df %>% group_by(Manager) %>% summarise(total_sales=sum(Sale_amt))
  total<- sum(df$Sale_amt)
  percent_sales<-(agg_1$total_sales/total)*100
  fres<-cbind(agg_1,percent_sales)
  fres_1<-select(fres,Manager,percent_sales)
  return(fres_1)
}

#7
fifth_movie<- function(df1){
  return(df1[5,]$imdbRating)
}

#8
movies<- function(df1){
  min_val<-min(df1[,"duration"],na.rm=TRUE)
  max_val<-max(df1[,"duration"],na.rm=TRUE)
  min_movie<-filter(df1,df1$duration==min_val)
  max_movie<-filter(df1,df1$duration==max_val)
  print(min_movie)
  print(max_movie)
  #return(min_movie,max_movie)
  
}


#9
sort_df<- function(df1){
  dfsort<-df1[order(df1$title_year,-df1$imdb_score),]
  return(dfsort)
  
}


#10
subset_df<-function(df2){
  ts<-filter(df2,gross>=2000000,budget<1000000,duration >= 30 & duration <=180)
  return(ts)
}

#11
dupl_rows<- function(df3){
  ans<-nrow(df3)-nrow(unique(df3))
  return(ans)
}

#12-problem-in r
drop_row<- function(df){
  ans<- df[!is.na(df$carat) & !is.na(df$cut),]
  return(ans)
}

#13
sub_numeric<- function(df){
  res<-select_if(df, is.numeric)
  return(res)
}

#14
volume<- function(df){
  sapply(df$z,class)
  as.numeric(as.character(df$z))
  for(i in 1:length(df$depth))
  {
    if(df$depth[i]>60)
    {
      df$vol[i]<-df$x[i]*df$y[i]*as.numeric(as.character(df$z[i]))
    }
    else
    {
      df$vol[i]<-8
    }
  }
  df[is.na(df)]<-8
  return(df)
}

#15
impute<- function(df){
  df$price[is.na(df$price)] = mean(df$price, na.rm=TRUE)
  return(df)
}



# #Bonus questions
# #1
# final_list <- c()
# for (i in 1:4){
#   temp_list_1 <- c('Action', 'Adult', 'Adventure', 'Animation', 'Biography',
#                'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy',
#                'FilmNoir', 'GameShow', 'History', 'Horror', 'Music', 'Musical',
#                'Mystery', 'News', 'RealityTV', 'Romance', 'SciFi', 'Short', 'Sport',
#                'TalkShow', 'Thriller', 'War', 'Western')
#   temp_list_2 <- c()
#   temp_var_1=df1[i,]
#   temp_var_2 <- temp_var_1[1,17:44]
#   for (k in ncol(temp_var_2) ){
#     if(temp_var_2[k,1]==1){
#       temp_list_2 <- c(temp_list_2,temp_list_1[k])
#     }
#     print(temp_list_2)
#     final_list <- (final_list,temp_list_2)
#   }
   
  cat("\n")
}










