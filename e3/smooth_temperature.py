import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.nonparametric.smoothers_lowess import lowess
from pykalman import KalmanFilter


def main():
    filename = sys.argv[1]
    cpu_data = pd.read_csv(filename, parse_dates = [4])
    plt.figure(figsize=(12, 4))
    plt.plot(cpu_data['timestamp'], cpu_data['temperature'], 'b.', alpha=0.5)
    
    loess_smoothed = lowess(cpu_data['temperature'], cpu_data['timestamp'],frac=0.035)
    plt.plot(cpu_data['timestamp'], loess_smoothed[:, 1], 'r-')


    observation_covariance = np.diag([cpu_data['temperature'].std(),
                                  cpu_data['cpu_percent'].std(),
                                  cpu_data['sys_load_1'].std()]) ** 2
    kalman_data = cpu_data[['temperature', 'cpu_percent', 'sys_load_1']]
    initial_value_guess = kalman_data.iloc[0]
    transition_matrix = [[1, 0, 0], [0, 0.6,0 ], [0, 0, 0.8]]
    transition_covariance = np.diag([0.3, 0.3, 0.3]) ** 2
    kf = KalmanFilter(
    initial_state_mean=initial_value_guess,
    initial_state_covariance=observation_covariance,
    observation_covariance=observation_covariance,
    transition_covariance=transition_covariance,
    transition_matrices=transition_matrix
    )
    kalman_smoothed, _ = kf.smooth(kalman_data)
    plt.plot(cpu_data['timestamp'], kalman_smoothed[:, 0], 'g-')
    plt.legend(['scatterplot', 'LOESS Filtering', 'Kalman FIltering'])
    plt.savefig('cpu.svg')


if __name__ == '__main__':
    main()
