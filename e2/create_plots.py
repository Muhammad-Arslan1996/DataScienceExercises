import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def main():
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    dataAt12 = pd.read_csv(filename1, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])
    dataAt13 = pd.read_csv(filename2, sep=' ', header=None, index_col=1,
        names=['lang', 'page', 'views', 'bytes'])

    dataAt12['viewsAt13'] = dataAt13['views']
    dataAt12Sorted = dataAt12.sort_values(by='views', ascending=False)

    plt.figure(figsize=(10,5))

    plt.subplot(1, 2, 1)
    plt.plot(dataAt12Sorted['views'].values)
    plt.title("Popularity Distribution")
    plt.xlabel("Rank")
    plt.ylabel("Views")

    plt.subplot(1, 2, 2)
    plt.scatter(dataAt12['views'].values,dataAt12['viewsAt13'].values)
    plt.yscale("log")
    plt.xscale("log")
    plt.title("Daily Correlation")
    plt.xlabel("Day 1 Views")
    plt.ylabel("Day 2 Views")
    plt.savefig('wikipedia.png')

if __name__ == '__main__':
    main()
