# install.packages("readxl")
library("readxl")


# Jointure saved.rds et le fichier Excel des 100 couples
saved = readRDS("~/proj/en_cours_2/résultats/shiny_app/saved.rds")


xls_100 = read_excel("~/proj/en_cours_2/résultats/all_sampled_100_couples.xlsx")

# names(saved)
names(saved)[names(saved) == "urla"] = "URL_two"
names(saved)[names(saved) == "urlb"] = "URL_one"
# names(xls_100)
df_merged = merge(saved,xls_100[c("URL_one","URL_two","confidence_score", "strate_var_score")],by.x = c("URL_two","URL_one"), by.y = c("URL_one","URL_two"))

table(df_merged$decision)
table(df_merged$strate_var_score)

# Distribution de decision par strates
filter = df_merged$decision == "doubt"
df_merged_doubt = df_merged[filter,]
table(df_merged_doubt$strate_var_score)

# Distribution des match vs unmatch
df_eval = df_merged[which(df_merged$decision != "doubt"),]

# % des match par strates
tab_temp = table(df_eval$decision,df_eval$strate_var_score)
# install.packages("gmodels")
# library(gmodels)
# CrossTable(df_eval$decision, df_eval$strate_var_score) 
prop.table(tab_temp,2)

str(prop.table(tab_temp,2))

# Changer les "cont diff" en "match"

# Plot des % de match par strate
