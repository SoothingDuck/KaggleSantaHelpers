library(lubridate)
library(ggplot2)

soln.file <- "DATA/my_solution_third_num_elves_900_num_toys_10000000_prod_3_5_minutes_120.csv"

df <- read.csv(soln.file, stringsAsFactors = FALSE)
df$timestamp <- ymd_hm(df$StartTime)
df$rapport <- df$Sanctioned/(df$Sanctioned+df$Unsanctioned)

ggplot(subset(df, ElfId <= 5)) + geom_point(aes(x=timestamp, y=Duration)) + facet_wrap(~ ElfId) 

# Repartition duration
ggplot(df) + geom_boxplot(aes(x=factor(ElfId), y=Duration))

# Repartition duration
ggplot(df) + geom_boxplot(aes(x=factor(ElfId), y=Unsanctioned))

# Repartition productivity
ggplot(df) + geom_boxplot(aes(x=factor(ElfId), y=Old_Productivity))

# Par elfe
ggplot(subset(df, ElfId == 2)) + geom_point(aes(x=timestamp, y=Old_Productivity))

