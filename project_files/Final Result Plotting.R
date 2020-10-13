library(ggplot2)
library(readxl)

my_data <- read_excel("Output.xlsx", na = "NA")
i = 2
lengths = c()
means = c()
medians = c()
iqr_max = c()
iqr_min = c()
days = c()
total = c()
while(i <= 44) {
  lengths = c(lengths, length(na.omit(unlist(my_data[i], use.names = FALSE))))
  means = c(means, mean(na.omit(unlist(my_data[i], use.names = FALSE))))
  medians = c(medians, median(na.omit(unlist(my_data[i], use.names = FALSE))))
  iqr_max = c(iqr_max, summary(na.omit(unlist(my_data[i], use.names = FALSE)))[[5]])
  iqr_min = c(iqr_min, summary(na.omit(unlist(my_data[i], use.names = FALSE)))[[2]])
  days = c(days, na.omit(unlist(my_data[i-1], use.names = FALSE)))
  total = c(total, na.omit(unlist(my_data[i], use.names = FALSE)))
  i = i + 3
}
lengths = lengths / 10
x = c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)

#Plots, in order: Violin Plot (1 index), Mean infected (0 index)
#                 Median infected (0 index), Probability of infection
df <- data.frame(days, total)
df$days <- as.factor(df$days)
head(df)
a <- ggplot(data = df, aes(x = days, y = total))+geom_violin()+geom_boxplot(size = 0.2, width = 0.1)
a <-a + labs(x = "Time Lag Between Onset of Infectiousness and Quarantine for Patient 0 (Indexed at 0)", 
             y = "Number of People Infected",
             title = "Violin Plot of The Number of People Infected in Patient 0 Testing") 
a <- a + theme_bw()
ggsave("Violin_Data_0_Index.png", a, "png")

df <- data.frame(days, total)
df$days <- as.factor(df$days)
head(df)
a <- ggplot(data = df, aes(x = days, y = total))+geom_jitter()
a <-a + labs(x = "Time Lag Between Onset of Infectiousness and Quarantine for Patient 0 (Indexed at 0)", 
             y = "Number of People Infected",
             title = "Jitter Plot of The Number of People Infected in Patient 0 Testing") 
a <- a + theme_bw()
ggsave("Jitter_Data_0_Index.png", a, "png")

df <- data.frame(x,means, iqr_min, iqr_max)
b <- ggplot(data = df, aes(x,means, ymin = iqr_min, ymax = iqr_max))+geom_point()+geom_line()
b <- b + geom_errorbar()
b <- b + scale_x_continuous(expand = c(0, 0)) + 
  scale_y_continuous(expand = c(0, 0))
b <-b + labs(x = "Time Lag Between Onset of Infectiousness and Quarantine for Patient 0 (Indexed at 1)", 
             y = "Number of People Infected",
             title = "Mean Number of People Infected in Patient 0 Testing") 
b <- b + theme_bw()
ggsave("Mean_Data_1_Index.png", b, "png")

df <- data.frame(x,medians, iqr_min, iqr_max)
d <- ggplot(data = df, aes(x,medians, ymin = iqr_min, ymax = iqr_max))+geom_point()+geom_line()
d <- d + geom_errorbar()
d <- d + scale_x_continuous(expand = c(0, 0)) + 
  scale_y_continuous(expand = c(0, 0))
d <- d + labs(x = "Time Lag Between Onset of Infectiousness and Quarantine for Patient 0 (Indexed at 1)", 
             y = "Number of People Infected",
             title = "Median Number of People Infected in Patient 0 Testing") 
d <- d + theme_bw()
ggsave("Mean_Data_1_Index_Median.png", d, "png")

df <- data.frame(x,lengths)
e <- ggplot(data = df, aes(x,lengths))+geom_point()+geom_line()
e <- e + expand_limits(x = c(0, 15), y = c(0,110))
e <- e + scale_x_continuous(expand = c(0, 0)) + 
  scale_y_continuous(expand = c(0, 0))
e <- e + labs(x = "Time Lag Between Onset of Infectiousness and Quarantine for Patient 0 (Indexed at 1)", 
             y = "Probability of an Outbreak",
             title = "Probability of an Outbreak in Patient 0 Testing") 
e <- e + theme_bw()
ggsave("Outbreak_Probability.png", e, "png")