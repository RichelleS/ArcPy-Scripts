#-----------------------------------------------------------------------#
# Script Name: MxdDetailsInFolderToExcel.py
# Purpose: Iterates through a specified folder of MXDs and outputs into excel: the MXD name, tile of mxd, and map title (map element), last published date
# Author: Richelle Spry
# Created: February 2015
# ArcGIS Version: 10.2
# Python Version: 2.7
# Script Version: 1.0
#-----------------------------------------------------------------------#

# Import system modules
import os
import sys
import datetime
import xlwt
import arcpy

'''------- start classes --------------------------------------------------'''
'''------- start classes --------------------------------------------------'''

'''------- start functions ------------------------------------------------'''

# Set regression level of input folder (source: http://stackoverflow.com/questions/229186/os-walk-without-digging-into-directories-below)
def walk_level(some_dir, fol_level):
    if fol_level == 'Current Folder Only':
        level = 0
    else:
        level = 1
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.isdir(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        yield root, dirs, files
        num_sep_this = root.count(os.path.sep)
        if num_sep + level <= num_sep_this:
            del dirs[:]


# Ensure name length is suitable to excel sheet naming standards (source ESRI TableToExcel.py tool)     ## Cannot be greater than 31 charaters and no \ / ? * [ ]
def validate_sheet_name(sheet_name):

    import re
    if len(sheet_name) > 31:
        sheet_name = sheet_name[:31]

    # Replace invalid sheet character names with an underscore
    r = re.compile(r'[:\\\/?*\[\]]')
    sheet_name = r.sub("_", sheet_name)

    return sheet_name


# Obtain internal MXD details of title, element text, last export date
def mxd_details(MapDocLoc):

    mxd  = arcpy.mapping.MapDocument(MapDocLoc)

    arcpy.AddMessage("Checking " + MapDocLoc)

    # Get Map Element Text (map title)
    arcpy.AddMessage("Checking map elements")

    if mxd.author:
        mxdAuthorTxt = str(mxd.author)
    else:
        mxdAuthorTxt = '--'        #"*No 'Author'*"

    mxdPrjTxt = "--"            #"*No 'ProjectTitle'*"
    mxdFigNumTxt = "--"         #"*No 'FigureNo'*"
    mxdFigTitleTxt = "--"       #"*No 'FigureTitle'*"
    mxdAprovTxt = "--"          #"*No 'Approval'*"
    
    mxdElmTxt = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT")                       # Check elements exist in mxd - slow need something better
    if mxdElmTxt:
        for elm in mxdElmTxt:
            if elm.name == 'ProjectTitle':
                mxdPrjTxt = str(elm.text)                                                   # Need to better handle formatting tags (http://www.pythoncentral.io/cutting-and-slicing-strings-in-python/)
            elif elm.name == 'FigureNo':
                mxdFigNumTxt = str(elm.text)
            elif elm.name == 'FigureTitle':
                mxdFigTitleTxt = str(elm.text)  
            elif elm.name == 'Approval':
                mxdAprovTxt = str(elm.text) 
            elif elm.name == 'Author':
                if mxdAuthorTxt == "--":         # "*No 'Author'*":
                    mxdAuthorTxt = str(elm.text)
                else:
                    continue
            else:
                continue
    else:
        mxdPrjTxt = "--"    #"*No Text Elements in Map Document*"
  
    # Get Last Export Date
    if mxd.dateExported:
        format = '%d/%m/%Y, %I:%M%p'
        mxdExpDate = mxd.dateExported
        if mxdExpDate.year >= 1900:
            mxdExpDateStr = mxdExpDate.strftime(format)
        else:
            mxdExpDateStr = "--"
    else:
        mxdExpDateStr = "--"                #"*No Export Date*"

    del format, mxdExpDate, mxdElmTxt
    return mxdPrjTxt, mxdFigNumTxt, mxdFigTitleTxt, mxdAuthorTxt, mxdAprovTxt, mxdExpDateStr


# Generate output (Main Code)
def mxd_to_excel(inFolder, outWorkbook, folderLvl):

    # Create spreadsheet with file name as sheet name
    workbook = xlwt.Workbook()
    sheet1 = workbook.add_sheet(
            validate_sheet_name(os.path.splitext(os.path.basename(outWorkbook))[0]))

    # Set cell format/style for header 
    xlwt.add_palette_colour("hdcolour", 0x21)
    workbook.set_colour_RGB(0x21, 7, 97, 183)

    headerStyle = 'font: bold on, color white; align: horiz center; pattern: pattern solid, fore_color hdcolour'
    headerCols = ['MXD File Name','Project Title','Figure Number','Figure Title','Author','Approver','Export Date']

    timeNow = datetime.datetime.now()
    sheetCreateInfo = "Generated: " + timeNow.strftime('%d/%m/%Y, %I:%M%p')
    sheet1.row(0).write(0, sheetCreateInfo, xlwt.Style.easyxf('font: bold on, color red, italic on, height 160')) # Font height 8pt (20*8)

    naStyle = 'font: height 160' # Font height 8 * 20 for 8pt

    hdColIndex = 0
    for i in headerCols:
        sheet1.row(1).write(hdColIndex, headerCols[hdColIndex], xlwt.Style.easyxf(headerStyle))
        hdColIndex += 1
    sheet1.col(0).width = 256 * 25
    sheet1.col(1).width = 256 * 40
    sheet1.col(2).width = 256 * 22
    sheet1.col(3).width = 256 * 40
    sheet1.col(4).width = 256 * 22
    sheet1.col(5).width = 256 * 22
    sheet1.col(6).width = 256 * 22

    # If file is an mxd, add required information to excel cells
    row = 2                                                                         # Set row to start below header
    col = 1
    info = 0
    for root, dirs, files in walk_level(inFolder, folderLvl):
        for f in files:
            if os.path.splitext(f)[1] == '.mxd':
                mxd = os.path.join(root, f)
                mxdinfo = mxd_details(mxd)
                link = 'HYPERLINK("' + mxd + '"; "' + f + '")'
                sheet1.write(row, 0, xlwt.Formula(link), xlwt.Style.easyxf('font: color blue'))
                sheet1.write(row, 1, mxdinfo[0])
                sheet1.write(row, 2, mxdinfo[1])
                sheet1.write(row, 3, mxdinfo[2])
                sheet1.write(row, 4, mxdinfo[3])
                sheet1.write(row, 5, mxdinfo[4])
                sheet1.write(row, 6, mxdinfo[5])
                row += 1
            else:
                continue

    workbook.save(outWorkbook)
    arcpy.AddMessage(str(row) + ' rows added to Excel')
    os.startfile(outWorkbook)

'''------- end functions --------------------------------------------------'''

try:

    inputFolder = arcpy.GetParameterAsText(0)                 # Set Folder 
    outputExcel = arcpy.GetParameterAsText(1)                 ## When assigning in Toolbox, set Properties/(File) Filter to 'File' then: xls, xlsx
    folderLevel = arcpy.GetParameterAsText(2)                       # "Current Folder Only" or "Current Folder and Sub Folders"

    if __name__ == "__main__":
        mxd_to_excel(inputFolder, outputExcel, folderLevel)

except Exception as e: ##Check for better error handling
    print e.message
    arcpy.AddMessage(e)
