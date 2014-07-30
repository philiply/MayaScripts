#Pixelizer by Philip Ly

import maya.cmds as cmds

#make sure you have the model you want to pixelize selected already
def pixelizer():
	#grab object name
	objname = cmds.ls(sl=True).pop()
	
	#initial cube to be instanced
	cmds.polyCube(n='pixelcube')
	cmds.hide('pixelcube')
	
	#reselect the object to be pixelized
	cmds.select(objname)
	
	#selects all vertices
	cmds.ConvertSelectionToVertices()
	listofvertices = cmds.ls(selection=True)
	
	#this grabs the string that will be parsed to get the max number of vertices of the geo selected
	lestring = listofvertices.pop()
	
	#find the index of the last ':' and the index of the last ']' and grab the string in between these indices to get the max vertex number
	#ex: pCube1.vtx[0:7]
	begin = lestring.rfind(':')+1
	end = lestring.index(']')
	totalvertices = int(lestring[begin:end]) + 1
	
	print totalvertices
	
	#create a dictionary that stores 3-slot arrays that tell position of a vertex already drawn
	drawnvtxdict = {}
	
	#store number of boxes drawn
	boxnum = 0
	
	#for loop through number of vertices
	for vtxnum in range(0, totalvertices):
		#gets string to select specified vertex
		nextvtx = objname + '.vtx[' + str(vtxnum) + ']'
		cmds.select(nextvtx)
		#to get value of position (a 3 slot array), make the new instanced cubename, then create an array of the int values
		pos = cmds.xform(ws=True, q=True, t=True)
		x1 = str(int(pos[0]))
		y1 = str(int(pos[1]))
		z1 = str(int(pos[2]))
		intposstr = x1+','+y1+','+z1
		 
		#check if dictionary empty!!!!!! 
		if (drawnvtxdict.__len__() == 0):
			newcubename = 'pixelcube' + str(boxnum)
			cmds.select('pixelcube')
			cmds.instance(n=newcubename)
			cmds.xform(t=(int(pos[0]), int(pos[1]), int(pos[2])))
			cmds.showHidden(newcubename)
			drawnvtxdict[intposstr] = True
			boxnum+=1
		else:
			if (not intposstr in drawnvtxdict.keys()):
				newcubename = 'pixelcube' + str(boxnum)
				cmds.select('pixelcube')
				cmds.instance(n=newcubename)
				cmds.xform(t=(int(pos[0]), int(pos[1]), int(pos[2])))
				cmds.showHidden(newcubename)
				drawnvtxdict[intposstr] = True
				boxnum += 1
		
		print str(boxnum) + ' boxes drawn : ' + str(vtxnum+1) + ' of ' + str(totalvertices) + ' done'
	
	#selects all newly created blocks
	cmds.select('pixelcube*')
	
	#groups them together
	cmds.group(n='pixelated_obj')
	
	cmds.hide(objname)
	
def particle_pixelizer():
	#grab object name
	objname = cmds.ls(sl=True).pop()
	
	#selects all vertices
	cmds.ConvertSelectionToVertices()
	listofvertices = cmds.ls(selection=True, flatten=True)
	
	#get the number of total vertices
	totalvertices = len(listofvertices)
	
	print 'Total Vertices: ' + str(totalvertices)
	
	#create a list that stores 3-slot arrays that tell position of a vertex already drawn
	drawnvtxList = []
	
	#store number of boxes drawn
	partnum = 0
	vertexRead = 0
	
	#for loop through number of vertices
	#for vtxnum in range(0, totalvertices):
	for vtx in listofvertices:
		cmds.select(vtx)
		#to get value of position (a 3 slot array), make the new instanced cubename, then create an array of the int values
		pos = cmds.xform(ws=True, q=True, t=True)
		x1 = str(int(pos[0]))
		y1 = str(int(pos[1]))
		z1 = str(int(pos[2]))
		intposList = [x1, y1, z1]
		 
		#check if list empty!!!!!! 
		if (drawnvtxList.__len__() == 0):
			drawnvtxList.append(intposList)
			partnum+=1
		else:
			if (not intposList in drawnvtxList):
				drawnvtxList.append(intposList)
				partnum += 1
		vertexRead += 1
		print str(partnum) + ' positions kept : ' + str(vertexRead) + ' of ' + str(totalvertices) + ' done'
	
	print drawnvtxList
		
	
	cmds.particle(p=drawnvtxList, n='instancePositions')

def instanceThis():
	#grab object name
	objname = cmds.ls(sl=True).pop()
	
	#if there are particles
	if (cmds.objExists('instancePositions')):
		#make an instancer with the particles with object selected.
		cmds.particleInstancer('instancePositionsShape', addObject=True, object=objname)

#list must be only numbers
def multiplyList(list1, f):
	tmp = list1
	for i in range(len(list1)):
		tmp[i] = list[i] * f
	return tmp