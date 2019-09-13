import numpy as np

def main():
    data = np.load('monthdata.npz')
    totals = data['totals']
    counts = data['counts']
    cityWithMinPercip = np.argmin(np.sum(totals, 1))
    print ("Row with lowest total precipitation:\n", cityWithMinPercip)

    totalPercipByMonth = np.sum(totals, 0)
    totalCountByMonth = np.sum(counts, 0)
    print ("Average precipitation in each month:\n", totalPercipByMonth/totalCountByMonth)

    totalPercipByCity = np.sum(totals, 1)
    totalCountByCity = np.sum(counts, 1)
    print ("Average precipitation in each city:\n", totalPercipByCity/totalCountByCity)

    singleArray = np.reshape(totals, 108)
    quarterly = singleArray.reshape(36,3)
    sumQuarterly = np.sum(quarterly, 1)
    print ("Quarterly precipitation totals:\n", sumQuarterly.reshape(9,4))

if __name__ == '__main__':
    main()
