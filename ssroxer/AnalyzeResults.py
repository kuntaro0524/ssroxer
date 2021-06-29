import pandas as pd
from matplotlib import pyplot as plt
#%matplotlib inline

datadf = pd.read_csv("./summary.csv")

# 75 percentail
per75 = datadf['good_ratio'].quantile(0.75)
print("percentail",per75)

# Data selection No.1 (good_ratio)
sel1 = datadf['good_ratio'] > per75
s01 = datadf[sel1]
s01.describe()

# Good reflections based on 'percentail'
thresh_goodI = datadf['n_posI'].quantile(0.75)
print("Good I", thresh_goodI)
# number of positive 
sel2 = s01['n_posI'] > thresh_goodI
s02 = s01[sel2]
s02.describe()

score_series = s02['std_a'] + s02['std_b'] + s02['std_c']
std_a=1/(s02['std_a']+s02['std_b']+s02['std_c'])

s03=pd.concat([s02, std_a], axis=1)
s03.rename(columns={0: 'score'})

s03.to_csv("results.csv")

