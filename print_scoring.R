library(ggplot2)
library(stringr)

df <- read.csv("scores.csv", stringsAsFactors=FALSE)

df$minutes <- sapply(df$filename, function(x) { as.integer(strsplit(strsplit(x, "_")[[1]][14], "\\.")[[1]][1]) })
df$threshold <- sapply(df$filename, function(x) { 
  as.numeric(paste(strsplit(x, "_")[[1]][11:12], collapse = "."))
    })

ggplot(subset(df, nb_toys == 2000000)) + geom_point(aes(x=nb_elves, y=minutes, size=score)) + facet_wrap(~ nb_toys)

ggplot(df) + geom_point(aes(x=nb_elves, y=minutes, size=score)) + facet_wrap(~ nb_toys)


ggplot(subset(df, nb_toys == 10000000)) + geom_bar(aes(x=factor(nb_elves), weight=score)) + facet_wrap(~ minutes)

