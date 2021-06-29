#!/usr/bin/env python
# coding: utf-8
import sys, os
import pandas as pd
import sqlite3
import logging
import logging.config
import SSROXpinMaster as SSRM
import PDBconfig

class SSROXmaster():
    def __init__(self, zoodb_file, meas_rootdir, geomfile_path, pdbconf_path):
        # Initialization of the log file
        logname = "./ssrox_proc.log"
        each_env = "/data01/kundev/"
        logging.config.fileConfig('%s/kunpy/ssrox/logging.conf' % each_env, defaults={'logfile_name': logname})
        self.logger = logging.getLogger('SSROX')
        os.chmod(logname, 0666)

        # Various parameters to be used.
        self.zoodb_file = zoodb_file
        self.geom_orig = geomfile_path
        self.pdbconf_file = pdbconf_path
        self.meas_root = meas_rootdir
        # Data processing directory
        self.proc_root = os.path.abspath(".")
        self.isInit = False

    def init(self):
        conn = sqlite3.connect(self.zoodb_file)
        cursor = conn.cursor()
        self.df = pd.read_sql_query('SELECT * FROM ESA', conn)

        # root directory should not be extracted from the value in the zoodb
        # because the path should be replaced at beamline and laboratories soon.
        if os.path.exists(self.meas_root) == False:
            self.logger.info("No such directories.")
            sys.exit()

        # PDB config file
        try:
            self.pdbconf = PDBconfig.PDBconfig(self.pdbconf_file)
        except Exception as e:
            print(e.args)
            sys.exit()

        self.isInit = True

    def coreProc(self, scan_path, proc_path, pdbfile, nspots=10, nproc=12, beam_dx=0, beam_dy=0):
        if self.isInit == False:
            self.init()

        # For each sample consists of several pins
        n_hits_sample = 0
        if os.path.exists(proc_path) == False:
            os.makedirs(proc_path)

        try:
            ssrox_master = SSRM.SSROXpinMaster(scan_path, proc_path, self.geom_orig, pdbfile)
            ssrox_master.run(nspots, nproc=nproc, beam_dx=beam_dx, beam_dy=beam_dy, redo_flag=True)

        except Exception as e:
            self.logger.error(e.args)

    # Coded for the parameters
    def coreProcRefine(self, scan_path, proc_root, pdbfile, nspots=10, nproc=12):
        if self.isInit == False:
            self.init()

        # For each sample consists of several pins
        n_hits_sample = 0
        if os.path.exists(proc_path) == False:
            os.makedirs(proc_path)

        try:
            ssrox_master = SSRM.SSROXpinMaster(scan_path, proc_path, self.geom_orig, pdbfile)
            ssrox_master.run(nspots, nproc=nproc, beam_dx=beam_dx, beam_dy=beam_dy, redo_flag=True)

        except Exception as e:
            self.logger.error(e.args)

    def refineBeam(self, nspots, sample_for_refine, nproc=12, min_dx=-5, max_dx=5, min_dy=-5, max_dy=5, step=5):
        if self.isInit == False:
            self.init()

        for sample_name, newdf in self.df.groupby('sample_name'):
            if sample_name != sample_for_refine:
                continue

            puckids = newdf['puckid']
            pinids = newdf['pinid']
            n_mounts = newdf['n_mount']

            # For each sample consists of several pins
            n_hits_sample = 0
            for puckid, pinid, n_mount in zip(puckids, pinids, n_mounts):
                ppinfo = "%s-%02d" % (puckid, pinid)

                scan_dir = "%s/%s/scan%02d/ssrox/" % (self.meas_root, ppinfo, n_mount)
                self.logger.info("data directory = %s %s" % (sample_name, scan_dir))

                # Extract PDB file name from configure file
                try:
                    pdbfile = self.pdbconf.getPDB(sample_name)
                except Exception as e:
                    print(e.args)
                    pdbfile = ""

                self.logger.info("Loop to make beam position refinement.")
                for beam_dx in range(min_dx, max_dx+1, step):
                    for beam_dy in range(min_dy, max_dy+1, step):
                        self.logger.info("dx=%5d dy=%5d" % (beam_dx, beam_dy))
                        # Data processing directory
                        # beam refinement
                        beamrefine_dir = "beam_X%03d_Y%03d/" % (beam_dx, beam_dy)
                        proc_dir = os.path.join(self.proc_root, ppinfo, beamrefine_dir)

                        if os.path.exists(proc_dir) == False:
                            os.makedirs(proc_dir)

                        # processing core part
                        try:
                            self.coreProc(scan_dir, proc_dir, pdbfile, nspots, nproc, beam_dx, beam_dy)
                        except Exception as e:
                            self.logger.error(e.args)

    def proc(self, nspots=10, nproc=12):
        if self.isInit == False:
            self.init()

        for sample_name, newdf in self.df.groupby('sample_name'):
            puckids = newdf['puckid']
            pinids = newdf['pinid']
            n_mounts = newdf['n_mount']

            # For each sample consists of several pins
            n_hits_sample = 0
            for puckid, pinid, n_mount in zip(puckids, pinids, n_mounts):
                ppinfo = "%s-%02d" % (puckid, pinid)

                scan_dir = "%s/%s/scan%02d/ssrox/" % (self.meas_root, ppinfo, n_mount)
                self.logger.info("data directory = %s %s" % (sample_name, scan_dir))

                # Extract PDB file name from configure file
                try:
                    pdbfile = self.pdbconf.getPDB(sample_name)
                    self.logger.info("PDB file is set to %s" % pdbfile)
                except Exception as e:
                    print(e.args)
                    self.logger.error(e.args[0])
                    pdbfile = ""

                # Data processing directory
                proc_dir = os.path.join(self.proc_root, ppinfo)

                if os.path.exists(proc_dir) == False:
                    os.makedirs(proc_dir)

                # processing core part
                try:
                    self.coreProc(scan_dir, proc_dir, pdbfile, nspots, nproc, beam_dx=0, beam_dy=0)
                except Exception as e:
                    self.logger.error(e.args)

if __name__ == "__main__":
    zoodb_file = sys.argv[1]
    meas_rootdir = sys.argv[2]
    geomfile_path = sys.argv[3]
    pdbconf_path = sys.argv[4]

    ssroxmaster = SSROXmaster(zoodb_file, meas_rootdir, geomfile_path, pdbconf_path)

    # beam_dx = [-5, -3, 0, 3, 5]
    # beam_dy = [-5, -3, 0, 3, 5]
    # for dx in beam_dx:
    #     for dy in beam_dy:
    #         ssroxmaster.proc(nspots=10, nproc=12, beam_dx=dx, beam_dy=dy, beam_refine=True)

    # def refineBeam(self, nspots, sample_for_refine, nproc=12, min_dx=-5, max_dx=5, min_dy=-5, max_dy=5, step=5):
    min_dx=-5
    max_dx=+5
    min_dy=-5
    max_dy=+5
    ssroxmaster.refineBeam(10, "WTPhC1", min_dx=min_dx, max_dx=max_dx, min_dy=min_dy, max_dy=max_dy, step=3)
    # ssroxmaster.refineBeam(10, "WTPhC1")
