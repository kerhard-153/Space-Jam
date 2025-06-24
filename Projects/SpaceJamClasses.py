from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from panda3d.core import Vec3

class Universe(ShowBase):

    def __init__(self, loader, modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float):
        
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Planet(ShowBase):

    def __init__(self, loader, modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float):
        
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Drone(ShowBase):
    
    droneCount = 0

    def __init__(self, loader, modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float, color = (1, 1, 1, 1)):

        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        self.modelNode.setColor(*color, 1)

class SpaceStation(ShowBase):

    def __init__(self, loader, modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float):
        
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Spaceship(ShowBase):

    def __init__(self, renderNode, loader, modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float, taskMgr):
        
        self.render = renderNode
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        self.taskMgr = taskMgr

    def Thrust(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrust, "forward-thrust")
        else:
            self.taskMgr.remove("forward-thrust")

    def ApplyThrust(self, task):

        rate = 20
        quat = self.modelNode.getQuat(self.render)
        forwardTraj = quat.getForward()
        forwardTraj.normalize()

        self.modelNode.setFluidPos(self.modelNode.getPos() + (forwardTraj * rate))

        return Task.cont

    def LeftTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLeftTurn, "left-turn")
        else:
            self.taskMgr.remove("left-turn")

    def ApplyLeftTurn(self, task):
        
        rate = .5
        self.modelNode.setH(self.modelNode.getH() + rate)
        
        return Task.cont
    
    def RightTurn(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRightTurn, "right-turn")
        else:
            self.taskMgr.remove("right-turn")

    def ApplyRightTurn(self, task):
        
        rate = .5
        self.modelNode.setH(self.modelNode.getH() - rate)
        
        return Task.cont
    
    def LookUp(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLookUp, "look-up")
        else:
            self.taskMgr.remove("look-up")

    def ApplyLookUp(self, task):
        
        rate = .5
        self.modelNode.setP(self.modelNode.getP() + rate)
        
        return Task.cont
    
    def LookDown(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyLookDown, "look-down")
        else:
            self.taskMgr.remove("look-down")

    def ApplyLookDown(self, task):
        
        rate = .5
        self.modelNode.setP(self.modelNode.getP() - rate)
        
        return Task.cont
    
    def RollLeft(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRollLeft, "roll-left")
        else:
            self.taskMgr.remove("roll-left")

    def ApplyRollLeft(self, task):
        
        rate = .5
        self.modelNode.setR(self.modelNode.getR() + rate)
        
        return Task.cont
    
    def RollRight(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyRollRight, "roll-right")
        else:
            self.taskMgr.remove("roll-right")

    def ApplyRollRight(self, task):
        
        rate = .5
        self.modelNode.setR(self.modelNode.getR() - rate)
        
        return Task.cont