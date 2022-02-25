import pygame
import os
import neat
from passaro import Passaro
from chao import Chao
from cano import Cano

#Setups iniciais
pygame.font.init()

TELA_ALTURA = 800
TELA_LARGURA = 500

geracao = 0
ai_jogando = False

IMG_FUNDO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))

FONT_TEXTOS = pygame.font.SysFont('arial', 40)

#Desenha tudo o que é necessario na tela
def desenhar_tela(tela,passaros,canos,chao, pontos):
    tela.blit(IMG_FUNDO, (0,0))

    for passaro in passaros:
        passaro.desenhar(tela)

    for cano in canos:
        cano.desenhar(tela)

    pontuacao = FONT_TEXTOS.render(f"Pontuação: {pontos}", 1, (255,255,255))
    tela.blit(pontuacao, (TELA_LARGURA-10-pontuacao.get_width(), 10))

    if ai_jogando:
        geracao = FONT_TEXTOS.render(f"Geração: {geracao}", 1, (255,255,255))
        tela.blit(geracao, (10, 10))

    chao.desenhar(tela)

    pygame.display.update()

#def main(genomas, config):
def main(): 
    global geracao
    geracao += 1

    if ai_jogando:
        redes = []
        lista_genomas = []
        passaros = []

        for _,genoma in genomas:
            redes.append(neat.nn.FeedForwardNetwork.create(genoma, config))
            genoma.fitness = 0
            lista_genomas.append(genoma)
            passaros.append(Passaro(230, 350))

    else:
        passaros = [Passaro(230, 350)]
    
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((TELA_LARGURA,TELA_ALTURA))
    pontos = 0
    relogio = pygame.time.Clock()

    while True:
        relogio.tick(30)

        #Clique de teclas
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN and not ai_jogando:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        indice_cano = 0
        if len(passaros) > 0:
            pass
        else:
            break


        #Movimentos
        for passaro in passaros:
            passaro.mover()
        
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i,passaro in enumerate(passaros):
                if cano.colidir(passaro) or chao.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()

            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)
        
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600))
        
        for cano in remover_canos:
            canos.remove(cano)

        desenhar_tela(tela, passaros, canos, chao, pontos)

if __name__ == '__main__':
    main()