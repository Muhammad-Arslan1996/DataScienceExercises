import pandas as pd

def main():
    totals = pd.read_csv('totals.csv').set_index(keys=['name'])
    counts = pd.read_csv('counts.csv').set_index(keys=['name'])
    totalPercipByCity = totals.sum(axis=1)
    print ("Row with lowest total precipitation:\n", totalPercipByCity.idxmin())

    totalPercipByMonth= totals.sum(axis=0)
    totalCountByMonth= counts.sum(axis=0)
    print ("Average precipitation in each month:\n", totalPercipByMonth/totalCountByMonth)

    totalCountByCity= counts.sum(axis=1)
    print ("Average precipitation in each city:\n", totalPercipByCity/totalCountByCity)


if __name__ == '__main__':
    main()
