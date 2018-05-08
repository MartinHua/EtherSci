import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def draw_year(list, title = 'Transaction Fees (per block)', x = None):

    import numpy as np50

    sns.set_style("whitegrid")

    x = [dt.datetime.strptime(d, '%d/%m/%Y').date() for d in x]
    # plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%Y'))
    # plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    # print (x)
    # plt.gcf().autofmt_xdate()

    days = mdates.DayLocator()  # every day
    months = mdates.MonthLocator(interval=1)  # every month
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

def draw(list, title = 'Transaction Fees (per block)',x_label = 'time',  x_axis = None):
    sns.set_style("whitegrid")
    plt.figure(figsize=(10, 6))
    ax = plt.plot(list)
    if x_axis != None:
        x = range(len(list))

        plt.xticks(x,x_axis)
    plt.xlabel(x_label)
    plt.ylabel('Transaction Fees')

    plt.title(title)
    plt.grid(True)
    plt.show()

def draw_scattor_old(lists, title = 'Transaction Fees per Month', x_label = 'time', x_axis = None):
    # for i in range (len(x_axis)):
    #     df[x[i]] = lists[i]
    month = ['July', 'Aug','Sep', 'Oct', 'November']
    sns.set_style("whitegrid")
    print (lists)
    #sns.swarmplot( data=lists)
    for i in range (len(lists)):
        plt.subplot(2, 3, i+1)
        sns.distplot(lists[:][i])
        #ax.set_xticklabels(x_axis)
        plt.title(month[i])
        plt.ylabel('Transaction Fees')
        plt.grid(True)
    plt.show()
def draw_scattor(lists, title = 'Transaction Fees per Month', x_label = 'time', x_axis = None, y_label = 'Transaction Fees'):
    # for i in range (len(x_axis)):
    #     df[x[i]] = lists[i]
    sns.set_style("whitegrid")
    print (lists)
    plt.figure(figsize=(10, 6))
    ax =sns.swarmplot( data=lists)
    #ax = sns.boxplot( data=lists)
    ax.set_xticklabels(x_axis)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.show()

def draw_together(data1, data2, title = 'Transaction Fees (per block)',x_label = 'time',  x_axis = None):
    sns.set_style("darkgrid")
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(data1)
    ax2 = ax1.twinx()
    ax2.plot(data2, color='r')

    # ADD THIS LINE
    ax2.set_yticks(np.linspace(ax2.get_yticks()[0], ax2.get_yticks()[-1], len(ax1.get_yticks())))

    plt.show()