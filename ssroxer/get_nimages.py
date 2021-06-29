import sys, os
import numpy as np
import Libs.SummaryDat as SD

if __name__=="__main__":
    cxyz=(0.7379,   -11.5623,    -0.0629)
    phi=0.0
    prefix="ssrox"
    summary_dat_path=sys.argv[1]

    sumdat=SD.SummaryDat(summary_dat_path,45,83)
    nimages_all=10
    completeness=0.95

    # sumdat.readSummary(prefix,nimages_all,completeness,timeout=120)
    ngood = sumdat.getNumGoodImages()
    print(ngood)