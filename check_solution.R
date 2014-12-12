
library(lubridate)
library(ggplot2)

df <- read.csv("DATA/sampleSubmission_rev2_naive_100000.csv", stringsAsFactors = FALSE)

df$StartTime <- ymd_hm(df$StartTime)
df$ElfId <- factor(df$ElfId)

ggplot(df) +  geom_boxplot(aes(x=ElfId, y=Duration))
