import sys, os
import Libs.DiffscanLog as DiffscanLog
import Libs.SummaryDat as SD
import logging

# In this class: only puck and pin are important
# This class focuses to process each dataset only.
class SSROXpinMaster:
    def __init__(self, scan_dir, proc_dir, geom_file, pdbfile):
        #self.root_dir = root_dir

        # diffscan.log path
        # Scan directory should change if the data is transferred to other places.
        self.scan_dir = scan_dir
        self.diffscan_log_path=os.path.join(scan_dir,"diffscan.log")
        self.spotfinder_dir=os.path.join(scan_dir, "_spotfinder")
        self.sumdat_path=os.path.join(self.spotfinder_dir, "summary.dat")
        self.sample_name = "none"
        self.logger = logging.getLogger("SSROX").getChild("SSROXpinMaster")
        self.logger.info("Start SSROXpinMaster")

        # Data processing directory
        self.proc_dir=proc_dir

        # The original geometry file
        self.geom_file = geom_file

        # The PDB file for setting cell parameters
        self.pdbfile = pdbfile

    # Check all required files 2021/06/23
    def checkRequiredFiles(self):
        # scan directory should exist
        if os.path.exists(self.scan_dir) == False:
            self.logger.info("scan directory cannot be found: %s" % self.scan_dir)
            raise Exception("scan directory cannot be found: %s" % self.scan_dir)
        # _spotfinder directory should exist
        if os.path.exists(self.spotfinder_dir) == False:
            self.logger.info("_spotfinder directory cannot be found: %s" % self.spotfinder_dir)
            raise Exception("_spotfinder directory cannot be found: %s" % self.spotfinder_dir)
        # diffscan.log
        if os.path.exists(self.diffscan_log_path) == False:
            self.logger.info("diffscan.log was not in %s" % self.diffscan_log_path)
            raise Exception("diffscan.log cannot be found: %s" % self.diffscan_log_path)
        # diffscan.log, summary.dat are essential files
        if os.path.exists(self.sumdat_path)==False:
            self.logger.error("%s does not exist" % self.sumdat_path)
            raise Exception("summary.dat cannot be found: %s" % self.sumdat_path)

        self.logger.info("File check Okay!")
        return True

    def prepProcessing(self, nspot_thresh=10, redo_flag=False):
        # read prefix from diffscan.log
        dsl = DiffscanLog.DiffscanLog(self.scan_dir, "diffscan.log")
        allstep, block = dsl.getNewestScan()
        nv, nh, vstep_mm, hstep_mm = allstep

        # Number of frames in this scan
        self.n_frame_in_scan = len(block)

        # summary.dat does not exist -> spot finding is not done.
        try:
            self.checkRequiredFiles()
        except Exception as e:
            raise Exception(e)
        # check
        try:
            hit_file_path = self.checkAndMakeListFile(nspot_thresh, nv, nh, redo_flag=redo_flag)
        except Exception as e:
            raise Exception(e)

        abs_path = os.path.abspath(hit_file_path)
        return abs_path

    def checkAndMakeListFile(self, nspot_thresh, nv, nh, redo_flag=False):
        # name of hits
        hitsfile = "hits.lst"

        checkpath = os.path.join(self.proc_dir, hitsfile)
        if os.path.exists(checkpath) and redo_flag==False:
            self.logger.info("Already processed. %s" % checkpath)
            return True

        # Check if summary.dat completely contains all results of spot finding
        sd_class = SD.SummaryDat(self.spotfinder_dir, nv, nh)
        sd_class.setMinMax(nspot_thresh, 1000)
        nimages_all = nv * nh
        comp_thresh = 1.0 # the maximum 100% -> 1.0
        # Prepare the information
        try:
            sd_class.readSummary("ssrox",nimages_all,comp_thresh,timeout=0.0)
            hits_lines = sd_class.makeSSROXprocList()
        except Exception as e:
            self.logger.error("summary.dat could not read correctly.")
            raise(e)

        # Read and write the log
        ofile = open(checkpath, "w")
        for line in hits_lines:
            ofile.write(line)
        ofile.close()

        if os.path.exists(checkpath):
            return checkpath
        else:
            raise Exception("Error to generate!")

    # 210616 for beam position alignment.
    def countMeasuredFrames(self):
        print("prep")

    def countNspots(self):
        print("prep")

    def readSampleTxt(self):
        print("prep")

    def makeImageList(self, nspot_thresh=10):
        for img_num in img_list:
            tmpi = img_num - 1
            n = int(tmpi / 100) + 1
            j = tmpi % 100

            print(img_num, n, j)

    def run(self, nspot_thresh, nproc=12, beam_dx=0.0, beam_dy=0.0, redo_flag=False):
        try:
            path_of_hits = self.prepProcessing(nspot_thresh=nspot_thresh, redo_flag=redo_flag)
        except Exception as e:
            raise Exception(e)

        # Prep geometry file
        prefix = os.path.join(self.proc_dir, "ssrox_proc")

        import Geometrer
        geometrer = Geometrer.Geometrer(self.geom_file, self.proc_dir)

        # Beam position refinement
        if beam_dx!=0.0 or beam_dy!=0.0:
            geometrer.shift_beam(beam_dx, beam_dy)
        # Generating the geometry file for processing
        try:
            geom_path = geometrer.makeGeom("ssrox.geom")
        except Exception as e:
            logstr = "run() geometrer exception: %s" % e.args[0]
            self.logger.info(logstr)
            raise Exception(logstr)
        self.logger.info("new geom file=%s" % geom_path)
        # Prep CrystFEL filse
        # checking if the defined PDB model exists or not
        if os.path.exists(self.pdbfile)==False:
            self.logger.info("%s does not exist." % self.pdbfile)
            self.pdbfile = "none"
        params = {
            "geom": geom_path,
            "pdb": self.pdbfile,
            "prefix": prefix,
            "hitfile": path_of_hits,
            "proc_root": self.proc_dir,
            "nproc": nproc
        }
        self.prepCrystFELscripts(params)

    def prepCrystFELscripts(self, params):
        import CrystFELer
        cf = CrystFELer.CrystFEELer(self.proc_dir, params)
        jobscript = os.path.join(self.proc_dir, "crystfel.sh")
        cf.genJobScript(jobscript)

if __name__ == "__main__":
    scan_dir = sys.argv[1]

    print("PROGEAM DIFFSCAN_LOG_PATH SAMPLE_LIST_FILE PUCKID PINID")
    puckid=sys.argv[2]
    pinid = int(sys.argv[3])
    procd=sys.argv[4]

    #ssrox_master = SSROXmaster(diffscan_log_path, sample_list_file, puckid,pinid)
    # ssrox_master.run(10, redo_flag=True)
    geom_orig="/data02/sandbox/ssrox-test/hirata_proc/original.geom"
    pdbfile = "/data02/sandbox/ssrox-test/hirata_proc/2oh6.pdb"
    ssrox_master=SSROXpinMaster(scan_dir, puckid, pinid, procd, geom_orig, pdbfile)
    # ssrox_master.tuneBeamPosition(10, 5, 5, redo_flag=True)
    try:
        ssrox_master.run(10, beam_dx=5, beam_dy=5, redo_flag=True)
    except Exception as e:
        print(e.args)
