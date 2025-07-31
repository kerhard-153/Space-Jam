from panda3d.core import loadPrcFileData

loadPrcFileData("", """
win-size 1920 1080
fullscreen true
""")
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
from direct.gui.DirectGui import DirectButton, OnscreenImage, DirectCheckButton, DirectLabel, DirectFrame
from direct.gui import DirectGuiGlobals as DGG
from panda3d.core import TransparencyAttrib, TextNode, Vec4

class MyApp(ShowBase):

    def __init__(self):
        
        
        ShowBase.__init__(self)

        self.accept("escape", self.userExit)

        self.allGameObjects = {}

        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
        self.enableParticles()
        self.ShowStartScreen()

        self.droneList = [] 
        
        self.hudDisabled = False
    

        self.UpdateScene()


    def ShowStartScreen(self):

        self.startBackground = OnscreenImage(image="Assets/Universe/Universe.jpg", pos=(0, 0, 0), scale=(2.2, 1, 1))
        self.startBackground.setTransparency(TransparencyAttrib.M_alpha)

        self.titleLabel = DirectLabel(text="SPACE JAM",
                                    scale=0.15,
                                    pos=(0, 0, 0.3),
                                    frameColor=(0, 0, 0, 0),
                                    text_fg=(1, 1, 1, 1),
                                    text_font=self.loader.loadFont("Assets/Fonts/Orbitron-Bold.ttf"),  # match font with buttons
                                    text_shadow=(0, 0, 0, 0.5), 
                                    )

        buttonStyle = {
            "frameColor": (0.2, 0.2, 0.3, 1),
            "frameSize": (-0.3, 0.3, -0.1, 0.1),
            "relief": DGG.RIDGE,
            "borderWidth": (0.02, 0.02),
            "text_scale": 0.07,
            "text_pos": (0, -0.02),
            "text_fg": (1, 1, 1, 1),
            "text_font": self.loader.loadFont("Assets/Fonts/Orbitron-Bold.ttf"),
        }

        self.playButton = DirectButton(text="ENGAGE",
                                    pos=(0, 0, 0.00),
                                    command=self.StartGame,
                                    **buttonStyle)

        self.exitButton = DirectButton(text="ABORT",
                                    pos=(0, 0, -0.20),
                                    command=sys.exit,
                                    **buttonStyle)

        settingsStyle = buttonStyle.copy()
        settingsStyle["frameSize"] = (-0.2, 0.2, -0.07, 0.07)
        settingsStyle["text_scale"] = 0.05

        self.settingsButton = DirectButton(
            text="SETTINGS",
            pos=(1.55, 0, 0.85),
            scale=1.0,
            command=self.OpenSettings,
            **settingsStyle
        )

    def OpenSettings(self):
        print("Settings screen would appear here.")

        self.playButton.hide()
        self.exitButton.hide()
        self.settingsButton.hide()
        self.titleLabel.hide()

        self.settingsLabel = DirectLabel(
            text="SETTINGS",
            scale=0.1,
            pos=(0, 0, 0.4),
            text_fg=(1, 1, 1, 1),
            text_font=self.loader.loadFont("Assets/Fonts/Orbitron-Bold.ttf"),
            frameColor=(0, 0, 0, 0),
        )

        self.hudCheckbox = DirectCheckButton(
            text='',
            scale=0.07,
            pos=(-0.1, 0, 0.1),
            indicatorValue=False,
            command=self.ToggleHUDFromCheckbox,
            relief=None,
            frameColor=(0, 0, 0, 0),
        )

        self.hudLabel = DirectLabel(
            text="Disable HUD",
            scale=0.05,
            pos=(self.hudCheckbox.getX() + 0.05, 0, self.hudCheckbox.getZ() - 0.01), 
            text_fg=(1, 1, 1, 1),
            text_font=self.loader.loadFont("Assets/Fonts/Orbitron-Bold.ttf"),
            text_align=TextNode.ALeft,
            frameColor=(0, 0, 0, 0),
        )

        if hasattr(self, "Spaceship") and self.Spaceship:
            self.Spaceship.EnableHUD(not self.hudCheckbox["indicatorValue"])

        self.backButton = DirectButton(
            text="BACK",
            pos=(0, 0, -0.6),
            command=self.CloseSettings,
            frameColor=(0.2, 0.2, 0.3, 1),
            frameSize=(-0.2, 0.2, -0.07, 0.07),
            borderWidth=(0.02, 0.02),
            text_scale=0.06,
            text_pos=(0, -0.015),
            text_fg=(1, 1, 1, 1),
            text_font=self.loader.loadFont("Assets/Fonts/Orbitron-Bold.ttf")
        )
    def CloseSettings(self):
        self.settingsLabel.destroy()
        self.backButton.destroy()
        self.hudCheckbox.destroy()
        self.hudLabel.destroy()

        self.playButton.show()
        self.exitButton.show()
        self.settingsButton.show()
        self.titleLabel.show()

    def ToggleHUDFromCheckbox(self, isChecked):
        self.hudDisabled = isChecked
        if hasattr(self, "Spaceship") and self.Spaceship:
            self.Spaceship.EnableHUD(not self.hudDisabled)

            
    def StartGame(self):

        self.playButton.destroy()
        self.exitButton.destroy()
        self.startBackground.destroy()
        self.titleLabel.destroy()
        self.settingsButton.destroy()

        self.Universe = sjcRef.Universe(self.loader,"./Assets/Universe/Universe.x", 
                                        self.render, "Universe", "./Assets/Universe/Universe.jpg", (0, 0, 0), 15000)
        self.Planet1 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", 
                                     self.render, "Planet1", "./Assets/Planets/Marshy_04.png", (-6000, -3000, -800), 250, maxHealth=100)
        self.allGameObjects[self.Planet1.modelNode.getName()] = self.Planet1
        self.Planet2 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", 
                                     self.render, "Planet2", "./Assets/Planets/Gaseous_11.png", (1000, -5000, 500), 350, maxHealth=100)
        self.allGameObjects[self.Planet2.modelNode.getName()] = self.Planet2
        self.Planet3 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", 
                                     self.render, "Planet3", "./Assets/Planets/Martian_01.png", (0, 7000, 0), 500, maxHealth=100)
        self.allGameObjects[self.Planet3.modelNode.getName()] = self.Planet3
        self.Planet4 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", 
                                     self.render, "Planet4", "./Assets/Planets/Dusty_01.png", (8000, 8000, 800), 200, maxHealth=100)
        self.allGameObjects[self.Planet4.modelNode.getName()] = self.Planet4
        self.Planet5 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", 
                                     self.render, "Planet5", "./Assets/Planets/Gaseous_02.png", (4000, -2000, 1000), 450, maxHealth=100)
        self.allGameObjects[self.Planet5.modelNode.getName()] = self.Planet5
        self.Planet6 = sjcRef.Planet(self.loader,"./Assets/Planets/protoPlanet.x", 
                                     self.render, "Planet6", "./Assets/Planets/Snowy_03.png", (300, -3000, -8000), 700, maxHealth=100)
        self.allGameObjects[self.Planet6.modelNode.getName()] = self.Planet6
        self.SpaceStation = sjcRef.SpaceStation(self.loader,"./Assets/SpaceStation/spaceStation.x", 
                                                self.render, "SpaceStation", "./Assets/SpaceStation/SpaceStation1_Dif2.png", (1500, 1000, -100), 40, maxHealth=1000)
        self.allGameObjects[self.SpaceStation.modelNode.getName()] = self.SpaceStation
        self.Spaceship = pRef.Spaceship(self.render, self.loader, self, self.taskMgr, self.accept, "./Assets/Spaceship/Dumbledore.x", 
                                        self.render, "Spaceship", "./Assets/Spaceship/spacejet_C.png", Vec3(1000, 3000, -50), 50, self.cTrav, maxHealth=100)
        self.Spaceship.modelNode.lookAt(self.SpaceStation.modelNode)
        self.allGameObjects[self.Spaceship.modelNode.getName()] = self.Spaceship

        self.cTrav.traverse(self.render)
        self.pusher.addCollider(self.Spaceship.collisionNode, self.Spaceship.modelNode)
        self.cTrav.addCollider(self.Spaceship.collisionNode, self.pusher)
        # self.cTrav.showCollisions(self.render)

        self.Sentinels = []

        for i in range(10):
            droneName = f"Drone{i}"
            drone = sjcRef.Orbiter(self.loader, self.taskMgr, "./Assets/DroneDefender/single_donut.egg", 
                                self.render, droneName, 10.0, "./Assets/DroneDefender/donut_texture.png",
                                self.Planet5, 900, "MLB", self.Spaceship, 50, 
                                orbitIndex=i)
            self.Sentinels.append(drone)


        for i in range(20):
            droneName = f"Drone{i}"
            drone = sjcRef.Orbiter(self.loader, self.taskMgr, "./Assets/DroneDefender/single_donut.egg", 
                                self.render, droneName, 10.0, "./Assets/DroneDefender/donut_texture.png",
                                self.Planet2, 500, "Cloud", self.Spaceship, 50,
                                orbitIndex=i)
            self.Sentinels.append(drone)

        route1 = [Vec3(300, 6000, 500), Vec3(700, -2000, 100), Vec3(0, -900, -1400)]
        route2 = [Vec3(1000, 2000, 300), Vec3(-1000, -1500, 600), Vec3(0, 0, 0)]

        self.Wanderer1 = sjcRef.Wanderer(self.loader, "./Assets/DroneDefender/single_donut.egg", self.render, "drone", 6.0, "./Assets/DroneDefender/donut_texture.png", self.Spaceship, route1, 50)

        self.Wanderer2 = sjcRef.Wanderer(self.loader, "./Assets/DroneDefender/single_donut.egg", self.render, "drone", 6.0, "./Assets/DroneDefender/donut_texture.png", self.Spaceship, route2, 50)
        
        self.SetCamera()

        self.SetKeyBindings()

        if hasattr(self, "hudDisabled") and self.hudDisabled:
            self.Spaceship.EnableHUD(False)
        else:
            self.Spaceship.EnableHUD(True)

        fullCycle = 60
        

        for j in range(fullCycle):
            sjcRef.Drone.droneCount += 1
            nickName = "Drone" + str(sjcRef.Drone.droneCount)

            self.DrawCloudDefense(self.Planet1, nickName)
            self.DrawBaseballSeams(self.SpaceStation, nickName, j, fullCycle, 2)
        

        self.DrawCircles(self.Spaceship, axis = 'x', color = (1, 0, 0, 1))
        self.DrawCircles(self.Spaceship, axis = 'y', color = (0, 1, 0, 1))
        self.DrawCircles(self.Spaceship, axis = 'z', color = (0, 0, 1, 1)) 

    def ExitGame(self):
        from sys import exit
        exit()

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
        self.accept("shift", self.Spaceship.ActivateBoost) 
        self.accept("g", self.Spaceship.FireHeavyMisile)   

        
    def SetCamera(self):

        self.disable_mouse()

        self.camera.reparentTo(self.Spaceship.modelNode)

        self.camera.setFluidPos(0, 1, 0)


    def DrawCircles(self, centralObject, axis = 'z', radius = 500, count = 12, color = (1, 1, 1, 1)):
            
        for i in range(count):

            centralOffset = dpRef.Circles(radius, axis, i, count)    
            position = centralOffset + centralObject.modelNode.getPos()

            droneName = f"{axis}Drone{i}"

            sjcRef.Drone(self.loader, "./Assets/DroneDefender/single_donut.egg", self.render, droneName,"./Assets/DroneDefender/donut_texture.png", position, 20,  50, color = color)
            

    def DrawBaseballSeams(self, centralObject, droneName, step, numSeams, radius = 1):
        unitVec = dpRef.BaseballSeams(step, numSeams, B = 0.4)
        unitVec.normalize()
        position = unitVec * radius * 250 + centralObject.modelNode.getPos()
        drone = sjcRef.Drone(self.loader, "./Assets/DroneDefender/single_donut.egg", self.render, droneName, "./Assets/DroneDefender/donut_texture.png", position, 10, maxHealth=50)
        self.droneList.append(drone)
        self.allGameObjects[drone.modelNode.getName()] = drone

    def DrawCloudDefense(self, centralObject, droneName):
        unitVec = dpRef.Cloud()
        unitVec.normalize()
        position = unitVec * 500 + centralObject.modelNode.getPos()
        drone = sjcRef.Drone(self.loader, "./Assets/DroneDefender/single_donut.egg", self.render, droneName, "./Assets/DroneDefender/donut_texture.png", position, 10, maxHealth=50)
        self.droneList.append(drone)
        self.allGameObjects[drone.modelNode.getName()] = drone

app = MyApp()
app.run()
