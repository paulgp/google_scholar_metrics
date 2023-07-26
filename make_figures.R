library(data.table)
library(tidyverse)



# loop over every csv file in data folder
files <- dir("~/repos/google_scholar_metrics/data/", pattern = ".csv", full.names = TRUE)
dat <- rbindlist(lapply(files, read_csv, col_names = FALSE))
colnames(dat) <- c("v1", "paper_title", "authors", "year", "cites", "journal")

dat %>%
    unique() %>%
    filter(journal %in% c("American Economic Review", "The Review of Financial Studies", "Journal of Political Economy", "The Quarterly Journal of Economics", "The Journal of Finance", "The Review of Economic Studies", "Econometrica", "Journal of Financial Economics")) %>%
    ggplot(aes(y = cites, x = reorder(paper_title, cites), fill = as.factor(year))) +
    geom_col() +
    coord_flip() +
    facet_wrap(~journal, scales = "free_y", ncol = 2) +
    theme_minimal() +
    labs(y = "Total Cites", x = "", fill = "Pub. Year")
