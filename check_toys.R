
library(stringr)
library(lubridate)
library(ggplot2)

df <- read.csv("DATA/toys_rev2.csv", stringsAsFactor=FALSE)

df$DateArrival <- ymd_hm(df$Arrival_time)

df.month <- subset(df, DateArrival < ymd_hms("2014-02-01 00:00:00"))
df.day <- subset(df, DateArrival < ymd_hms("2014-01-02 00:00:00") & DateArrival > ymd_hms("2014-01-01 00:00:00"))

ggplot(df.day) + geom_histogram(aes(x=DateArrival), binwidth=10)
ggplot(df.day) + geom_histogram(aes(x=Duration), binwidth=5) + xlim(0,300)
ggplot(df.day) + geom_bar(aes(x=DateArrival, weight = Duration),binwidth=10) 
