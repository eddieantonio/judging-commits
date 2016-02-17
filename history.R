library(RSQLite)
con = dbConnect(drv="SQLite", dbname="commits.sqlite")
con <- dbConnect(RSQLite::SQLite(), "commits.sqlite")
RSQLite::SQLite().
install.packages("RSQLite")
install.packages("RSQLite")
install.packages("RSQLite")
install.packages("RSQLite")
library(RSQLite)
con <- dbConnect(RSQLite::SQLite(), "commits.sqlite")
library(RSQLite)
con <- dbConnect(RSQLite::SQLite(), "commits.sqlite")
install.packages("RSQLite")
library(RSQLite)
con <- dbConnect(RSQLite::SQLite(), "commits.sqlite")
con <- dbConnect(RSQLite::SQLite(), "commits.sqlite")
commits < dbGetQuery(con, "SELECT * FROM commits")
commits <- dbGetQuery(con, "SELECT * FROM commits")
attach(commits)
commits$xentropy <- sapply(perplexity, log2)
bin.width = 2*IRQ(perplexity)*count(perplexity)^(-1/3)
bin.width = 2*IQR(perplexity)*count(perplexity)^(-1/3)
bin.width = 2*IQR(perplexity)*length(perplexity)^(-1/3)
bin.width = 2*IQR(xentropy)*length(xentropy)^(-1/3)
bin.width = 2*IQR(xentropy)*length(xentropy)^(-1/3)
attach(commits)
bin.width = 2*IQR(xentropy)*length(xentropy)^(-1/3)
library(ggplot2)
ggplot(commits, aes(xentropy)) + geom_histogram(binwidth = bin.width)
last_plot() + ggtitle("Leave-one-out Cross-entropy")
library(RSQLite)
library(ggplot2)
con <- dbConnect(RSQLite::SQLite(), "commits.sqlite")
commits <- dbGetQuery(con, "SELECT * FROM commits")
commits$xentropy <- sapply(commits$perplexity, log2)
attach(commits)
bin.width <- 2 * IQR(xentropy) * length(xentropy) ^ (-1/3)
ggplot(commits, aes(xentropy, fill = status)) + geom_histogram(binwidth = bin.width)
library(RSQLite)
library(ggplot2)
con <- dbConnect(RSQLite::SQLite(), "commits.sqlite")
commits <- dbGetQuery(con, "SELECT * FROM commits")
commits$xentropy <- sapply(commits$perplexity, log2)
bin.width <- 2 * IQR(xentropy) * length(xentropy) ^ (-1/3)
attach(commits)
bin.width <- 2 * IQR(xentropy) * length(xentropy) ^ (-1/3)
View(commits)
ks.test(xentropy[status == 'passed'])
ks.test(xentropy[status == 'passed'], xentropy[status != 'passed'])
ks.test(xentropy[status == 'passed'], xentropy[status == 'passed'])
ks.test(xentropy[status == 'passed'], xentropy[status == 'errored'])
ks.test(xentropy[status == 'passed'], xentropy[status == 'failed'])
xentropy[status == "failed"]
qqplot(xentropy[status == 'passed'], xentropy[status == 'failed'])
plot(ecdf(xentropy[status == 'passed'])
)
plot(ecdf(xentropy[status == 'errored']))
plot(ecdf(xentropy[status == 'failed']))
plot(ecdf(xentropy[status == 'failed']) - ecdf(xentropy[status == 'passed']))
pairwise.t.test(xentropy, status)
qqnorm(xentropy[status == 'passed'])
shapiro.test(xentropy)
shapiro.test(sample(xentropy, 5000))
shapiro.test(rnorm(5000))
lower <- c(5.36627217556062, 1.563910848555837, 0.8326875164395318, 1.1251768492860539)
upper <- c(5.512516841983881, 1.7101555149790981, 0.9789321828627928, 1.271421515709315)
function good(x) {
for (i in 1:length(lower)) {
if (x >= lower[i] && x < upper[i]) {
return FALSE;
}
}
return TRUE;
}
good(5.37) == FALSE
good(5.35) == TRUE
good(1.20) == FALSE
good(1.28) == TRUE
good <- function(x) {
for (i in 1:length(lower)) {
if (x >= lower[i] && x < upper[i]) {
return FALSE;
}
}
return TRUE;
}
good <- function(x) {
for (i in 1:length(lower)) {
if (x >= lower[i] & x < upper[i]) {
return FALSE
}
}
return TRUE
}
length(lower)
for (i in 1:4) {
print(i)
}
FALSE & FALSE
FALSE && FALSE
upper
good <- function(x) {
for (i in 1:length(lower)) {
if (x >= lower[i] && x < upper[i]) {
return(FALSE)
}
}
return(TRUE)
}
function () {1}
(function () {1}) ()
good(5.37) == FALSE
good(5.35) == TRUE
good(1.20) == FALSE
good(1.28) == TRUE
sentropy <- xentropy[sapply(xentropy, good)]
statuses <- status[sapply(xentropy, good)]
pairwise.t.test(sentropy, statuses)
qqnorm(sentropy)
shapiro.test(sentropy)
shapiro.test(sample(sentropy, 5000))
pairwise.wilcox.test(sentropy, statuses)
ggplot(commits, aes(sentropy, fill=status)) + geom_histogram(binwidth = bin.width)
scommits <- commits[sapply(xentropy, good)]
scommits <- commits[,sapply(xentropy, good)]
scommits <- commits[sapply(xentropy, good),]
ggplot(scommits, aes(sentropy, fill=statuses)) + geom_histogram(binwidth = bin.width)
passed <- read.csv("passed.csv", header = FALSE)
plot(passed)
View(passed)
passed <- read.csv("passed.csv", header = TRUE)
plot(passed)
failed <- read.csv("failed.csv", header = TRUE)
plot(failed)
failed <- read.csv("failed.csv", header = TRUE)
plot(failed)
plot(passed)
attach(failed)
cor(est.xentropy, proportion)
cor.test(est.xentropy, proportion)
plot(failed)
ggplot(failed, aes(est.xentropy, proportion)) + geom_line()
ggplot(passed, aes(est.xentropy, proportion)) + geom_line()
ggplot(failed, aes(est.xentropy, proportion)) + geom_line()
ggplot(commits, aes(xentropy)) + stat_ecdf(geom = "step")
ggplot(commits, aes(xentropy, colour = status)) + stat_ecdf(geom = "step")
ggplot(scommits, aes(xentropy, colour = status)) + stat_ecdf(geom = "step")
lower <- c(5.36627217556062, 1.563910848555837, 0.8326875164395318, 1.1251768492860539, 4.488804177021055)
upper <- c(5.512516841983881, 1.7101555149790981, 0.9789321828627928, 1.271421515709315, 4.635048843444316)
(, )
good <- function(x) {
for (i in 1:length(lower)) {
if (x >= lower[i] && x < upper[i]) {
return(FALSE)
}
}
return(TRUE)
}
lower <- c(5.36627217556062, 1.563910848555837, 0.8326875164395318, 1.1251768492860539, 4.488804177021055)
upper <- c(5.512516841983881, 1.7101555149790981, 0.9789321828627928, 1.271421515709315, 4.635048843444316)
good <- function(x) {
for (i in 1:length(lower)) {
if (x >= lower[i] && x < upper[i]) {
return(FALSE)
}
}
return(TRUE)
}
scommits <- commits[sapply(xentropy, good),]
ggplot(scommits, aes(xentropy, colour = status)) + stat_ecdf(geom = "step")
pairwise.wilcox.test(scommits$xentropy, scommits$status)
scommits$broken <- if (scommits$status == 'Passed') 'passed' else 'Broken'
scommits$broken <- sapply(scommits$status, function (x) {if (x == 'Passed') 'passed' else 'Broken'})
View(scommits)
scommits$broken <- sapply(scommits$status, function (x) {if (x == 'passed') 'Passed' else 'Broken'})
pairwise.wilcox.test(scommits$xentropy, scommits$broken)
ggplot(scommits, aes(xentropy, colour = scommits$broken)) + stat_ecdf(geom = "step")
scommits$broken2 <- ifelse(scommits$status == 'passed', 'Passed', 'Broken')
ggplot(commits, aes(xentropy, fill=status)) + geom_histogram(binwidth = bin.width)
last_plot() + scale_fill_manual(c("orange", "red", "green"))
last_plot() + scale_fill_manual(values =c("orange", "red", "green"))
last_plot() + xlab("Cross-Entropy (bits)") + ylab("Number of commit messages")
last_plot() + labs(fill = "Status")
last_plot() + labs(fill = "Build Status")
count(commits)
length(commits)
length(commits$xentropy)
last_plot() + scale_fill_manual(values = c("#0ABBFF", "#FF0095", "#ADFF00"))
