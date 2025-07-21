from panda3d.core import PandaNode, Loader, NodePath, CollisionNode, CollisionSphere, CollisionInvSphere, CollisionCapsule, Vec3

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

    def TakeDamage(self, amount: int):
        if not self.alive:
            return
        self.health -= amount
        print(f"[{self.modelNode.getName()}] took {amount} damage. Health now: {self.health}")
        if self.health <= 0:
            self.Die()

    def Die(self):
        print(f"[{self.modelNode.getName()}] died.")
        self.alive = False
        self.modelNode.removeNode()

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
        