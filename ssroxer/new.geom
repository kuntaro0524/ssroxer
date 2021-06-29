photon_energy=12398.40
; adu_per_eV      = 0.00015272 ; 1 / photon_energy
adu_per_photon = 1 ; in future versions, you can specify like this
clen =  0.18000; /entry/instrument/detector/detector_distance
res             = 13333.3 ; 1 m / 75 um
max_adu         = 165904.0 ; /entry/instrument/detector/detectorSpecific/countrate_correction_count_cutoff

0/min_fs        = 0
0/max_fs        = 3109 ; /entry/instrument/detector/detectorSpecific/x_pixels_in_detector - 1
0/min_ss        = 0
0/max_ss        = 3268 ; /entry/instrument/detector/detectorSpecific/y_pixels_in_detector - 1
0/corner_x = -1551.600000
0/corner_y = -1590.180000
0/fs            = x
0/ss            = y

0/data = /entry/data/data
0/dim0 = %
0/dim1 = ss
0/dim2 = fs

; used by geoptimiser
rigid_group_0 = 0
rigid_group_collection_0 = 0

0/mask = /pixel_mask
0/mask_file = /isilon/users/target/target/AutoUsers/200131/abe/_yamproc/crystfel/mask.h5
mask_good = 0x00
mask_bad  = 0xFF
