import numpy,os,sys,scipy
import pandas as pd
import logging
import logging.config

class StreamFile():
    def __init__(self, streamfile):
        self.filename=streamfile
        self.isInit=False
        self.isDebug=False
        self.logger = logging.getLogger("SSROX").getChild("StreamFile")
        self.logger.info("=== StreamFiles ===")

    def check_refl(self, line):
        #print("LINE=%s"%line)
        intensity=float(line.split()[3])
        return intensity

    def init(self):
        lines = open(self.filename,"r").readlines()

        dict_all=[]
        start_flag=False
        refl_start=False
        n_refl=0
        index_flag=False
        # Number of reflections
        n_plus_intensity=0
        # All lines: including many chunks from many processed images.
        for line in lines:
            # Chunk loop
            if start_flag==False and "Begin chunk" in line:
                start_flag=True

            if "End chunk" in line:
                if n_refl > 0:
                    mean_intensity=float(n_plus_intensity)/float(n_refl)
                else:
                    mean_intensity=0

                #print(h5name, taginfo)
                start_flag=False
                if index_flag==False:
                    cell_a=999.999
                    cell_b=999.999
                    cell_c=999.999
                    cell_alpha=999.999
                    cell_beta=999.999
                    cell_gamma=999.999
                dict_each={
                    "h5name": h5name,
                    "taginfo":taginfo,
                    "serial_num": serial_num,
                    "energy": energy,
                    "dist": dist,
                    "n_refl": n_refl,
                    "cell_a": cell_a,
                    "cell_b": cell_b,
                    "cell_c": cell_c,
                    "cell_alpha": cell_alpha,
                    "cell_beta": cell_beta,
                    "cell_gamma": cell_gamma,
                    "index_ok": index_flag,
                    "n_positive_I": n_plus_intensity,
                    "mean_intensity": mean_intensity
                }
                if self.isDebug:
                    if n_refl > 0:
                        print("%s: %5d" % (h5name, n_refl))

                dict_all.append(dict_each)
                # Reset parameters for next chunk
                n_refl=0
                index_flag = False
                n_plus_intensity=0

            # Each chunk has reflection information
            # Reflection information in each processed results
            if "   h    k    l          I   sigma(I)       peak background  fs/px  ss/px panel" in line:
                refl_start=True
                continue
            if "End of reflections" in line:
                refl_start=False
            if refl_start==True:
                n_refl+=1
                if self.check_refl(line) > 0:
                    n_plus_intensity+=1

            # Cell parameters
            if "Cell parameters" in line:
                cell_strs=line.split()
                cell_a=float(cell_strs[2])
                cell_b=float(cell_strs[3])
                cell_c=float(cell_strs[4])
                cell_alpha=float(cell_strs[6])
                cell_beta=float(cell_strs[7])
                cell_gamma=float(cell_strs[8])
                index_flag=True
                
            # Each chunk has event information
            if start_flag==True:
                if "Image filename:" in line:
                    h5name=line.split()[2]
                if "Event:" in line:
                    taginfo=line.split()[1]
                if "Image serial number:" in line:
                    serial_num=int(line.split()[3])
                if "photon_energy_eV" in line:
                    energy=float(line.split()[2])
                if "average_camera_length" in line:
                    dist=float(line.split()[2])

        self.df=pd.DataFrame(dict_all)
        self.isInit=True
        self.n_processed=len(self.df)

        return self.df

    def getIndexedDF(self):
        if self.isInit==False: self.init()
        # rejects 'irregular' cells
        sel1 = ~(self.df['cell_a']==999.999)
        ok_df=self.df[sel1]

        return ok_df

    def getIndexedInfo(self):
        ok_df=self.getIndexedDF()
        nrefl, sumI, meanI=self.calcIproperty()
        self.success_ratio=float(len(ok_df))/float(self.n_processed)*100.0
        print("Success=%5.2f percent" % self.success_ratio)

        return nrefl, sumI, meanI, self.success_ratio

    # through the data frame: = all processing results
    def calcIproperty(self):
        ok_df=self.getIndexedDF()
        all_refl = self.df['n_refl'].sum()
        all_posI = self.df['n_positive_I'].sum()
        mean_intensity=self.df['mean_intensity'].mean()

        return all_refl, all_posI, mean_intensity

    def getIndexedCell(self):
        ok_df=self.getIndexedDF()
        # Averaged cell parameters (nm -> Angstrome)
        mean_a=ok_df['cell_a'].mean() * 10.0
        mean_b=ok_df['cell_b'].mean() * 10.0
        mean_c=ok_df['cell_c'].mean() * 10.0
        mean_alpha=ok_df['cell_alpha'].mean()
        mean_beta=ok_df['cell_beta'].mean()
        mean_gamma=ok_df['cell_gamma'].mean()
        std_a=ok_df['cell_a'].std() * 10.
        std_b=ok_df['cell_b'].std() * 10.0
        std_c=ok_df['cell_c'].std() * 10.0
        std_alpha=ok_df['cell_alpha'].std()
        std_beta=ok_df['cell_beta'].std()
        std_gamma=ok_df['cell_gamma'].std()
        all_refl = self.df['n_refl'].sum()
        """
        print("%s: %5d %8.5f(%5.1f) %8.5f(%5.1f) %8.5f(%5.1f) %8.5f(%5.1f) %8.5f(%5.1f) %8.5f(%5.1f)" % 
            (self.filename, all_refl,
            mean_a, std_a,
            mean_b, std_b,
            mean_c, std_c,
            mean_alpha, std_alpha,
            mean_beta, std_beta,
            mean_gamma, std_gamma))
        """
        # ok_df.to_csv("cell_ok.csv")

        return mean_a, std_a, mean_b, std_b, mean_c, std_c, mean_alpha, std_alpha, mean_beta, std_beta, mean_gamma, std_gamma

if __name__ == "__main__":
    import glob

    tmp_data=[]
    stream_files=glob.glob("./*.stream")

    for stream_file in stream_files:
        strm=StreamFile(stream_file)
        strm.init()
        all_refl, all_posI,mean_intensity=strm.calcIproperty()
        mean_a, std_a, mean_b, std_b, mean_c, std_c, mean_alpha, std_alpha, mean_beta, std_beta, mean_gamma, std_gamma=strm.getIndexedCell()

        tmp_dict = {
            "filename": stream_file,
            "n_refl": all_refl,
            "n_posI": all_posI,
            "mean_intensity": mean_intensity,
            "mean_a": mean_a, 
            "std_a": std_a,
            "mean_b": mean_b, 
            "std_b": std_b,
            "mean_c": mean_c, 
            "std_c": std_c,
            "mean_alpha": mean_alpha, 
            "std_alpha": std_alpha,
            "mean_beta": mean_beta, 
            "std_beta": std_beta,
            "mean_gamma": mean_gamma, 
            "std_gamma": std_gamma
        }
        # Dataframe making list
        tmp_data.append(tmp_dict)

    df=pd.DataFrame(tmp_data)
    df=df.sort_values(by='n_posI',ascending=False)
    df.to_csv("summary.csv")

    print(df.mean_a,df.mean_b, df.mean_c)

"""
Image filename: ../run958655-1.h5
Event: tag-563539862//
Image serial number: 221
indexed_by = dirax-raw-nolatt-nocell-retry-nomulti-refine
photon_energy_eV = 8911.890000
beam_divergence = 0.00e+00 rad
beam_bandwidth = 1.00e-08 (fraction)
hdf5/%/photon_energy_ev = 8911.890000
average_camera_length = 0.090000 m
num_peaks = 36
num_saturated_peaks = 0
Peaks from peak search

----- Begin chunk -----
Image filename: ../run958655-1.h5
Event: tag-563540788//
Image serial number: 346
indexed_by = dirax-raw-nolatt-nocell-retry-nomulti-refine
photon_energy_eV = 9124.110000
beam_divergence = 0.00e+00 rad
beam_bandwidth = 1.00e-08 (fraction)
hdf5/%/photon_energy_ev = 9124.110000
average_camera_length = 0.090000 m
num_peaks = 29
num_saturated_peaks = 0
Peaks from peak search
  fs/px   ss/px (1/d)/nm^-1   Intensity  Panel
 170.33 2247.95       3.00     3090.44   q3
 392.68 2268.19       2.27     2577.98   q3
 372.23 2304.21       2.39      455.42   q3
 386.47 2456.10       2.62     5423.60   q3
 361.08 2538.91       2.87      786.14   q3
 227.00 2739.00       3.62      183.25   q3
 404.38 2949.96       3.79      586.11   q3
 152.32 3208.08       1.11      687.89   q4
"""
