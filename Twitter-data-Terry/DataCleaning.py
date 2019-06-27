import pandas as pd

data = pd.read_csv("jpm-12Aug17-2015.csv",sep = ',',encoding="utf-8", error_bad_lines=False)
# data
data["combine"] =data["geo"] + " " + data["mentions"] + " " + data["hashtag"]+ " " + data["Unnamed: 8"]+ " " + data["Unnamed: 9"]+ " " + data["Unnamed: 10"] + " " + data["Unnamed: 11"] + " " + data["Unnamed: 12"] + " " + data["Unnamed: 13"]+ " " + data["Unnamed: 14"]
data.drop(['geo', 'mentions', 'hashtag','Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10','Unnamed: 11','Unnamed: 12','Unnamed: 13','Unnamed: 14',], axis=1, inplace=True)
data["text"] = data["text"] + " " + data["combine"]
del data["combine"]
tmp = data[~data['username'].str.contains('jpm')]
tmp.to_csv("jpm-12Aug17-2015-clean.csv",encoding='utf-8-sig',index=False)


data = pd.read_csv("jpm-today-12Aug17.csv",sep = ',',encoding="utf-8", error_bad_lines=False)
# data
data["combine"] =data["geo"] + " " + data["mentions"] + " " + data["hashtag"]+ " " + data["Unnamed: 8"]+ " " + data["Unnamed: 9"]+ " " + data["Unnamed: 10"] + " " + data["Unnamed: 11"] + " " + data["Unnamed: 12"] + " " + data["Unnamed: 13"]+ " " + data["Unnamed: 14"]
data.drop(['geo', 'mentions', 'hashtag','Unnamed: 8', 'Unnamed: 9', 'Unnamed: 10','Unnamed: 11','Unnamed: 12','Unnamed: 13','Unnamed: 14',], axis=1, inplace=True)
data["text"] = data["text"] + " " + data["combine"]
del data["combine"]
tmp = data[~data['username'].str.contains('jpm')]
tmp.to_csv("today-12Aug17-clean.csv",encoding='utf-8-sig',index=False)
