from direct.showbase.ShowBase import ShowBase
import SpaceJamClasses as sjcRef
import DefensePaths as dpRef
from panda3d.core import Vec3

class MyApp(ShowBase):

    def __init__(self):
        
        
        ShowBase.__init__(self)

        self.SetupScene()


        # fullCycle = 60

        # for j in range(fullCycle):
        #     sjcRef.Drone.droneCount += 1
        #     nickName = "Drone" + str(sjcRef.Drone.droneCount)

        #     self.DrawCloudDefense(self.Planet1, nickName)
        #     self.DrawBaseballSeams(self.SpaceStation, nickName, j, fullCycle, 2)

        

    def SetupScene(self):
        
        self.Universe = sjcRef.Universe(self.loader,"./Assets/Universe/Universe.x", self.render, "Universe", "./Assets/Universe/Universe.jpg", (0, 0, 0), 15000)
        self.Planet1 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", self.render, "Planet1", "./Assets/Planets/Marshy_04.png", (-6000, -3000, -800), 250)
        self.Planet2 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", self.render, "Planet2", "./Assets/Planets/Gaseous_11.png", (1000, -5000, 500), 350)
        self.Planet3 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", self.render, "Planet3", "./Assets/Planets/Martian_01.png", (0, 7000, 0), 500)
        self.Planet4 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", self.render, "Planet4", "./Assets/Planets/Dusty_01.png", (8000, 8000, 800), 200)
        self.Planet5 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", self.render, "Planet5", "./Assets/Planets/Gaseous_02.png", (4000, -2000, 1000), 450)
        self.Planet6 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", self.render, "Planet6", "./Assets/Planets/Snowy_03.png", (300, -3000, -8000), 700)
        self.SpaceStation = sjcRef.SpaceStation(self.loader,"./Assets/SpaceStation/spaceStation.x", self.render, "SpaceStation", "./Assets/SpaceStation/SpaceStation1_Dif2.png", (1500, 1000, -100), 40)
        self.Spaceship = sjcRef.Spaceship(self.loader,"./Assets/Spaceship/Dumbledore.x", self.render, "Spaceship", "./Assets/Spaceship/spacejet_C.png", Vec3(1000, 3000, -50), 50)


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
