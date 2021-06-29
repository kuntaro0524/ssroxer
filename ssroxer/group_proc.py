#!/usr/bin/env python
# coding: utf-8
import sys
import pandas as pd

names = ["puckpin","pdbid","sample_name"]
df = pd.read_csv(sys.argv[1],names=names,delim_whitespace=True)

for sample_name, newdf in df.groupby('sample_name'):
    ppinfo=newdf['puckpin']
    for pp in ppinfo:
        print(sample_name,pp.split("-"))

    diffscan_log_path = sys.argv[1]
    sample_list_file = sys.argv[2]

    print("PROGEAM DIFFSCAN_LOG_PATH SAMPLE_LIST_FILE PUCKID PINID")
    puckid=sys.argv[3]
    pinid = int(sys.argv[4])

    ssrox_master = SSROXmaster(diffscan_log_path, sample_list_file, puckid,pinid)
    ssrox_master.run()
