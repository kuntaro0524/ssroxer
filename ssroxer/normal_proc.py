import SSROXmaster
import sys, os, optparse

if __name__ == "__main__":
    parser = optparse.OptionParser()

    # zoodb_file = sys.argv[1]
    # meas_rootdir = sys.argv[2]
    # geomfile_path = sys.argv[3]
    # pdbconf_path = sys.argv[4]


    parser.add_option(
        "-z", "--zoodb",
        default="None",
        help="ZOO .db file for extracting sample/measurement information.",
        type="string",
        dest="zoodb"
    )

    parser.add_option(
        "-p", "--nproc",
        default=12,
        help="Number of CPUs for crystfel processing.",
        type="int",
        dest="nproc"
    )

    parser.add_option(
        "-s", "--nspots",
        default=5,
        help="Number of diffraction spots/image for data processing",
        type="int",
        dest="nspots"
    )

    parser.add_option(
        "-g", "--geom",
        default=None,
        help="geometry file for processing.",
        type="string",
        dest="geomfile"
    )

    parser.add_option(
        "-m", "--measurement_root",
        default=None,
        help="A root directory of the measurements.",
        type="string",
        dest="meas_root"
    )

    parser.add_option(
        "-c", "--pdbconf",
        default=None,
        help="Configure file of PDB files",
        type="string",
        dest="pdbconf"
    )

    (opts, args) = parser.parse_args()

    print(opts.nspots, opts.nproc, opts.zoodb, opts.geomfile, opts.meas_root, opts.pdbconf)

    ssroxmaster = SSROXmaster.SSROXmaster(opts.zoodb, opts.meas_root, opts.geomfile, opts.pdbconf)
    ssroxmaster.proc(opts.nspots, opts.nproc)
