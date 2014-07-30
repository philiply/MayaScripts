import maya.cmds as cmds

def cubefractal(length, depth, x, y, z):
	if (depth == 0):
		cmds.polyCube(w=length, h=length, d=length)
		cmds.xform(t=(x, y, z))
	else:
		length2 = length/3
		x1 = y1 = z1 = length2/1
		cubefractal(length2, depth-1, x,y,z)
		cubefractal(length2, depth-1, x+x1,y+y1,z+z1)
		cubefractal(length2, depth-1, x-x1,y+y1,z+z1)
		cubefractal(length2, depth-1, x+x1,y+y1,z-z1)
		cubefractal(length2, depth-1, x+x1,y-y1,z+z1)
		cubefractal(length2, depth-1, x-x1,y-y1,z+z1)
		cubefractal(length2, depth-1, x-x1,y+y1,z-z1)
		cubefractal(length2, depth-1, x+x1,y-y1,z-z1)
		cubefractal(length2, depth-1, x-x1,y-y1,z-z1)

cubefractal(4.0, 4, 0, 0, 0)
cmds.select(all=True)
cmds.group(n='cubefractal')