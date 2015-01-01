library(lubridate)
library(ggplot2)

soln.file <- "DATA/my_solution_third_num_elves_900_num_toys_100000_prod_3_75_minutes_60_toy_decay_1_0.csv"

df <- read.csv(soln.file, stringsAsFactors = FALSE)
df$timestamp <- ymd_hm(df$StartTime)

ggplot(subset(df, ElfId <= 5)) + geom_point(aes(x=timestamp, y=Duration)) + facet_wrap(~ ElfId) 

# Repartition duration
ggplot(df) + geom_boxplot(aes(x=factor(ElfId), y=Duration))

# Repartition duration
ggplot(df) + geom_boxplot(aes(x=factor(ElfId), y=Unsanctioned))



# Repartition productivity
ggplot(df) + geom_boxplot(aes(x=factor(ElfId), y=Old_Productivity))

# Par elfe
ggplot(subset(df, ElfId == 500)) + geom_point(aes(x=timestamp, y=Old_Productivity))
