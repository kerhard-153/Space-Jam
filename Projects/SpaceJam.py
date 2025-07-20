from direct.showbase.ShowBase import ShowBase
import SpaceJamClasses as sjcRef
import DefensePaths as dpRef
import Player as pRef
import CollideObjectBase as colBaseRef
from panda3d.core import Vec3
import math, random, sys
from panda3d.core import CollisionTraverser, CollisionHandlerPusher
from direct.task.Task import TaskManager
from direct.task import Task

class MyApp(ShowBase):

    def __init__(self):
        
        
        ShowBase.__init__(self)

        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.enableParticles()
        self.SetupScene()

        self.cTrav.traverse(self.render)
        self.pusher.addCollider(self.Spaceship.collisionNode, self.Spaceship.modelNode)
        self.cTrav.addCollider(self.Spaceship.collisionNode, self.pusher)
        self.cTrav.showCollisions(self.render)

        self.SetCamera()

        fullCycle = 60
        

        for j in range(fullCycle):
            sjcRef.Drone.droneCount += 1
            nickName = "Drone" + str(sjcRef.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.SpaceStation, nickName, j, fullCycle, 2)
        

        self.DrawCircles(self.Spaceship, axis = 'x', color = (1, 0, 0, 1))
        self.DrawCircles(self.Spaceship, axis = 'y', color = (0, 1, 0, 1))
        self.DrawCircles(self.Spaceship, axis = 'z', color = (0, 0, 1, 1)) 

        self.SetKeyBindings() 
        

        self.UpdateScene()

        

    def UpdateScene(self):
        
        self.cTrav.traverse(self.render)

        return Task.cont

    def SetKeyBindings(self):
        self.accept("space", self.Spaceship.Thrust, [1])
        self.accept("space-up", self.Spaceship.Thrust, [0]) 
        self.accept("a", self.Spaceship.LeftTurn, [1])
        self.accept("a-up", self.Spaceship.LeftTurn, [0])
        self.accept("d", self.Spaceship.RightTurn, [1])
        self.accept("d-up", self.Spaceship.RightTurn, [0])     
        self.accept("w", self.Spaceship.LookUp, [1])
        self.accept("w-up", self.Spaceship.LookUp, [0])     
        self.accept("s", self.Spaceship.LookDown, [1])
        self.accept("s-up", self.Spaceship.LookDown, [0])     
        self.accept("q", self.Spaceship.RollLeft, [1])
        self.accept("q-up", self.Spaceship.RollLeft, [0])     
        self.accept("e", self.Spaceship.RollRight, [1])
        self.accept("e-up", self.Spaceship.RollRight, [0])
        self.accept("f", self.Spaceship.Fire)    

        
    def SetCamera(self):

        self.disable_mouse()

        self.camera.reparentTo(self.Spaceship.modelNode)

        self.camera.setFluidPos(0, 1, 0)


    def DrawCircles(self, centralObject, axis = 'z', radius = 500, count = 12, color = (1, 1, 1, 1)):
            
        for i in range(count):

            centralOffset = dpRef.Circles(radius, axis, i, count)    
            position = centralOffset + centralObject.modelNode.getPos()

            droneName = f"{axis}Drone{i}"

            sjcRef.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.x", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5,  color = color)

        

    def SetupScene(self):
        
        self.Universe = sjcRef.Universe(self.loader,"./Assets/Universe/Universe.x", 
                                        self.render, "Universe", "./Assets/Universe/Universe.jpg", (0, 0, 0), 15000)
        self.Planet1 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", 
                                     self.render, "Planet1", "./Assets/Planets/Marshy_04.png", (-6000, -3000, -800), 250)
        self.Planet2 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", 
                                     self.render, "Planet2", "./Assets/Planets/Gaseous_11.png", (1000, -5000, 500), 350)
        self.Planet3 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", 
                                     self.render, "Planet3", "./Assets/Planets/Martian_01.png", (0, 7000, 0), 500)
        self.Planet4 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", 
                                     self.render, "Planet4", "./Assets/Planets/Dusty_01.png", (8000, 8000, 800), 200)
        self.Planet5 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", 
                                     self.render, "Planet5", "./Assets/Planets/Gaseous_02.png", (4000, -2000, 1000), 450)
        self.Planet6 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", 
                                     self.render, "Planet6", "./Assets/Planets/Snowy_03.png", (300, -3000, -8000), 700)
        self.SpaceStation = sjcRef.SpaceStation(self.loader,"./Assets/SpaceStation/spaceStation.x", 
                                                self.render, "SpaceStation", "./Assets/SpaceStation/SpaceStation1_Dif2.png", (1500, 1000, -100), 40)
        self.Spaceship = pRef.Spaceship(self.render, self.loader, self.taskMgr, self.accept, "./Assets/Spaceship/Dumbledore.x", 
                                        self.render, "Spaceship", "./Assets/Spaceship/spacejet_C.png", Vec3(1000, 3000, -50), 50, self.cTrav)
        self.Spaceship.SetParticles()
        self.Hud = pRef.Spaceship.EnableHUD(self)

        self.Sentinels = []

        for i in range(10):
            drone = sjcRef.Orbiter(self.loader, self.taskMgr, "./Assets/DroneDefender/DroneDefender.x", 
                                self.render, "Drone", 6.0, "./Assets/DroneDefender/octotoad1_auv.png", 
                                self.Planet5, 900, "MLB", self.Spaceship,
                                orbitIndex=i)
            self.Sentinels.append(drone)


        for i in range(20):
            drone = sjcRef.Orbiter(self.loader, self.taskMgr, "./Assets/DroneDefender/DroneDefender.x", 
                                self.render, "Drone", 6.0, "./Assets/DroneDefender/octotoad1_auv.png", 
                                self.Planet2, 500, "Cloud", self.Spaceship,
                                orbitIndex=i)
            self.Sentinels.append(drone)



    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = dpRef.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        sjcRef.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.x", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 5)

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = dpRef.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        sjcRef.Drone(self.loader, "./Assets/DroneDefender/DroneDefender.x", self.render, droneName, "./Assets/DroneDefender/octotoad1_auv.png", position, 10)

app = MyApp()
app.run()
