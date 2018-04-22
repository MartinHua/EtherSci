def draw(list):
    import matplotlib.pyplot as plt
    import numpy as np50
    import seaborn as sns


    sns.set_style("darkgrid")
    plt.plot(list)
    plt.xlabel('time')
    plt.ylabel('Transaction Fees')
    plt.title('Transaction Fees (per block) per day')
    plt.show()


