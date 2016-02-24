mxd = arcpy.mapping.MapDocument("CURRENT")
layers = arcpy.mapping.ListLayers(mxd)
for l in layers:
	if l.isGroupLayer:
		print l.name, " (Group)"
	elif l.isFeatureLayer:
		print l.name
	elif l.isRasterLayer:
		print l.name, " (Raster)"