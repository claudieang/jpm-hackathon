import pandas as pd

data = pd.read_csv("jpm-12Aug17-2015.csv",sep = ';,',encoding="utf-8", error_bad_lines=False)
data.columns = ['user','date','retweets','likes','text','geo','mention','tag']
tmp = data[~data['user'].str.contains('jpm')]
tmp.to_csv("jpm-12Aug17-2015-clean.csv",encoding='utf-8-sig',index=False)


data = pd.read_csv("jpm-today-12Aug17.csv",sep = ';,',encoding="utf-8", error_bad_lines=False)
data.columns = ['user','date','retweets','likes','text','geo','mention','tag']
tmp = data[~data['user'].str.contains('jpm')]
tmp.to_csv("jpm-today-12Aug17-clean.csv",encoding='utf-8-sig',index=False)


