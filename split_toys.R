toys.df <- read.csv("DATA/toys_rev2.csv", stringsAsFactors=FALSE)

sample.nums <- sample(1:900, 10000000, replace = TRUE)

for(i in 1:900) {
  toy.filename <- paste("DATA/toys_for_elf_", i, ".csv", sep = "")
  cat("writing ", toy.filename, "\n")
  
  df <- toys.df[sample.nums == i,]
  write.csv(df, file=toy.filename, row.names=FALSE, quote=FALSE)
}
