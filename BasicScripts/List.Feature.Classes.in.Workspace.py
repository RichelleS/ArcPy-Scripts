#-----------------------------------------------------------------------#
# Print on Screen all Feature Classes within a workspace                       #
#-----------------------------------------------------------------------#

arcpy.env.workspace = "F:/Project/W2B/Data/20130917_TenderWorking/01_Data/01_Data_GIS/PROD/"
fcs = arcpy.ListFeatureClasses()
for f in fcs:
	print f