mxd = arcpy.mapping.MapDocument("CURRENT")
layers = arcpy.mapping.ListLayers(mxd)
for l in layers:
	if l.isFeatureLayer:
		coreName = l.datasetName
		if l.name != "AreaOfInterest":
			print 'Input: ' + l.name + "(" + coreName + ")"
			address = 'C:\Users\spryr\Documents\ArcGIS\ExtractTest.gdb\\' + coreName + '_clip'
			print 'Output: ' + address
			arcpy.analysis.Clip(l, "AreaOfInterest", address)
	
	
	
	
	
		name = str(l.name)
		newName = "_".join(name.split())
		chaRemove = newName.translate(None, "()/\$?;:-")
		print chaRemove
		print 'Input: ' + name
		if name != "AreaOfInterest":
			address = 'C:\Users\spryr\Documents\ArcGIS\ExtractTest.gdb\\' + newName + '_clip'
			print 'Output: ' + address
			arcpy.analysis.Clip(l, "AreaOfInterest", address)