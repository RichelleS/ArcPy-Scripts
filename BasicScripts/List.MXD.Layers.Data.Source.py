#-----------------------------------------------------------------------#
# Script Name: ListLayersDataSource.py                                  #
# Purpose: Sorted List of Layer datasources from a specified mxd        #
# Author: Richelle Spry                                                 #
# Created: 28/01/2015                                                   #
# ArcGIS Version:  10.2                                                 #
# Python Version:  2.7                                                  #
# Script Version:  1.0                                                  #
#-----------------------------------------------------------------------#

# Import system modules
import arcpy, os, sys

#------- start functions ------------------------------------------------
#------- end functions --------------------------------------------------

try:
    #Set input parameters
    arcpy.AddMessage("Start")
    mxd = arcpy.GetParameterAsText(0)
    outputTxtFile = arcpy.GetParameterAsText(1)

    #Open txt file
    outputTxtFileWrite = open(outputTxtFile, "w")

    #Create temporary list
    lyrList = []

    #Check layer supports datasource and add to list
    mxdDoc = arcpy.mapping.MapDocument(mxd)
    for lyr in arcpy.mapping.ListLayers(mxdDoc):
        if lyr.supports("DATASOURCE"):
            lyrSource = lyr.dataSource
            lyrList.append(lyrSource)
            arcpy.AddMessage("Creating List")

    #Sort list and write to text file            
    lyrList.sort()
    arcpy.AddMessage("Sorting List")
    for i in lyrList:
        outputTxtFileWrite.write(i + "\n")
        arcpy.AddMessage("Writing to file")

    outputTxtFileWrite.close()
    arcpy.AddMessage("End")
    del mxd, lyrList
    os.startfile(outputTxtFile)

except Exception as e:
    print arcpy.GetMessages()
    arcpy.AddMessage(e)