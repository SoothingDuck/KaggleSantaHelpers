library(ggplot2)

result <- data.frame()

for(filename in list.files("DATA", "*_of_900*.csv")) {
  cat("Traitement de", filename, "\n")
  elf.number <- as.integer(strsplit(filename, "_")[[1]][5])
  tmp <- read.csv(file.path("DATA", filename), stringsAsFactors = FALSE)
  tmp$ElfId <- elf.number
  
  result <- rbind(result, tmp)
}

result.1 <- subset(result, ElfId == 1)
result.2 <- subset(result, ElfId == 2)
result.900 <- subset(result, ElfId == 900)

result.sub <- subset(result, ElfId %in% c(1:20))

ggplot(result.sub) + geom_boxplot(aes(x=factor(ElfId), y=Duration)) + ylim(0,500)
