#!/usr/bin/env Rscript

library(RSQLite)
library(ggplot2)

con <- dbConnect(RSQLite::SQLite(), "commits.sqlite")
commits <- dbGetQuery(con, "SELECT * FROM commits")
commits$xentropy <- sapply(commits$perplexity, log2)


with(commits, {
    # Calculated using the Freedman–Diaconis rule.
    bin.width <- 2 * IQR(xentropy) * length(xentropy) ^ (-1/3)

    ggplot(commits, aes(xentropy)) +
        geom_histogram(binwidth = bin.width) +
        ggtitle("Leave-one-project-out cross-entropy") +
        ylab("Cross-entropy of message (bits)") +
        xlab("Count") +
        ggsave("histo.pdf")
});
