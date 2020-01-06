# config
rm(list=ls())

# Load le dataframe des paires
if ("saved.rds" %in% list.files()){
  
  df = readRDS("saved.rds")
  html_available = list.files(path = "www/",pattern = "*.html")
  filtera = df$filea %in% html_available
  filterb = df$fileb %in% html_available
  filter = as.logical(filtera + filterb)
  df = df[filter,]
  
  # On ajoute les scores des couples
  xls_100 = read_excel("data/all_sampled_100_couples_all_columns.xlsx")
  names(df)[names(df) == "urla"] = "URL_two"
  names(df)[names(df) == "urlb"] = "URL_one"
  
  df = merge(df,xls_100[c("URL_one","URL_two","confidence_score", "strate_var_score")],by.x = c("URL_two","URL_one"), by.y = c("URL_one","URL_two"))
  
} else {
  
  source(file = "initdfpaire.R",encoding = "UTF-8")
  df = readRDS("saved.rds")
  html_available = list.files(path = "www/",pattern = "*.html")
  filtera = df$filea %in% html_available
  filterb = df$fileb %in% html_available
  filter = as.logical(filtera + filterb)
  df = df[filter,]
  }

# Stats sur le nombre de matchs par strate
statsbystrate = df %>%
  group_by(strate_var_score,decision) %>%
  summarise(f = n()) %>%
  filter(decision=="match")



# load functions
source(file = "fun.R",encoding = "UTF-8")
