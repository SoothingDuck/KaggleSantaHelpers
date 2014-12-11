
library(stringr)
library(lubridate)
library(ggplot2)
library(plyr)

df <- read.csv("DATA/toys_rev2.csv", stringsAsFactor=FALSE)

df$DateArrival <- ymd_hm(df$Arrival_time)

df$in.working.hours <- factor(ifelse(hour(df$DateArrival) < 9 & df$DateArrival > 18, "No", "Yes"))

df.one.day <- subset(df, DateArrival <= ymd_hm("2014-01-01 23:59"))

agg <- ddply(
  df.one.day,
  .(in.working.hours),
  summarise,
  total.dur=sum(Duration),
  min.dur=min(Duration),
  max.dur=max(Duration),
  avg.dur=mean(Duration)
  )

ggplot(df.one.day) + geom_histogram(aes(x=DateArrival, weight=Duration),binwidth=60)
