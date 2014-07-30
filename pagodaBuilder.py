#pagoda builder!

import maya.cmds as cmds

def pagoda(numStory):
	for i in range(0,numStory):
		#build a level of the pagoda
		cmds.polyCube(name='pagoda_story' + str(i), d=5, h=3, w=5)
		cmds.move(0,i*3, 0)
		
		if i == numStory-1:
			cmds.polyPyramid(name='pagoda_finalRoof', w=6)
			cmds.move(0,2.5+3*i,0)
			cmds.rotate(0,45,0)
			cmds.scale(1.15,0.655,1.15)
			cmds.polyBevel()
			cmds.select('pagoda_finalRoof.f[5]', 'pagoda_finalRoof.f[8]', 'pagoda_finalRoof.f[10]', 'pagoda_finalRoof.f[12]', 'pagoda_finalRoof.f[17]')
			cmds.polyExtrudeFacet(kft=True, translateY=.1607)
			cmds.select('pagoda_finalRoof.f[18]', 'pagoda_finalRoof.f[21]', 'pagoda_finalRoof.f[24]', 'pagoda_finalRoof.f[27]')
			cmds.polyExtrudeFacet(kft=True, localTranslateZ=0.65, translateY=0.3)
			cmds.polyExtrudeFacet(kft=True, localScale=(0.7, 0.8, 1))
			cmds.polyExtrudeFacet(kft=True, localTranslateZ=0.43)
			cmds.select('pagoda_finalRoof.f[17]')
			cmds.polyExtrudeFacet(kft=True, translateY = numStory, divisions=12)
			#cmds.select('pagoda_finalRoof.f[0]', 'pagoda_finalRoof.f[2]', 'pagoda_finalRoof.f[3]', 'pagoda_finalRoof.f[4]')
			
		else:
			n='pagoda_roof' + str(i)
			cmds.polyCube(name=n, d=7, h=1, w=7)
			cmds.move(0,1.5 + 3*i,0)
			#faces 0,2,4,5
			cmds.select(n+'.f[0]', n+'.f[2]', n+'.f[4:5]')
			cmds.polyExtrudeFacet(kft=True, localScaleY = 0.397, localTranslateZ=0.873108)
			cmds.move(0, -.204, 0, r=True)
			cmds.polyExtrudeFacet(kft=True, localScaleY = 0.397, localTranslateZ = 0.9)
			cmds.move(0, -.4, 0, r=True)
			cmds.select(n)
			#cmds.polyBevel()
			#cmds.select([n+'.f[27]', n+'.f[30]', n+'.f[32]', n+'.f[34]', n+'.f[43]', n+'.f[46]', n+'.f[48]', n+'.f[50]', n+'.f[56]', n+'.f[58]', n+'.f[63:64]', n+'.f[76:79]', n+'.f[84:87]'])
			#cmds.polyExtrudeFacet(kft=True, translateY=.12)

			
	cmds.select([node for node in cmds.ls() if 'pagoda' in node and 'Shape' not in node])
	cmds.group(name='pagoda_' + str(numStory) + 'stories')

def clean():
	cmds.delete([node for node in cmds.ls() if 'pagoda' in node])