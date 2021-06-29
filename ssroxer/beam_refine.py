import os, sys, optparse
import SSROXmaster

if __name__ == "__main__":

    parser = optparse.OptionParser()

    parser.add_option(
        "--nw", "--nwing",
        default=2,
        help="wing is the number of conditions add to the left/right and upper/lower wings",
        type="int",
        dest="nwing"
    )

    parser.add_option(
        "--stp", "--step",
        default=3,
        help="pixel length between each grid.",
        type="int",
        dest="step"
    )

    (options, args) = parser.parse_args()

    print(options.nwing, options.step)

    zoodb_file = sys.argv[1]
    meas_rootdir = sys.argv[2]
    geomfile_path = sys.argv[3]
    pdbconf_path = sys.argv[4]

    ssroxmaster = SSROXmaster.SSROXmaster(zoodb_file, meas_rootdir, geomfile_path, pdbconf_path)

    # beam position calculation
    count=0
    for i in range(-options.nwing, options.nwing+1):
        for j in range(-options.nwing, options.nwing + 1):
            dx = i * options.step
            dy = j * options.step
            print(dx, dy)
            count+=1

    # Min/Max X
    min = -options.nwing * options.step
    max = options.nwing * options.step

    print("Counter=", count)
    print("Min/Max = ", min, max)
    ssroxmaster.refineBeam(10, "WTPhC1", min_dx=min, max_dx=max, min_dy=min, max_dy=max, step=options.step)
