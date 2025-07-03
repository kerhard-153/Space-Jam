from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from SpaceJamClasses import Missile
from direct.gui.OnscreenImage import OnscreenImage

class Spaceship(SphereCollideObject):

    def __init__(self, renderNode, loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float): # type: ignore
        super(Spaceship, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.0)
        self.taskMgr = taskMgr
        self.accept = accept
        self.render = renderNode
        self.loader = loader
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)

        self.reloadTime = .25
        self.missileDistance = 4000
        self.missileBay = 1

        self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)

        




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
    
    def Fire(self):
        
        if self.missileBay:
            
            travRate = self.missileDistance
            aim = self.render.getRelativeVector(self.modelNode, Vec3.forward())
            aim.normalize()

            fireSolution = aim * travRate
            infront = aim * 150
            travVec = fireSolution + self.modelNode.getPos()

            self.missileBay -= 1
            tag = "Missile" + str(Missile.missileCount)
            posVec = self.modelNode.getPos() + infront

            currentMissile = Missile(self.render, self.loader, self.taskMgr, self.accept, './Assets/Phaser/phaser.egg', self.render, tag, posVec, 4.0)

            Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
            Missile.Intervals[tag].start()

            if not self.taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')
                self.taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task.cont
        else:
            print('Waiting to reload...')
            
    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1

            if self.missileBay > 1:
                self.missileBay = 1
                print("Reload complete.")
                return Task.done
        elif task.time <= self.reloadTime:
            print("Reload proceeding")
            return Task.cont
        
    def CheckIntervals(self, task):
        for i in Missile.Intervals:
            if not Missile.Intervals[i].isPlaying():
                Missile.cNodes[i].detachNode()
                Missile.fireModels[i].detachNode()
                del Missile.Intervals[i]
                del Missile.fireModels[i]
                del Missile.cNodes[i]
                del Missile.collisionSolids[i]
                print(i + 'has detached from the end of its fire solution')
                break
        return Task.cont
    
    # def EnableHUD(self):

    #     self.Hud = OnscreenImage(image = "./Assets/Hud/Reticle.png", pos = Vec3(0, 0, 0), scale = 0.1)
        # self.Hud.setTransparency(TransparencyAttrib.MAlpha)