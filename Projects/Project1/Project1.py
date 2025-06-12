from direct.showbase.ShowBase import ShowBase

class MyApp(ShowBase):

    def __init__(self):
        
        
        ShowBase.__init__(self)

        self.SetupScene()

    def SetupScene(self):
        
        self.Universe = self.loader.loadModel("./Assets/Universe/Universe.x")
        self.Universe.reparentTo(self.render)
        self.Universe.setScale(15000)
        uniTex = self.loader.loadTexture("./Assets/Universe/Universe.jpg")
        self.Universe.setTexture(uniTex, 1)
        
        self.Planet1 = self.loader.loadModel("./Assets/Planets/protoPlanet.x")
        self.Planet1.reparentTo(self.render)
        self.Planet1.setPos(150, 5000, 67)
        self.Planet1.setScale(350)
        moonTex = self.loader.loadTexture("./Assets/Planets/Moon.png")
        self.Planet1.setTexture(moonTex, 1)

app = MyApp()
app.run()
