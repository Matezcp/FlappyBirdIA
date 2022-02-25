import pygame
import os

IMGS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png'))),
]

class Passaro:
    IMGS = IMGS_PASSARO

    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.angulo = 0 
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.img = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        #Calcula o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo

        #Restringe o deslocamento
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2
        
        #Atualiza a posição y e o angulo do passaro
        self.y += deslocamento

        if deslocamento < 0:
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo < 90:
                self.angulo -= self.VELOCIDADE_ROTACAO
    
    def desenhar(self,tela):
        self.contagem_imagem += 1

        #Animação do bater de asas (ordem das imagens)
        if self.TEMPO_ANIMACAO <= 15:
            self.img = self.IMGS[round(self.TEMPO_ANIMACAO/5)%3]
        else:
            self.img = self.IMGS[round(self.TEMPO_ANIMACAO/5)%2]

        #Se tiver caindo não faz animação de bater asas
        if self.angulo <= -80:
            self.img = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO*2

        #Desenha a imagem
        img_rotacionada = pygame.transform.rotate(self.img, self.angulo)
        pos_centro_imagem = self.img.get_rect(topleft=(self.x,self.y)).center
        retangulo = img_rotacionada.get_rect(center=pos_centro_imagem)
        tela.blit(img_rotacionada,retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)