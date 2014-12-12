
library(ggplot2)
library(lubridate)

df <- read.csv("DATA/trace_Naive.log", stringsAsFactors=FALSE)
df$TimeStamp <- ymd_hm(df$TimeString)

g <- ggplot(df) + geom_point(aes(x=TimeStamp, y=AvgProductivity))
g
