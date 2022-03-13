# -*- coding: utf-8 -*-
"""Edited Copy of Number of Textbooks needed_LSTM_additional_factors.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yS3nbGqJ5_niFCmDyGQaBIAAMSorc0Ju
"""

"""Import data ⚡"""
import streamlit as st

import pandas as pd

import seaborn as sns
import numpy as np

from gsheetsdb import connect

import matplotlib.pyplot as pyplot
import datetime

gsheet_url = "https://docs.google.com/spreadsheets/d/13zqKByCKmAp4470U4audPRMtoRwo4APO/edit#gid=253062979"
conn = connect()
rows = conn.execute(f'SELECT * FROM "{gsheet_url}"')
df = pd.DataFrame(rows)

textbook_df = df[['LEVEL_EXTRACT_3', 'Registration_Date', 'Textbook_Price', 'Student Name', 'Sheet', 'COMBINED_EXTRACTED_START_DATE']].copy()
textbook_df = textbook_df.loc[textbook_df['Sheet']>2011]
textbook_df['Textbook_Price'] = textbook_df['Textbook_Price'].apply(lambda x: x.upper().strip() if isinstance(x, str) else x)
#str upper changed to nans, try applying only when its a string

textbook_df = textbook_df[~textbook_df['Textbook_Price'].isin(['.', '-', 'X', 'O'])]
textbook_df.dropna(subset=['Textbook_Price'], inplace=True)
#we only want those that bought the textbook/ given away for free also

#if the rest cannot match, just replace with class start date
textbook_df['Registration_Date'] = textbook_df.apply(lambda x: x['Registration_Date'] if isinstance(x['Registration_Date'], datetime.datetime) else pd.to_datetime(x['COMBINED_EXTRACTED_START_DATE']), axis=1)

#B1 & B2
B1_df = textbook_df.loc[textbook_df['LEVEL_EXTRACT_3'].isin(['B1', 'B2'])]
B1_df = B1_df.groupby('Registration_Date')['Student Name'].count()
B1_df_daily=B1_df.loc[(B1_df.index>'2010-01-01') & (B1_df.index<'2022-01-01')] #drop one wrongly entered year
#fill in the missing gaps with 0
date_range = pd.DataFrame(pd.date_range(start='1/1/2012', end='30/12/2021'), columns=['date'])
B1_df_daily = date_range.merge(B1_df_daily, how='left', left_on='date', right_on='Registration_Date')
B1_df_daily = B1_df_daily.fillna(0).set_index('date').iloc[:, 0]
st.write(sns.lineplot(data = B1_df_daily, x= B1_df_daily.index, y=B1_df_daily.values))

#aggregate to annual (bulk purchase) - basically follows same trend as the class size

B1_df = textbook_df.loc[textbook_df['LEVEL_EXTRACT_3'].isin(['B1','B2'])]
B1_df = B1_df.groupby(pd.Grouper(key = 'Registration_Date', freq = '1AS'))['Student Name'].count()
B1_df=B1_df.loc[(B1_df.index>'2010-01-01') & (B1_df.index<'2022-01-01')] #drop one wrongly entered year
st.write(sns.lineplot(data = B1_df, x= B1_df.index, y=B1_df.values))

"""LSTM Time! :)

Import Additional Factors
"""

#korean interest

#elearning trend --> how to incorporate into the model since the train and test are separated? :(

#social media presence

#elearning trend

#duolingo trend




# #START HERE!!!!

# duolingo_df = pd.read_excel('/content/drive/My Drive/BA FYP/Data for Prediction/duolingo 2016-2021.xlsx')

# duolingo_df = duolingo_df.iloc[:, :2]

# duolingo_df

# sns.lineplot(data = duolingo_df, x = 'Year', y='MAU (millions)')

# #competitor trend

# competitor_df = pd.read_excel('/content/drive/My Drive/BA FYP/Data for Prediction/Korean School Competitor Numbers.xlsx', sheet_name='Cleaned')

# competitor_df['Year'] = competitor_df['Year'].astype(str).str.split('.').str[0]

# sns.lineplot(data = competitor_df, x='Year', y='Total Branches Open')

# #korean interest

# learn_korean_df = pd.read_excel('/content/drive/My Drive/BA FYP/Data for Prediction/SGSearchLearnKorean (1).xlsx', sheet_name='Cleaned')
# learn_korean_df['date']=pd.to_datetime(learn_korean_df['Month'])
# sns.lineplot(data = learn_korean_df, x='date', y='Interest Relative to Peak (out of 100)')

# #covid government measures

# covid_stringency_df = pd.read_csv('/content/drive/My Drive/BA FYP/Data for Prediction/covid_oxford.csv')

# covid_stringency_df = covid_stringency_df[covid_stringency_df['CountryName']=='Singapore'][['Date','StringencyIndex']]

# covid_stringency_df['Date'] = pd.to_datetime(covid_stringency_df['Date'], format='%Y%m%d')

# covid_stringency_df = covid_stringency_df.groupby(pd.Grouper(key='Date', freq='1MS'))['StringencyIndex'].mean().to_frame()
# #get mean for each month

# #engineered feature -- online learning available?

# #according to excel online started in july
# online_class_df = pd.DataFrame(pd.date_range(start='2020-04-01', end='2022-03-01', freq='1MS'))

# online_class_df['Online?']=1

# online_class_df.columns=['Date', 'Online?']
# online_class_df= online_class_df.set_index('Date')



# #social media

# # social_media_df = pd.read_excel('/content/drive/My Drive/BA FYP/Data for Prediction/Social Media.xlsx')

# # social_media_df['Starts']

# # social_media_df['Reach']

# #try each factor 1 by 1

# ! pip install ray[tune]
# #maybe can just use normal pytorch early stopping inside

# from ray import tune
# from ray.tune import CLIReporter
# from ray.tune.schedulers import ASHAScheduler

# import numpy as np
# import matplotlib.pyplot as plt
# import pandas as pd
# import torch
# import torch.nn as nn
# from torch.autograd import Variable
# from sklearn.preprocessing import MinMaxScaler

# #aggregate to monthly - how many books need to be bought per month?

# #B1+B2
# B1_df = textbook_df.loc[textbook_df['LEVEL_EXTRACT_3'].isin(['B1', 'B2'])]
# B1_monthly_df = B1_df.groupby(pd.Grouper(key = 'Registration_Date', freq = '1MS'))['Student Name'].count()
# B1_monthly_df = B1_monthly_df.loc[(B1_monthly_df.index>'2010-01-01') & (B1_monthly_df.index<'2022-01-01')] #drop one wrongly entered year
# #fill in the missing gaps with 0
# date_range = pd.DataFrame(pd.date_range(start='1/1/2012', end='30/12/2021', freq = '1MS'), columns=['date'])
# B1_monthly_df = date_range.merge(B1_monthly_df, how='left', left_on='date', right_on='Registration_Date')
# B1_monthly_df = B1_monthly_df.fillna(0).set_index('date').iloc[:, 0]
# sns.lineplot(data = B1_monthly_df, x= B1_monthly_df.index, y=B1_monthly_df.values)

# #only student count for now
# B1_monthly_df = B1_monthly_df.to_frame('Student_Count')

# # B1_monthly_df['dummy'] = range(len(B1_monthly_df))

# class MyDataset(torch.utils.data.Dataset):
#     def __init__(self, data, window):
#         self.data = data
#         self.window = window

#     def __getitem__(self, index):
#         x = self.data.iloc[index-self.window:index].values
#         y = self.data.iloc[index]['Student_Count']
#         return x, y

#     def __len__(self):
#         return len(self.data)

# # config = {
# #     "LR": tune.loguniform(1e-3, 1e-2),
# #     "hidden_size": tune.sample_from(lambda _: np.random.randint(2, 5)),
# #     "num_layers": tune.choice([1]),
# #     "seq_length": tune.sample_from(lambda _: np.random.randint(2, 6))
# # }

# config = {
#     "LR": tune.loguniform(4e-3, 6e-3),
#     "hidden_size": tune.sample_from(lambda _: np.random.randint(4, 6)),
#     "num_layers": tune.choice([1, 2]),
#     "seq_length": tune.sample_from(lambda _: np.random.randint(3, 5))
# }

# train_size = len(B1_monthly_df)-6
# #CHANGED FROM 75% OF DATASET!

# B1_monthly_df_w_korean = B1_monthly_df.merge(learn_korean_df, on='date', how='left').drop(columns=['Month']).set_index('date')

# #merging datasets

# B1_monthly_df_w_korean['Year'] = B1_monthly_df_w_korean.index.year
# #only started korean in 2017
# duolingo_df = duolingo_df.iloc[1:, :]
# B1_monthly_df_w_korean_duo = B1_monthly_df_w_korean.merge(duolingo_df , how='left', on='Year')
# B1_monthly_df_w_korean_duo['MAU (millions)'] = B1_monthly_df_w_korean_duo['MAU (millions)'].fillna(0)

# #merge competitors
# competitor_df['Year'] = competitor_df['Year'].astype(int)
# B1_monthly_df_w_korean_duo_compet = B1_monthly_df_w_korean_duo.merge(competitor_df, how='left', on='Year')
# B1_monthly_df_w_korean_duo_compet.index = B1_monthly_df_w_korean.index

# #merge covid stringency
# B1_monthly_df_w_korean_duo_compet_stringency = B1_monthly_df_w_korean_duo_compet.merge(covid_stringency_df, how='left', left_index=True, right_on='Date').set_index('Date')

# B1_monthly_df_w_korean_duo_compet_stringency['StringencyIndex'] = B1_monthly_df_w_korean_duo_compet_stringency['StringencyIndex'].fillna(0)

# B1_monthly_df_training = B1_monthly_df_w_korean_duo_compet_stringency.copy()
# val_size = 4

# B1_monthly_df_training = B1_monthly_df_training.drop(columns=['Year'])

# train_data = B1_monthly_df_training.iloc[:train_size-val_size]

# #standardisation

# from sklearn.preprocessing import StandardScaler

# sc = StandardScaler()
# #fit only on train data
# scaler = sc.fit(train_data[train_data.columns])

# #transform on entire dataset
# B1_monthly_df_training[B1_monthly_df_training.columns] = scaler.transform(B1_monthly_df_training[B1_monthly_df_training.columns])



# #merge online class - dont standardise binary variable
# B1_monthly_df_training = B1_monthly_df_training.merge(online_class_df, how='left', left_index=True, right_index=True)
# B1_monthly_df_training['Online?'] = B1_monthly_df_training['Online?'].fillna(0)

# # val_data = B1_monthly_df_training.iloc[train_size-val_size:train_size]

# #using another 6 months as validation might be okay

# # train_data[train_data['StringencyIndex']!=0]

# # B1_monthly_df_training[60:88]

# from torch.utils.data import Subset
# from torch.utils.data import DataLoader

# class LSTM(nn.Module):

#     def __init__(self, num_classes, input_size, hidden_size, num_layers):
#         super(LSTM, self).__init__()
        
#         self.num_classes = num_classes
#         self.num_layers = num_layers
#         self.input_size = input_size
#         self.hidden_size = hidden_size
        
#         self.lstm = nn.LSTM(input_size=input_size, hidden_size=hidden_size,
#                             num_layers=num_layers, batch_first=True)
        
#         self.fc = nn.Linear(hidden_size, num_classes)


#     def forward(self, x):
#         # Propagate input through LSTM
#         h_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size)).requires_grad_()
#         c_0 = Variable(torch.zeros(self.num_layers, x.size(0), self.hidden_size)).requires_grad_()

#         ula, (h_out, _) = self.lstm(x, (h_0, c_0))

#         out = self.fc(h_out[0]).flatten()
        
#         return out

# # !cp 'drive/MyDrive/BA FYP/Data for Prediction/early_stopping_script.py' .

# import os

# # B1_monthly_df_training.iloc[int(train_size*0.67)-3: train_size]

# # import EarlyStopping from early_stopping_script.py

# #train should include the non zero values as well, check the inclusion!

# # df1 = B1_monthly_df_training.iloc[:int(len(B1_monthly_df_training)*0.95), :]
# # df1.groupby('Online?').count()

# # B1_monthly_df_training.iloc[int(len(B1_monthly_df_training)*0.95):, :]

# # dataset = MyDataset(B1_monthly_df_training, 3)
# # test_dataset = Subset(dataset, range(train_size, len(dataset)))
# # testloader = DataLoader(test_dataset, batch_size=3, shuffle=False)

# # iter_test = iter(testloader)

# # iter_test.next()

# # B1_monthly_df_training[: train_size-val_size].groupby('Online?').count() #ok maybe val can be a bit smaller.

# def train_lstm(config, checkpoint_dir='drive/MyDrive/BA FYP/Data for Prediction', data_dir=None):
#     #optimise value
#     seq_length = config['seq_length']
#     dataset = MyDataset(B1_monthly_df_training, seq_length)

#     #start from window size onwards

#     train_dataset = Subset(dataset, range(config['seq_length'], train_size-val_size))
#     val_dataset = Subset(dataset, range(train_size-val_size, train_size))
#     test_dataset = Subset(dataset, range(train_size, len(dataset)))

#     #use entire dataset for each batch
#     trainloader = DataLoader(train_dataset, batch_size=3, shuffle=False)
#     valloader = DataLoader(val_dataset, batch_size=3, shuffle=False)
#     testloader = DataLoader(test_dataset, batch_size=3, shuffle=False)


#     num_epochs = 40
#     # learning_rate = 0.01
#     learning_rate = config['LR']

#     input_size = 6 #RMBR TO CHANGE THIS! WHEN U ADD VARIABLES!
#     hidden_size = config['hidden_size']
#     num_layers = config['num_layers']

#     num_classes = 1

#     # print(num_classes, input_size, hidden_size, num_layers)

#     lstm = LSTM(num_classes, input_size, hidden_size, num_layers)

#     criterion = torch.nn.MSELoss()    # mean-squared error for regression
#     optimizer = torch.optim.Adam(lstm.parameters(), lr=learning_rate)
#     #optimizer = torch.optim.SGD(lstm.parameters(), lr=learning_rate)

#     if checkpoint_dir:
#         model_state, optimizer_state = torch.load(
#             os.path.join(checkpoint_dir, "checkpoint"))
#         lstm.load_state_dict(model_state)
#         optimizer.load_state_dict(optimizer_state)

#     # Train the model
#     for epoch in range(num_epochs):

#         #train phase
#         lstm.train()
#         optimizer.zero_grad()

#         #get training x and y
#         total_train_loss = 0
#         train_steps = 0
#         for i, batch in enumerate(trainloader):
#           train_x, train_y = batch[0], batch[1]
#           outputs = lstm(train_x.float())

#           # print(i)
#           # print('output', outputs) #CHECKING BUG
#           # print('actual', train_y)
#           # print('actual_float', train_y.float().size(), train_y.float())
#           # print('squeeze o/p', np.squeeze(outputs))
          
#           # obtain the loss
#           loss = criterion(outputs, train_y.float()) #remove squeeze op
#           loss.backward()
          
#           optimizer.step()

#           total_train_loss +=loss.item()
#           train_steps +=1

#         #validation phase
#         lstm.eval()

#         #get validation data
#         total_val_loss = 0
#         val_steps = 0
#         for i, batch in enumerate(valloader):
#           val_x, val_y = batch[0], batch[1]
#           outputs = lstm(val_x.float())

#           # obtain the loss
#           val_loss = criterion(outputs, val_y.float()).item() #removed squeeze
#           total_val_loss +=val_loss
#           val_steps+=1

#         if epoch % 100 == 0:
#           print("Epoch: %d, train loss: %1.5f" % (epoch, total_train_loss/train_steps))
#           print("Epoch: %d, validation loss: %1.5f" % (epoch, total_val_loss/val_steps))


#         with tune.checkpoint_dir(epoch) as checkpoint_dir:
#             path = os.path.join(checkpoint_dir, "checkpoint")
#             torch.save((lstm.state_dict(), optimizer.state_dict()), path)

#         avg_val_loss = total_val_loss/val_steps
#         # print(avg_val_loss)
#         tune.report(loss=avg_val_loss)

#     print("Finished Training")

# train_size-val_size

# def get_loaders(config):
#     #optimise value
#     seq_length = config['seq_length']
#     dataset = MyDataset(B1_monthly_df_training, seq_length)

#     #start from window size onwards

#     train_dataset = Subset(dataset, range(seq_length, train_size-val_size))
#     val_dataset = Subset(dataset, range(train_size-val_size, train_size))
#     test_dataset = Subset(dataset, range(train_size, len(dataset)))

#     #use entire dataset for each batch
#     trainloader = DataLoader(train_dataset, batch_size=3, shuffle=False)
#     valloader = DataLoader(val_dataset, batch_size=3, shuffle=False)
#     testloader = DataLoader(test_dataset, batch_size=3, shuffle=False)

#     return trainloader, valloader, testloader, dataset

# reporter = CLIReporter(
#         # parameter_columns=["l1", "l2", "lr", "batch_size"],
#         metric_columns=["loss", "training_iteration"])

# analysis = tune.run(
#     train_lstm,
#     num_samples=5,
#     scheduler=ASHAScheduler(metric="loss", mode="min"),
#     config=config,
#     progress_reporter=reporter)

# #https://datascience.stackexchange.com/questions/36861/how-to-add-confidence-to-models-prediction

# #ADD THIS CALCULATION IN!

# # config={'LR': 0.005, 'hidden_size': 5, 'num_layers': 1, 'seq_length': 4}

# best_trial = analysis.get_best_trial("loss", "min", "last")
# print("Best trial config: {}".format(best_trial.config))
# print("Best trial final validation loss: {}".format(
#     best_trial.last_result["loss"]))

# #get best model

# lstm = LSTM(num_classes=1, input_size=6, hidden_size=best_trial.config['hidden_size'], num_layers=best_trial.config['num_layers'])

# best_checkpoint_dir = best_trial.checkpoint.value
# model_state, optimizer_state = torch.load(os.path.join(
#     best_checkpoint_dir, "checkpoint"))
# lstm.load_state_dict(model_state)

# trainloader, valloader, testloader, dataset = get_loaders(best_trial.config)

# # lstm, trainloader, testloader, valloader = train_lstm(config)

# criterion = torch.nn.MSELoss()

# total_loss = []
# outputs = []
# train_steps = 0
# for i, batch in enumerate(trainloader):
#   lstm.eval()
#   test_x, test_y = batch[0], batch[1]
#   output = lstm(test_x.float())
#   loss = criterion(output, test_y.float())
#   total_loss.append(loss.item())
#   outputs.append(output)
#   train_steps+=1
# print(f'training loss is: {sum(total_loss)/train_steps}')
# print(len(torch.cat(outputs)))

# total_loss = []
# val_steps = 0
# for i, batch in enumerate(valloader):
#   lstm.eval()
#   test_x, test_y = batch[0], batch[1]
#   output = lstm(test_x.float())
#   loss = criterion(output, test_y.float())
#   total_loss.append(loss.item())
#   outputs.append(output)
#   val_steps+=1
# print(f'validation loss is: {sum(total_loss)/val_steps}')
# print(len(torch.cat(outputs)))

# total_loss = []
# test_steps = 0
# for i, batch in enumerate(testloader):
#   lstm.eval()
#   test_x, test_y = batch[0], batch[1]
#   output = lstm(test_x.float())
#   loss = criterion(output, test_y.float())
#   total_loss.append(loss.item())
#   outputs.append(output)
#   test_steps+=1
# print(f'testing loss is: {sum(total_loss)/test_steps}')
# print(len(torch.cat(outputs)))

# data_predict = torch.cat(outputs)

# scaling_df  = pd.DataFrame(torch.cat(outputs).detach().numpy().reshape(-1, 1), columns=['Student_Count'])
# scaling_df['Interest Relative to Peak (out of 100)'] = 0

# scaling_df['MAU (millions)'] = 0
# scaling_df['Total Branches Open'] = 0
# scaling_df['StringencyIndex'] = 0
# # scaling_df['Online?'] = 0

# scaling_df

# data_predict_inv = scaler.inverse_transform(scaling_df)
# # test_w_predict = B1_monthly_df.iloc[4:train_size].copy()
# test_w_predict = B1_monthly_df.iloc[best_trial.config['seq_length']:].copy()
# test_w_predict['Predicted_Student_Count'] = pd.DataFrame(data_predict_inv)[0].to_numpy()

# plot_df = B1_monthly_df.iloc[best_trial.config['seq_length']:].merge(test_w_predict, on='date', how='left')
# plot_df[['Student_Count_x', 'Predicted_Student_Count']].plot()
# pyplot.show()

# #the lags should be able to get from the previous segment of data (if not the val and test end up with less rows) --> include
# #them in the datasets
# B1_monthly_df_training[train_size:]

# B1_monthly_df_training[train_size-val_size:train_size]



# from sklearn.metrics import r2_score

# test_df = test_w_predict[test_w_predict.index>='2019-08-01'].copy()
# y_true = test_df['Student_Count']
# y_estimate = test_df['Predicted_Student_Count']

# r2_score(y_true, y_estimate)

# """this is the baseline model LOLOL - in case i cant come up with anything later"""

# stop

# #kind of seems like it can learn from the data to some extent, so the code itself is probably not the cause

# dfs = analysis.trial_dataframes
# # Plot by epoch
# ax = None  # This plots everything on the same plot
# for d in dfs.values():
#     ax = d.loss.plot(ax=ax, legend=False)

# #wait it doesnt seem to be learning at all.... ->-



# #get the test data

# seq_length = best_trial.config['seq_length']
# dataset = MyDataset(B1_monthly_df_training, seq_length)

# #start from window size onwards
# test_dataset = Subset(dataset, range(train_size, len(dataset)))

# #use entire dataset for each batch
# testloader = DataLoader(test_dataset, batch_size=len(test_dataset), shuffle=False)

# criterion = torch.nn.MSELoss()

# for batch in testloader:
#   best_trained_model.eval()
#   test_x, test_y = batch[0], batch[1]
#   output = best_trained_model(test_x.float())
#   loss = criterion(output, test_y.float()).item()
#   print(f'testing loss is: {loss}')

# dataset = MyDataset(B1_monthly_df_training, seq_length)

# #start from window size onwards

# train_dataset = Subset(dataset, range(seq_length, int(train_size*0.9)))
# # val_dataset = Subset(dataset, range(int(train_size*0.9), train_size))
# # test_dataset = Subset(dataset, range(train_size, len(dataset)))

# #use entire dataset for each batch
# trainloader = DataLoader(train_dataset, batch_size=len(train_dataset), shuffle=False)

# criterion = torch.nn.MSELoss()

# for batch in trainloader:
#   best_trained_model.eval()
#   test_x, test_y = batch[0], batch[1]
#   output = best_trained_model(test_x.float())
#   loss = criterion(output, test_y.float()).item()
#   data_predict = scaler.inverse_transform(output.data.numpy())

#   print(f'training loss is: {loss}')

# # data_predict = output.data.numpy()
# # data_predict = scaler.inverse_transform(data_predict)
# test_w_predict = B1_monthly_df.iloc[:len(data_predict)].copy()
# test_w_predict['Predicted_Student_Count'] = data_predict

# plot_df = B1_monthly_df.reset_index().merge(test_w_predict, on='date', how='left')
# plot_df.set_index('date')[['Student_Count_x', 'Predicted_Student_Count']].plot()
# pyplot.show()
# #not so good lmao

# plot_df['Student_Count_x'].plot()

# plot_df['Student_Count_y'].plot()

# plot_df['Predicted_Student_Count'].plot()
