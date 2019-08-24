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
  
} else {
  
  source(file = "initdfpaire.R",encoding = "UTF-8")
  df = readRDS("saved.rds")
  html_available = list.files(path = "www/",pattern = "*.html")
  filtera = df$filea %in% html_available
  filterb = df$fileb %in% html_available
  filter = as.logical(filtera + filterb)
  df = df[filter,]
  }

# load functions
source(file = "fun.R",encoding = "UTF-8")
