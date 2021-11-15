import pandas as pd
import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def convert_date_format(date):
    '''
    Convert the date from the string format given by Cake into the datetime object.
    '''
    
    year = int(date[:4])
    month = int(date[5:7])
    day = int(date[8:10])
    hour = int(date[11:13])
    minute = int(date[14:16])
    second = int(date[17:19])
    
    return datetime.datetime(year,month,day,hour,minute,second)


def load_transactions(path):
    
    data = pd.read_csv(path).iloc[::-1].reset_index(drop=True)
    data['Date'] = data.Date.apply(convert_date_format)
    
    return data

def rewards_report(data, asset):
    
    delta = datetime.timedelta(days=1)
    earnings_to_consider = ["Staking reward", 
                            "Freezer staking bonus",
                            "Liquidity mining reward BTC-DFI",
                            "10 years freezer reward",
                            "Freezer liquidity mining bonus"]

    start_date = data.Date.iloc[0]
    end_date = data.Date.iloc[-1]


    report = {'description': "{} rewards".format(asset),
              'asset':asset,
              'date': [],
              'amount': []}

    total_rewards = 0.
    
    while start_date<=end_date:

        report['date'].append(datetime.date(start_date.year, start_date.month, start_date.day))

        daily_transactions = data[[(x.year, x.month, x.day)==(start_date.year, start_date.month, start_date.day) 
                                   for x in data.Date]]
    
        for i in range(len(daily_transactions)):

            transaction = daily_transactions.iloc[i]

            operation = transaction['Operation'] 
            amount = transaction['Amount']

            if (transaction['Coin/Asset']==asset) and (operation in earnings_to_consider):
                
                    total_rewards += amount

        report['amount'].append(total_rewards)
        start_date+=delta
    
    return report


def plot_report(report, second_axis=None, second_axis_converter=1.):
    
    fig, ax = plt.subplots(figsize=(8,6))
    
    x = report['date']
    y = report['amount']


    ax.plot(x,y, 'o--')

    formatter = mdates.DateFormatter("%m/%d")
    ax.xaxis.set_major_formatter(formatter)
    ax.grid()
    ax.set_ylim(0., max(y)*1.1)
    ax.set_ylabel(report['asset'], fontsize=20)
    ax.set_xlabel('Day')

    if second_axis is not None:
    
        ax2 = ax.twinx()
        m,M=ax.get_ylim()
        ax2.set_ylim(m*second_axis_converter,M*second_axis_converter)
        ax2.yaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter("%.2f"))
        ax2.set_ylabel(second_axis, fontsize=20)

    ax.set_title(report['description'], fontsize=20)

    return fig, ax
