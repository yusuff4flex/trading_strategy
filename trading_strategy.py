import pandas as  pd
import numpy as np
#from get_sunrise_time import get_sunrise_time
#from get_sunset_time import get_sunset_time



df=pd.read_csv('nivData22.csv')

df = df.rename(columns={'Unnamed: 0': 'Time'})


df['Time'] = df['Time'].drop_duplicates()
df.dropna(subset=['Time'])

df2=pd.read_csv('trading_strategy.csv')

columns_to_remove=['Unnamed: 0', 'hour', 'Wind Day Ahead Forecast [in MW]',
       'Wind Intraday Forecast [in MW]', 'PV Day Ahead Forecast [in MW]',
       'PV Intraday Forecast [in MW]']
df2 = df2.drop(columns=columns_to_remove)

#print(df2.columns)

new_data=pd.concat([df[:len(df2)],df2],axis=1)


new_data=new_data.dropna(subset=['new_col'])

new_data['Time'] = pd.to_datetime(new_data['Time'],utc=True)
new_data['Time'] = new_data['Time'].dt.tz_convert('CET')
new_data['BETR.']=new_data['BETR.'].str.replace('.', '')
new_data['BETR.']=new_data['BETR.'].str.replace(',', '.')
new_data['BETR.']=new_data['BETR.'].astype(float)

new_data.to_csv('strategy.csv')
data=new_data.groupby([new_data['Time'].dt.date], group_keys=True).apply(lambda x: x)
data['date'] = data.index

data['date'] = data['date'].apply(lambda x: x[0])

data['new_col'] = data.groupby('date')['new_col'].transform(lambda x: range(1, len(x)+1))
data['Imbalance Price Quarter Hourly  [in EUR/MWh]'] = pd.to_numeric(data['Imbalance Price Quarter Hourly  [in EUR/MWh]'], errors='coerce')
data['Intraday Price Price Quarter Hourly  [in EUR/MWh]'] = pd.to_numeric(data['Intraday Price Price Quarter Hourly  [in EUR/MWh]'], errors='coerce')
data.reset_index(drop=True)

grouped_data = data.groupby('new_col').mean()
grouped_data['sunset_indicator'] = grouped_data.index
grouped_data.reset_index(drop=True)

#print(grouped_data.columns)

grouped_data['multiplicator'] = np.where(grouped_data['BETR.'] > 0, 0, -1)
dict=dict([(i,x) for i,x in zip(grouped_data['sunset_indicator'], grouped_data['multiplicator'])])
#print(dict)
data['multiplier']=data['new_col'].map(dict)
#print(data)
data['spread']=data['Imbalance Price Quarter Hourly  [in EUR/MWh]']-data['Intraday Price Price Quarter Hourly  [in EUR/MWh]']
data['PnL']=data['spread']*data['multiplier']
data['Cum_PnL']=data['PnL'].cumsum()
#print(data.columns)

data.to_csv('trading_strategy_new_2022.csv')
grouped_data.to_csv('trading_strategy_updated_2022.csv')

print(data)
data['date'] = pd.to_datetime(data['date'])
data['Year'] = data['date'].dt.year
data_2022=data['Year'] == 2022

data=data[data_2022]
data['month'] = data['date'].dt.month
#average_ida_and_rebap=data.groupby(data['month'], group_keys=True).apply(lambda x: x)
average_ida_and_rebap = data.groupby(['month', 'new_col'])
average_ida_and_rebap=average_ida_and_rebap[['Imbalance Price Quarter Hourly  [in EUR/MWh]','Day Ahead Price hourly [in EUR/MWh]']].mean()
average_ida_and_rebap.to_csv('average_rebap_and_Ida.csv')
print(average_ida_and_rebap)