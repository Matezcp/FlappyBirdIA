import pygame
import os
import neat
from math import sqrt
from passaro import Passaro
from chao import Chao
from cano import Cano

#Setups iniciais
pygame.font.init()

TELA_ALTURA = 800
TELA_LARGURA = 500
VELOCIDADE_MAXIMA_CANO = 12

geracao = 0
ai_jogando = True

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
        geracao_atual = FONT_TEXTOS.render(f"Geração: {geracao}", 1, (255,255,255))
        tela.blit(geracao_atual, (10, 10))

    chao.desenhar(tela)

    pygame.display.update()

def main(genomas, config):
    global geracao
    geracao += 1
    redes = []
    lista_genomas = []
    passaros = []

    if ai_jogando:
        for _,genoma in genomas:
            redes.append(neat.nn.FeedForwardNetwork.create(genoma, config))
            genoma.fitness = 0
            lista_genomas.append(genoma)
            passaros.append(Passaro(230, 350))

    else:
        passaros = [Passaro(230, 350)]
    
    velocidade_cano = 5
    chao = Chao(730)
    canos = [Cano(700,velocidade_cano)]
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
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].CANO_TOPO.get_width()):
                indice_cano = 1
        else:
            break


        #Movimentos
        for i,passaro in enumerate(passaros):
            passaro.mover()
            if ai_jogando:
                #aumentar a fitness dele
                lista_genomas[i].fitness += 0.1
                #Roda a rede
                dist_cima = sqrt(((passaro.x-canos[indice_cano].x)**2 + (passaro.y-canos[indice_cano].altura)**2))
                dist_baixo = sqrt(((passaro.x-canos[indice_cano].x)**2 + (passaro.y-canos[indice_cano].pos_base)**2))
                output = redes[i].activate((passaro.y,dist_cima,dist_baixo))

                if output[0] > 0.5:
                    passaro.pular()

        
        chao.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i,passaro in enumerate(passaros):
                if cano.colidir(passaro) or chao.colidir(passaro):
                    passaros.pop(i)
                    if ai_jogando:
                        #Diminui o fitness dele
                        lista_genomas[i].fitness -= 2
                        lista_genomas.pop(i)
                        redes.pop(i)
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()

            if cano.x + cano.CANO_TOPO.get_width() < 0:
                remover_canos.append(cano)
        
        if adicionar_cano:
            pontos += 1
            canos.append(Cano(600,velocidade_cano))
            if pontos % 5 == 0:
                if velocidade_cano < VELOCIDADE_MAXIMA_CANO:
                    for cano in canos:
                        velocidade_cano += 1
                        cano.increase_velocidade()
            if ai_jogando:
                #Aumenta o fitness dele
                for genoma in lista_genomas:
                    genoma.fitness += 4
        
        for cano in remover_canos:
            canos.remove(cano)

        desenhar_tela(tela, passaros, canos, chao, pontos)

def rodar(config_path):
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())

    if ai_jogando:
        populacao.run(main, 50)
    else:
        main(None,None)

if __name__ == '__main__':
    rodar(os.path.join(os.path.dirname(__file__),'config.txt'))