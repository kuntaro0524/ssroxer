import os, sys, math, numpy


class CrystFEELer():
    def __init__(self, proc_dir, params):
        self.proc_dir = proc_dir
        self.params = params
        # initialization flag
        self.isInit = False

    def init(self):
        # Read parameters from dictionary(params)
        check_pdb = self.params['pdb']
        if check_pdb == "none":
            self.params['pdb']=""
        else:
            self.params['pdb']="-p %s" % check_pdb
            self.pdbfile = check_pdb
        self.geom = self.params['geom']
        self.isInit = True

    def genJobScript(self, script_name):
        if self.isInit==False:
            self.init()
        comstr="""#!/bin/bash
indexamajig \
 -i %(hitfile)s \
 -g %(geom)s \
 --peaks=peakfinder8 --threshold=10 --min-snr=4 \
 --indexing=dirax \
 --int-radius=3,4,5 \
 %(pdb)s \
 -j %(nproc)d \
 -o %(prefix)s.stream
        """ % self.params

        ofile=open(script_name, "w")
        ofile.write(comstr)
        ofile.close()

    def runJobScript(self):
        print("runJobScript")

    def checkFinished(self):
        print("checkFinished")

if __name__ == "__main__":
    params = {
        "geom": "geom_file_no_path/geom_file.geom",
        "pdb": "1oh6.pdb",
        "prefix": "stream_file_no_path/dataproc",
        "hitfile": "hits.lst"
    }
    cf = CrystFEELer(sys.argv[1], params)
    cf.genJobScript()