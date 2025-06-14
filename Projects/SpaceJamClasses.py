from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

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

    def __init__(self, loader, modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float):

        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

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

    def __init__(self, loader, modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float):
        
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)