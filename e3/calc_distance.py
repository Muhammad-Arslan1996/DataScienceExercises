import sys
import pandas as pd
import numpy as np
from xml.dom import minidom
from math import radians, sin, cos, sqrt, asin
from pykalman import KalmanFilter

def output_gpx(points, output_filename):
    """
    Output a GPX file with latitude and longitude from the points DataFrame.
    """
    from xml.dom.minidom import getDOMImplementation
    def append_trkpt(pt, trkseg, doc):
        trkpt = doc.createElement('trkpt')
        trkpt.setAttribute('lat', '%.8f' % (pt['lat']))
        trkpt.setAttribute('lon', '%.8f' % (pt['lon']))
        trkseg.appendChild(trkpt)

    doc = getDOMImplementation().createDocument(None, 'gpx', None)
    trk = doc.createElement('trk')
    doc.documentElement.appendChild(trk)
    trkseg = doc.createElement('trkseg')
    trk.appendChild(trkseg)

    points.apply(append_trkpt, axis=1, trkseg=trkseg, doc=doc)

    with open(output_filename, 'w') as fh:
        doc.writexml(fh, indent=' ')

def get_data(filename):
    #reference https://www.mkyong.com/python/python-read-xml-file-dom-example/
    lon = []
    lat = []
    dataXml = minidom.parse(filename)
    longLats = dataXml.getElementsByTagName("trkpt")
    for longLat in longLats:
        lat.append(longLat.getAttribute("lat"))
        lon.append(longLat.getAttribute("lon"))
    #reference https://stackoverflow.com/questions/20763012/creating-a-pandas-dataframe-from-a-numpy-array-how-do-i-specify-the-index-colum
    longLatDf = pd.DataFrame(
        data={'lat': lat, 'lon': lon},
        dtype=float)
    return longLatDf

def distance(df):
    shifted_df = df.shift(-1)
    shifted_df = shifted_df.rename(columns = {"lon":"lon1", "lat":"lat1"})
    df = df.join(shifted_df)
    distArray = df.apply(calculate, axis = 1)
    distArray = distArray[~np.isnan(distArray)]  #reference https://stackoverflow.com/questions/11620914/removing-nan-values-from-an-array
    dd = np.sum(distArray)*1000
    return dd

def calculate(series):
    #reference https://www.geeksforgeeks.org/python-pandas-series-get/
    lat1 = series.get(key = 'lat')
    lat2 = series.get(key = 'lat1')
    lon1 = series.get(key = 'lon')
    lon2 = series.get(key = 'lon1')
    #reference https://rosettacode.org/wiki/Haversine_formula#Python
    R = 6372.8  # Earth radius in kilometers
    dLat = radians(lat2 - lat1)
    dLon = radians(lon2 - lon1)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    a = sin(dLat / 2)**2 + cos(lat1) * cos(lat2) * sin(dLon / 2)**2
    c = 2 * asin(sqrt(a))

    return R * c
def smooth(df):
    observation_covariance = np.diag([0.00005, 1]) ** 2
    kalman_data = df
    initial_value_guess = kalman_data.iloc[0]
    transition_matrix = [[1, 0], [0, 1]]
    transition_covariance = np.diag([0.00005, 1]) ** 2
    kf = KalmanFilter(
    initial_state_mean=initial_value_guess,
    observation_covariance=observation_covariance,
    transition_covariance=transition_covariance,
    transition_matrices=transition_matrix
    )
    kalman_smoothed, _ = kf.smooth(kalman_data)
    #reference https://stackoverflow.com/questions/20763012/creating-a-pandas-dataframe-from-a-numpy-array-how-do-i-specify-the-index-colum
    smoothedDF = pd.DataFrame(
        data={'lat': kalman_smoothed[:,0], 'lon': kalman_smoothed[:,1]},
        dtype=float)
    return smoothedDF

def main():
    points = get_data(sys.argv[1])
    print('Unfiltered distance: %0.2f' % (distance(points),))

    smoothed_points = smooth(points)
    print('Filtered distance: %0.2f' % (distance(smoothed_points),))
    output_gpx(smoothed_points, 'out.gpx')


if __name__ == '__main__':
    main()
