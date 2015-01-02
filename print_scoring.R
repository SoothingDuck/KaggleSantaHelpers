library(ggplot2)
library(stringr)

df <- read.csv("scores.csv", stringsAsFactors=FALSE)

df$minutes <- sapply(df$filename, function(x) { as.integer(strsplit(strsplit(x, "_")[[1]][14], "\\.")[[1]][1]) })
df$threshold <- sapply(df$filename, function(x) { 
  as.numeric(paste(strsplit(x, "_")[[1]][11:12], collapse = "."))
    })

ggplot(df) + geom_point(aes(x=nb_elves, y=minutes, size=score)) + facet_wrap(~ nb_toys)


