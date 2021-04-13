import pickle
import pandas as pd

bot_names = pd.read_csv('dataset/botnames.csv', names=['screen_name_from'])
fastest_df = pd.read_csv('shares_df_2018_6_10.csv')
bots_in_SWM_dataset = fastest_df[(fastest_df['screen_name_to'].isin(bot_names['screen_name_from']))]
df1 = bots_in_SWM_dataset.drop_duplicates(subset=['screen_name_to'])
bots_in_SWM_dataset = fastest_df[(fastest_df['screen_name_from'].isin(bot_names['screen_name_from']))]
df2 = bots_in_SWM_dataset.drop_duplicates(subset=['screen_name_from'])
print ('total unique bots in this dataset: ',len(df1)+len(df2))

with open('graph_pickled_2018_6_10_q10_visualization.pkl', 'rb') as f:
    data = pickle.load(f)
    nodes = [node[0] for node in data.nodes(data=True)]


print ('unique nodes in the graph (result of algorithm)',len(nodes))
TP=1
TN=1
FP=1
FN=1
bot_names = pd.read_csv('dataset/botnames.csv', names=['screen_name_from'])

for i,r in fastest_df.iterrows():
    if r['is_coordinated']==True and r['screen_name_to'] in nodes:
        if bot_names['screen_name_from'].str.contains(r['screen_name_to']).any()==True:
            TP = TP+1
        elif bot_names['screen_name_from'].str.contains(r['screen_name_to']).any()==False:
            FP+=1
    elif r['is_coordinated']==True and r['screen_name_to'] not in nodes:
        if bot_names['screen_name_from'].str.contains(r['screen_name_to']).any()==True:
            FN+=1
        elif bot_names['screen_name_from'].str.contains(r['screen_name_to']).any()==False:
            TN+=1
    elif r['is_coordinated']==False and r['screen_name_to'] not in nodes:
        if bot_names['screen_name_from'].str.contains(r['screen_name_to']).any()==False:
            TN+=1
        elif bot_names['screen_name_from'].str.contains(r['screen_name_to']).any()==True:
            FN+=1
    elif r['is_coordinated']==False and r['screen_name_to'] in nodes:
        if bot_names['screen_name_from'].str.contains(r['screen_name_to']).any()==False:
            FP+=1
        elif bot_names['screen_name_from'].str.contains(r['screen_name_to']).any()==True:
            TP = TP+1


print ('TP =',TP)
print ('TN =',TN)
print ('FP =',FP)
print ('FN =',FN)

accuracy = (TP+TN)/(TP+FP+TN+FN)
precision = TP/(TP+FP)
recall = TP/(TP+FN)

print ('accuracy',accuracy)
print ('precision',precision)
print ('recall',recall)

# print ('Total =',len(fastest_df))
# bots_in_SWM_dataset = fastest_df[(fastest_df['screen_name_to'].isin(bot_names['screen_name_from']))]
# print ('Total Bots',len(bots_in_SWM_dataset))
# non_bots_in_SWM_dataset = fastest_df[(~fastest_df['screen_name_to'].isin(bot_names['screen_name_from']))]
# print ('Total Non-Bots',len(non_bots_in_SWM_dataset))



