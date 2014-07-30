import maya.cmds as cmds
import random

######################
# Dancing Boxes Script
# by Philip Ly
# -put in BPM of music, length of song, 
# and number of boxes you want dancing
######################

# alternate between stationary and translate each beat
# pulse each beat
# song len must be in seconds

def convertToSeconds(minutes, seconds):
	print minutes*60 + seconds

def boxParty(bpm, songLen, numBoxes):
	cmds.camera()
	cmds.rename('partyCam')
	
	bps = bpm/60.0
	fpb = 24/bps
	cmds.polyCube(name='boxMain', w=1,h=1,d=1)
	
	for i in range(0,numBoxes):
		cmds.select('boxMain')
		cmds.instance(name= 'box' + str(i))
		randX = random.random()*10 - 5
		randY = random.random()*10 - 5
		randZ = random.random()*10 - 5
		cmds.xform(t=(randX,randY,randZ))
	
	cmds.hide('boxMain')
	cmds.select([node for node in cmds.ls() if 'box' in node and 'Shape' not in node])
	cmds.group(name='dancingBoxes')
	cmds.select('dancingBoxes')
	cmds.viewFit('partyCamShape')
	
	#for each beat
	framesKeyed = 0
	elevAngle = 0
	#moveToggle = True
	
	beat = 1
	while framesKeyed/24 < songLen:
		cmds.currentTime(framesKeyed-fpb+4) # set time to get latest position
		for i in range(0,numBoxes):
		#pulsing
			cmds.select('box'+str(i))
			cmds.setKeyframe(at='scaleX', value=1, t=framesKeyed-2)
			cmds.setKeyframe(at='scaleX', value=1.7, t=framesKeyed)
			cmds.setKeyframe(at='scaleX', value=1, t=framesKeyed+2)
			
			cmds.setKeyframe(at='scaleY', value=1, t=framesKeyed-2)
			cmds.setKeyframe(at='scaleY', value=1.7, t=framesKeyed)
			cmds.setKeyframe(at='scaleY', value=1, t=framesKeyed+2)
			
			cmds.setKeyframe(at='scaleZ', value=1, t=framesKeyed-2)
			cmds.setKeyframe(at='scaleZ', value=1.7, t=framesKeyed)
			cmds.setKeyframe(at='scaleZ', value=1, t=framesKeyed+2)
	
		#translating
			if beat == 1 or beat == 3:
				cmds.select('box' + str(i))
				pos = cmds.xform(ws=True, q=True, t=True)
				direction = random.randint(0,2)
				
				displacement = random.randint(0,10) - 5
				
				#try to keep within borders
				while pos[direction] + displacement > 6 or pos[direction] + displacement < -6:
					displacement = random.randint(0,10) - 5
					direction = random.randint(0,2)
				
				if direction == 0: #going in x direction
					cmds.setKeyframe(at='translateX', value = pos[0], t = framesKeyed)
					cmds.setKeyframe(at='translateX', value = pos[0] + displacement, t = framesKeyed+4)
					cmds.setKeyframe(at='translateY', value = pos[1], t=framesKeyed)
					cmds.setKeyframe(at='translateY', value = pos[1], t=framesKeyed+4)
					cmds.setKeyframe(at='translateZ', value = pos[2], t=framesKeyed)
					cmds.setKeyframe(at='translateZ', value = pos[2], t=framesKeyed+4)
				elif direction == 1: #going in y direction
					cmds.setKeyframe(at='translateY', value = pos[1], t = framesKeyed)
					cmds.setKeyframe(at='translateY', value = pos[1] + displacement, t = framesKeyed+4)
					cmds.setKeyframe(at='translateX', value = pos[0], t=framesKeyed)
					cmds.setKeyframe(at='translateX', value = pos[0], t=framesKeyed+4)
					cmds.setKeyframe(at='translateZ', value = pos[2], t=framesKeyed)
					cmds.setKeyframe(at='translateZ', value = pos[2], t=framesKeyed+4)
				else: #going in z direction
					cmds.setKeyframe(at='translateZ', value = pos[2], t = framesKeyed)
					cmds.setKeyframe(at='translateZ', value = pos[2] + displacement, t = framesKeyed+4)
					cmds.setKeyframe(at='translateX', value = pos[0], t=framesKeyed)
					cmds.setKeyframe(at='translateX', value = pos[0], t=framesKeyed+4)
					cmds.setKeyframe(at='translateY', value = pos[1], t=framesKeyed)
					cmds.setKeyframe(at='translateY', value = pos[1], t=framesKeyed+4)
			
		#key partyCam every 4 beats
		if beat == 1:
			cmds.setKeyframe('partyCam', at='translateX', t = framesKeyed)
			cmds.setKeyframe('partyCam', at='translateY', t = framesKeyed)
			cmds.setKeyframe('partyCam', at='translateZ', t = framesKeyed)
			cmds.setKeyframe('partyCam', at='rotateX', t = framesKeyed)
			cmds.setKeyframe('partyCam', at='rotateY', t = framesKeyed)
			cmds.setKeyframe('partyCam', at='rotateZ', t = framesKeyed)

			elevAngleChange = random.random()*70 - 35
			aAngleChange = random.random()* 360 - 180
			if elevAngle + elevAngleChange > 70 or elevAngle + elevAngleChange < -20:
				elevAngle = elevAngle - elevAngle
			else:
				elevAngle = elevAngle + elevAngleChange
			
			cmds.tumble('partyCamShape', ea=elevAngle, aa=aAngleChange)
			cmds.setKeyframe('partyCam', at='translateX', t = framesKeyed+4)
			cmds.setKeyframe('partyCam', at='translateY', t = framesKeyed+4)
			cmds.setKeyframe('partyCam', at='translateZ', t = framesKeyed+4)
			cmds.setKeyframe('partyCam', at='rotateX', t = framesKeyed+4)
			cmds.setKeyframe('partyCam', at='rotateY', t = framesKeyed+4)
			cmds.setKeyframe('partyCam', at='rotateZ', t = framesKeyed+4)
		
		if beat == 4:
			beat = 1
		else: 
			beat += 1
		framesKeyed += fpb

