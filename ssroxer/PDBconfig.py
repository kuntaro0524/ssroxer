import numpy as np
import os, sys
import pandas as pd

class PDBconfig() :
    def __init__(self, pdb_config_path):
        self.pdbconf = pdb_config_path
        self.isInit = False

    def init(self):
        if os.path.exists(self.pdbconf)==False:
            raise Exception("No such PDB config file!!")
        df = pd.read_csv(self.pdbconf, delim_whitespace=True, names=['sample_name', 'pdbfile'])
        self.pdb_dict = dict(zip(df['sample_name'], df['pdbfile']))
        self.isInit = True
        self.pdb_root = self.pdb_dict['root_path']

    def getPDB(self, sample_name):
        if self.isInit == False:
            self.init()
        if sample_name in self.pdb_dict.keys():
            filepath = os.path.join(self.pdb_root, self.pdb_dict[sample_name])
            return filepath
        else:
            raise Exception("No such PDB file in your pdb config file. %s" % self.pdbconf)

if __name__ == "__main__":
    pc=PDBconfig(sys.argv[1])
    try:
        pdbname = pc.getPDB(sys.argv[2])
    except Exception as e:
        print(e.args)
    print("Processing %s" % pdbname)
