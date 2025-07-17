from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3, TransparencyAttrib
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from SpaceJamClasses import Missile
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import CollisionHandlerEvent
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from direct.particles.ParticleEffect import ParticleEffect
from direct.interval.LerpInterval import LerpFunc
import re

class Spaceship(SphereCollideObject):

    def __init__(self, renderNode, loader, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float, traverser: CollisionTraverser): 
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

        self.cntExplode = 0
        self.explodeIntervals = {}
        self.traverser = traverser
        self.handler = CollisionHandlerEvent()

        self.handler.addInPattern('into')
        self.accept('into', self.HandleInto)        

    def HandleInto(self, entry):

        fromNode = entry.getFromNodePath().getName()
        print("fromNode: " + fromNode)
        intoNode = entry.getIntoNodePath().getName()
        print("intoNode: " + intoNode)

        intoPosition = Vec3(entry.getSurfacePoint(self.render))

        tempVar = fromNode.split('_')
        print("tempVar: " + str (tempVar))
        shooter = tempVar[0]
        print("Shooter: " + str(shooter))
        tempVar = intoNode.split('-')
        print("TempVar1: " + str(tempVar))
        tempVar = intoNode.split('_')
        print("TempVar2: " + str(tempVar))
        victim = tempVar[0]
        print("Victim: " + str(victim))

        pattern = r'[0-9]'
        strippedString = re.sub(pattern, '', victim)

        if shooter == victim:
            print("Ignored self-collision")
            return

        if strippedString in ["Drone", "Planet", "Space Station"]:
            print(victim, ' hit at ', intoPosition)
            self.DestroyObject(victim, intoPosition)

        print(shooter + ' is DONE.')

        if shooter in Missile.Intervals:
            Missile.Intervals[shooter].finish()

        # if (strippedString == "Drone" or strippedString == "Planet" or strippedString == "Space Station"):
        #     print (victim, ' hit at ', intoPosition)
        #     self.DestroyObject(victim, intoPosition)

        # print(shooter + ' is DONE.')
        # Missile.Intervals[shooter].finish()

    def DestroyObject(self, hitID, hitPosition):
        nodeID = self.render.find(hitID)
        nodeID.detachNode()

        self.explosionNode.setPos(hitPosition)
        self.Explode()

    def Explode(self):
        self.cntExplode += 1
        tag = 'particles-' + str(self.cntExplode)

        self.explodeIntervals[tag] = LerpFunc(self.ExplodeLight, duration = 4.0)
        self.explodeIntervals[tag].start

    def ExplodeLight(self, t):
        if t == 1.0 and self.explodeEffect:
            self.explodeEffect.disable()

        elif t == 0:
            self.explodeEffect.start(self.explodeNode)

    def SetParticles(self):

        
        
        self.explodeEffect = ParticleEffect()
        # self.explodeEffect.loadConfig('./Assets/ParticleEffects/basic_xpld_efx.ptf')
        # self.explodeEffect.setScale(20)
        self.explosionNode = self.render.attachNewNode('ExplosionEffects')

    def Thrust(self, keyDown):
        if keyDown:
            self.taskMgr.add(self.ApplyThrust, "forward-thrust")
        else:
            self.taskMgr.remove("forward-thrust")

    
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
            
            currentMissile.modelNode.setName(tag + '_' + "Spaceship")

            Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
            Missile.Intervals[tag].start()
            
            self.traverser.addCollider(currentMissile.collisionNode, self.handler)

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
    
    def EnableHUD(self):

        self.Hud = OnscreenImage(image = "./Assets/HUD/center.png", pos = Vec3(0, 0, 0), scale = 0.2)
        self.Hud.setTransparency(TransparencyAttrib.MAlpha)
    
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