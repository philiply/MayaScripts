#ripple effect
#works on flat planes

import maya.cmds as cmds
import math

def ripple(height, radius = 3, thresh = 1, selectedObj = cmds.ls(sl=True)[0], maxTime = cmds.playbackOptions(q=True, maxTime=True)):
	#have an expanding radius until hit bounding box
	bbox = cmds.exactWorldBoundingBox(selectedObj) #which returns [xmin, ymin, zmin, xmax, ymax, zmax]
	
	cx,cy,cz = getCenter(bbox)
	print "center:", cx, cy, cz
	
	cmds.ConvertSelectionToVertices()
	#bbox[4] is ymax
	listOfVtx = [node for node in cmds.ls(sl=True, flatten=True) if cmds.xform(node, q=True, t=True)[1] >= bbox[4]]
	
	#have starting min radius
	#select the top vertices within radius and threshold and lift them up
	
	#have actual circle, then check for points certain distance away from radius
	#initial radius = 3, initial thresh = 1
	
	maxDist = max(bbox) + thresh
	#for loop till radius = maxDist
	#interval timed by maxDist/(maxTime-5)
	interval = (maxDist-radius)/(maxTime-5)
	
	for vtx in listOfVtx:
		cmds.setKeyframe(vtx, attribute='translateY', t=1)
	
	vtxEnterRipple = []
	vtxInRipple = []
	vtxExitRippe = []
	frame = 5
	currRad = radius
	# give 5ish frames for initial bump up, then rest of time to expand out
	for vtx in listOfVtx:
		if inCircle(cx, cz, radius, thresh, vtx):
			#set key
			vtxInRipple.append(vtx)
			cmds.setKeyframe(vtx, attribute='translateY', v=height, t=frame)
	
	#at frame, make sure to key up and down the next, or partially up?
	while frame < maxTime:
		
		#print "currRad:", currRad, 'frame:', frame
		frame += 1
		currRad += interval
	
	cmds.select(vtxInRipple)

def inCircle(cx, cz, radius, thresh, selectedVtx):
	#get x and z coords for every point and check if they are a certain distance from the center 
	vtxCoords = cmds.xform(selectedVtx, q=True, t=True)
	xCoord = vtxCoords[0]
	zCoord = vtxCoords[2]
	vtxDist = getDist2D(cx, cz, xCoord, zCoord)
	if vtxDist < (radius + thresh) or vtxDist > (radius - thresh):
		#print selectedVtx,"in circle with radius",radius
		return True
	else:
		return False

def getDist2D(p1a, p1b, p2a, p2b):
	return math.sqrt((p1a-p2a)**2 + (p1b-p2b)**2)
	
def getCenter(bbox):
	#bbox is list of min max values
	xCenter = (bbox[0] + bbox[3])/2
	print "xCenter:", xCenter
	yCenter = (bbox[1] + bbox[4])/2
	zCenter = (bbox[2] + bbox[5])/2
	return [xCenter, yCenter, zCenter]