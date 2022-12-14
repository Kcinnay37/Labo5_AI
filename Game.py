import pygame
from Engine import Engine
from AI import AI
from Timer import Timer

class Game:
    isRun:bool

    width:int = 1000
    height:int = 800
    size:float = []

    screen:pygame.display.set_mode

    BGColor:int = [2, 0, 102]

    engine:Engine

    timer:Timer

    AI:AI

    def __init__(self):
        self.isRun = True
        self.engine = Engine()
        self.timer = Timer()
        pygame.init()
        self.GameInit()

    def GameInit(self):
        self.size = [self.width, self.height]
        self.screen = pygame.display.set_mode(self.size)

        self.AI = AI("AI", "Image\\Zombi.png")
        self.engine.AddActor(self.AI)

        self.engine.Start()

    def GameLoop(self):
        self.ProcessInput()

        self.timer.Update()
        self.engine.Update(self.timer.GetDeltaTime())

        self.Render()

        return self.isRun

    def ProcessInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRun = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    self.AI.SetDestination(pygame.mouse.get_pos())
                    self.AI.ResetCurrVelo()



    def Render(self):
        self.screen.fill(self.BGColor)

        self.engine.Render(self.screen)

        pygame.display.flip()

    def ChangeMode(self, mode:str):
        self.AI.SetState(mode)
