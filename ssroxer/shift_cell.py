import sys
import os
import re

geom = sys.argv[1]
dx, dy = sys.argv[2:]

out = "%s_%s.geom" % (dx,dy)
dx, dy = float(dx), float(dy)

ofs = open(out, 'w')
for l in open(geom):
  if "corner_x" in l:
    v = float(l[l.index("=")+1:])
    l = l[:l.index("=")] + "= %f\n" % (v+dx)
  if "corner_y" in l:
    v = float(l[l.index("=")+1:])
    l = l[:l.index("=")] + "= %f\n" % (v+dy)
  ofs.write(l)