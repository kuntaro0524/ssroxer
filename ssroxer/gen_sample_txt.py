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

ofile=open("sample_prep.txt","w")
for sample_name, newdf in df.groupby('sample_name'):
    puckids=newdf['puckid']
    pinids=newdf['pinid']
    for puckid, pinid in zip(puckids, pinids):
        ofile.write("%s-%02d PDBID %s\n" % (puckid, pinid, sample_name))


print("Please replace the PDBID in 'sample_prep.txt'")
