library(ggplot2)
library(stringr)

df <- read.csv("scores.csv", stringsAsFactors=FALSE)

df$minutes <- sapply(df$filename, function(x) { as.integer(strsplit(strsplit(x, "_")[[1]][11], "\\.")[[1]][1]) })
df$threshold <- sapply(df$filename, function(x) { 
  as.numeric(paste(strsplit(x, "_")[[1]][8:9], collapse = "."))
    })
df$ratio <- sapply(df$filename, function(x) { 
  tmp <- strsplit(x, "_")[[1]][14:15]
  tmp <- str_replace(tmp, ".csv", "")
  as.numeric(paste(tmp, collapse = "."))
})
df$min.duration <- sapply(df$filename, function(x) { 
  tmp <- strsplit(x, "_")[[1]][18]
  tmp <- str_replace(tmp, ".csv", "")
  as.numeric(paste(tmp, collapse = "."))
})



ggplot(df) + geom_bar(aes(x=ratio, weight=score, fill=factor(minutes)),position="dodge") + facet_grid(min.duration ~ threshold)
