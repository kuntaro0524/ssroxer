import os,sys,numpy,scipy
import pandas as pd
import Stream

stream_path = sys.argv[1]

stream=Stream.StreamFile(sys.argv[1])

stream.getIndexedInfo()
mean_a, std_a, mean_b, std_b, mean_c, std_c, mean_alpha, std_alpha, mean_beta, std_beta, mean_gamma, std_gamma = stream.getIndexedCell()

all_refl, all_posI, good_ratio = stream.calcIproperty()
print("Refl. num= %5d, Summed intensity= %10.3f : Mean intensity=%10.3f"%(all_posI, all_refl, good_ratio))
print("mean cell parameters: %8.3f %8.3f %8.3f %8.3f %8.3f %8.3f" %(mean_a, mean_b, mean_c, mean_alpha, mean_beta, mean_gamma))
