# Script to automatically feed the output of one OOMMF simulation into the
# input of another
# Duncan Parkes
# deparkes.co.uk
import subprocess
import os
import glob

# We'll be using a function to help find the omf file output from oommf.
def get_omf(path):
	""" 
	A function to find the omf magnetisation vector files in a particular folder.
	We're only expecting one file so there's an if statement to try to 
	prevent things from going wrong if there are multiple files somehow
	Use os.path.basename(path) to strip away everything but the file name 
	from the path.
	"""    
    omf_path = '%s/*.omf' % (path)
    files = glob.glob(omf_path)
    if len(files) == 1: 
        omf_file = files[0]
        omf_file = os.path.basename(omf_file)
        print 'omf file'
        print omf_file
        return omf_file

# define the path to your oommf install
path_oommf = 'C:/oommf-1.2a5bis/oommf.tcl'

# the name of the input mif file
mif_file = os.path.abspath('../examples/squarecubic_scripted2.mif')

# This time we will use the default size values in our mif file, but will be 
# looping through a series of anisotropy values in KJ/m3
anisotropies = [530, 630, 730, 830]

# The first value of Kc used was 430kJ/m3. The omf file from this value is the
# one that will be used for the initialisation.

# We will also pass the name of the initial magnetisation vector file we will
# start from
initial_omf_file = '../examples/squarecubic_scripted2_start_file.omf'

# We'll be making a new folder for each Kc value we pass into OOMMF.
# To try and avoid too many complications we'll be checking that that folder
# doesn't already exist - if it doesn't we'll create it

# We'll be over-writing this after the first iteration
in_omf = initial_omf_file

for Kc in anisotropies:
	# Set our output folder for this iteration
	out_folder = '../output/Kc_%s' % Kc
	
	# If this folder doesn't already exist, let's make it
	if not os.path.exists(out_folder):
		os.makedirs(out_folder)
			
	# Prepare our string to call oommf
	oommf_string = 'tclsh85' + ' ' + path_oommf + \
	' boxsi -parameters \"in_omf %s Kc %s out_folder %s\" -- %s' % \
	 (in_omf, Kc ,out_folder, mif_file)
	subprocess.call(oommf_string, shell=True)
	
	# After this runs the new output file should be in the new output folder.
	# So we can use the get_omf function to find the omf file in that folder.
	in_omf = out_folder + '/' + get_omf(out_folder)
