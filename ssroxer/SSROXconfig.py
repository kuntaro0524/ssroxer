import pandas as pd, sys

class myconf:
    def __init__(self, config_file):
        self.prog_path = "/usr/local/bin"
        self.pdbconfig = "/data02/pdbfile.conf"
        self.isInit = False

        self.config_path=config_file

    def init(self):
        confdf = pd.read_csv(self.config_path, delim_whitespace=True, names=['param','value'])
        self.confdict = dict(zip(confdf['param'],confdf['value']))
        print(self.confdict)

    def printProp(self):
        print(self.prog_path)

mm=myconf(sys.argv[1])
mm.init()
#mm.printProp()

print(mm.confdict['pdb_conf'])
