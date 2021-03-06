import pandas as pd
import os,sys

scan_dir=os.path.abspath(sys.argv[1])

# makeSSROXprocList(self.scan_dir)

datafile = os.path.join(scan_dir, "summary.dat")
df = pd.read_csv(datafile, delim_whitespace=True)

score_min=10
score_max=100

# filter
selc01 = df['kind']=='n_spots'
selc02 = df['data']>score_min
selc03 = df['data']<=score_max
df01 = df[selc01 & selc02 & selc03]

# return list
rtn_list=[]

# filter
for index, ser in df01.iterrows():
    imgname = ser['filename']
    #print("imgname=",imgname)
    prefix=ser['prefix']
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
    
    my_dic['hd5_index']=hd5_index
    my_dic['inner_imgnum']=inner_imgnum

    h5_str="%s/%sdata_%06d.h5 //%d"%(scan_dir, prefix, hd5_index, inner_imgnum)
    rtn_list.append(h5_str)

for rtn in rtn_list:
    print(rtn)
#/isilon/users/target/target/AutoUsers/200715/abe/HSK0001-01/scan00/ssrox/ssrox_data_000044.h5 //59
