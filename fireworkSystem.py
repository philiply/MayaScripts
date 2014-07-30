###################
### Fireworks System
### By Philip Ly
### Given the number of fireworks and the duration,
### this function can create a fireworks show
### can also shoot fireworks given a specified path.
### To Run: Open Maya Script Editor, Copy and paste, and run!
### Call fwUI()
####################

#create gravity for particles to fall down

#import modules here
import maya.cmds as cmds
import random
import maya.mel as mel
from functools import partial

######
#Each type of firework will require __init__(), makeMe(), shadeMe(), and keyMe() procedures
######


############
### FIREWORK TYPE 1
### launch up with trail, circular explosion
############

class firework:
	def __init__(self,xbound, zbound):
		#self.type = type
		self.height = 150*random.random() + 420
		self.time1 = 72 #72 frames = 3 seconds
		self.rate1 = 100
		self.rate2 = 3000 #+ random.randint(0,6000)
		self.initSpeed = 0.2
		self.exSpeed = 45.0
		self.x = xbound*random.random() - xbound/2
		self.z = zbound*random.random() - zbound/2
		self.speedRand = 0.4
		self.minDist = 0.2
		self.life = 2.2
		self.lifeRand = 0.4
		self.anglex = random.random() * 30 - 15
		self.anglez = random.random() * 30 - 15
		
	def makeMe(self, e, p):
		#create emitters for firework effect and set certain attributes that don't need to be keyed
		cmds.emitter(n=e)
		cmds.particle(n=p)
		cmds.connectDynamic(p, em=e)
		cmds.setAttr(p+'Shape.lifespanMode', 2)
		cmds.setAttr(p+'Shape.lifespan', self.life)
		cmds.setAttr(p+'Shape.lifespanRandom', self.lifeRand)
		cmds.setAttr(p+'Shape.particleRenderType', 4)
		cmds.setAttr(e+'.minDistance', self.minDist)
		cmds.setAttr(e+'.speedRandom', self.speedRand)
	
	def shadeMe(self, fireworkName, particleName):
		newshader = cmds.shadingNode('lambert', asShader=True, n=fireworkName+'Shader')
		cmds.sets(r=True, nss=True, em=True, n=newshader+'SG')
		cmds.connectAttr(newshader+'.outColor', newshader+'SG.surfaceShader', force=True)
		cmds.select(particleName)
		mel.eval('hyperShade -assign ' + newshader)
		redval = random.random()
		greenval = random.random()
		blueval = random.random()
		cmds.setAttr(newshader+'.color', redval, greenval, blueval, type='double3')
		cmds.setAttr(newshader+'.incandescence', redval, greenval, blueval, type='double3')
		#cmds.setAttr(newshader+'.glowIntensity', 0.2)
	
	def keyMe(self, emitterName, prtcl, time):
	
		cmds.setAttr(prtcl+'Shape.startFrame', time)
		#key rate
		cmds.setKeyframe(emitterName, at="rate", v=self.rate1, t=time+self.time1-1)
		cmds.setKeyframe(emitterName, at="rate", v=0, t=time+self.time1)
		cmds.setKeyframe(emitterName, at="rate", v=self.rate2, t=time+self.time1+1)
		cmds.setKeyframe(emitterName, at="rate", v=0, t=time+self.time1+12)
		
		#key translate y
		cmds.setKeyframe(emitterName, at="translateY", v=0, t=time)
		cmds.setKeyframe(emitterName, at="translateY", v=self.height, t=time+self.time1)
		
		#key emitting speed
		cmds.setKeyframe(emitterName, at="speed", v=self.initSpeed, t=time+self.time1)
		cmds.setKeyframe(emitterName, at="speed", v=self.exSpeed, t=time+self.time1+1)


############
### FIREWORK TYPE 2
### -launch up with trail, circular explosion, two types of particles (spheres, streaks)
### -since two particles objects, particlename+'a' and particlename+'b' will differentiate
############

# two emitters and particles, A and B. A is initial launch with spheres. explodes spheres too. B is streaks. B is connected to light gravity field.

class firework2:
	def __init__(self, xbound, zbound):
		#self.type = type
		self.height = 150*random.random() + 420
		self.time1 = 60 #72 frames = 3 seconds
		self.rate1 = 100
		self.rate2 = 2500 #+ random.randint(0,6000)
		self.initSpeed = 0.2
		self.exSpeedA = 45.0
		self.exSpeedB = 50.0
		self.x = xbound*random.random() - xbound/2
		self.z = zbound*random.random() - zbound/2
		self.speedRand = 0.4
		self.minDist = 0.2
		self.lifeA = 3.0
		self.lifeB = 3.8
		self.lifeRand = 0.4
		self.anglex = random.random() * 30 - 15
		self.anglez = random.random() * 30 - 15
	
	def makeMe(self, e, p):
		#create emitters for firework effect and set certain attributes that don't need to be keyed
		ea = e + "_A"
		eb = e + "_B"
		pa = p + "_A"
		pb = p + "_B"
		cmds.emitter(n=ea)
		cmds.particle(n=pa)
		cmds.connectDynamic(pa, em=ea)
		cmds.setAttr(pa+'Shape.lifespanMode', 2)
		cmds.setAttr(pa+'Shape.lifespan', self.lifeA)
		cmds.setAttr(pa+'Shape.lifespanRandom', self.lifeRand)
		cmds.setAttr(pa+'Shape.particleRenderType', 4)
		cmds.setAttr(ea+'.minDistance', self.minDist)
		cmds.setAttr(ea+'.speedRandom', self.speedRand)
		
		cmds.select(cl=True)
		
		cmds.emitter(n=eb)
		cmds.particle(n=pb)
		cmds.connectDynamic(pb, em=eb)
		cmds.setAttr(pb+'Shape.lifespanMode', 2)
		cmds.setAttr(pb+'Shape.lifespan', self.lifeB)
		cmds.setAttr(pb+'Shape.lifespanRandom', self.lifeRand)
		cmds.setAttr(pb+'Shape.particleRenderType', 6)
		cmds.setAttr(eb+'.minDistance', self.minDist)
		cmds.setAttr(eb+'.speedRandom', self.speedRand)
		cmds.setAttr(eb+'.speed', self.exSpeedB)
		mel.eval("AEparticleAddDynamicRenderAttr " + pb + "Shape")
		cmds.setAttr(pb+'.tailFade', -0.166)
		cmds.setAttr(pb+'.tailSize', 30.0)
		
		"""
		cmds.addAttr(pb+"Shape", internalSet=True, ln="colorAccum", at="boolean", dv=False)
		cmds.addAttr(pb+"Shape", internalSet=True, ln="useLighting", at="boolean", dv=False)
		cmds.addAttr(pb+"Shape", internalSet=True, ln="linewidth", at="long", min=1, max=20, dv=3)
		cmds.addAttr(pb+"Shape", internalSet=True, ln="tailFade", at="long", min=-1, max=1, dv=-0.166)
		cmds.addAttr(pb+"Shape", internalSet=True, ln="tailSize", at="long", min=-100, max=100, dv=30.0)
		cmds.addAttr(pb+"Shape", internalSet=True, ln="normalDir", at="long", min=1, max=3, dv=2)
		"""
		
		#TODO:
		#If firework2 gravity field exists, connect particles to it!
		cmds.group(ea,eb, n=e)
		cmds.group(pa,pb, n=p)
	
	
	def shadeMe(self, fireworkName, particleName):
		newshader = cmds.shadingNode('lambert', asShader=True, n=fireworkName+'AShader')
		cmds.sets(r=True, nss=True, em=True, n=newshader+'SG')
		cmds.connectAttr(newshader+'.outColor', newshader+'SG.surfaceShader', force=True)
		cmds.select(particleName+'_A')
		mel.eval('hyperShade -assign ' + newshader)
		redval = random.random()
		greenval = random.random()
		blueval = random.random()
		cmds.setAttr(newshader+'.color', redval, greenval, blueval, type='double3')
		cmds.setAttr(newshader+'.glowIntensity', 0.2)
		
		newshader = cmds.shadingNode('lambert', asShader=True, n=fireworkName+'BShader')
		cmds.sets(r=True, nss=True, em=True, n=newshader+'SG')
		cmds.connectAttr(newshader+'.outColor', newshader+'SG.surfaceShader', force=True)
		cmds.select(particleName+'_B')
		mel.eval('hyperShade -assign ' + newshader)
		redval = random.random()
		greenval = random.random()
		blueval = random.random()
		cmds.setAttr(newshader+'.color', redval, greenval, blueval, type='double3')
		cmds.setAttr(newshader+'.glowIntensity', 0.3)

	
	def keyMe(self, emitterName, prtcl, time):
		pNameA = prtcl + "_A"
		pNameB = prtcl + "_B"
	
		cmds.setAttr(pNameA+'Shape.startFrame', time)
		cmds.setAttr(pNameB+'Shape.startFrame', time)
	
		emitterNameA = emitterName + "_A"
		emitterNameB = emitterName + "_B"
		#key rate
		cmds.setKeyframe(emitterNameA, at="rate", v=self.rate1, t=time+self.time1-1)
		cmds.setKeyframe(emitterNameA, at="rate", v=0, t=time+self.time1)
		cmds.setKeyframe(emitterNameA, at="rate", v=self.rate2, t=time+self.time1+1)
		cmds.setKeyframe(emitterNameA, at="rate", v=0, t=time+self.time1+12)
		cmds.setKeyframe(emitterNameB, at="rate", v=0, t=time + self.time1)
		cmds.setKeyframe(emitterNameB, at="rate", v=self.rate2, t=time+self.time1+1)
		cmds.setKeyframe(emitterNameB, at="rate", v=0, t=time+self.time1+12)
		
		#key translate y
		cmds.setKeyframe(emitterNameA, at="translateY", v=0, t=time)
		cmds.setKeyframe(emitterNameA, at="translateY", v=self.height, t=time+self.time1)
		cmds.setKeyframe(emitterNameB, at="translateY", v=0, t=time)
		cmds.setKeyframe(emitterNameB, at="translateY", v=self.height, t=time+self.time1)
		
		#key emitting speed
		cmds.setKeyframe(emitterNameA, at="speed", v=self.initSpeed, t=time+self.time1)
		cmds.setKeyframe(emitterNameA, at="speed", v=self.exSpeedA, t=time+self.time1+1)
	

############
# add to fireworkDict when creating a new firework
# figure out how to randomly choose different fireworks.
############

#fireworkDict = {1:firework(), 2:firework2()}

############
# showtime()
# Creates fireworks
# for loop, counting down how much time we have left to launch fireworks
# if countdown of fireworks isn't done yet, reset time
# xb and zb are the x and z Bounds that fireworks can be made in.
############

def showtime(numfireworks, duration, xb, zb):
	############
	# add to fireworkDict when creating a new firework
	# figure out how to randomly choose different fireworks.
	############

	#fireworkDict = {1:firework(xb, zb), 2:firework2(xb,zb)}
	fireworkDict = {1:firework, 2:firework2}
	
	t1 = 0
	
	#Progress window stuff
	total = numfireworks
	initializeProgressWindow('Firworks', total)
	
	#TODO:
	#make gravity for firework2 things to work with.
	
	#for t1 in range(0,duration):
	while t1 < duration:
		ifCreate = random.randint(0,1)
		if ifCreate == 1 and numfireworks > 0:
			#whichFirework = random.randint(1,2)
			whichFirework = 1
			#newFirework = firework(xb, zb)
			newFirework = fireworkDict[whichFirework](xb,zb)
			numfireworks -= 1
			
			fname = "firework"+"%03d"%numfireworks
			emname = fname+"EM"
			pname = fname+"P"
			
			#create emitters for firework effect and set certain attributes that don't need to be keyed
			
			newFirework.makeMe(emname, pname)
			cmds.xform(emname, t=(newFirework.x, 0, newFirework.z), ro=(newFirework.anglex, 0, newFirework.anglez))
			#cmds.setAttr(pname+'Shape.startFrame', t1)
			
			#connect particle to new shader
			newFirework.shadeMe(fname, pname)
			newFirework.keyMe(emname, pname, t1)
			
			#group emitter and particle together in firework###
			cmds.group(emname, pname, n=fname)
			
			#deselect particle so that next iteration's emitters aren't created in each particle
			cmds.select(cl=True)
			
		if numfireworks > 0 and t1 == duration - 1:
			t1 = 0
		
		if numfireworks < 0:
			break
		
		t1 += 1
		updateProgressWindow(total-numfireworks, total)
		
	#selects all fireworks and groups them together
	cmds.select([node for node in cmds.ls() if 'firework' in node and 'EM' not in node and 'P' not in node and 'Shape' not in node])
	cmds.group(name='fireworkShow')
	killProgressWindow()

############
# If curve is selected, can create fireworks along curve with given number of fireworks and a given time
# Traverse curve within duration, unless duration is less than 0, then loops
# Fire fireworks within radius of a point along curve
# Variation variable for how much displacement you want it to possibly be from the curve
# If loop variable is 1, when while reaches end but still have ammo, time also resets to 0
############
def showtimeOnCurve(numFireworks, duration, variation, loop):
	
	selectedCurve = cmds.ls(sl=True)[0]
	
	#if (cmds.objectType(cmds.ls(sl=True)[0], isType = 'nurbsCurve') != 1):
	#	cmds.error('You didn\'t select a curve yo!')
	
	#Checks for correct naming format for script to work
	if cmds.objExists(selectedCurve+'Shape'):
		curveLen = cmds.getAttr(selectedCurve+'Shape.max')
	else:
		cmds.error('Please select/rename your curve cuz')
	
	d = curveLen / duration
	locOnCurve = 0
	t1 = 0
	print "curveLen: " + str(curveLen)
	
	total = numFireworks
	initializeProgressWindow('Firworks Along Cuve', total)
	
	while locOnCurve < curveLen:
		print "locOnCurve: " + str(locOnCurve)
		ifCreate = random.randint(0,1)
		if ifCreate == 1 and numFireworks > 0: #you can now create a firework
			loc = cmds.pointOnCurve(pr=locOnCurve, p=True)
			print "loc: " + str(loc)
			cmds.select(cl=True)
			
			newFirework = firework(0, 0)
			numFireworks -= 1
			
			fname = "firework"+"%03d"%numFireworks
			emname = fname+"EM"
			pname = fname+"P"
			
			#create emitters for firework effect and set certain attributes that don't need to be keyed
			newFirework.makeMe(emname, pname)
			cmds.xform(emname, t=(loc[0] + random.random()*variation - variation/2, loc[1] + random.random()*variation - variation/2, loc[2] + random.random()*variation - variation/2), ro=(newFirework.anglex, 0, newFirework.anglez))
			cmds.setAttr(pname+'Shape.startFrame', t1)

			#Shade and Key newly created firework.
			newFirework.shadeMe(fname, pname)
			newFirework.keyMe(emname, pname, t1)
			
			#group emitter and particle together in firework###
			cmds.group(emname, pname, n=fname)
			
			#deselect particle so that next iteration's emitters aren't created in each particle
			cmds.select(cl=True)
			
		locOnCurve += d
		
		if numFireworks > 0 and  locOnCurve >= curveLen:
			if loop == True:
				t1 = 0
			locOnCurve = 0
		if numFireworks < 0:
			break
		
		t1 +=1
		
		updateProgressWindow(total-numFireworks, total)
		cmds.select(selectedCurve)
		
	#selects all fireworks and groups them together
	cmds.select([node for node in cmds.ls() if 'firework' in node and 'EM' not in node and 'P' not in node and 'Shape' not in node])
	cmds.group(name='fireworkShow')
	
	#kills progress window
	killProgressWindow()

#cleans up all fireworks
def cleanup():
	try:
		cmds.delete("firework*")
	except ValueError:
		print "No firework objects"

################	
#UI Elements
################
def initializeProgressWindow(t, maxSize):
	cmds.progressWindow(title=t, progress=0, max=maxSize, isInterruptable=True)
	#pass

def updateProgressWindow(i, maxSize):
	if(cmds.progressWindow(q=True, ic=True)):
		return False
	else:
		cmds.progressWindow(e=True, pr=i, st=("Firing: " + str(i) + "/" + str(maxSize)))
		return True

def killProgressWindow():
	cmds.progressWindow(ep=True)
	print "Build Completed"

#Class that holds all UI building information
class fireworksUI():
	def __init__(self, winName="fireworksUI"):
		self.winTitle = "fireworks script"
		self.winName = winName

	#the function that the showtim button runs to create fireworks in a specified bounded region
	def showtimeButton(self, unusedArg):
		num = int(self.getNewTextValue(self.numFireworksArg))
		dur = int(self.getNewTextValue(self.duration))
		xb = int(self.getNewTextValue(self.xboundField))
		zb = int(self.getNewTextValue(self.zboundField))
		print "num: " + str(num)
		print "dur: " + str(dur)
		print "xb: " + str(xb)
		print "zb: " + str(zb)
		showtime(num, dur, xb, zb)
	
	#the function that the showtime button runs for creating fireworks on a curve
	def showtimeCButton(self, unusedArg):
		num = int(self.getNewTextValue(self.numFireworksArg))
		dur = int(self.getNewTextValue(self.duration))
		cv = float(cmds.textField(self.curveVars, q=True, text=True))
		loopB = cmds.checkBox(self.loopBool, q=True, v=True)
		showtimeOnCurve(num, dur, cv, loopB)
	
	#runs cleanup() function to delete all fireworks related objects in scene
	def cleanupButton(*args):
		cleanup()
	
	def getNewTextValue(self, txtf):
		return cmds.textField(txtf, q=True, text=True)
		
	#create() generates the UI and the look
	def create(self):
		if cmds.window(self.winName, exists=True):
			cmds.deleteUI(self.winName)
			
		cmds.window(self.winName, title=self.winTitle)
		
		#edit here to fix window size and layout
		self.layout = cmds.rowColumnLayout( numberOfColumns=2, columnAttach=(1, 'left', 0), columnWidth=[(1, 175), (2, 100)] )
		
		#start adding items to UI here
		cmds.text(label = 'Number of Fireworks: ')
		self.numFireworksArg = cmds.textField(text='50', ed=True)
		cmds.text(label = 'Show Duration: ')
		self.duration = cmds.textField(text = '120', ed=True)
		cmds.text(label = 'xBound (not for curve)')
		self.xboundField = cmds.textField(text = '300', ed=True)
		cmds.text(label = 'zBound (not for curve)')
		self.zboundField = cmds.textField(text = '300', ed=True)
		
		cmds.text(label='') #blank space
		
		self.makeFrwks=cmds.button(label='MakeFireworks!', c=partial(self.showtimeButton))
		
		cmds.text(label='Curve Variance (Req: Curve)')
		self.curveVars = cmds.textField(text = '0')
		self.loopBool = cmds.checkBox(label='loop fireworks? (Req: Curve)') 
		cmds.text(label='')
		cmds.text(label='Requires selected curve:')
		self.makeFrwksOnCurve = cmds.button(label='Make Fireworks On Curve', width=150, c=partial(self.showtimeCButton))
		cmds.text(label='')
		cmds.text(label='')
		cmds.button(label="Clean Up Fireworks", c=partial(self.cleanupButton))
		cmds.showWindow(self.winName)
		cmds.window(self.winName, edit=True, widthHeight=[340,200])

#Function to start UI
def fwUI():
	fUI = fireworksUI()
	fUI.create()