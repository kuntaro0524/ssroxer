import os,sys,numpy,scipy
import pandas as pd
import glob

stream_files=glob.glob("./*stream")

def read_cell(stream_file):
        for l in open(stream_file):
                if "Cell" in l:
                        cols=l.split()
                        x,y = stream_file.replace(".stream","").split("/")[-1].split('_')
                        rtn_dict = {
                            'stream_name': stream_file,
                            'a': float(cols[2]),
                            'b': float(cols[3]),
                            'c': float(cols[4]),
                            'alpha': float(cols[6]),
                            'beta': float(cols[7]),
                            'gamma': float(cols[8]),
                            'x': float(x),
                            'y': float(y)
                        }
                        return rtn_dict

cell_array=[]
for stream_file in stream_files:
        data_dict=read_cell(stream_file)
        cell_array.append(data_dict)

ppp=pd.DataFrame(cell_array)

print(ppp.describe())
ppp.to_csv("cell_param.csv")

