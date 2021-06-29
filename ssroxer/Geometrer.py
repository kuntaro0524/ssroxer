import numpy as np
import scipy
import os

class Geometrer:
    def __init__(self, initial_geom, proc_dir):
        self.initial_geom = initial_geom
        self.proc_dir = os.path.abspath(proc_dir)
        self.dx =0
        self.dy =0

        # initialization flag
        self.isInit = False

    def init(self):
        # File check
        if os.path.exists(self.initial_geom) == False:
            raise Exception("The initial geometry file does not exist. %s" % self.initial_geom)
        self.geom_lines = open(self.initial_geom).readlines()
        # print(self.geom_lines)
        self.isInit = True

    def change_dist(self, new_dist):
        if self.isInit == False: self.init()
        new_lines = []
        for l in self.geom_lines:
            if "clen" in l:
                l="clen = %8.5f; /entry/instrument/detector/detector_distance\n" % new_dist
            new_lines.append(l)
        self.geom_lines = new_lines

    def shift_beam(self, dx, dy):
        if self.isInit == False: self.init()
        new_lines = []
        for l in self.geom_lines:
            if "corner_x" in l:
                v = float(l[l.index("=") + 1:])
                l = l[:l.index("=")] + "= %f\n" % (v + dx)
            if "corner_y" in l:
                v = float(l[l.index("=") + 1:])
                l = l[:l.index("=")] + "= %f\n" % (v + dy)
            new_lines.append(l)

        self.geom_lines = new_lines

    def set_wavelength(self, wavelength):
        # energy
        energy = 12398.4/wavelength
        if self.isInit == False: self.init()
        new_lines = []
        for l in self.geom_lines:
            cols = l.split()
            if len(cols)>0 and "photon_energy" in cols[0]:
                photon_energy = 12398.40
                l="photon_energy=%8.2f\n" % photon_energy
            new_lines.append(l)
        self.geom_lines = new_lines

    def makeGeom(self, geom_name):
        try:
            if self.isInit == False: self.init()
        except Exception as e:
            raise(e)
        # print(self.geom_lines)
        oname= os.path.join(self.proc_dir, geom_name)
        ofile = open(oname, "w")

        for line in self.geom_lines:
            ofile.write("%s"%line)
        ofile.close()

        return oname

if __name__ == "__main__":
    import sys
    g=Geometrer(sys.argv[1], "./")
    g.shift_beam(5,5)
    g.change_dist(0.18)
    g.set_wavelength(1.5)
    g.makeGeom("new.geom")
    # for line in g.geom_lines:
    #     print(line,)