import pygame
import os
import random

IMG_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))

class Cano:
    DISTANCIA = 200

    def __init__(self, x):
        self.velocidade = 5
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMG_CANO, False, True)
        self.CANO_BASE = IMG_CANO
        self.passou = False
        self.definir_altura()
    
    def definir_altura(self):
        self.altura = random.randrange(50,450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self,tela):
        tela.blit(self.CANO_TOPO, (self.x,self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x,self.pos_base))

    def colidir(self,passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        colisao_topo = passaro_mask.overlap(topo_mask, distancia_topo)
        colisao_base = passaro_mask.overlap(base_mask, distancia_base)

        return (colisao_topo or colisao_base)