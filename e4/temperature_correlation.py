import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import radians, sin, cos, sqrt, asin



def calculate(city, station):
    lat1 = city.get(key = 'latitude')
    lon1 = city.get(key = 'longitude')
    lat2 = station['latitude']
    lon2 = station['longitude']
    #reference https://rosettacode.org/wiki/Haversine_formula#Python
    R = 6372.8  # Earth radius in kilometers
    dLat = np.subtract(lat2, lat1)
    dLat = dLat.apply(radians)
    dLon = np.subtract(lon2, lon1)
    dLon = dLon.apply(radians)
    lat1 = radians(lat1)
    lat2 = lat2.apply(radians)
    a = np.sin(dLat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dLon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def best_tmax(city, stations):
    indexOfMin = calculate(city, stations).idxmin()
    best_tmax = stations.iloc[indexOfMin]
    return best_tmax[0]


def main():

    stations_file = sys.argv[1]
    city_data_file = sys.argv[2]
    outputFilename = sys.argv[3]

    stations = pd.read_json(stations_file, lines=True)
    print (stations)
    city_data = pd.read_csv(city_data_file)
    city_data = city_data.dropna()
    city_data['area/sq(km)'] = city_data['area']/1000000
    city_data = city_data[city_data['area/sq(km)'] <= 10000]
    city_data['population_density'] = city_data['population']/city_data['area']
    #city_tmax = city_data.apply(best_tmax, args=(stations,), axis=1)
    city_data['t_max'] = city_tmax/10
    plt.plot(city_data['t_max'], city_data['population_density'], 'b.')
    plt.xlabel('Avg Max Temperature (\u00b0C)')
    plt.ylabel('Population Density (people/km\u00b2)')
    plt.title('Temperature vs Population Density')
    plt.savefig(outputFilename)


if __name__ == '__main__':
    main()
