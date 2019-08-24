# install.packages("readxl")
library(readxl)
library(ggplot2)

# Jointure saved.rds et le fichier Excel des 100 couples
saved = readRDS("resultats/shiny_app/saved.rds")
xls_100 = read_excel("resultats/all_sampled_100_couples.xlsx")

# names(saved)
names(saved)[names(saved) == "urla"] = "URL_two"
names(saved)[names(saved) == "urlb"] = "URL_one"

df_merged = merge(saved,xls_100[c("URL_one","URL_two","confidence_score", "strate_var_score")],by.x = c("URL_two","URL_one"), by.y = c("URL_one","URL_two"))

table(df_merged$decision)
table(df_merged$strate_var_score)

# Distribution de decision par strates
filter = df_merged$decision == "doubt"
df_merged_doubt = df_merged[filter,]
table(df_merged_doubt$strate_var_score)

# Distribution des match vs unmatch
df_eval = df_merged[which(df_merged$decision != "doubt"),]
df_eval_svg = df_eval

# Changer les "cont diff" en "match"
# df_eval$decision_modified = ifelse(df_eval$decision == "cont diff","match",df_eval$decision)
# Changer les "cont diff" en "doubt"
df_eval$decision_modified = ifelse(df_eval$decision == "cont diff","doubt",df_eval$decision)

# % des match par strates
tab_temp = table(df_eval$decision_modified,df_eval$strate_var_score)
# install.packages("gmodels")
# library(gmodels)
# CrossTable(df_eval$decision, df_eval$strate_var_score) 
prop.table(tab_temp,2)
str(prop.table(tab_temp,2))

mytable = prop.table(tab_temp,2)

# Plot des % de match par strate
# x = as.numeric(names(mytable[1,]))
# y = mytable[1,]
# plot(y[order(x,decreasing = F)],type="l")
mydf = as.data.frame(mytable, stringsAsFactors = FALSE)
names(mydf) = c("decision","strate","f")

# class(mydf$strate)
mydf$strate = as.numeric(mydf$strate)
mydf = mydf[order(mydf$strate,decreasing=FALSE),]

df_temp = mydf[mydf$decision == "match",]
# Correction / interpolation de strate = 9
# df_temp$f[df_temp$strate == 9] = 0.8815

# y = mydf$f[mydf$decision == "match"]
# y = df_temp$f
# plot(y,type = 'l',ylim = c(0,1))

# names(df_temp)[names(df_temp) == "f"] = "prop_match"
ggplot(df_temp, aes(strate, f)) + geom_line() + ylim(c(0,1)) + ggtitle("Model performance")
# lapply(df_temp,class)

# mydfroc= mydf[mydf$decision=="match",]
mydfroc= df_temp
rownames(mydfroc) = NULL
# Nombre de valeurs observées = "match" pour chaque strate

# Correction / interpolation de strate = 9
# mydfroc$f[mydfroc$strate == 9] = 0.945
mydfroc$f[mydfroc$strate == 9] = 0.8815

mydfroc$nb_match = mydfroc$f * 10
total_match = sum(mydfroc$nb_match)

mydfroc = mydfroc[order(mydfroc$strate,decreasing = TRUE),]
mydfroc$cum_nb_match = cumsum(mydfroc$nb_match)

mydfroc$score = mydfroc$cum_nb_match / total_match
#plot(mydfroc$score,type="l",ylim = c(0,1))
mydfroc$strate = 11 - mydfroc$strate
mydfroc = rbind(c(0,0,0,0,0,0),mydfroc)
# ggplot(mydfroc, aes(strate, score)) + geom_line() + ylim(c(0,1))

mydfroc$decision[mydfroc$strate == 0] = "match"

names(mydfroc)
lapply(mydfroc, class)
# "decision","strate","f","nb_match", "cum_nb_match", "score"
mydfroc$decision = "chunking"
decision = c("random","random")
strate = c(0,10)
f = c(0,0)
nb_match = c(0,0)
cum_nb_match = c(0,0)
score = c(0,1)
dfbiss = data.frame(decision,strate,f,nb_match,cum_nb_match,score)
mydfroc = rbind(mydfroc,dfbiss)

names(mydfroc)[names(mydfroc) == "decision"] = "model"
names(mydfroc)[names(mydfroc) == "score"] = "recall"
ggplot(mydfroc, aes(strate, recall, color = model)) + geom_line() + ylim(c(0,1)) + ggtitle("ROC curve")

lapply(mydfroc, class)
auc = (sum(mydfroc$recall) - 1) / 10
auc
# 0.65800
# On a : 0.653968





