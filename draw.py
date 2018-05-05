import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
def draw_year(list, title = 'Transaction Fees (per block)', x = None):

    import numpy as np50

    sns.set_style("darkgrid")

    x = [dt.datetime.strptime(d, '%d/%m/%Y').date() for d in x]
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    # print (x)
    # plt.gcf().autofmt_xdate()

    days = mdates.DayLocator()  # every day
    months = mdates.MonthLocator(interval=2)  # every month
    monthsFmt = mdates.DateFormatter('%Y-%m')
    plt.gca().xaxis.set_major_locator(months)
    plt.gca().xaxis.set_major_formatter(monthsFmt)
    plt.gca().xaxis.set_minor_locator(days)
    plt.plot(x, list)
    plt.xlabel('time')
    plt.ylabel('Transaction Fees')
    plt.title(title)
    plt.grid(True)
    plt.show()

def draw(list, title = 'Transaction Fees (per block)', x_axis = None):
    sns.set_style("darkgrid")
    plt.plot(list)
    plt.xlabel('time')
    plt.ylabel('Transaction Fees')
    plt.title(title)
    plt.grid(True)
    plt.show()

def draw_scattor(lists, title = 'Transaction Fees per Month'):
    sns.set_style("darkgrid")
    sns.swarmplot(data=lists)
    plt.title(title)
    plt.xlabel('time')
    plt.ylabel('Transaction Fees')
    plt.grid(True)
    plt.show()
