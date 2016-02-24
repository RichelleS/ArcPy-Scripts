#-----------------------------------------------------------------------#
# Script Name:                                                          #
# Purpose:                                                              #
# Author: Richelle Spry                                                 #
# Created:                                                              #
# Copyright: -                                                          #
# ArcGIS Version:  10.2                                                 #
# Python Version:  2.7                                                  #
# Script Version:  1.0                                                  #
#-----------------------------------------------------------------------#

# Import system modules
import arcpy, os, time, sys

#------- start functions ------------------------------------------------
### Report error
def ReportError(e):

    import traceback, sys
    tb = sys.exc_info()[2]

    lineMessage = "Line %i" % tb.tb_lineno
    errorMessage = e
    if log != None:
        LogEntry(log, str(lineMessage))
        LogEntry(log, str(errorMessage))
        log.close()
    else:
        print str(lineMessage)
        arcpy.AddMessage(lineMessage)
        print str(errorMessage)
        arcpy.AddMessage(errorMessage)

    return

### log entry
def LogEntry(log, message):

    print message
    arcpy.AddMessage(message)

    time_str = time.strftime("%H:%M:%S %d/%m/%Y")
    log.write("%s   %s\n" % (time_str, message))
    log.flush()

    return


#------- end functions --------------------------------------------------

#try:
#    LogEntry(log, "Start")



#except Exception as e:
#    ReportError(e)