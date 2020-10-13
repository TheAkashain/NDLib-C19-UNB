library(ggplot2)
library(readxl)

my_data <- read_excel("Output.xlsx", na = c("NA",0))
i = 2
#1 = Total, 2 = Active, 3 = Tested
lengths1 = c()
means1 = c()
medians1 = c()
iqr_max1 = c()
iqr_min1 = c()
days = c()
total1 = c()

lengths2 = c()
means2 = c()
medians2 = c()
iqr_max2 = c()
iqr_min2 = c()
total2 = c()

lengths3 = c()
means3 = c()
medians3 = c()
iqr_max3 = c()
iqr_min3 = c()
total3 = c()
while(i <= 5*15-1) {
  #Total Infected Data
  lengths1 = c(lengths1, length(na.omit(unlist(my_data[i], use.names = FALSE))))
  means1 = c(means1, mean(na.omit(unlist(my_data[i], use.names = FALSE))))
  medians1 = c(medians1, median(na.omit(unlist(my_data[i], use.names = FALSE))))
  iqr_max1 = c(iqr_max1, summary(na.omit(unlist(my_data[i], use.names = FALSE)))[[5]])
  iqr_min1 = c(iqr_min1, summary(na.omit(unlist(my_data[i], use.names = FALSE)))[[2]])
  total1 = c(total1, na.omit(unlist(my_data[i], use.names = FALSE)))
  
  #Days Data
  days = c(days, na.omit(unlist(my_data[i-1], use.names = FALSE)))
  
  #Current Infected Data
  lengths2 = c(lengths2, length(na.omit(unlist(my_data[i+1], use.names = FALSE))))
  means2 = c(means2, mean(na.omit(unlist(my_data[i+1], use.names = FALSE))))
  medians2 = c(medians2, median(na.omit(unlist(my_data[i+1], use.names = FALSE))))
  iqr_max2 = c(iqr_max2, summary(na.omit(unlist(my_data[i+1], use.names = FALSE)))[[5]])
  iqr_min2 = c(iqr_min2, summary(na.omit(unlist(my_data[i+1], use.names = FALSE)))[[2]])
  total2 = c(total2, na.omit(unlist(my_data[i+1], use.names = FALSE)))
  
  #Tested Data
  lengths3 = c(lengths3, length(na.omit(unlist(my_data[i+2], use.names = FALSE))))
  means3 = c(means3, mean(na.omit(unlist(my_data[i+2], use.names = FALSE))))
  medians3 = c(medians3, median(na.omit(unlist(my_data[i+2], use.names = FALSE))))
  iqr_max3 = c(iqr_max3, summary(na.omit(unlist(my_data[i+2], use.names = FALSE)))[[5]])
  iqr_min3 = c(iqr_min3, summary(na.omit(unlist(my_data[i+2], use.names = FALSE)))[[2]])
  total3 = c(total3, na.omit(unlist(my_data[i+2], use.names = FALSE)))
  i = i + 5
}
lengths1 = lengths1 / 10
lengths2 = lengths2 / 10
lengths3 = lengths3 / 10
x = c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)

df1 <- data.frame(x,means1, iqr_min1, iqr_max1)
df2 <- data.frame(x,means2, iqr_min2, iqr_max2)
df3 <- data.frame(x,means3, iqr_min3, iqr_max3)
b <- ggplot()
b <- b + geom_line(data = df1, aes(x,means1, color = 'black'))+
  geom_point(data = df1, aes(x,means1, color = 'black')) + 
  geom_errorbar(data = df1, aes(x,means1, ymin = iqr_min1, ymax = iqr_max1, color = 'black'))
b <- b + geom_line(data = df2, aes(x,means2, color = 'red')) +
  geom_point(data = df2, aes(x,means2, color = 'red')) +
  geom_errorbar(data = df2, aes(x,means2, ymin = iqr_min2, ymax = iqr_max2, color = 'red'))
b <- b + geom_line(data = df3, aes(x,means3, color = 'blue')) +
  geom_point(data = df3, aes(x,means3, color = 'blue')) +
  geom_errorbar(data = df3, aes(x,means3, ymin = iqr_min3, ymax = iqr_max3, color = 'blue'))
b <- b + labs(x = 'Time Lag Between Onset of Infectiousness and Quarantine for Patient 0 (Indexed at 1)', 
              y = 'Number of People Infected',
              title = 'Summary of The Mean ASPT Model Results in Patient 0 Testing') 
b <- b + theme_bw()
b <- b + scale_color_identity(name = 'Key', guide = 'legend', labels = c('Total Cases', 'Tested Cases','Active Cases at Day 30'))
b <- b + scale_x_continuous(expand = c(0, 0)) + 
  scale_y_continuous(expand = c(0, 0))
b
ggsave('Mean_Data_1_Index.png', b, 'png')

df1 <- data.frame(x,means1)
df2 <- data.frame(x,means2)
df3 <- data.frame(x,means3)
b <- ggplot()
b <- b + geom_bar(data = df1, aes(x = x, y = means1, fill = 'black'), alpha = 0.5, stat='identity')
b <- b + geom_bar(data = df2, aes(x = x, y = means2, fill = 'red'), alpha = 0.5, stat='identity') 
b <- b + geom_bar(data = df3, aes(x = x, y = means3, fill = 'blue'), alpha = 0.5, stat='identity')
b <- b + labs(x = 'Time Lag Between Onset of Infectiousness and Quarantine for Patient 0 (Indexed at 1)', 
              y = 'Number of People Infected',
              title = 'Summary of The Mean ASPT Model Results in Patient 0 Testing') 
b <- b + theme_bw()
b <- b + scale_fill_identity(name = 'Key', guide = 'legend', labels = c('Total Cases', 'Tested Cases','Active Cases at Day 30'))
b
ggsave('Histogram_Data_0_Index.png', b, 'png')

df1 <- data.frame(x,lengths1, iqr_min1, iqr_max1)
df2 <- data.frame(x,lengths2, iqr_min2, iqr_max2)
df3 <- data.frame(x,lengths3, iqr_min3, iqr_max3)
b <- ggplot()
b <- b + geom_line(data = df1, aes(x,lengths1, color = 'black'))+
  geom_point(data = df1, aes(x,lengths1, color = 'black'))
b <- b + geom_line(data = df2, aes(x,lengths2, color = 'red'))+
  geom_point(data = df2, aes(x,lengths2, color = 'red'))
b <- b + geom_line(data = df3, aes(x,lengths3, color = 'blue')) +
  geom_point(data = df3, aes(x,lengths3, color = 'blue'))
b <- b + labs(x = 'Time Lag Between Onset of Infectiousness and Quarantine for Patient 0 (Indexed at 1)', 
              y = 'Number of People Infected',
              title = 'Proabilities of The ASPT Model in Patient 0 Testing') 
b <- b + scale_color_identity(name = 'Key', guide = 'legend', labels = c('Any Cases', 'Any Tested Cases','Any Active Cases at Day 30'))
b <- b + expand_limits(x = 1, y = 0)
b <- b + theme_bw()
b
ggsave('Probability_Data_0_Index.png', b, 'png')