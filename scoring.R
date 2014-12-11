
library(lubridate)
library(ggplot2)

df <- read.csv("DATA/toys_rev2.csv", stringsAsFactors=FALSE)

df$Arrival_Posix <- ymd_hm(df$Arrival_time)

first_minute <- as.integer(difftime(max(df$Arrival_Posix), ymd_hm("2014-01-01 12:00"), units = "mins"))
last_minute <- as.integer(difftime(ymd_hm("2700-12-24 23:59"), ymd_hm("2014-01-01 12:00"), units = "mins"))

minutes.span <- seq(first_minute, last_minute, 50000)
nb.elfs <- seq(1, 900, length.out=20)

result <- data.frame()

for(nb.elf in nb.elfs) {
  
  result <- rbind(
      result,
      data.frame(
        minute=minutes.span,
        nb.elf=nb.elf,
        score=minutes.span*log(1+nb.elf)
        )
    )
  
}

minute.naive <- as.integer(difftime(ymd_hm("2538-03-09 09:00"), ymd_hm("2014-01-01 12:00"), units = "mins"))



ggplot(result) + geom_line(aes(x=minute, y=score, color=factor(nb.elf))) +
  geom_hline(yintercept=1273164785) +
  geom_vline(xintercept=minute.naive)
  
  
