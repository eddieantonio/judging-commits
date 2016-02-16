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

good(5.37) == FALSE
good(5.35) == TRUE

good(1.20) == FALSE
good(1.28) == TRUE

#> qqplot(xentropy[status == 'passed'], xentropy[status == 'failed'])
#> plot(ecdf(xentropy[status == 'passed'])
#+ )
#> plot(ecdf(xentropy[status == 'errored']))
#> plot(ecdf(xentropy[status == 'failed']))
#> plot(ecdf(xentropy[status == 'failed']) - ecdf(xentropy[status == 'passed']))
#Error in ecdf(xentropy[status == "failed"]) - ecdf(xentropy[status ==  : 
#  non-numeric argument to binary operator
#> pairwise.t.test(xentropy, status)
#
#	Pairwise comparisons using t tests with pooled SD 
#
#data:  xentropy and status 
#
#       errored failed 
#failed < 2e-16 -      
#passed 1.4e-10 < 2e-16
#
#P value adjustment method: holm 
#> qqnorm(xentropy[status == 'passed'])
#> shapiro.test(xentropy)
#Error in shapiro.test(xentropy) : sample size must be between 3 and 5000
#> shapiro.test(sample(xentropy, 5000))
#
#	Shapiro-Wilk normality test
#
#data:  sample(xentropy, 5000)
#W = 0.96965, p-value < 2.2e-16
#
#> shapiro.test(rnorm(5000))
#
#	Shapiro-Wilk normality test
#
#data:  rnorm(5000)
#W = 0.99964, p-value = 0.5326
#
#> lower <- c(5.36627217556062, 1.563910848555837, 0.8326875164395318, 1.1251768492860539)
#> upper <- c(5.512516841983881, 1.7101555149790981, 0.9789321828627928, 1.271421515709315)
#> 
#> function good(x) {
#Error: unexpected symbol in "function good"
#>     for (i in 1:length(lower)) {
#+         if (x >= lower[i] && x < upper[i]) {
#+             return FALSE;
#Error: unexpected numeric constant in:
#"        if (x >= lower[i] && x < upper[i]) {
#            return FALSE"
#>         }
#Error: unexpected '}' in "        }"
#>     }
#Error: unexpected '}' in "    }"
#>     return TRUE;
#Error: unexpected numeric constant in "    return TRUE"
#> }
#Error: unexpected '}' in "}"
#> 
#> good(5.37) == FALSE
#Error: could not find function "good"
#> good(5.35) == TRUE
#Error: could not find function "good"
#> 
#> good(1.20) == FALSE
#Error: could not find function "good"
#> good(1.28) == TRUE
#Error: could not find function "good"
#> 
#> good <- function(x) {
#+     for (i in 1:length(lower)) {
#+         if (x >= lower[i] && x < upper[i]) {
#+             return FALSE;
#Error: unexpected numeric constant in:
#"        if (x >= lower[i] && x < upper[i]) {
#            return FALSE"
#>         }
#Error: unexpected '}' in "        }"
#>     }
#Error: unexpected '}' in "    }"
#>     return TRUE;
#Error: unexpected numeric constant in "    return TRUE"
#> }
#Error: unexpected '}' in "}"
#> good <- function(x) {
#+     for (i in 1:length(lower)) {
#+         if (x >= lower[i] & x < upper[i]) {
#+             return FALSE
#Error: unexpected numeric constant in:
#"        if (x >= lower[i] & x < upper[i]) {
#            return FALSE"
#>         }
#Error: unexpected '}' in "        }"
#>     }
#Error: unexpected '}' in "    }"
#>     return TRUE
#Error: unexpected numeric constant in "    return TRUE"
#> }
#Error: unexpected '}' in "}"
#> length(lower)
#[1] 4
#> for (i in 1:4) {
#+    print(i)
#+ }
#[1] 1
#[1] 2
#[1] 3
#[1] 4
#> FALSE & FALSE
#[1] FALSE
#> FALSE && FALSE
#[1] FALSE
#> upper
#[1] 5.5125168 1.7101555 0.9789322 1.2714215
#> good <- function(x) {
#+     for (i in 1:length(lower)) {
#+         if (x >= lower[i] && x < upper[i]) {
#+             return(FALSE)
#+         }
#+     }
#+     return(TRUE)
#+ }
#> function () {1}
#function () {1}
#> (function () {1}) ()
#[1] 1
#> good(5.37) == FALSE
#[1] TRUE
#> good(5.35) == TRUE
#[1] TRUE
#> 
#> good(1.20) == FALSE
#[1] TRUE
#> good(1.28) == TRUE
#[1] TRUE
#> 
#> sentropy <- xentropy[sapply(xentropy, good)]
#> statuses <- status[sapply(xentropy, good)]
#> pairwise.t.test(sentropy, statuses)
#
#	Pairwise comparisons using t tests with pooled SD 
#
#data:  sentropy and statuses 
#
#       errored failed 
#failed 0.022   -      
#passed 0.022   6.6e-10
#
#P value adjustment method: holm 
#> qqnorm(sentropy)
#> shapiro.test(sentropy)
#Error in shapiro.test(sentropy) : sample size must be between 3 and 5000
#> shapiro.test(sample(sentropy, 5000))
#
#	Shapiro-Wilk normality test
#
#data:  sample(sentropy, 5000)
#W = 0.99052, p-value < 2.2e-16
#
#> pairwise.wilcox.test(sentropy, statuses)
#
#	Pairwise comparisons using Wilcoxon rank sum test 
#
#data:  sentropy and statuses 
#
#       errored failed 
#failed 0.017   -      
#passed 0.122   1.6e-07
#
#P value adjustment method: holm 
# 
#> passed <- read.csv("passed.csv", header = TRUE)
#> failed <- read.csv("failed.csv", header = TRUE)
#> plot(passed)
#> plot(failed)
#> attach(failed)
#> cor(est.xentropy, proportion)
#[1] 0.3518528
#> cor.test(est.xentropy, proportion)
#
#	Pearson's product-moment correlation
#
#data:  est.xentropy and proportion
#t = 3.7589, df = 100, p-value = 0.0002874
#alternative hypothesis: true correlation is not equal to 0
#95 percent confidence interval:
# 0.1689377 0.5113386
#sample estimates:
#      cor 
#0.3518528 
#
#> plot(failed)
#> ggplot(failed, aes(est.xentropy, proportion)) + geom_line()
#> ggplot(passed, aes(est.xentropy, proportion)) + geom_line()
#> scommits <- commits[sapply(xentropy, good),]
#> 
#> good <- function(x) {
#+     for (i in 1:length(lower)) {
#+         if (x >= lower[i] && x < upper[i]) {
#+             return(FALSE)
#+         }
#+     }
#+     return(TRUE)
#+ }
#> 
#> scommits <- commits[sapply(xentropy, good),]
#> ggplot(scommits, aes(xentropy, colour = status)) + stat_ecdf(geom = "step")
#> pairwise.wilcox.test(scommits$xentropy, scommits$status)
#
#	Pairwise comparisons using Wilcoxon rank sum test 
#
#data:  scommits$xentropy and scommits$status 
#
#       errored failed 
#failed 0.2518  -      
#passed 0.0021  1.7e-07
#
#P value adjustment method: holm 
#> scommits$broken <- if (scommits$status == 'Passed') 'passed' else 'Broken'
#Warning message:
#In if (scommits$status == "Passed") "passed" else "Broken" :
#  the condition has length > 1 and only the first element will be used
#> scommits$broken <- sapply(scommits$status, function (x) {if (x == 'Passed') 'passed' else 'Broken'})
#> 
#> View(scommits)
#> scommits$broken <- sapply(scommits$status, function (x) {if (x == 'passed') 'Passed' else 'Broken'})
#> pairwise.wilcox.test(scommits$xentropy, scommits$broken)
#
#	Pairwise comparisons using Wilcoxon rank sum test 
#
#data:  scommits$xentropy and scommits$broken 
#
#       Broken 
#Passed 7.8e-09
#
#P value adjustment method: holm 
#> ggplot(scommits, aes(xentropy, colour = scommits$broken)) + stat_ecdf(geom = "step")
#> scommits$broken2 <- ifelse(scommits$status == 'passed', 'Passed', 'Broken')
