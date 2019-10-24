import sys
import pandas as pd
import numpy as np
from scipy import stats
import time
from implementations import all_implementations


def main():
    data = pd.DataFrame(columns=['qs1', 'qs2', 'qs3', 'qs4', 'qs5', 'merge1', 'partition_sort'])
    for i in range(100):
        row = np.array([])
        random_array = np.random.randint(1000000, size=10000)
        for sort in all_implementations:
            st  = time.time()
            res = sort(random_array)
            en  = time.time()
            tot = en - st
            row = np.append(row, tot)
        data.loc[i] = row
    data.to_csv('data.csv', index=False)


if __name__ == '__main__':
    main()
