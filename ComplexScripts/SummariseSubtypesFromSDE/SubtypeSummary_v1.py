#-----------------------------------------------------------------------#
# Export all subtypes in feature classes to tables                      #
#-----------------------------------------------------------------------#

import os, sys
import arcpy

# Source SDE Connection
sde = "Database Connections/quwprddbs-gis02_gism_mofo.sde/" ##CH
datasets = ["gism.ARCFM.RecycledWater/", "gism.ARCFM.Water/", "gism.ARCFM.Sewer/"]

# Output Location
outloc = "C:/temp/Scripts/SubtypeCheck/"  ##CH

for set in datasets:
    arcpy.env.workspace = sde + set
    fclist = arcpy.ListFeatureClasses()

    for fc in fclist:
        fcfields = arcpy.ListFields(fc)
        for f in fcfields:
            fieldname = str(f.name)      ##Convert object to string
            if fieldname == "SubtypeCD":
                outfcname = str(fc.replace("gism.ARCFM.", ""))
                outtable = outloc + outfcname + ".dbf"
                arcpy.Frequency_analysis(fc, outtable, "SubtypeCD")
                domains = "C:/temp/MoFo/Domains/Domains.dbf"
                arcpy.JoinField_management(outtable, "SubtypeCD", domains, "CODE", ["DESCR", "DOMAIN"])
        
print "End"
