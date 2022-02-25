import pygame
import os

IMG_CHAO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))

class Chao:
    
    VELOCIDADE = 5
    LARGURA = IMG_CHAO.get_width()
    IMG = IMG_CHAO

    def __init__(self, y):
        self.y = y
        self.x0 = 0
        self.x1 = self.LARGURA

    def mover(self):
        self.x0 -= self.VELOCIDADE
        self.x1 -= self.VELOCIDADE

        if self.x0 + self.LARGURA < 0:
            self.x0 = self.x1 + self.LARGURA
        
        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x0 + self.LARGURA

    def desenhar(self,tela):
        tela.blit(self.IMG, (self.x0,self.y))
        tela.blit(self.IMG, (self.x1,self.y))
