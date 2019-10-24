import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv('data.csv')

x_melt = pd.melt(data)
print (x_melt)
posthoc = pairwise_tukeyhsd(x_melt['value'], x_melt['variable'], alpha=0.05)

print('Multiple Comparison of Means - Tukey HSD,FWER=0.05\n', posthoc)
fig = posthoc.plot_simultaneous()
plt.show()
