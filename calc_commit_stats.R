library(RSQLite)
library(ggplot2)

# Connect to SQLite
con <- dbConnect(RSQLite::SQLite(), "commits.sqlite")
commits <- dbGetQuery(con, "SELECT repo, sha, message, perplexity,
                              CASE status
                                WHEN 'passed' THEN 'Passed'
                                WHEN 'errored' THEN 'Errored'
                                WHEN 'failed' THEN 'Failed'
                                ELSE NULL
                                END as status
                      FROM commits")

# Pre-calculate cross-entropy.
commits$xentropy <- sapply(commits$perplexity, log2)
commits$build <- ifelse(commits$status == 'Passed', 'Passed', 'Broken')

with(commits, {
    bin.width <- 2 * IQR(xentropy) * length(xentropy) ^ (-1/3)
    print(length(xentropy))
    print(bin.width)

    # Do a pairwise Wilcox test.
    print(pairwise.wilcox.test(xentropy, status))

    # Compare builds that have passed against builds that are broken.
    print(ks.test(xentropy[build == 'Passed'], xentropy[build == 'Broken']))


    #ggplot(commits, aes(xentropy, fill=status)) +
    #    geom_histogram(binwidth = bin.width) +
    #    xlab("Cross-Entropy (bits)") +
    #    ylab("Number of commit messages") +
    #    ylim(0, 4500) +
    #    scale_fill_manual(values = c("#0ABBFF", "#FF0095", "#ADFF00")) +
    #    labs(fill = "Build Status")

    #ggsave("histo-removed.pdf",
    #       width=6.7, height=4)


    #ggplot(commits[status != 'errored',], aes(x=xentropy, colour = status)) +
    ggplot(commits, aes(x=xentropy, colour = status)) +
        stat_ecdf() +
        #scale_fill_manual(values = c("#0ABBFF", "#FF0095", "#ADFF00")) +
        scale_colour_brewer(type = "qual", palette = 1) +
        xlab("Cross-Entropy (bits)") +
        ylab("Number of commit messages (commulative)") +
        labs(fill = "Build Status")

    ggsave("ecdf.pdf",
           width=6.7, height=4)
})


#pairwise.wilcox.test(scommits$xentropy, scommits$broken)
#ggplot(scommits, aes(xentropy, colour = scommits$broken)) + stat_ecdf(geom = "step")

#ks.test(xentropy[status == 'passed'])
#ks.test(xentropy[status == 'passed'], xentropy[status == 'passed'])
#ks.test(xentropy[status == 'passed'], xentropy[status == 'errored'])
#ks.test(xentropy[status == 'passed'], xentropy[status == 'failed'])

#xentropy[status == "failed"]
#qqplot(xentropy[status == 'passed'], xentropy[status == 'failed'])
#plot(ecdf(xentropy[status == 'passed']))
#plot(ecdf(xentropy[status == 'errored']))
#plot(ecdf(xentropy[status == 'failed']))
#plot(ecdf(xentropy[status == 'failed']) - ecdf(xentropy[status == 'passed']))
#pairwise.t.test(xentropy, status)
#qqnorm(xentropy[status == 'passed'])

# Normality test
#shapiro.test(xentropy)
#shapiro.test(sample(xentropy, 5000))
#shapiro.test(rnorm(5000))

# Some good tests!
#print(good(5.37) == FALSE)
#print(good(5.35) == TRUE)
#print(good(1.20) == FALSE)
#print(good(1.28) == TRUE)

#scommits <- commits[sapply(xentropy, good),]
#pairwise.t.test(sentropy, statuses)
#qqnorm(sentropy)
#shapiro.test(sentropy)
#shapiro.test(sample(sentropy, 5000))
#pairwise.wilcox.test(sentropy, statuses)
#ggplot(commits, aes(sentropy, fill=status)) + geom_histogram(binwidth = bin.width)
#ggplot(scommits, aes(sentropy, fill=statuses)) + geom_histogram(binwidth = bin.width)

#passed <- read.csv("passed.csv", header = FALSE)
#plot(passed)
#View(passed)
#passed <- read.csv("passed.csv", header = TRUE)
#plot(passed)
#failed <- read.csv("failed.csv", header = TRUE)
#plot(failed)
#failed <- read.csv("failed.csv", header = TRUE)
#plot(failed)
#plot(passed)
#attach(failed)
#cor(est.xentropy, proportion)
#cor.test(est.xentropy, proportion)
#plot(failed)
#ggplot(failed, aes(est.xentropy, proportion)) + geom_line()
#ggplot(passed, aes(est.xentropy, proportion)) + geom_line()
#ggplot(failed, aes(est.xentropy, proportion)) + geom_line()
#ggplot(commits, aes(xentropy)) + stat_ecdf(geom = "step")
#ggplot(commits, aes(xentropy, colour = status)) + stat_ecdf(geom = "step")
#ggplot(scommits, aes(xentropy, colour = status)) + stat_ecdf(geom = "step")

#scommits <- commits[sapply(xentropy, good),]
#ggplot(scommits, aes(xentropy, colour = status)) + stat_ecdf(geom = "step")
#pairwise.wilcox.test(scommits$xentropy, scommits$status)
#scommits$broken <- if (scommits$status == 'Passed') 'passed' else 'Broken'
#scommits$broken <- sapply(scommits$status, function (x) {if (x == 'Passed') 'passed' else 'Broken'})
#View(scommits)
#scommits$broken <- sapply(scommits$status, function (x) {if (x == 'passed') 'Passed' else 'Broken'})
