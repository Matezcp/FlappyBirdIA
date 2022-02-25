import pygame
from passaro import Passaro
from chao import Chao
from cano import Cano

pygame.font.init()

TELA_ALTURA = 800
TELA_LARGURA = 500

IMG_FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))

FONT_PONTOS = pygame.font.SysFont('arial', 50)



