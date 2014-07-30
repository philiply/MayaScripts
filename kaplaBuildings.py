#make kapla buildings

import maya.cmds as cmds
import math

def makeKaplaBlock(orientation):
	if orientation==0:
		cmds.polyCube(n="kapla", w=1, h=3, d=15)
	else:
		cmds.polyCube(n="kapla", w=15, h=3, d=1)

def makeKaplaGrid(height):
	for h in range (0,height):
		for i in range (-2,3):
			orientation = h %2
			if orientation == 0:
				makeKaplaBlock(orientation)
				cmds.move(i*3.5, h*3, 0)
			else:
				makeKaplaBlock(orientation)
				cmds.move(0, h*3, i*3.5)
		
def makeKaplaBlockBuilding(sideLength):
	depthNum = int(sideLength/15)
	levels = int(sideLength/3)
	widthNum = int(sideLength/5)
	
	makeKaplaBlock()
	cmds.move(j*5, i*3, k*15)
	cmds.group([node for node in cmds.ls() if "kapla" in node and "Shape" not in node], n="kaplaBlocks")


def fillShapeKapla(lenX, lenY, lenZ):
	numBlocksHeight = int(lenY/3)
	print "numBlocksHeight:",numBlocksHeight
	for h in range(0,numBlocksHeight):
		#print "h:", h
		orientation = h%2
		if orientation == 0:
			gappedSideNumBlocks = int(lenX/3.5)
			if gappedSideNumBlocks < 1:
				gappedSideNumBlocks = 1
			gap = lenX/3.5
			longSideNumBlocks = int(lenZ/15)
			if longSideNumBlocks < 1:
				longSideNumBlocks = 1
			longGap = lenZ/15
			#print "orient0:", gappedSideNumBlocks, gap, longSideNumBlocks, longGap
			for i in range(0, gappedSideNumBlocks):
				for j in range(0, longSideNumBlocks):
					makeKaplaBlock(orientation)
					cmds.move(i*gap, h*3, j*15)
		else:
			gappedSideNumBlocks = int(lenZ/3.5)
			gap = lenZ/3.5
			longSideNumBlocks = int(lenX/15)
			longGap = lenX/15
			#print "orient1:", gappedSideNumBlocks, gap, longSideNumBlocks, longGap
			for i in range(0, longSideNumBlocks):
				for j in range(0, gappedSideNumBlocks):
					makeKaplaBlock(orientation)
					cmds.move(i*15, h*3, j*gap)

def selectKapla():
	cmds.select([node for node in cmds.ls() if 'kapla' in node and 'Shape' not in node])
					
def buildKapla(shortSideBlocks, height, longSideBlocks, shortBlockGap = 3.625, longBlockGap = 15):
	numBlocksHeight = int(height/3)
	for h in range(0,numBlocksHeight):
		orientation = h%2
		if orientation == 0:
			for i in range(0, shortSideBlocks):
				for j in range(0, longSideBlocks):
					makeKaplaBlock(orientation)
					cmds.move(i*shortBlockGap-7, 3*h, j*longBlockGap)
		else:
			for i in range(0, longSideBlocks):
				for j in range(0, shortSideBlocks):
					makeKaplaBlock(orientation)
					cmds.move(i*longBlockGap, 3*h, j*shortBlockGap-7)
	selectKapla()
	cmds.group(n="buildingGroup")

def cleanKapla():
	selectKapla()
	cmds.delete()
	cmds.delete('buildingGroup')