import sys, os
import Libs.DiffscanLog as DiffscanLog
import Libs.SummaryDat as SD
import logging

# SSROX data processing of each geom file
class ProcMaster:
    def __init__(self, scan_dir, puck, pin, proc_dir):
        #self.root_dir = root_dir

        # diffscan.log path
        self.scan_dir = scan_dir
        self.diffscan_log_path=os.path.join(scan_dir,"diffscan.log")
        self.spotfinder_dir=os.path.join(scan_dir, "_spotfinder")
        self.sumdat_path=os.path.join(self.spotfinder_dir, "summary.dat")
        #self.sample_list_file = sample_list_file
        self.puck = puck
        self.pin = pin
        self.sample_name = "none"
        self.logger = logging.getLogger("TEST")
        self.logger.info("TEST")

        # Data processing directory
        self.proc_dir=proc_dir

    def init(self):
        # diffscan.log path
        path_diffscan = "%s/diffscan.log" % scan_dir
        print(path_diffscan)
        # summary.dat path
        summary_path = "%s/_spotfinder/summary.dat" % scan_dir
        print(summary_path)

    def prepProcessing(self, nspot_thresh=10, redo_flag=False):
        # read prefix from diffscan.log
        dsl = DiffscanLog.DiffscanLog(self.scan_dir, "diffscan.log")
        allstep, block = dsl.getNewestScan()
        nv, nh, vstep_mm, hstep_mm = allstep

        # Number of frames in this scan
        self.n_frame_in_scan = len(block)

        # summary.dat does not exist -> spot finding is not done.
        if os.path.exists(self.sumdat_path)==False:
            print("%s does not exist" % self.sumdat_path)
            if os.path.exists(self.scan_dir)==True:
                print("Scan directory %s exists." % self.scan_dir)
            if os.path.exists(self.diffscan_log_path)==True:
                print("diffscan.log exists.")
            return -1

        # check
        cnt_good_frames = self.checkAndMakeListFile(nspot_thresh, nv, nh, redo_flag=redo_flag)

        return cnt_good_frames

    def checkAndMakeListFile(self, nspot_thresh, nv, nh, redo_flag=False):
        # name of hits
        hitsfile = "hits_ssrox_test.lst"

        checkpath = os.path.join(self.scan_dir, hitsfile)
        if os.path.exists(checkpath) and redo_flag==False:
            self.logger.info("Already processed. %s" % checkpath)
            return True

        # Check if summary.dat completely contains all results of spot finding
        sd_class = SD.SummaryDat(self.spotfinder_dir, nv, nh)
        sd_class.setMinMax(nspot_thresh, 1000)
        nimages_all = nv * nh
        comp_thresh = 1.0 # the maximum 100% -> 1.0
        # Prepare the information
        sd_class.readSummary("ssrox",nimages_all,comp_thresh,timeout=120)
        hits_lines = sd_class.makeSSROXprocList(self.proc_dir)

        # Read and write the log
        ofile = open(checkpath, "w")
        for line in hits_lines:
            ofile.write(line)
        ofile.close()

        return len(hits_lines)

    def countMeasuredFrames(self):
        print("prep")

    def countNspots(self):
        print("prep")

    def readSampleTxt(self):
        print("prep")

    def makeCrystFelCom(self):
        print("prep")

    def makeImageList(self, nspot_thresh=10):
        for img_num in img_list:
            tmpi = img_num - 1
            n = int(tmpi / 100) + 1
            j = tmpi % 100

            print(img_num, n, j)

    def run(self, nspot_thresh, redo_flag=False):
        cnt_good_frames = self.prepProcessing(nspot_thresh=nspot_thresh,redo_flag=redo_flag)
        if cnt_good_frames==-1:
            print("Strange")

        # Making the list of images to be processed
        # makeImageList();
        return cnt_good_frames

if __name__ == "__main__":
    scan_dir = sys.argv[1]

    print("PROGEAM DIFFSCAN_LOG_PATH SAMPLE_LIST_FILE PUCKID PINID")
    puckid=sys.argv[2]
    pinid = int(sys.argv[3])
    procd=sys.argv[4]

    # print("TESTESTEST")
    ssrox_master=SSROXpinMaster(scan_dir, puckid, pinid, procd)
    #ssrox_master = SSROXmaster(diffscan_log_path, sample_list_file, puckid,pinid)
    ssrox_master.run(10, redo_flag=True)
