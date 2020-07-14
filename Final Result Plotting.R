library(ggplot2)
library(readxl)

my_data <- read_excel("Output.xlsx", na = "NA")
i = 2
lengths = c()
means = c()
iqr_max = c()
iqr_min = c()
while(i <= 44) {
  lengths = c(lengths, length(na.omit(unlist(my_data[i], use.names = FALSE))))
  means = c(means, mean(na.omit(unlist(my_data[i], use.names = FALSE))))
  iqr_max = c(iqr_max, summary(na.omit(unlist(my_data[i], use.names = FALSE)))[[5]])
  iqr_min = c(iqr_min, summary(na.omit(unlist(my_data[i], use.names = FALSE)))[[2]])
  i = i + 3
}
lengths = lengths / 10
x = c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)


df <- data.frame(x,means, iqr_min, iqr_max)
g <- ggplot(data = df, aes(x,means, ymin = iqr_min, ymax = iqr_max))+geom_point()+geom_line()
g <- g + geom_errorbar()
g <- g + expand_limits(x = c(0, 15), y = c(0,110))
g <- g + scale_x_continuous(expand = c(0, 0)) + 
  scale_y_continuous(expand = c(0, 0))
g <-g + labs(x = "Time Lag Between Onset of Infectiousness and Quarantine for Patient 0 (Indexed at 1)", 
             y = "Number of People Infected",
         title = "Mean Number of People Infected in Patient 0 Testing") 
g <- g + theme_bw()
ggsave("Mean_Data_1_Index.png", g, "png")

x = c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14)
df <- data.frame(x,means, iqr_min, iqr_max)
h <- ggplot(data = df, aes(x,means, ymin = iqr_min, ymax = iqr_max))+geom_point()+geom_line()
h <- h + geom_errorbar()
h <- h + expand_limits(x = c(0, 15), y = c(0,110))
h <- h + scale_x_continuous(expand = c(0, 0)) + 
  scale_y_continuous(expand = c(0, 0))
h <-h + labs(x = "Time Lag Between Onset of Infectiousness and Quarantine for Patient 0 (Indexed at 0)", 
             y = "Number of People Infected",
             title = "Mean Number of People Infected in Patient 0 Testing") 
h <- h + theme_bw()
ggsave("Mean_Data_0_Index.png", h, "png")

df <- data.frame(x,lengths)
k <- ggplot(data = df, aes(x,lengths))+geom_point()+geom_line()
k <- k + expand_limits(x = c(0, 15), y = c(0,110))
k <- k + scale_x_continuous(expand = c(0, 0)) + 
  scale_y_continuous(expand = c(0, 0))
k <-k + labs(x = "Time Lag Between Onset of Infectiousness and Quarantine for Patient 0 (Indexed at 1)", 
             y = "Probability of an Outbreak",
             title = "Probability of an Outbreak in Patient 0 Testing") 
k <- k + theme_bw()
ggsave("Outbreak_Probability.png", k, "png")