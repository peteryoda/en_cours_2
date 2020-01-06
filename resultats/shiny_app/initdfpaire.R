# init df paire
# A ne lancer que la toute premiere fois
# construit le dataframe des paires avec les pages web sauvegardées associées

rm(list=ls())
dfurl = read.csv("data/idurl.csv",stringsAsFactors = F)
dfp = read.csv("data/paires.csv",stringsAsFactors = F)
dfurl$id = seq(0,nrow(dfurl)-1)
essai = merge(x = dfp,
              y =dfurl,
              by.x = "a",
              by.y = "url",
              all.x = T)
essai = merge(x = essai,
              y =dfurl,
              by.x = "b",
              by.y = "url",
              all.x = T)
names(essai) = c("urlb","urla","ida","idb")
essai$filea = paste0(essai$ida,".html")
essai$fileb = paste0(essai$idb,".html")
essai$id = seq(1,nrow(essai))

# On ajoute les scores des couples


saveRDS(object = essai,file = "saved.rds")
