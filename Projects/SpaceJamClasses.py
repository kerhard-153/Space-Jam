from typing import Callable
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from direct.task.Task import TaskManager
import DefensePaths as defensePaths
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

class Orbiter(SphereCollideObject):

    numOrbits = 0
    velocity = 0.005
    cloudTimer = 240

    def __init__(self, loader: Loader, taskMgr:  TaskManager, modelPath: str, parentNode: NodePath, nodeName: str, scaleVec: float, texPath: str,
                 centralObject: PlacedObject, orbitRadius: float, orbitType: str, staringAt: Vec3, orbitIndex):
        super(Orbiter, self,).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.2)

        self.taskMgr = taskMgr
        self.orbitType = orbitType
        self.modelNode.setScale(scaleVec)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.orbitObject = centralObject
        self.orbitRadius = orbitRadius
        self.staringAt = staringAt

        self.orbitIndex = orbitIndex
        Orbiter.numOrbits += 1

        self.cloudClock = 0

        self.taskFlag = "Traveler-" + str(self.orbitIndex)
        taskMgr.add(self.Orbit, self.taskFlag)

        self.modelNode.show()
        print(f"[Orbiter Created] {nodeName} around {centralObject.modelNode.getName()} at radius {orbitRadius}")



    def Orbit(self, task):
        if self.orbitType == "MLB":
            positionVec = defensePaths.BaseballSeams(task.time * Orbiter.velocity, 2, self.orbitIndex)
            self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())
        elif self.orbitType == "Cloud":
            if self.cloudClock < Orbiter.cloudTimer:
                self.cloudClock += 1
            else:
                self.cloudClock = 0
                positionVec = defensePaths.Cloud()
                self.modelNode.setPos(positionVec * self.orbitRadius + self.orbitObject.modelNode.getPos())

        self.modelNode.lookAt(self.staringAt.modelNode)
        return Task.cont
    