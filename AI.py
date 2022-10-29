from sys import flags
from Actor import Actor
import pygame
import random
import math

class AI(Actor):
    img:pygame.image.load
    defaultImg:pygame.image.load

    pos:pygame.math.Vector2
    midPos:pygame.math.Vector2
    size:pygame.math.Vector2
    angle:float

    vectRight:pygame.math.Vector2
    forward:pygame.math.Vector2
    currVelo:pygame.math.Vector2
    initialVelo:pygame.math.Vector2

    destination:pygame.math.Vector2

    aiState:str

    maxSpeed:float
    minSpeed:float

    isMoving:bool

    initialPos:pygame.math.Vector2
    lenghtDest:float

    accelerateAndDecelerateTime:float
    currTime:float
    distDecelerate:float
    distMoveWander:float
    wanderSet:bool

    def __init__(self, tag:str, imagePath:str):
        super().__init__("tag")

        self.aiState = "Seek"

        self.size = pygame.math.Vector2(100, 100)
        self.pos = pygame.math.Vector2(100, 100)
        self.midPos = pygame.math.Vector2(self.pos + (self.size / 2))

        self.angle = 0
        self.vectRight = pygame.math.Vector2(1, 0)
        self.forward = pygame.math.Vector2(1, 0)
        self.currVelo = pygame.math.Vector2()
        self.initialVelo = pygame.math.Vector2()

        self.defaultImg = pygame.image.load(imagePath)
        self.defaultImg = pygame.transform.scale(self.defaultImg, self.size)
        self.img = self.defaultImg

        self.destination = pygame.math.Vector2(self.midPos)
        self.isMoving = False

        self.maxSpeed = 8
        self.minSpeed = 4

        self.lenghtDest = 0
        self.initialPos = pygame.math.Vector2(self.midPos)

        self.accelerateAndDecelerateTime = 0.5
        self.currTime = 0
        self.distDecelerate = 200
        self.distMoveWander = 300
        self.wanderSet = False

    def SetPos(self, pos:float):
        self.pos = pos

    def SetDestination(self, dest:float):
        self.wanderSet = False
        self.destination.x = dest[0]
        self.destination.y = dest[1]

        match(self.aiState):
            case "Seek":
                pass
            case "Flee":
                temp = self.midPos - self.destination
                self.destination = self.midPos + temp
            case "Wander":
                self.wanderSet = True

        #ici je set la longeur du trajet et la position initial
        vectDist = self.destination - self.midPos
        self.lenghtDest = vectDist.length()
        self.initialPos = self.midPos

        self.SetRotation()

    def SetRotation(self):
        #pour eviter un bug car on ne peux pas normalizer un vecteur d'une longueur de 0
        if (self.destination - self.midPos).length() > 0:
            self.forward = self.destination - self.midPos
            self.forward = self.forward.normalize()

        #ici j'inverse l'angle car ca me donne l'angle dans l'autre sens
        self.angle = -self.vectRight.angle_to(self.forward)


    def SetState(self, state:str):
        self.aiState = state
        print("current state = " + self.aiState)

    def ResetCurrVelo(self):
        self.initialVelo = self.forward * self.minSpeed
        self.currVelo = self.initialVelo
        self.currTime = 0

    def Seek(self, dt:float):
        distArrive:float = (self.pos - self.destination).magnitude()

        if distArrive <= self.distDecelerate:
            self.currTime -= dt
            if self.currTime < 0:
                self.currTime = 0
            self.currVelo = self.initialVelo.lerp(self.initialVelo * self.maxSpeed, self.currTime / self.accelerateAndDecelerateTime)
        elif self.currVelo.magnitude() < (self.initialVelo * self.maxSpeed).magnitude():
            self.currTime += dt
            if self.currTime > self.accelerateAndDecelerateTime:
                self.currTime = self.accelerateAndDecelerateTime
            self.currVelo = self.initialVelo.lerp(self.initialVelo * self.maxSpeed, self.currTime / self.accelerateAndDecelerateTime)

        self.Move(self.currVelo)

    def Flee(self, dt:float):
        self.Seek(dt)

    def Wander(self, dt:float):
        if not self.isMoving or self.wanderSet:
            #je fais foi 50 car 1 degree na pas un gros impact
            angle = self.angle + ((random.random() - random.random()) * 50)

            #ici j'inverse l'angle car l'angle ce fais inverser lorsque je prends l'angle selon la
            #destination dans la fonction SetRotation(self):
            angle = -angle

            radAngle = math.radians(angle)
            x = math.cos(radAngle)
            y = math.sin(radAngle)

            vectAngle = pygame.math.Vector2(x, y)

            destination = self.midPos + (vectAngle * self.distMoveWander)

            self.SetDestination(destination)
            self.ResetCurrVelo()

            self.wanderSet = False

        self.Seek(dt)

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
