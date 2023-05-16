import os
import time
import arcpy
from arcpy.sa import *

in_nc = arcpy.GetParameterAsText(0)  # input .nc file ("time" variable is multidimensional) 
out_folder = arcpy.GetParameterAsText(1)  # folder of output tiff files
variable = arcpy.GetParameterAsText(2)  # name of target variable

# Input data source
in_folder, nc_file = os.path.split(in_nc)

arcpy.env.workspace = in_folder
arcpy.env.overwriteOutput = True

# Loop through a list of times
times = range(0, 187) # target time range 
nums = len(times)
for num, t in enumerate(times):
    s = time.time()
    inNCfiles = in_nc
    fileroot = nc_file + "_" + str(num)
    outRaster = out_folder + "/" + fileroot
    try:
        temp = "time {0}".format(t)
        # Process1: Make NetCDF Raster Layer
        arcpy.MakeNetCDFRasterLayer_md(inNCfiles, variable, "lon", "lat", variable, "", temp, "BY_INDEX")
        # Process2: Copy Raster
        arcpy.CopyRaster_management(variable, outRaster + ".tif", "", "", "", "NONE", "NONE", "")
        e = time.time()
        arcpy.AddMessage("{0}/{1} | {2} Completed, time used {3}s".format(num+1, nums, t, e-s))
    except:
        arcpy.AddMessage("{0}/{1} | {2} Errored".format(num+1, nums, t))
