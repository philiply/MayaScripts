import maya.cmds as cmds
depth = 1
cmds.polyCone(n='pyramid1_1', sx=4, r=2)
cmds.rotate(0, '45deg', 0, pivot=(0, 1,0))
cmds.scale(0.5, 0.5, 0.5, r=True)
#pcount+=4
while depth < 7:
	cmds.duplicate('pyramid'+str(depth)+'_1')
	cmds.duplicate('pyramid'+str(depth)+'_1')
	cmds.duplicate('pyramid'+str(depth)+'_1')
	cmds.duplicate('pyramid'+str(depth)+'_1')
	cmds.move(0, 0.25, 0, 'pyramid'+str(depth)+'_1')
	cmds.move(-0.705, -0.75, -0.705,'pyramid'+str(depth)+'_2')
	cmds.move(0.705, -0.75, -0.705, 'pyramid'+str(depth)+'_3')
	cmds.move(0.705, -0.75, 0.705, 'pyramid'+str(depth)+'_4')
	cmds.move(-0.705, -0.75, 0.705, 'pyramid'+str(depth)+'_5')
	cmds.group('pyramid'+str(depth)+'_1', 'pyramid'+str(depth)+'_2', 'pyramid'+str(depth)+'_3', 'pyramid'+str(depth)+'_4', 'pyramid'+str(depth)+'_5', n = 'pyramid'+str(depth+1)+'_1')
	cmds.scale(0.5, 0.5, 0.5, r=True)
	depth+=1

def make(depth):
	i = 1
	cmds.polyCone(n='pyramid1_1', sx=4, r=2)
	cmds.rotate(0, '45deg', 0, pivot=(0, 1,0))
	cmds.scale(0.5, 0.5, 0.5, r=True)
	
	while i < depth:
		cmds.duplicate('pyramid'+str(i)+'_1')
		cmds.duplicate('pyramid'+str(i)+'_1')
		cmds.duplicate('pyramid'+str(i)+'_1')
		cmds.duplicate('pyramid'+str(i)+'_1')
		cmds.move(0, 0.25, 0, 'pyramid'+str(i)+'_1')
		cmds.move(-0.705, -0.75, -0.705,'pyramid'+str(i)+'_2')
		cmds.move(0.705, -0.75, -0.705, 'pyramid'+str(i)+'_3')
		cmds.move(0.705, -0.75, 0.705, 'pyramid'+str(i)+'_4')
		cmds.move(-0.705, -0.75, 0.705, 'pyramid'+str(i)+'_5')
		cmds.group('pyramid'+str(i)+'_1', 'pyramid'+str(i)+'_2', 'pyramid'+str(i)+'_3', 'pyramid'+str(i)+'_4', 'pyramid'+str(i)+'_5', n = 'pyramid'+str(i+1)+'_1')
		cmds.scale(0.5, 0.5, 0.5, r=True)
		i+=1