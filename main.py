import sys
import math
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
soloLunar = pygame.image.load("bases/soloLunar.png").convert_alpha()

astronauta = pygame.image.load("bases/astronauta.png")
astronauta = pygame.transform.scale(astronauta, (59, 110))
asteroide = pygame.image.load("bases/asteroide.png")
asteroide = pygame.transform.scale(asteroide, (98,72))
ovni = pygame.image.load("bases/ovni.png").convert_alpha()
ovni = pygame.transform.smoothscale(ovni, (78, 58))
tamanho_base_terra = round(int(tamanho[1] * 0.14) * 1.20) * 3
terra_base = pygame.image.load("bases/terra.png").convert_alpha()
terra_base = pygame.transform.smoothscale(terra_base, (tamanho_base_terra, tamanho_base_terra))
asteroideSound = pygame.mixer.Sound("bases/asteroideSound.mp3")
ovniSound = pygame.mixer.Sound("bases/ovniSound.mp3")
explosaoSound = pygame.mixer.Sound("bases/impacto.mp3")
pygame.mixer.music.load("bases/spaceSound.mp3")
fonteMenu = pygame.font.Font("bases/HomeVideo-Regular.otf", 18)
fonteTitulo = pygame.font.Font("bases/HomeVideo-Regular.otf", 26)
nome = ""

def jogar():
    # Executa o loop principal da partida com propulsor, gravidade lenta e ondas de 1 a 2 asteroides.
    fundoMov1 = 0
    fundoMov2 = 1000
    largura_persona, altura_persona = 59, 110
    largura_asteroide, altura_asteroide = 98, 72

    limite_superior = int(tamanho[1] * 0.10)
    limite_inferior = int(tamanho[1] * 0.90)
    min_y_persona = limite_superior
    max_y_persona = limite_inferior - altura_persona
    min_y_asteroide = limite_superior
    max_y_asteroide = limite_inferior - altura_asteroide

    posicaoXPersona = int(tamanho[0] * 0.10)
    posicaoYPersona = (tamanho[1] - altura_persona) // 2
    velocidadeSubida = 5
    velocidadeQuedaLenta = 2
    velocidadeDescidaRapida = 6

    velocidadeAsteroide = 2
    pontos = 0
    dificuldade = 20
    pausado = False
    angulo_terra = 0.0
    fase_pulso = 0.0
    centro_terra = (tamanho[0] // 2, 455)

    largura_ovni = 78
    intervalo_ovni_frames = 15 * 60
    duracao_ovni_frames = 7 * 60
    velocidade_ovni = (tamanho[0] + largura_ovni) / duracao_ovni_frames
    ovni_ativo = False
    contador_intervalo_ovni = 0
    frames_ovni = 0
    ovni_x = 0.0
    ovni_y_base = 0
    ovni_direcao = 1

    def gerar_onda_asteroides():
        # Gera de 1 a 2 asteroides em posições Y distintas e com atraso mínimo no eixo X.
        quantidade = random.randint(1, 2)
        y1 = random.randint(min_y_asteroide, max_y_asteroide)
        onda = [{"x": tamanho[0], "y": y1, "som_tocado": False}]

        if quantidade == 2:
            candidatos_y = [
                y for y in range(min_y_asteroide, max_y_asteroide + 1)
                if abs(y - y1) >= 100
            ]
            y2 = random.choice(candidatos_y) if candidatos_y else y1
            atraso_x = random.randint(280, 450)
            onda.append({"x": tamanho[0] + atraso_x, "y": y2, "som_tocado": False})

        return onda

    asteroides = gerar_onda_asteroides()
    pygame.mixer.music.play(-1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pausado = not pausado
                if pausado:
                    pygame.mixer.music.pause()
                    pygame.mixer.pause()
                else:
                    pygame.mixer.music.unpause()
                    pygame.mixer.unpause()

        if not pausado:
            teclas = pygame.key.get_pressed()

            if teclas[pygame.K_UP]:
                movimentoYPersona = -velocidadeSubida
            elif teclas[pygame.K_DOWN]:
                movimentoYPersona = velocidadeDescidaRapida
            else:
                movimentoYPersona = velocidadeQuedaLenta

            posicaoYPersona += movimentoYPersona

            if posicaoYPersona < min_y_persona:
                posicaoYPersona = min_y_persona
            elif posicaoYPersona > max_y_persona:
                posicaoYPersona = max_y_persona

            asteroides_restantes = []
            for ast in asteroides:
                ast["x"] -= velocidadeAsteroide
                if not ast["som_tocado"] and ast["x"] <= tamanho[0]:
                    pygame.mixer.Sound.play(asteroideSound)
                    ast["som_tocado"] = True

                if ast["x"] < -largura_asteroide:
                    pontos += 1
                    velocidadeAsteroide += 1
                else:
                    asteroides_restantes.append(ast)

            asteroides = asteroides_restantes
            if not asteroides:
                asteroides = gerar_onda_asteroides()

            fundoMov1 -= 1
            fundoMov2 -= 1
            if fundoMov1 <= -1000:
                fundoMov1 = 1000
            elif fundoMov2 <= -1000:
                fundoMov2 = 1000

            angulo_terra = (angulo_terra - 0.2) % 360
            fase_pulso += 0.025

            if not ovni_ativo:
                contador_intervalo_ovni += 1
                if contador_intervalo_ovni >= intervalo_ovni_frames:
                    ovni_ativo = True
                    frames_ovni = 0
                    ovni_y_base = random.randint(60, 210)
                    ovni_direcao = random.choice((-1, 1))
                    ovni_x = float(-largura_ovni if ovni_direcao == 1 else tamanho[0])
                    pygame.mixer.Sound.play(ovniSound)
            else:
                ovni_x += velocidade_ovni * ovni_direcao
                frames_ovni += 1
                if frames_ovni >= duracao_ovni_frames:
                    ovni_ativo = False
                    ovniSound.stop()
                    contador_intervalo_ovni = 0

        tela.fill(branco)
        tela.blit(fundo, (fundoMov1, 0))
        tela.blit(fundo, (fundoMov2, 0))

        escala_pulso = 1.0 + 0.04 * math.sin(fase_pulso)
        terra_animada = pygame.transform.rotozoom(terra_base, angulo_terra, escala_pulso)
        rect_terra = terra_animada.get_rect(center=centro_terra)
        tela.blit(terra_animada, rect_terra)

        tela.blit(soloLunar, (fundoMov1, 0))
        tela.blit(soloLunar, (fundoMov2, 0))

        if ovni_ativo:
            ovni_y = ovni_y_base + int(8 * math.sin(frames_ovni * 0.08))
            tela.blit(ovni, (int(ovni_x), ovni_y))

        tela.blit(astronauta, (posicaoXPersona, posicaoYPersona))
        for ast in asteroides:
            tela.blit(asteroide, (ast["x"], ast["y"]))

        texto_pontos = f"Pontos: {pontos}"
        largura_caixa = max(170, fonteMenu.size(texto_pontos)[0] + 32)
        caixa_pontos = pygame.Rect(tamanho[0] - largura_caixa - 20, 15, largura_caixa, 40)
        pygame.draw.rect(tela, preto, caixa_pontos, border_radius=10)
        pygame.draw.rect(tela, branco, caixa_pontos, 2, border_radius=10)
        desenhar_texto_centralizado(tela, texto_pontos, fonteMenu, branco, caixa_pontos.centerx, caixa_pontos.centery)

        desenhar_texto_centralizado(tela, "Pressione Space para pausar o jogo", fonteMenu, branco, tamanho[0] // 2, 650, sombra=True)

        if pausado:
            desenhar_texto_centralizado(tela, "JOGO PAUSADO", fonteTitulo, branco, tamanho[0] // 2, tamanho[1] // 2, sombra=True)
        else:
            pixelsPersonaX = set(range(posicaoXPersona, posicaoXPersona + largura_persona))
            pixelsPersonaY = set(range(posicaoYPersona, posicaoYPersona + altura_persona))
            for ast in asteroides:
                pixelsAsteroideX = set(range(int(ast["x"]), int(ast["x"]) + largura_asteroide))
                pixelsAsteroideY = set(range(int(ast["y"]), int(ast["y"]) + altura_asteroide))
                if len(pixelsAsteroideY.intersection(pixelsPersonaY)) > dificuldade:
                    if len(pixelsAsteroideX.intersection(pixelsPersonaX)) > dificuldade:
                        ovniSound.stop()
                        escreverDados(nome, pontos)
                        dead(tela, relogio, tamanho, fonteMenu, fundoDead, explosaoSound, jogar, iniciar_jogo)

        pygame.display.update()
        relogio.tick(60)

def start():
    # Exibe a primeira tela do jogo com o nome do jogador, botão Jogar e o maior pontuador.
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
    # Executa o fluxo inicial completo: pedir nome, tela de instruções e tela inicial.
    global nome
    nome = pedir_nome(tela, relogio, tamanho, fonteMenu, fonteTitulo)
    como_jogar(tela, relogio, tamanho, fonteMenu, fonteTitulo, nome)
    start()


iniciar_jogo()