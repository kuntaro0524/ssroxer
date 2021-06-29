#!/usr/bin/env python
# coding: utf-8
import sys
import pandas as pd
import sqlite3

file_sqlite3=sys.argv[1]
conn = sqlite3.connect(file_sqlite3)
cursor=conn.cursor()

df=pd.read_sql_query('SELECT * FROM ESA', conn)
df.columns

# root directory should not be extracted from the value in the zoodb
# because the path should be replaced at beamline and laboratories soon.

# ofile=open("sample_prep.txt","w")
for sample_name, newdf in df.groupby('sample_name'):
    puckids=newdf['puckid']
    pinids=newdf['pinid']
    rootdir=newdf['root_dir'].iloc[-1]
    print("ROOT_DIR=",rootdir)

    for puckid, pinid in zip(puckids, pinids):
        ppinfo="%s-%02d" % (puckid, pinid)
        # print(ppinfo)
        scan_dir = "%s/%s/scan00/ssrox/" % (rootdir, ppinfo)
        #print(scan_dir)
        # diffscan.log path
        path_diffscan = "%s/diffscan.log" % scan_dir
        #print(path_diffscan)
        # summary.dat path
        summary_path = "%s/_spotfinder/summary.dat" % scan_dir
        #print(summary_path)

    # Data processing
    # print("rootdir=", rootdir)
    # Scan directory

print("Please replace the PDBID in 'sample_prep.txt'")
