import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
whole_data = plt.figure(figsize=(15,8))

log_data=pd.read_csv('train_log.csv',encoding = 'utf-8',index_col=0)
log_data1=log_data['train_loss']
log_data2=log_data[ 'train_accuracy']
log_data3=log_data['train_recall']
log_data4=log_data['train_f1']
log_data5=log_data['val_loss']
log_data6=log_data['val_accuracy']
log_data7=log_data['val_recall']
log_data8=log_data['val_f1']

whole_data.add_subplot(3, 2, 1)  
plt.plot(log_data2, color='#d62828', marker='o', linestyle='dashed',label= 'train_accuracy')
plt.plot(log_data3, color='#003049', marker='o', linestyle='dashed',label='train_recall')
plt.plot(log_data4, color='#fcbf49', marker='o', linestyle='dashed',label='train_f1')
plt.yticks([0,0.2,0.4,0.6,0.8,1])
plt.grid(True,axis='y',linestyle='--')
plt.legend()

whole_data.add_subplot(3, 2, 2)  
plt.plot(log_data6, color='#d62828', marker='o', linestyle='solid',label= 'val_accuracy')
plt.plot(log_data7, color='#003049', marker='o', linestyle='solid',label='val_recall')
plt.plot(log_data8, color='#fcbf49', marker='o', linestyle='solid',label='val_f1')
plt.yticks([0,0.2,0.4,0.6,0.8,1])
plt.grid(True,axis='y',linestyle='--')
plt.legend()

whole_data.add_subplot(3, 2, 3)  
plt.plot(log_data1, color='#d62828', marker='o', linestyle='dashed', label='train_loss')
plt.plot(log_data5, color='#003049', marker='o', linestyle='solid',label= 'val_loss')
plt.yticks([0,0.2,0.4,0.6,0.8,1])
plt.grid(True,axis='y',linestyle='--')
plt.legend()

whole_data.add_subplot(3, 2, 4)  
plt.plot(log_data2, color='#d62828', marker='o', linestyle='dashed', label='train_accuracy')
plt.plot(log_data6, color='#003049', marker='o', linestyle='solid',label= 'val_accuracy')
plt.yticks([0,0.2,0.4,0.6,0.8,1])
plt.grid(True,axis='y',linestyle='--')
plt.legend()

whole_data.add_subplot(3, 2, 5)  
plt.plot(log_data3, color='#d62828', marker='o', linestyle='dashed', label='train_recall')
plt.plot(log_data7, color='#003049', marker='o', linestyle='solid',label= 'val_recall')
plt.yticks([0,0.2,0.4,0.6,0.8,1])
plt.grid(True,axis='y',linestyle='--')
plt.legend()
plt.xlabel('epoch')

whole_data.add_subplot(3, 2, 6)  
plt.plot(log_data4, color='#d62828', marker='o', linestyle='dashed', label='train_f1')
plt.plot(log_data8, color='#003049', marker='o', linestyle='solid',label= 'val_f1')
plt.yticks([0,0.2,0.4,0.6,0.8,1])
plt.grid(True,axis='y',linestyle='--')
plt.legend()
plt.xlabel('epoch')

plt.savefig('./train_data.png')