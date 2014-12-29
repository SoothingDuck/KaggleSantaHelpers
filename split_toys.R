library(lubridate)
library(plyr)
library(ggplot2)

num.elves <- 900

toys.df <- read.csv("DATA/toys_rev2.csv", stringsAsFactors=FALSE)
toys.df$Arrival_time <- ymd_hm(toys.df$Arrival_time)

toys.df$Normalized_Arrival_time <- toys.df$Arrival_time
toys.df$Normalized_Arrival_time[toys.df$Normalized_Arrival_time <= ymd_hm("2014-01-01 09:00")] <- ymd_hm("2014-01-01 09:00")

test.vec <- toys.df$Normalized_Arrival_time
test.vec[hour(test.vec) < 9] <- floor_date(test.vec[hour(test.vec) < 9], "day") + (9*3600)
test.vec[hour(test.vec) > 18] <- ceiling_date(test.vec[hour(test.vec) > 18], "day") + (9*3600)

toys.df$Normalized_Arrival_time <- test.vec
rm(test.vec)
gc(TRUE)

toys.df$Normalized_Arrival_date <- as.Date(toys.df$Normalized_Arrival_time)

toys.df$Min_Possible_Finish_Time <- toys.df$Normalized_Arrival_time + (toys.df$Duration*60)

toys.df$Min_Possible_Finish_date <- as.Date(toys.df$Min_Possible_Finish_Time)

toys.df$Min_Mandatory_Num_days_to_build <- as.integer(toys.df$Min_Possible_Finish_date - toys.df$Normalized_Arrival_date)

toys.df$sample.num <- sample(1:num.elves, 10000000, replace = TRUE)

toys.df <- toys.df[order(toys.df$Min_Possible_Finish_Time, toys.df$Duration),]

agg <- ddply(
  toys.df,
  .(sample.num),
  summarise,
  total_duration=sum(Duration)
  )

agg <- agg[order(-agg$total_duration),]
write.csv(agg, file="DATA/toys_repartition_duration.csv", row.names=FALSE, quote=FALSE)

# 31000000

for(i in 1:900) {
  toy.filename <- paste("DATA/toys_for_elf_", i, ".csv", sep = "")
  cat("writing ", toy.filename, "\n")
  
  df <- toys.df[toys.df$sample.num == i,]
  write.csv(df, file=toy.filename, row.names=FALSE, quote=FALSE)
}
