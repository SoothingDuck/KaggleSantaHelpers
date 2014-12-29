library(lubridate)
library(plyr)
library(reshape2)
library(ggplot2)

df <- read.csv("DATA/toys_for_elf_683.csv", stringsAsFactors=FALSE)

nb.hours.to.4 <- (log(4)/log(1.02))*60
nb.hours.to.2 <- (log(2)/log(1.02))*60

nb.hours.to.4 <- ((log(4)-log(0.25))/log(1.02))*60

