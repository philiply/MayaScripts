import maya.cmds as cmds
import random

#HONEYCOMB script

def honeycomb(xbound, zbound, flat, buildCity):
	dx = 0
	indentOn = False #start 0.867 ahead
	cellnum = 0
	while (dx < xbound):
		dz = 0
		if(indentOn):
			dz = 0.867
		while (dz < zbound):
			cellname = "cell" + "%04d"%cellnum
			randomheight = 0
			raiseMe = False
			if not flat:
				randomheight = .1 - (0.2 * random.random())
			if buildCity:
				if xbound/2 - xbound/10 < dx and dx < xbound/2 + xbound/10 and zbound/2 - zbound/10 < dz and dz < zbound/2 + zbound/10:
					raiseMe = True
					randombuildingheight = 20 - (10 * random.random())
				
			cmds.polyCylinder(name = cellname, ax=[0,1,0], radius=1, height=1, sx=6, sy=1, sz=0)
			if raiseMe:
				cmds.move(0, randombuildingheight, 0, cellname+'.f[7]', r=True)
			else:
				cmds.move(0, randomheight, 0, cellname+'.f[7]', r=True)
			cmds.polyExtrudeFacet(cellname+'.f[7]', kft=False, s=(0.896415,0.896415,0.896415), divisions = 3)
			cmds.polyExtrudeFacet(cellname+'.f[7]', kft=False, ty=-0.15636, divisions=3)
			cmds.select(cellname)
			cmds.polyBevel(offset = 0.7, offsetAsFraction = 1, autoFit = 1, segments = 1, worldSpace = 1, uvAssignment = 0, fillNgons = 1, mergeVertices = 1, mergeVertexTolerance = 0.0001,  miteringAngle = 180, angleTolerance = 180, ch = 1)

			cmds.move(dx, 0, dz)
			
			print "cylinder " + cellname + " location = dx: " + str(dx) + ", dz: " + str(dz)
			
			dz+=1.729
			cellnum += 1
		dx += 1.5
		indentOn = not indentOn
		
	cmds.select([node for node in cmds.ls() if 'cell' in node and 'Shape' not in node])
	cmds.group(name='honeycomb')
	cmds.move(-xbound/2, 0, -zbound/2, 'honeycomb')
	
def fallingAnim(endTime, minHeight, maxHeight):
	cmds.select([node for node in cmds.ls() if 'cell' in node and 'Shape' not in node])
	cells = cmds.ls(sl=True)
	
	for c in cells:
		startFrame = random.randint(0, endTime)
		while startFrame == endTime:
			startFrame = random.randint(0,endTime)
		dropHeight = random.randint(minHeight, maxHeight)
		cmds.setKeyframe(c, at='translateY', v=dropHeight, t=startFrame)
		cmds.setKeyframe(c, at='translateY', v=0, t=endTime)