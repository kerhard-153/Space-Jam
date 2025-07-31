from CollideObjectBase import SphereCollideObject
from panda3d.core import Loader, NodePath, Vec3, Vec4, TransparencyAttrib
from direct.task.Task import TaskManager
from typing import Callable
from direct.task import Task
from SpaceJamClasses import Missile
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import CollisionHandlerEvent
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from direct.particles.ParticleEffect import ParticleEffect
from direct.interval.LerpInterval import LerpFunc, LerpHprInterval
import re
from panda3d.core import Filename
from panda3d.core import ClockObject

class Spaceship(SphereCollideObject):

    def __init__(self, renderNode, loader, app, taskMgr: TaskManager, accept: Callable[[str, Callable], None], modelPath: str, parentNode, nodeName: str, texPath: str, posVec, scaleVec: float, traverser: CollisionTraverser, maxHealth): 
        super(Spaceship, self).__init__(loader, modelPath, parentNode, nodeName, Vec3(0, 0, 0), 3.0)
        self.taskMgr = taskMgr
        self.accept = accept
        self.render = renderNode
        self.loader = loader
        self.app = app
        
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scaleVec)

        self.modelNode.setName(nodeName)
        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.maxHealth = maxHealth

        self.reloadTime = .25
        self.missileDistance = 7500
        self.missileBay = 1
        self.heavyMissileBay = 1

        self.taskMgr.add(self.CheckIntervals, 'checkMissiles', 34)

        self.cntExplode = 0
        self.explodeIntervals = {}
        self.traverser = traverser
        self.handler = CollisionHandlerEvent()

        self.handler.addInPattern('into')
        self.accept('into', self.HandleInto)  

        self.baseSpeed = 15
        self.boostMultiplier = 2.0
        self.currentSpeed = self.baseSpeed
        self.isBoosting = False
        self.boostDuration = 3.0
        self.boostCooldown = 5.0
        self.lastBoostTime = -999  

        self.lastHeavyMissileTime = 0
        self.heavyMissileCooldown = 5.0

        

    def ActivateBoost(self):
        
        globalClock = ClockObject.getGlobalClock()
        currentTime = globalClock.getRealTime() 

        if self.isBoosting:
            return
        if currentTime - self.lastBoostTime < self.boostCooldown:
            print("Cooling down: Boost")   
            return
        
        print("Boosting!")
        self.isBoosting = True
        self.currentSpeed = self.baseSpeed * self.boostMultiplier
        self.lastBoostTime = currentTime

        self.taskMgr.doMethodLater(self.boostDuration, self.EndBoost, "EndBoost")

    def EndBoost(self, task):

        print("UR DONE")
        self.currentSpeed = self.baseSpeed
        self.isBoosting = False
        return task.done

    def HandleInto(self, entry):

        fromNode = entry.getFromNodePath().getName()
        intoNode = entry.getIntoNodePath().getName()

        print("fromNode:", fromNode)
        print("intoNode:", intoNode)

        fromParts = fromNode.split('_')
        intoParts = intoNode.split('_')

        shooter = fromParts[0]
        victim = intoParts[0]

        if shooter == victim:
            print("Ignored self-collision")
            return

        pattern = r'[0-9]'
        strippedVictim = re.sub(pattern, '', victim)

        victimNode = entry.getIntoNodePath()
        victimObject = victimNode.getPythonTag("object")

        missileNode = entry.getFromNodePath()
        missileObject = missileNode.getPythonTag("object")

        if strippedVictim in ["Drone", "Planet", "SpaceStation"]:
            hitPos = Vec3(entry.getSurfacePoint(self.render))
            print(f"{victim} hit at {hitPos}")

            damage = missileObject.damage if hasattr(missileObject, "damage") else Missile.damage

            victimObject.TakeDamage(damage, self.render, self.taskMgr, hitPos)

        if shooter in Missile.Intervals:
            Missile.Intervals[shooter].finish()


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
            infront = aim * 200
            travVec = fireSolution + self.modelNode.getPos()

            self.missileBay -= 1
            tag = "Missile" + str(Missile.missileCount)
            posVec = self.modelNode.getPos() + infront

            currentMissile = Missile(self.render, self.loader, self.taskMgr, self.accept, './Assets/Phaser/phaser.egg', self.render, tag, posVec, 4.0, 50)
            
            currentMissile.modelNode.setName(tag + '_' + "Spaceship")
            currentMissile.modelNode.setPythonTag("object", currentMissile)

            Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
            Missile.Intervals[tag].start()
            
            self.traverser.addCollider(currentMissile.collisionNode, self.handler)

            if not self.taskMgr.hasTaskNamed('reload'):
                print('Initializing reload...')
                self.taskMgr.doMethodLater(0, self.Reload, 'reload')
                return Task.cont
        else:
            print('Waiting to reload...')
    
    def FireHeavyMisile(self):

        globalClock = ClockObject.getGlobalClock()
        currentTime = globalClock.getRealTime() 
        
        if currentTime - self.lastHeavyMissileTime > self.heavyMissileCooldown:
            self.heavyMissileBay += 1
            if self.heavyMissileBay > 1:
                self.heavyMissileBay = 1
        
        if currentTime - self.lastHeavyMissileTime < self.heavyMissileCooldown:
            print("Cooling down: Heavy Missile")
            return
        
        if self.heavyMissileBay <= 0:
            print("No missiles left!")
            return
        
        
        
        print("Firing Heavy Missile!")
        self.lastHeavyMissileTime = currentTime
            
        travRate = self.missileDistance
        aim = self.render.getRelativeVector(self.modelNode, Vec3.forward())
        aim.normalize()


        fireSolution = aim * travRate
        infront = aim * 200
        travVec = fireSolution + self.modelNode.getPos()

        self.heavyMissileBay -= 1
        tag = "Missile" + str(Missile.missileCount)
        posVec = self.modelNode.getPos() + infront

        heavyDamage = 200

        currentMissile = Missile(self.render, self.loader, self.taskMgr, self.accept, './Assets/Phaser/phaser.egg', self.render, tag, posVec, 4.0, heavyDamage)
        
        currentMissile.modelNode.setName(tag + '_' + "Spaceship")
        currentMissile.modelNode.setPythonTag("object", currentMissile)

        Missile.Intervals[tag] = currentMissile.modelNode.posInterval(2.0, travVec, startPos = posVec, fluid = 1)
        Missile.Intervals[tag].start()
        
        self.traverser.addCollider(currentMissile.collisionNode, self.handler)


            
    def Reload(self, task):
        if task.time > self.reloadTime:
            self.missileBay += 1

            if self.missileBay > 1:
                self.missileBay = 1
                print("Reload complete.")
                return Task.done
        elif task.time <= self.reloadTime:
            # print("Reload proceeding")
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
    
    def EnableHUD(self, show: bool):
        if show:
            if not getattr(self, 'hudImage', None):
                windowProps = self.app.win.getProperties()
                windowAspect = (windowProps.getXSize() / windowProps.getYSize())


                self.hudImage = OnscreenImage(image = "./Assets/HUD/HUD_Screen.png", 
                                              pos = Vec3(0, 0, 0), 
                                              scale=(windowAspect, 1, 1), 
                                              parent=self.app.aspect2d)
                self.hudImage.setTransparency(TransparencyAttrib.MAlpha)
                self.hudImage.setBin("fixed", 0)
                self.hudImage.setDepthTest(False)
                self.hudImage.setDepthWrite(False)
            else:
                self.hudImage.show()
        else:
            if hasattr(self, 'hudImage'):
                self.hudImage.hide()
            
    def ApplyThrust(self, task):

        rate = self.currentSpeed
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
            currentHpr = self.modelNode.getHpr()
            newHpr = currentHpr + (0, 0, 90)
            self.rollInterval = LerpHprInterval(self.modelNode, 0.5, newHpr)
            self.rollInterval.start() 
    
    def RollRight(self, keyDown):
        if keyDown:
            currentHpr = self.modelNode.getHpr()
            newHpr = currentHpr + (0, 0, -90)
            self.rollInterval = LerpHprInterval(self.modelNode, 0.5, newHpr)
            self.rollInterval.start()