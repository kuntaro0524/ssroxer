#!/usr/bin/env python
# coding: utf-8
import sys, os
import pandas as pd
import sqlite3
import logging
import logging.config
import SSROXpinMaster as SSRM
import PDBconfig

# Initialization of the log file
logname = "./ssrox_proc.log"
each_env = "/data01/kundev/"
logging.config.fileConfig('%s/kunpy/ssrox/logging.conf' % each_env, defaults={'logfile_name': logname})
logger = logging.getLogger('SSROX')
os.chmod(logname, 0666)

# Parsing arguments
if len(sys.argv) != 5:
    print("PROGRAM requires X arguments")
    print("ZOODB_PATH MEAS_ROOTDIR GEOMFILE PDBCONFIG")
    sys.exit()
file_sqlite3 = sys.argv[1]
conn = sqlite3.connect(file_sqlite3)
cursor = conn.cursor()

df = pd.read_sql_query('SELECT * FROM ESA', conn)

# root directory should not be extracted from the value in the zoodb
# because the path should be replaced at beamline and laboratories soon.

meas_root = os.path.abspath(sys.argv[2])
if os.path.exists(meas_root) == False:
    logger.info("No such directories.")
    sys.exit()

# Data processing directory
proc_root = os.path.abspath(".")

# geom_orig = "/data02/sandbox/ssrox/original.geom"
# pdbfile = "/data02/sandbox/ssrox-test/hirata_proc/2oh6.pdb"
# pdbconf_file = "/data02/sandbox/ssrox/test_proc01/pdbfile.conf"

geom_orig = sys.argv[3]
pdbconf_file = sys.argv[4]

# PDB config file
try:
    pdbconf = PDBconfig.PDBconfig(pdbconf_file)
except Exception as e:
    print(e.args)
    sys.exit()

# ofile=open("sample_prep.txt","w")
for sample_name, newdf in df.groupby('sample_name'):
    puckids = newdf['puckid']
    pinids = newdf['pinid']
    n_mounts = newdf['n_mount']

    # For each sample consists of several pins
    n_hits_sample = 0
    for puckid, pinid, n_mount in zip(puckids, pinids, n_mounts):
        ppinfo = "%s-%02d" % (puckid, pinid)

        scan_dir = "%s/%s/scan%02d/ssrox/" % (meas_root, ppinfo, n_mount)
        logger.info("data directory = %s %s" % (sample_name, scan_dir))

        # Extract PDB file name from configure file
        try:
            pdbfile = pdbconf.getPDB(sample_name)
        except Exception as e:
            print(e.args)
            pdbfile = ""

        # Processing
        proc_dir = os.path.join(proc_root, ppinfo)
        if os.path.exists(proc_dir) == False:
            os.makedirs(proc_dir)
        ssrox_master = SSRM.SSROXpinMaster(scan_dir, proc_dir, geom_orig, pdbfile)
        try:
            ssrox_master.run(10, nproc=128, beam_dx=5, beam_dy=5, redo_flag=True)
        except Exception as e:
            logger.error(e.args)

    # ssrox_master = SSROXmaster(diffscan_log_path, sample_list_file, puckid,pinid)
    # n_hits_sample+=ssrox_master.run(5)

    # print(sample_name, n_hits_sample)
