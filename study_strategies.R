library(ggplot2)

# Etude objet duration 10000
start.minute <- 540
toy.duration <- 10000
productivity <- 1.0

source("functions.R")

# Test selon productivite
df <- data.frame(
  productivity <- seq(0.25, 4, length.out=1000)
  )

df$last.minute <- sapply(productivity, function(x) { get.next.available.time(540, 20000, x) })

ggplot(df) + geom_point(aes(x=productivity, y=last.minute))

# Comparatif 2 scénario
# 1 : productivité 1 et faire le jouet à 10000
# 2 : augmenter la productivité puis faire le jouet à 10000

df <- data.frame(
  duration = seq(0, 10000, 1)  
)

df$first.productivity <- 1.0
df$last.productivity <- sapply(df$duration, function(x) { get.productivity.without.unsanctioned(1.0, x) })

df$minute.begin.big.object <- sapply(df$duration, function(x) { get.next.without.unsanctionned(540, x) })

vec <- mapply(get.next.available.time, df$minute.begin.big.object, 20000, df$last.productivity)
df$last.minute <- vec

ggplot(df) + geom_point(aes(x=duration, y=last.minute))
