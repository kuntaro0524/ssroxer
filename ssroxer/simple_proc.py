import sys
import SSROXmaster

if __name__ == "__main__":
    zoodb_file = sys.argv[1]
    meas_rootdir = sys.argv[2]
    geomfile_path = sys.argv[3]
    pdbconf_path = sys.argv[4]

    ssroxmaster = SSROXmaster.SSROXmaster(zoodb_file, meas_rootdir, geomfile_path, pdbconf_path)
    ssroxmaster.proc(nspots=10, nproc=12)