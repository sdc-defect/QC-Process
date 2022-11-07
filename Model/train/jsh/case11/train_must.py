import json
from types import CoroutineType
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

whole_data = plt.figure('v2_data',figsize=(20,8))
def_group=["def_4933.jpeg",
"def_369.jpeg",
 "def_7603.jpeg",
 "def_6641.jpeg",
 "def_6296.jpeg", 
"def_7581.jpeg", 
"def_744.jpeg", 
"def_9547.jpeg", 
"def_7384.jpeg",
 "def_5128.jpeg", 
"def_4379.jpeg", 
"def_3812.jpeg",
 "def_571.jpeg", 
"def_7039.jpeg", 
"def_7553.jpeg", 
"def_7381.jpeg", 
"def_9640.jpeg",
 "def_356.jpeg", 
"def_7520.jpeg",
 "def_3394.jpeg",
 "def_6582.jpeg",
 "def_9206.jpeg",
 "def_8213.jpeg",
 "def_3818.jpeg",
"def_3735.jpeg",
"def_5892.jpeg",
 "def_966.jpeg",
 "def_8764.jpeg",
"def_4653.jpeg",
"def_4590.jpeg",
"def_5004.jpeg",
"def_3855.jpeg",
 "def_5221.jpeg",
"def_7797.jpeg",
"def_852.jpeg",
"def_556.jpeg",
"def_4032.jpeg",
"def_3148.jpeg",
"def_7396.jpeg",
"def_3354.jpeg",
 "def_7051.jpeg",
 "def_8486.jpeg",
 "def_8321.jpeg",
"def_9750.jpeg",
 "def_5094.jpeg",
"def_8587.jpeg",
"def_9613.jpeg",
 "def_102.jpeg",
"def_9038.jpeg",
"def_3431.jpeg"] 
def_count=[0]*50
with open("train_must_log.json", encoding='utf-8') as json_file:
    jdata = json_file.read()
    mustJSON = json.loads(jdata)
for i in range(len(mustJSON)):
    for j in range(len(def_group)):
        if mustJSON[str(i+1)][def_group[j]]['result']=='True':
            def_count[j]+=1
df_list2 = pd.DataFrame(def_count)
plt.plot(df_list2, color='#003049', label='def_count')
plt.axhline(50, 0, 1, color='lightgray', linestyle='--', linewidth=2)
plt.axhline(80, 0, 1, color='darkgray', linestyle='--', linewidth=2)
for i in range(50):
    if def_count[i]<50:
        plt.text(i,def_count[i],
         def_group[i],
         color='r',
         horizontalalignment='center',
         verticalalignment='top')
    elif def_count[i]<80:
        plt.text(i,def_count[i],
         def_group[i],
         color='#fcbf49',
         horizontalalignment='center',
         verticalalignment='top')
plt.savefig('./v2_data.png')