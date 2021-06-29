import pandas as pd

# makeSSROXprocList(self.scan_dir)

df = pd.read_csv("./summary.dat", delim_whitespace=True)

# filter
selc01 = df['kind']=='n_spots'
selc02 = df['data']>8.0
df01 = df[selc01 & selc02]

# filter
selc01 = df['kind']=='n_spots'
selc02 = df['data']>8.0
df01 = df[selc01 & selc02]
all_series=[]

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
    
    my_dic['hd5_index']=hd5_index
    my_dic['inner_imgnum']=inner_imgnum

    all_series.append(pd.Series(my_dic))

df = pd.DataFrame(all_series)
df.to_csv("first_analysis.csv")
