from Actor import Actor
import pygame

class AI(Actor):
    img:pygame.image.load
    defaultImg:pygame.image.load

    pos:pygame.math.Vector2
    midPos:pygame.math.Vector2
    size:pygame.math.Vector2
    angle:float

    vectRight:pygame.math.Vector2
    forward:pygame.math.Vector2

    destination:pygame.math.Vector2

    aiState:str

    maxSpeed:float
    minSpeed:float

    isMoving:bool

    initialPos:pygame.math.Vector2
    lenghtDest:float

    def __init__(self, tag:str, imagePath:str):
        super().__init__("tag")

        self.aiState = "Seek"

        self.size = pygame.math.Vector2(100, 100)
        self.pos = pygame.math.Vector2(100, 100)
        self.midPos = pygame.math.Vector2(self.pos + (self.size / 2))

        self.angle = 0
        self.vectRight = pygame.math.Vector2(1, 0)
        self.forward = pygame.math.Vector2(1, 0)

        self.defaultImg = pygame.image.load(imagePath)
        self.defaultImg = pygame.transform.scale(self.defaultImg, self.size)
        self.img = self.defaultImg

        self.destination = pygame.math.Vector2(self.midPos)
        self.isMoving = False

        self.maxSpeed = 10
        self.minSpeed = 5

        self.lenghtDest = 0
        self.initialPos = pygame.math.Vector2(self.midPos)

    def SetPos(self, pos:float):
        self.pos = pos

    def SetDestination(self, dest:float):
        self.destination.x = dest[0]
        self.destination.y = dest[1]

        vectDist = self.destination - self.midPos
        self.lenghtDest = vectDist.length()
        self.initialPos = self.midPos

        self.SetRotation()

    def SetRotation(self):
        if (self.destination - self.midPos).length() > 0:
            self.forward = self.destination - self.midPos
            self.forward = self.forward.normalize()

        self.angle = -self.vectRight.angle_to(self.forward)

    def SetState(self, state:str):
        self.aiState = state
        print("current state = " + self.aiState)

    def Seek(self, dt:float):

        velo = self.forward
        self.Move(velo)

    def Flee(self, dt:float):
        pass

    def Wander(self, dt:float):
        pass

    def Move(self, velo:pygame.math.Vector2):
        vectAI = self.midPos - self.initialPos
        lengthAI = vectAI.length()

        if lengthAI >= self.lenghtDest:
            self.isMoving = False
        else:
            self.isMoving = True
        
        if self.isMoving:
            self.pos += velo
            self.midPos = self.pos + (self.size / 2)

    def Render(self, screen):
        if self.img != None:
            img = pygame.transform.rotate(self.defaultImg, self.angle)

            screen.blit(img, self.pos)

            pygame.draw.line(screen, pygame.Color(255, 255, 255), self.midPos, self.destination, 5)

    def Update(self, dt:float):
        match(self.aiState):
            case "Seek":
                self.Seek(dt)
            case "Flee":
                self.Flee(dt)
            case "Wander":
                self.Wander(dt)
