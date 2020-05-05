##Jake Chanenson 
##May 2, 2020
##This R file creates graphs from the files in the data folder

library(readxl)
library(tidyverse)
library(readr)

##Import Data
hugo_novel <- read_excel("data\\hugo_data.xlsx", sheet = "Best Novel", col_types = c("text",
                                                                                   "text", "text", "numeric", "numeric", "numeric"))
hugo_novella <- read_excel("data\\hugo_data.xlsx", sheet = "Best Novella", col_types = c("text", 
                                                                                       "text", "text", "numeric", "numeric", "numeric"))
hugo_novelette <- read_excel("data\\hugo_data.xlsx", sheet = "Best Novelette", col_types = c("text", 
                                                                                       "text", "text", "numeric", "numeric", "numeric"))

calc_hyp <- function(mydata){
  pronouns_rand_samp <- sample(mydata, 30)
  num_success <- 0
  for(x in pronouns_rand_samp){
    if (x == "F") num_success = num_success+1
  }
  
  sample_size <- length(pronouns_rand_samp)
  p_null <- (length(mydata)/2) / length(mydata)
  
  ret_val <- prop.test(num_success, n=sample_size, p=p_null, alternative = "two.sided", conf.level = 1-0.05)
  
  return(ret_val)
}

##Hypothesis Tests
novel_hyp <- calc_hyp(hugo_novel$Pronouns)

novella_hyp <- calc_hyp(hugo_novella$Pronouns)

novelette_hyp <- calc_hyp(hugo_novelette$Pronouns)


##Best Novel
#Stacked barplot 
p <- ggplot(data=hugo_novel, aes(x=Year, y=Nominations, fill=Pronouns)) +
  geom_bar(stat="identity")

p + labs(title = "Hugo Best Novel Nominations 2009-2020") + 
          scale_fill_manual(values=c("#8e9aad","#f3d076","#372648"))


##Best Novella
#Stacked barplot 
p <- ggplot(data=hugo_novella, aes(x=Year, y=Nominations, fill=Pronouns)) +
  geom_bar(stat="identity")

p + labs(title = "Hugo Best Novella Nominations 2009-2020") + 
          scale_fill_manual(values=c("#8e9aad","#f3d076","#372648"))


##Best Novelette
#Stacked barplot 
p <- ggplot(data=hugo_novelette, aes(x=Year, y=Nominations, fill=Pronouns)) +
  geom_bar(stat="identity")

p + labs(title = "Hugo Best Novelette Nominations 2009-2020") + 
            scale_fill_manual(values=c("#8e9aad","#f3d076","#372648"))

##---------------------------------------------------------------------------------------##
##Nominations By author 
auth_stats <- read_csv("data\\auth_stats.csv", col_types = cols(Freq = col_integer(), 
                                                Nominations = col_integer()))
#Stacked barplot
p <- ggplot(data=auth_stats, aes(x=Nominations, y=Freq, fill=Pronouns)) +
  geom_bar(stat="identity")

p + labs(title = "Number of Hugo Award Nominations By Author 2009-2020", caption = "Data: Best Novel, Best Novella, and Best Novelette") + 
  xlab("Instances An Author Has Been Nominated") + 
  scale_fill_manual(values=c("#8e9aad","#f3d076","#372648")) + 
  scale_y_continuous(breaks=c(1,5,10,20,40,60,80)) +  scale_x_continuous(breaks=seq(0,7,1))
