import data_organize as do

data = do.get_data('secondary_rate_sec')
data = do.get_data('primary_isu')

rates = do.get_data('rates')
rates.index=rates.date
from matplotlib import pyplot as plt
rates.loc[rates.date>'2020-03-01' ,'国开10年'].plot()

date_list = data.date.unique()
date_list.sort()

for date in date_list:
    df = data.loc[data.date == date]
    print(date,end =',')
    print(df.loc[df['代码'] == '200215.IB'].shape[0] , end=':')
    print(df.loc[df['代码'] == '210205.IB'].shape[0])
    
d