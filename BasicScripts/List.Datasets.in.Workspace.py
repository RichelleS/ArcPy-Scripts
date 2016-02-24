#-----------------------------------------------------------------------#
# Print on Screen all Datasets within a workspace                       #
#-----------------------------------------------------------------------#

arcpy.env.workspace = "F:/Project/W2B/Data/20130917_TenderWorking/01_Data/01_Data_GIS/MAINT/"
fcs = arcpy.ListDatasets()
for f in fcs:
	print f