###################
### Autocity script
### By Philip Ly
### Generate a procedural city from just a plane object!
### Call autocity(type), type = 0 for city, type = 1 for suburban
### (make sure plane is selected)
####################

import maya.cmds as cmds
import random

#make sure to select an object (preferably plane) first
#type variable could be 0 = city, 1 = suburban, 2 = sparse/rural
def autoCity(type):
	objName = cmds.ls(sl=True).pop()
	#objName = cmds.rename(objName, 'autoCity')
	
	cmds.ConvertSelectionToFaces()
	
	listOfFaces = cmds.ls(sl=True, flatten=True)
	
	numOfFaces = len(listOfFaces)
	currentFace = 1
	
	clearHistoryCount = 0
	
	for f in listOfFaces:
		cmds.select(f)
		if type == 0:
			randHeight = random.randint(2,6)
			ifPark = random.randint(0,4)
			ifPointy = random.randint(0,10)
			ifRectBuilding = random.randint(0,20)
			ifTwist = random.randint(0,40)
			
			
			if ifPark == 0:
				makePark()
			elif ifRectBuilding==0:
				makeRectBuilding(randHeight)
			elif ifPointy==0:
				makePointy(randHeight)
			elif ifTwist==0:
				makeTwistingBuilding(randHeight)
			else:
				makeRegular(randHeight)
		elif type == 1:
			makeHouse()
		
		#if clearHistoryCount > 30:
		cmds.select(objName)
		cmds.delete(ch=True)
			
		print str(currentFace) + " of " + str(numOfFaces) + " done"
		currentFace += 1
		clearHistoryCount += 1
	
	cmds.select('regBuildingCap*')
	cmds.group(n='regBuildingCapGroup')
	cmds.select('autoCity', 'regBuildingCapGroup')
	cmds.group(n='autoCityObjects')

#generates rectangular building
def makeRegular(h):
	cmds.polyExtrudeFacet(scale=(0.834, 0, 0.834), kft=True)
	heightVariance = random.random() * 4 - 2
	cmds.polyExtrudeFacet(translate=(0, h + heightVariance, 0),kft=True)
	
	maketop = random.randint(0,4)
	
	if maketop == 0:
		makeBox(h/2)
	
#generates park with surrounding walls		
def makePark():
	cmds.polyExtrudeFacet(scale=(0.834, 0, 0.834), kft=True)
	cmds.polyExtrudeFacet(translate=(0, 0.2, 0), kft=True)
	cmds.polyExtrudeFacet(scale=(0.95, 0, 0.95), kft=True)
	cmds.polyExtrudeFacet(translate=(0,-0.2,0), kft=True)

#generates a pointy building
def makePointy(h):
	h+=3
	cmds.polyExtrudeFacet(scale=(0.834, 0, 0.834), kft=True)
	heightVariance = random.random() * 4 - 2
	cmds.polyExtrudeFacet(translate=(0, h + heightVariance, 0),kft=True)
	
	#roof
	if random.randint(0,1) == 0:
		cmds.polyExtrudeFacet(translate=(0, 2,0), scale=(0.12, 1, 0.06))
	else:
		cmds.polyExtrudeFacet(translate=(0, 2,0), scale=(0.06, 1, 0.12))

#generates a rectangular building
def makeRectBuilding(h):
	if random.randint(0,1) == 0:
		sx = 0.834
		sz = 0.5
	else:
		sx = 0.5
		sz = 0.834
		
	cmds.polyExtrudeFacet(scale=(sx, 0, sz), kft=True)
	cmds.polyExtrudeFacet(translate=(0, random.random()+1, 0), kft=True)
	
	for i in range(0, h):
		cmds.polyExtrudeFacet(scale=(0.8, 0, 0.8), kft=True)
		cmds.polyExtrudeFacet(translate=(0,0.2,0), kft=True)
		cmds.polyExtrudeFacet(scale=(1.2, 0, 1.2), kft=True)
		cmds.polyExtrudeFacet(translate=(0, 0.4, 0), kft=True)
	
	cmds.polyExtrudeFacet(scale=(0.8, 0, 0.8), kft=True)
	cmds.polyExtrudeFacet(translate=(0, 0.5, 0), kft=True)

#generates cool twisting building for every floor	
def makeTwistingBuilding(h):
	cmds.polyExtrudeFacet(scale=(0.8, 0, 0.8), kft=True)
	cmds.polyExtrudeFacet(translate=(0, random.random()+1, 0), kft=True)
	
	twistDir = random.randint(0,1)
	
	for i in range(0, h*4):
		cmds.polyExtrudeFacet(translate=(0, 0.3, 0), kft=True)
		if twistDir == 0:
			cmds.polyExtrudeFacet(translate=(0,0.2, 0), rotate=(0,10,0), kft=True)
		else:
			cmds.polyExtrudeFacet(translate=(0,0.2, 0), rotate=(0,-10,0), kft=True)
		#cmds.rotate(0, 10, 0)
	
	cmds.polyExtrudeFacet(translate=(0, 0.4, 0), kft=True)

#generates a suburban house structure	
def makeHouse():
	cmds.polyExtrudeFacet(scale=(0.5, 0, 0.5), kft=True)
	cmds.polyExtrudeFacet(translate=(0,0.25,0), kft=True)
	cmds.polyExtrudeFacet(scale=(1.2, 0, 1.2), kft=True)
	cmds.polyExtrudeFacet(translate=(0,0.25,0), scaleX=(0.1), kft=True)
	#cmds.xform(t=(0,0.2,0))

#generates extra box caps on certain regular buldings
def makeBox(h):
	vertPos = cmds.xform(q=True, t=True, ws=True)
	xmid = (vertPos[0] + vertPos[3])/2
	size = abs(vertPos[0] - vertPos[3]) * 0.7
	zmid = (vertPos[2] + vertPos[8])/2
	newBuilding = cmds.polyCube(w=size, h=h, d=size, name='regBuildingCap')
	cmds.xform(t=(xmid, vertPos[1]+h/2, zmid))
	
