from typing import Callable
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from direct.task.Task import TaskManager
from panda3d.core import Vec3
from CollideObjectBase import *

class Universe(InverseSphereCollideObject):

    def __init__(self, loader, modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float):
        super(Universe, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 0.9)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)


class Planet(SphereCollideObject):

    def __init__(self, loader, modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float):

        super(Planet, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 1.05)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Drone(SphereCollideObject):
    
    droneCount = 0

    def __init__(self, loader, modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float, color = (1, 1, 1, 1)):
        super(Drone, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.0)

        # self.modelNode = loader.loadModel(modelPath)
        # self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        self.modelNode.setColor(*color, 1)

class SpaceStation(CapsuleCollidableObject):

    def __init__(self, loader, modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float):
        super(SpaceStation, self).__init__(loader, modelPath, parentNode, nodeName, 1, -1, 5, 1, -1, -5, 10)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

class Missile(SphereCollideObject):

    fireModels = {}
    cNodes = {}
    collisionSolids = {}
    Intervals = {}

    missileCount = 0

    def __init__(self, renderNode, loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str, parentNode, nodeName: str, posVec, scaleVec: float):

        super(Missile, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.0)
        
        self.taskMgr = taskMgr
        self.accept = accept
        self.render = renderNode
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)

        Missile.missileCount += 1
        Missile.fireModels[nodeName] = self.modelNode
        Missile.cNodes[nodeName] = self.collisionNode 
        Missile.collisionSolids[nodeName] = self.collisionNode.node().getSolid(0)
        Missile.cNodes[nodeName].show()

        print("Fire torpedo #" + str(Missile.missileCount))