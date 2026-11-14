import sys
import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados
from recursos.trabalho import (
    desenhar_texto_centralizado,
    formatar_maior_pontuador,
    pedir_nome,
    como_jogar,
    dead,
)

limpar_tela()
inicializarBancoDeDados()
pygame.init()
        
tamanho = (1000,700)
pygame.display.set_caption("Apollo12 - Pensamento Computacional")
icone  = pygame.image.load("bases/icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
branco = (255, 255, 255)
preto = (0, 0, 0)

fundo = pygame.image.load("bases/background.jpg")
fundoDead = pygame.image.load("bases/backgroundDead.jpg")
fundoStart = pygame.image.load("bases/backgroundStart.jpg")

astronauta = pygame.image.load("bases/astronauta.png")
astronauta = pygame.transform.scale(astronauta, (66,122))
asteroide = pygame.image.load("bases/asteroide.png")
asteroide = pygame.transform.scale(asteroide, (98,72))
asteroideSound = pygame.mixer.Sound("bases/asteroideSound.mp3")
explosaoSound = pygame.mixer.Sound("bases/impacto.mp3")
pygame.mixer.music.load("bases/spaceSound.mp3")
fonteMenu = pygame.font.Font("bases/HomeVideo-Regular.otf", 18)
fonteTitulo = pygame.font.Font("bases/HomeVideo-Regular.otf", 26)
nome = ""

def jogar():
    fundoMov1 = 0
    fundoMov2 = 1000
    posicaoXPersona = 0
    posicaoYPersona = 60
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    velocidadeMovPersona = 5
    posicaoXAsteroide = 800
    posicaoYAsteroide = 100
    velocidadeAsteroide = 2
    pontos = 0
    pygame.mixer.Sound.play(asteroideSound)
    pygame.mixer.music.play(-1)
    dificuldade = 20
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
                movimentoXPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP:
                movimentoYPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN:
                movimentoYPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0
                
        
        posicaoXPersona = posicaoXPersona + movimentoXPersona          
        posicaoYPersona = posicaoYPersona + movimentoYPersona            
        if posicaoXPersona < 0 :
            posicaoXPersona = 0
        elif posicaoXPersona > 685:
            posicaoXPersona = 685
        if posicaoYPersona < 0 :
            posicaoYPersona = 0
        elif posicaoYPersona > 150:
            posicaoYPersona = 150
            
            
        posicaoXAsteroide = posicaoXAsteroide - velocidadeAsteroide
        if posicaoXAsteroide < -125:
            pygame.mixer.Sound.play(asteroideSound)
            posicaoXAsteroide = 800
            pontos = pontos + 1
            velocidadeAsteroide = velocidadeAsteroide + 1
            posicaoYAsteroide = random.randint(0,200)
                            
        tela.fill(branco)
        tela.blit(fundo, (fundoMov1,0) )
        tela.blit(fundo, (fundoMov2,0) )
        fundoMov1 -= 1
        fundoMov2 -= 1
        if fundoMov1 <= -1000:
            fundoMov1 = 1000
        elif fundoMov2 <= -1000:
            fundoMov2 = 1000

        
        tela.blit(astronauta, (posicaoXPersona,posicaoYPersona))
        tela.blit( asteroide, (posicaoXAsteroide, posicaoYAsteroide) )
        desenhar_texto_centralizado(tela, f"Pontos: {pontos}", fonteMenu, branco, tamanho[0] // 2, 650, sombra=True)
            
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+66))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+122))
        pixelsAsteroideX = list(range(posicaoXAsteroide, posicaoXAsteroide + 218))
        pixelsAsteroideY = list(range(posicaoYAsteroide, posicaoYAsteroide + 182))
        if  len( list( set(pixelsAsteroideY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsAsteroideX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                escreverDados(nome, pontos)
                dead(tela, relogio, tamanho, fonteMenu, fundoDead, explosaoSound, jogar, iniciar_jogo)
        
        
        pygame.display.update()
        relogio.tick(60)

def start():
    """Exibe a primeira tela do jogo com o nome do jogador, botão Jogar e o maior pontuador."""
    texto_recorde = formatar_maior_pontuador()
    largura_button_start = 180
    altura_button_start = 48
    centro_x = tamanho[0] // 2
    centro_y_botao = 380

    while True:
        start_button = pygame.Rect(0, 0, largura_button_start, altura_button_start)
        start_button.center = (centro_x, centro_y_botao)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if start_button.collidepoint(evento.pos):
                    largura_button_start = 170
                    altura_button_start = 44
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                largura_button_start = 180
                altura_button_start = 48
                if start_button.collidepoint(evento.pos):
                    jogar()

        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))

        desenhar_texto_centralizado(tela, f"Nome Jogador - {nome}", fonteTitulo, branco, centro_x, centro_y_botao - 60, sombra=True)

        start_button = pygame.Rect(0, 0, largura_button_start, altura_button_start)
        start_button.center = (centro_x, centro_y_botao)
        pygame.draw.rect(tela, branco, start_button, border_radius=15)
        desenhar_texto_centralizado(tela, "Jogar", fonteMenu, preto, start_button.centerx, start_button.centery)

        desenhar_texto_centralizado(tela, texto_recorde, fonteMenu, branco, centro_x, 650, sombra=True)

        pygame.display.update()
        relogio.tick(60)


def iniciar_jogo():
    """Executa o fluxo inicial completo: pedir nome, tela de instruções e tela inicial."""
    global nome
    nome = pedir_nome(tela, relogio, tamanho, fonteMenu, fonteTitulo)
    como_jogar(tela, relogio, tamanho, fonteMenu, fonteTitulo, nome)
    start()


iniciar_jogo()