import subprocess
import os
# define the path to your oommf install
path_oommf = 'C:/oommf-1.2a5bis/oommf.tcl'

# the name of the mif file
mif_file = os.path.abspath('../examples/squarecubic_scripted.mif')

# make our list of sizes that we will loop through
# in nm as our mif file converts to metres.
sizes = [100, 200, 300, 400]

for size in sizes:
	oommf_string = 'tclsh85' + ' ' + path_oommf + \
	' boxsi -parameters \"xsize %s ysize %s\" -- %s' % \
	 (size, size, mif_file)
	print oommf_string
	subprocess.call(oommf_string, shell=True)
