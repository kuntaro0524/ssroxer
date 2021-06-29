#!/usr/bin/env python
# coding: utf-8

import pandas as pd
df = pd.read_csv("./summary.dat", delim_whitespace=True)
# filter
selc01 = df['kind']=='n_spots'
selc02 = df['data']>8.0
df01 = df[selc01 & selc02]

all_series=[]

# script to run eiger2cbf
e2c=open("h5toCBF.sh", "w")
for index, ser in df01.iterrows():
    imgname = ser['filename']
    findex_str = imgname.replace(".img","").replace(ser['prefix'],"")
    img_num = int(findex_str)
    my_dic = {}
    my_dic['image_file']=imgname
    my_dic['score']=ser['data']
    my_dic['image_num']=img_num
    # HD5 name and image number in the file.
    imgindex = img_num - 1
    hd5_index = (imgindex//100)+1
    inner_imgnum = (imgindex%100)
    #print("HD_INDEX=", hd5_index)
    
    my_dic['hd5_index']=hd5_index
    my_dic['inner_imgnum']=inner_imgnum

    hd5_name = "%sdata_%06d.h5" % (ser['prefix'],hd5_index)
    my_dic['hd5_name']=hd5_name
    e2c.write("H5ToXds ../%smaster.h5 %d out_%06d.cbf\n" % (ser['prefix'], imgindex, imgindex))

    all_series.append(pd.Series(my_dic))

df = pd.DataFrame(all_series)
df.sort_values('score')
df.to_csv("first_analysis.csv")
