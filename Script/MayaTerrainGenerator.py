##### M A R K   B R O U W E R ###
##### T E R M  P R O J E C T  ###
##### T E R R A I N  G E N E R A T O R ###
 
import maya.cmds as cmds
import random
import math


##Creates a new scene when the new asceme
def newScene():
    cmds.file( force=True, new=True)     
    cmds.deleteUI(myWin, window=True)   
    #cannot figure out how to re enable buttons
    #resulted to having the UI be deleted and the user must re initialize it
    #mound = cmds.button(label="Create Mounds", command=('createHill()'), en=True)
    #ditch = cmds.button(label="Create Ditchs", command=('createDitch()'), en=True)
    #build = cmds.button(label="Create Buildings", command=('createBuildings()'), en=True)
    #fbutton = cmds.button(label="Add Fractal Noise", command=('addNoise()'), en=True)
    #smooth = cmds.button(label="Smooth", command=('smoothPlane()'))
    #cmds.window(myWin, window=True)
    #cmds.showWindow( myWin )

#cmds.file( force=True, new=True)
if 'myWin' in globals():
    if cmds.window(myWin, exists=True):
        cmds.deleteUI(myWin, window=True)

##############
###   UI   ###
##############        
myWin = cmds.window(title="Terrain Generator", menuBar=True)
cmds.menu(label="Basic options")
cmds.menuItem(label="New Scene", command=('newScene()')) #create new scene
cmds.menuItem(label="Delete Selected", command=('cmds.delete()'), ec=True) #delete selected object


### PLANE  ##
cmds.frameLayout(collapsable=True, label="Create Plane")
###user set width and depth
cmds.intSliderGrp('PlaneWidth', label="Width", field=True, min=5, max=40, value=20) 
cmds.intSliderGrp('PlaneDepth', label="Depth", field=True, min=5, max=40, value=20) 
#user set subDiv's
cmds.intSliderGrp('SdWidth', label="Subdivide Width", field=True, min=4, max=20, value=10) 
cmds.intSliderGrp('SdDepth', label="Subdivide Depth", field=True, min=4, max=20, value=10) 


cmds.columnLayout()
cmds.button(label="Create Terrain", command=('createPlane()'))

cmds.setParent('..')
cmds.setParent('..')

## Modifications to terrain
cmds.frameLayout(collapsable=True, label="Modifications")
cmds.intSliderGrp('MoundAmp', label="Amplitude", field=True, min=1, max=3, value=1)
mound = cmds.button(label="Create Mounds", command=('createHill()'), en=True)
ditch = cmds.button(label="Create Ditchs", command=('createDitch()'), en=True)
build = cmds.button(label="Create Buildings", command=('createBuildings()'), en=True)

cmds.setParent('..')
cmds.setParent('..')

## colouring of hte terrain presets
cmds.frameLayout(collapsable=True, label="Colour Plane")
cmds.rowLayout( numberOfColumns=5)
cmds.button(label="Desert", command=('colourDesert()'))
cmds.button(label="Grass", command=('colourGrass()'))
cmds.button(label="Rock", command=('colourRock()'))

#for personal colour selection
cmds.colorSliderGrp('planeColour', label="Colour", rgb=(1.0,1.0,1.0))
cmds.button(label="SetColour", command=("colourChoice()"))

cmds.setParent("..")
cmds.setParent("..")

#this function is creates a fractal subdivision simulation of the diamond square algorithm
cmds.frameLayout(collapsable=True, label="Fractal Modifications")
cmds.columnLayout()
fbutton = cmds.button(label="Add Fractal Noise", command=('addNoise()'), en=True)

cmds.setParent('..')
cmds.setParent('..')

#smooth function for hill looking terrains
cmds.frameLayout(collapsable=True, label="Smooth Plane")
smooth = cmds.button(label="Smooth", command=('smoothPlane()'))

cmds.setParent('..')
cmds.setParent('..')


cmds.showWindow( myWin )



###########################################
###########################################
##### T E R R A I N  G E N E R A T O R ####
###########################################
###########################################

#initializing globals for access in all functions
vCount = 0
fCount = 0

testMesh = "Nothing"

SubWidth = 0
SubDepth = 0

tallness = 0

count = 0
mod = False

PWidth = 0
PDepth = 0

bCount = 0


## this function is to handle the UI enable and disable options
## depending on if the object has deleted or a new scene is created
def boolSwitch():
    if(cmds.objExists('myRef')):
       print "myRef Exists\n"
       cmds.delete('myRef')
       
    cmds.select(testMesh)
    cmds.delete()
    
    mod = False
    mound = cmds.button(label="Create Mounds", command=('createHill()'), en=True)
    ditch = cmds.button(label="Create Ditchs", command=('createDitch()'), en=True)
    count = 0


##################
###CREATE PLANE###
##################
def createPlane():
    global PWidth
    PWidth = cmds.intSliderGrp('PlaneWidth', q=True, v=True)
    global PDepth
    PDepth = cmds.intSliderGrp('PlaneDepth', q=True, v=True)
    global SubWidth
    SubWidth = cmds.intSliderGrp('SdWidth', q=True, v=True) 
    global SubDepth
    SubDepth = cmds.intSliderGrp('SdDepth', q=True, v=True)
    #step 1 : create a poplygonal mesh
    global testMesh
    testMesh = "perturbedMesh"
    cmds.polyPlane(w=PWidth*2, h=PDepth*2, sx=SubWidth, sy=SubDepth, n=testMesh)
    
    #step 2 obtain the vertex and face count so we can then lop through the verticies and faces
    global vCount
    vCount = cmds.polyEvaluate(v=True)
    global fCount
    fCount = cmds.polyEvaluate(f=True)
    #print vCount
    
    
    
    
###################    
### CREATE HILL ###
###################
def createHill():
    height = cmds.intSliderGrp('MoundAmp', q=True, v=True)
    cmds.disable(build)
        
    for face in xrange(0,fCount,3):     
        noise = perlin(face)

        ##if noise returns a 1 then we will print ONE, this is for debugging as it only happens when the result is = 0, which shouldnt happen
        if(noise == 1):
            print "ONE"
        ##if the noise returns a 2 then
        if(noise == 2):
            print "Two"
            #gather a list of the faces nearby verticies
            vtxLst = cmds.polyInfo(testMesh + ".f[" + str(face) + "]", faceToVertex=True)
            vtxIdx = str(vtxLst[0]).split()
            #select a vertex randomly
            loc = random.randint(2,5);
            vtx = vtxIdx[loc]
            #select that vertex
            cmds.select(testMesh+".vtx["+vtx+"]")
            #randomly creates a value between 0.0 and 1.0 to devide by
            rn = random.random()
            tmpValueY = height#*(math.sin(face/rn))
            
            #This control makes sure all values are positive or nothing will happen
            if(tmpValueY < 0):
                tmpValueY = 0.0
            #moves the location of the vertex vertically
            cmds.move(0.0, tmpValueY, 0.0, r=True)
            
        #if the noise is returned with 3, do the same thing as if noise is 2, but a different random iterator to devide by, which will create larger hills
        if(noise == 3):
            print "three"
            
    
####################
### CREATE DITCH ### 
#################### 
#function works seperatly then the above create hill
#this is because I am still experimenting with how the perlion noise function works before applying the algorithm here as awell
#this one is a simulation random uniform selection that is similar to the results of perlin noise, but not particularly running the perling noise funtion
def createDitch():
    height = cmds.intSliderGrp('MoundAmp', q=True, v=True)
    cmds.disable(build)
    for face in xrange(0,fCount,3):     
        noise = perlin(face)
    
        ##if noise returns a 1 then we will print ONE, this is for debugging as it only happens when the result is = 0, which shouldnt happen
        if(noise == 1):
            print "ONE"
        ##if the noise returns a 2 then
        if(noise == 2):
            print "Two"
               
        #if the noise is returned with 3, do the same thing as if noise is 2, but a different random iterator to devide by, which will create larger hills
        if(noise == 3):
            print "three"
            #gather a list of the faces nearby verticies
            vtxLst = cmds.polyInfo(testMesh + ".f[" + str(face) + "]", faceToVertex=True)
            vtxIdx = str(vtxLst[0]).split()
            #select a vertex randomly
            loc = random.randint(2,5);
            vtx = vtxIdx[loc]
            #select that vertex
            cmds.select(testMesh+".vtx["+vtx+"]")
            #randomly creates a value between 0.0 and 1.0 to devide by
            rn = random.random()
            tmpValueY = height#*(math.sin(face/rn))
            
            #This control makes sure all values are positive or nothing will happen
            if(tmpValueY < 0):
                tmpValueY = 0.0
            #moves the location of the vertex vertically
            cmds.move(0.0, -tmpValueY, 0.0, r=True)
            
            
            
#######################
### CREATE Building ### 
####################### 
def createBuildings():
    #gather desired building height
    bHeight = cmds.intSliderGrp('MoundAmp', q=True, v=True)
    
    createLocator(bHeight)
    
    #disabling the buttons that will interfere with the appearance of buildings
    global bCount
    bCount = bCount+1
    if(bCount == 3):
        cmds.disable(build)
    cmds.disable(smooth)
    cmds.disable(mound)
    cmds.disable(ditch)
    cmds.disable(fbutton)
    
#creates a reference point for the building extrusion
def createLocator(bHeight):
    #if reference exists delete it
    if(cmds.objExists('myRef')):
        print "myRef Exists\n"
        cmds.delete('myRef')
    #create a locator for referecne for extrusion
    cmds.spaceLocator(n='myRef')
    cmds.move(20, 5, 20)
    print "myRef Created\n"
    adjustSelected("extrude", "all",bHeight)

#gathers the selected mesh and sends the object to be adjusted  
def adjustSelected(action, direction, bHeight):
    #ensures the testMesh is created
    cmds.select(testMesh)
    #puts it into a shape list
    selectedShapes = cmds.ls(selection=True)
    #goes through the list
    for shape in selectedShapes:
        #checks to see if the object is a shape
        shapeType = cmds.objectType(shape)
        # if it is a transform shape then its added to another list
        if(shapeType == 'transform'):
            childShape = cmds.listRelatives(shape, fullPath=True, shapes=True)
            if(cmds.objectType(childShape) != 'mesh'):    continue
            #if its a mesh then we pass the shape to the adjusted Object function
            adjustSelectedObject(action, direction, shape, bHeight)
            
#this function decides if the face is going to be extruded     
def adjustSelectedObject(action, direction, object, bHeight):
    posShape = cmds.xform(object, query=True, translation=True, worldSpace=True)
    posRef = cmds.xform('myRef', query=True, translation=True, worldSpace=True)
    
    #gets the object vector in relation to our reference locator
    objVec = [0,0,0]
    objVec[0] = posShape[0] - posRef[0]
    objVec[1] = posShape[1] - posRef[1]
    objVec[2] = posShape[2] - posRef[2]
    
    #sets update face to false
    updateFace = False
    #creates random seed for the face extrusions to be offset the slightest
    seed = random.randint(1,4)
    #goes through each face
    for face in xrange(0, fCount,seed):
        #obtain vertex list of the face
        vtxLst = cmds.polyInfo(object + ".f[" + str(face) + "]", faceToVertex=True)
        vtxIdx = str(vtxLst[0]).split()
        #get vertices seperated
        vtxA = cmds.getAttr(object + ".vt[" + vtxIdx[2] + "]")
        vtxB = cmds.getAttr(object + ".vt[" + vtxIdx[3] + "]")
        vtxC = cmds.getAttr(object + ".vt[" + vtxIdx[4] + "]")
        
        #function to get the normal value of each face
        fN = getNormal(vertexA=list(vtxA[0]), vertexB=list(vtxB[0]), vertexC=list(vtxC[0]))

        #applys a random value to the y attribute, and zeros the x and z attributes
        fN[0] = fN[0] * 0.0 # zero because we only want translation in the y diretion
        fN[1] = fN[1] * random.uniform(0.5, 1.0) * (bHeight * 10) #making the value relative to the set height ampplitude
        fN[2] = fN[2] * 0.0
        
        #makes sure that update face is set to false
        updateFace = False
       
        #if all is selected it will update every face ( the ones incrtemented throught the loop
        if(direction == "all"):    updateFace = True
        
        # when the face gets chosen we extrude the face to an amount requested
        if(updateFace == True):
            theFace = object + ".f[" + str(face) + "]"
            if(action == "del"):
                cmds.polyDelFacet(theFace)
            if(action == "extrude"):
                cmds.polyExtrudeFacet(theFace, t=[fN[0], fN[1], fN[2]])
        
        #re counts the face numbers as they will be changed    
        global vCount
        vCount = cmds.polyEvaluate(v=True)
        global fCount
        fCount = cmds.polyEvaluate(f=True)
  
#function to gather normal vector of a face      
def getNormal(vertexA, vertexB, vertexC):
    vecA = [0,0,0]
    vecB = [0,0,0]
    
    vecA[0] = vertexB[0] - vertexA[0]
    vecA[1] = vertexB[1] - vertexA[1]
    vecA[2] = vertexB[2] - vertexA[2]
    
    vecB[0] = vertexC[0] - vertexA[0]
    vecB[1] = vertexC[1] - vertexA[1]
    vecB[2] = vertexC[2] - vertexA[2]
    
    #Cross Product
    nrmVec = [0,0,0]
    nrmVec[0] = (vecA[1] * vecB[2]) - (vecA[2] * vecB[1])
    nrmVec[1] = (vecA[2] * vecB[0]) - (vecA[0] * vecB[2])
    nrmVec[2] = (vecA[0] * vecB[1]) - (vecA[1] * vecB[0])
    
    nrmMag = ((nrmVec[0] ** 2) + (nrmVec[1] ** 2) + (nrmVec[2] ** 2)) ** 0.5
    
    nrmVec[0] = nrmVec[0] / nrmMag;
    nrmVec[1] = nrmVec[1] / nrmMag;
    nrmVec[2] = nrmVec[2] / nrmMag;
    
    return nrmVec
    
#gets the dot product of two vectors
def getDotProduct(vtxA, vtxB):
    result = (vtxA[0] * vtxB[0]) + (vtxA[1] * vtxB[1]) + (vtxA[2] * vtxB[2])
    return result
  


################
###PolySmooth###
################
def smoothPlane():
    cmds.select(testMesh)
    #checking to make sure the poly count isnt too large
    global vCount
    vCount = cmds.polyEvaluate(v=True)
    global fCount
    fCount = cmds.polyEvaluate(f=True)
    
    #if(fCount < 2500):
    cmds.polySmooth(n=testMesh)
    #gotta reset the global count
    global vCount
    vCount = cmds.polyEvaluate(v=True)
    global fCount
    fCount = cmds.polyEvaluate(f=True)



####################
###COLOUR TERRAIN###
####################
###    DESERT    ###
####################
def colourDesert():
    r = 0.6
    g = 0.4
    b = 0.1
    colourSurface(r,g,b)
    
####################
###COLOUR TERRAIN###
####################
###    GRASS     ###
####################
def colourGrass():
    r = 0.1
    g = 0.2
    b = 0.1
    colourSurface(r,g,b)
    
    
    
####################
###COLOUR TERRAIN###
####################
###     Rock     ###
####################
def colourRock():
    r = 0.43
    g = 0.42
    b = 0.45
    colourSurface(r,g,b)


####################
###COLOUR TERRAIN###
####################
###    Choice    ###
####################
def colourChoice():
    rgb = cmds.colorSliderGrp('planeColour', q=True, rgbValue=True)
    colourSurface(rgb[0],rgb[1],rgb[2])
    
####################
###COLOUR TERRAIN###
####################
###   Function   ###
####################  
def colourSurface(r,g,b):

    nsTmp = "Plane" + str(random.randint(1000,9999))    #makes it easier to keep track of object we are creating witihin this function
    
    cmds.namespace(add=nsTmp) 
    cmds.namespace(set=nsTmp) 
   
    myShader = cmds.shadingNode('lambert', asShader=True, name="blckMat")

    cmds.setAttr(nsTmp+":blckMat.color", r, g, b, typ='double3')        
    cmds.select(testMesh)

    cmds.hyperShade(assign=(nsTmp+":blckMat"))
    
    cmds.namespace(removeNamespace=":"+nsTmp, mergeNamespaceWithParent=True) #now can leave the namespace


##############################
#### RANDOM FRACTAL NOISE ####
##############################
def addNoise(): 
    #disable the other commands when the noise is modified to the terrain
    mod = True
    
    #subdivide the facet
    cmds.polyTriangulate( testMesh ,ch=False)
    
    # ensure that the whole mesh is selected
    cmds.select(testMesh)
    ##recalculations of the global variables   
    global vCount
    vCount = cmds.polyEvaluate(v=True)
    global fCount
    fCount = cmds.polyEvaluate(f=True)
    global count
    
    #fractal subdivisde ggoes through every face
    for face in range (1,fCount):
        facetNum = str(face)
        #select the face
        cmds.select(testMesh+".f["+facetNum+"]")
        
        #get vertex list and select one
        vtxLst = cmds.polyInfo(testMesh + ".f[" + str(face) + "]", faceToVertex=True)
        vtxIdx = str(vtxLst[0]).split()

        vtxB = cmds.getAttr(testMesh + ".vt[" + vtxIdx[2] + "]")

        print vtxB
        #create some random values to be aded at the random location
        tmpValueX = random.uniform(-0.2, 0.2)
        tmpValueY = random.uniform(-0.3, 0.3)
        tmpValueZ = random.uniform(-0.2, 0.2)
        
        #moves the vertex to add some noise to the terrain
        cmds.move(tmpValueX, tmpValueY, tmpValueZ, r=True)

    #counting to make sure that the function doesnt calculate too many faces
    count = count + 1
    
    #if count gets to twice
    #disables the button to prevent the script from calculating for a large period of time
    if(count == 3):
        cmds.disable(fbutton)
    
    #disables the mound and ditch commands when the face count increases because the results are ugly
    if (mod == True):
        cmds.disable(mound)
        cmds.disable(ditch)
        cmds.disable(build)
        

######################
#### PERLIN NOISE ####
######################
def perlin( face):
    #PERLIN GRID DEFINITION
    #going throuhg each face and extracting its verticies so that I can apply perlin noise 
    vtxLst = cmds.polyInfo(testMesh + ".f[" + str(face) + "]", faceToVertex=True)
    vtxIdx = str(vtxLst[0]).split()

    #grab the faces veticies
    vtxA = cmds.getAttr(testMesh + ".vt[" + vtxIdx[2] + "]")
    vtxB = cmds.getAttr(testMesh + ".vt[" + vtxIdx[3] + "]")
    vtxC = cmds.getAttr(testMesh + ".vt[" + vtxIdx[4] + "]")
    vtxD = cmds.getAttr(testMesh + ".vt[" + vtxIdx[5] + "]")
    
    #get the x y z values of each
    newvtxA = vtxA[0]
    vtxAx = newvtxA[0]
    vtxAy = newvtxA[1]
    vtxAz = newvtxA[2]
    
    newvtxB = vtxB[0]
    vtxBx = newvtxB[0]
    vtxBy = newvtxB[1]
    vtxBz = newvtxB[2]
    
    newvtxC = vtxC[0]
    vtxCx = newvtxC[0]
    vtxCy = newvtxC[1]
    vtxCz = newvtxC[2]
    
    newvtxD = vtxD[0]
    vtxDx = newvtxD[0]
    vtxDy = newvtxD[1]
    vtxDz = newvtxD[2]
    
    #gathering random input point for each gradient calculation
    inputx = random.uniform(-1.0,1.0) 
    inputy = random.uniform(-1.0,1.0)
    inputz = random.uniform(-1.0,1.0)
    
    #getting gradient positions for 4 surrounding points, only extracting x and z here as the transformation to y happens depending on a if it is a ditch or hill
    ax0 = vtxAx - int(vtxAx)
    ax1 = ax0 + 1.0
    ay0 = vtxAy - int(vtxAy)
    ay1 = ay0 + 1.0

    bx0 = vtxBx - int(vtxBx)
    bx1 = bx0 + 1.0
    by0 = vtxBy - int(vtxBy)
    by1 = by0 + 1.0
  
    cx0 = vtxCx - int(vtxCx)
    cx1 = cx0 + 1.0
    cy0 = vtxCy - int(vtxCy)
    cy1 = cy0 + 1.0

    
    dx0 = vtxDx - int(vtxDx)
    dx1 = cx0 + 1.0
    dy0 = vtxDy - int(vtxDy)
    dy1 = cy0 + 1.0
       
    #calculating gradient with Dot Product
    gradA = gradient(ax0,ax1,ay0,ay1, inputx,inputy)
    gradB = gradient(bx0,bx1,by0,by1, inputx,inputy)
    gradC = gradient(cx0,cx1,cy0,cy1, inputx,inputy)
    gradD = gradient(dx0,dx1,dy0,dy1, inputx,inputy)

    #calcualte linear distance of vectors
    distA = distance(vtxAx,vtxAy,vtxAz)
    distB = distance(vtxBx,vtxBy,vtxBz)
    distC = distance(vtxCx,vtxCy,vtxCz)
    distD = distance(vtxDx,vtxDy,vtxDz) 
    
    
    #dot Product
    dpA = (distA[0] * gradA[0]) + (distA[1] * gradA[1])# + (distA[2] * gradA[2])
    dpB = (distB[0] * gradB[0]) + (distB[1] * gradB[1])# + (distB[2] * gradB[2])
    dpC = (distC[0] * gradC[0]) + (distC[1] * gradC[1])# + (distC[2] * gradC[2])
    dpD = (distD[0] * gradD[0]) + (distD[1] * gradD[1])# + (distD[2] * gradD[2])
        
    #INTERPOLATION
    val = lerp(lerp(lerp(dpA,dpB),lerp(dpB,dpC)), lerp(lerp(dpC,dpD),lerp(dpD,dpA)))

    #depending on the if the interpolation result is greater than or less than zero or equal
    #noise will be returned in either 1 2 or 3, which decides the amplitude of the hill at this location
    if(val > 0.1):
        noise = 2
    elif(val < 0.1):
        noise = 3
    else:
        noise = 1
        
    return noise
    

###calculate linear distance
def distance(x,y,z):
    #apply a random value to be tested to location of
    ix = x * random.uniform(-1.0,1.0)
    iy = x * random.uniform(-1.0,1.0)
    iz = x * random.uniform(-1.0,1.0)
    
    #calculate the distance of the vector
    vecX = ix - x
    vecY = iy - y
    vecZ = iz - z
    
    vector = [0.0,0.0,0.0]
    vector[0] = vecX
    vector[1] = vecY
    vector[2] = vecZ

    return vector

#calculate gradient
def gradient(gx0,gx1,gy0,gy1, inputx, inputy):    
    gx = (gx0 - gx1) * inputx
    gy = (gy0 - gy1) * inputx
    
    g = [gx,gy]

    return g
    
#interpolation values that changes the way the values will be outputted based on cosin and a random input
def lerp(a,b):
        #create random input value
        w = random.uniform(0.0,1.0)  
        
        #creates a value related to radians so it can be applied to the cosin value
        ft = w * 3.1415927
        
        f = (1.0 - math.cos(ft)) * 0.5 
        
        val = a*(1-f) + b*f
        
        return val
