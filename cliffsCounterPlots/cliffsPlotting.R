library(tidyr); library(ggplot2); library(dplyr); library(readr); library(stringr)

##
raw_counts <- read_csv('/Users/alexandercheung/Desktop/School/cliffsCounter/occupancy-counter.csv')

# Check class
sapply(raw_counts, class)  

# Select columns to change
i <- c(1:5)

# Change classes of all columns
raw_counts[ , i] <- apply(raw_counts[ , i], 2,            # Specify own function within apply
                    function(x) as.numeric(as.character(x)))
# Check again
sapply(raw_counts, class)                           # Get classes of all columns


## Add days of week
test_plot_df <- raw_counts %>% mutate(time = hour + minute/60) %>%
  mutate(day_of_week = case_when(
           weekday == 0 ~ 'Monday',
           weekday == 1 ~ 'Tuesday',
           weekday == 2 ~ 'Wednesday',
           weekday == 3 ~ 'Thursday',
           weekday == 4 ~ 'Friday',
           weekday == 5 ~ 'Saturday', 
           weekday == 6 ~ 'Sunday'
           )
  ) %>% arrange(weekday) %>% 
  filter(time >= 6) %>% 
  filter(!(day_of_week %in% c('Saturday','Sunday') & time < 9)) %>% 
  filter(!(day_of_week %in% c('Saturday','Sunday') & time > 22.5))

test_plot_df$day_of_week_f = factor(test_plot_df$day_of_week,
                                    levels=c('Monday', 'Tuesday', 'Wednesday','Thursday','Friday','Saturday','Sunday'))

## Plot
plot <- ggplot(data = test_plot_df) + geom_smooth(aes(x = time, y = n_climbers)) +
  theme_bw() + scale_x_discrete(name ="Time of day", limits=seq.int(6,24, 1)) + ylab('Number of Climbers') + 
  facet_grid(day_of_week_f ~ .)

ggsave('/Users/alexandercheung/Desktop/School/cliffsCounter/updated_occup_plot.pdf')
