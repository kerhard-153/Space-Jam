from panda3d.core import PandaNode, Loader, NodePath, CollisionNode, CollisionSphere, CollisionInvSphere, CollisionCapsule, Vec3
from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import Filename, NodePath
from direct.task import Task

class PlacedObject(PandaNode):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,):

        self.modelNode: NodePath = loader.loadModel(modelPath)

        if not isinstance(self.modelNode, NodePath):
            raise AssertionError("PlacedObject loader.loadModel(" + modelPath + ") did not return a proper PandaNode!")
        
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setName(nodeName)

class CollidableObject(PlacedObject):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, maxHealth: int = 100):
        super(CollidableObject,self).__init__(loader, modelPath, parentNode, nodeName)

        self.maxHealth = maxHealth
        self.health = maxHealth
        self.alive = True

        self.collisionNode = self.modelNode.attachNewNode(CollisionNode(nodeName + '_cNode'))
        self.collisionNode.setPythonTag("object", self)

    def Explode(self, render, taskMgr, hitPosition):

        self.cntExplode = str(getattr(self, 'cntExplode', 0) + 1)
        tag = "explosion-" + self.cntExplode

        explodeEffect = ParticleEffect()
        explodeEffect.loadConfig(Filename.fromOsSpecific(
            'C:/Users/kmerh/OneDrive/Desktop/Space Jam/Projects/Assets/ParticleEffects/explosion3.ptf'
        ))
        explodeEffect.setScale(70)

        explosionNode = render.attachNewNode("ExplosionEffect" + tag)
        explosionNode.setPos(hitPosition)
        explosionNode.setTransparency(True)

        explodeEffect.start(parent=explosionNode, renderParent=render)

        def cleanup(task):
            explodeEffect.cleanup()
            explosionNode.removeNode()
            return Task.done

        taskMgr.doMethodLater(2.0, cleanup, 'explosion-cleanup' + tag)

    def TakeDamage(self, amount: int, render, taskMgr, hitPosition):
        if not self.alive:
            return
        self.health -= amount
        print(f"[{self.modelNode.getName()}] took {amount} damage. Health now: {self.health}")
        if self.health <= 0:
            print(f"[{self.modelNode.getName()}] died.")
            self.alive = False
            self.Explode(render, taskMgr, hitPosition)
            self.modelNode.detachNode()
            

class InverseSphereCollideObject(CollidableObject):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, colPositionVec: Vec3, colRadius: float):
        super(InverseSphereCollideObject, self).__init__(loader, modelPath, parentNode, nodeName)
        self.collisionNode.node().addSolid(CollisionInvSphere(colPositionVec, colRadius))

class SphereCollideObject(CollidableObject):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, colPositionVec: Vec3, colRadius: float, maxHealth=100):
        super(SphereCollideObject, self).__init__(loader, modelPath, parentNode, nodeName, maxHealth=maxHealth)
        self.collisionNode.node().addSolid(CollisionSphere(colPositionVec, colRadius))
        

class CapsuleCollidableObject(CollidableObject):

    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str, ax: float, ay: float, az: float, bx: float, by: float, bz: float, r: float, maxHealth=100):

        super(CapsuleCollidableObject, self).__init__(loader, modelPath, parentNode, nodeName, maxHealth=maxHealth)

        self.collisionNode.node().addSolid(CollisionCapsule(ax, ay, az, bx, by, bz, r))
        