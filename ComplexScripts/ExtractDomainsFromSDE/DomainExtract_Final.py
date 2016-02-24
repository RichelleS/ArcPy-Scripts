#-----------------------------------------------------------------------#
# Export all coded value domains in a geodatabase to tables in that gdb #
#-----------------------------------------------------------------------#
# Created: Richelle Spry
# Date: 2012

import os, sys
import arcpy

# Source SDE Connection
sde = "Database Connections/quwprddbs-gis02_gism_mofo.sde/" ##CH

# Workspace & Output Location
outloc = "C:/temp/MoFo/Domains/"  ##CH
arcpy.env.workspace = outloc

# Create Final Table
arcpy.CreateTable_management(outloc, "Domains.dbf")
arcpy.AddField_management("Domains.dbf", "CODE", "TEXT", "", "", 50)
arcpy.AddField_management("Domains.dbf", "DESCR", "TEXT", "", "", 100)
arcpy.AddField_management("Domains.dbf", "DOMAIN", "TEXT", "", "", 100)

##Final table
outfinal = outloc + "Domains.dbf"
## Delete extra field
arcpy.DeleteField_management(outfinal, "Field1")


# Create Working Folder
arcpy.CreateFolder_management(outloc, "Working")
workingloc = outloc + "Working/"

# Domain to Output Table
desc = arcpy.Describe(sde)
domains = desc.domains
arcpy.env.workspace = workingloc

##Create string list of domains
domlist = []

for domain in domains:
    domlist.append(str(domain))

##Run through list of domains and create table outputs
for dom in domlist:
    print dom
    issue = "/"
    if issue in dom:
        newdome = dom.replace("/", "")
        print newdome
        output = newdome + ".dbf"
        arcpy.DomainToTable_management(sde, dom, output, "CODE", "DESCR")
        arcpy.AddField_management(output, "DOMAIN", "TEXT", "", "", 100)
    else:
        output = dom + ".dbf"
        arcpy.DomainToTable_management(sde, dom, output, "CODE", "DESCR")
        arcpy.AddField_management(output, "DOMAIN", "TEXT", "", "", 100)        

    arcpy.CalculateField_management(output, "DOMAIN", "\"" + dom + "\"", 'PYTHON_9.3')

    domtableout = outloc + "Domains.dbf"
    arcpy.Append_management(output, domtableout, "NO_TEST")

# Delete Working Folder - Uncomment if required
##arcpy.Delete_management(workingloc)
    
print "End"
