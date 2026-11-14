import sys
import threading
import pygame
import pyttsx3
from recursos.funcoes import maior_pontuador

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 80, 80)


def desenhar_texto_centralizado(tela, texto, fonte, cor, centro_x, centro_y, sombra=False):
    """Renderiza e centraliza um texto na tela na posição informada."""
    if sombra:
        superficie_sombra = fonte.render(texto, True, PRETO)
        rect_sombra = superficie_sombra.get_rect(center=(centro_x + 2, centro_y + 2))
        tela.blit(superficie_sombra, rect_sombra)

    superficie_texto = fonte.render(texto, True, cor)
    rect_texto = superficie_texto.get_rect(center=(centro_x, centro_y))
    tela.blit(superficie_texto, rect_texto)


def formatar_maior_pontuador():
    """Retorna o texto formatado do maior pontuador com pontos, data e hora."""
    nome_maior, maior_pontos, dataJogada, horaJogada = maior_pontuador()
    if nome_maior is None:
        return "Nenhum recorde registrado ainda"
    if horaJogada:
        return f"Maior Pontuador: {nome_maior} - {maior_pontos} pts - {dataJogada} as {horaJogada}"
    return f"Maior Pontuador: {nome_maior} - {maior_pontos} pts - {dataJogada}"


def quebrar_texto_em_linhas(texto, fonte, largura_max):
    """Quebra o texto em linhas respeitando parágrafos e a largura máxima em pixels."""
    linhas = []
    for paragrafo in texto.splitlines():
        palavras = paragrafo.split()
        if not palavras:
            linhas.append("")
            continue

        linha_atual = palavras[0]
        for palavra in palavras[1:]:
            teste = f"{linha_atual} {palavra}"
            if fonte.size(teste)[0] <= largura_max:
                linha_atual = teste
            else:
                linhas.append(linha_atual)
                linha_atual = palavra
        linhas.append(linha_atual)
    return linhas


def falar_boas_vindas(nome_jogador):
    """Fala a mensagem de boas-vindas em PT-BR em uma thread separada."""
    mensagem = f"Seja bem-vindo Astronauta {nome_jogador} a Apollo 12"

    def _executar_fala():
        try:
            motor = pyttsx3.init()
            for voz in motor.getProperty("voices"):
                idiomas = " ".join(str(lang) for lang in (voz.languages or []))
                descricao = f"{voz.id} {voz.name} {idiomas}".lower()
                if (
                    "pt-br" in descricao
                    or "pt_br" in descricao
                    or "brazil" in descricao
                    or "portuguese" in descricao
                    or "portugu" in descricao
                    or "maria" in descricao
                ):
                    motor.setProperty("voice", voz.id)
                    break
            motor.say(mensagem)
            motor.runAndWait()
        except Exception as erro:
            print(f"Erro ao sintetizar voz: {erro}")

    threading.Thread(target=_executar_fala, daemon=True).start()


def pedir_nome(tela, relogio, tamanho, fonteMenu, fonteTitulo):
    """Exibe uma tela preta centralizada para o jogador digitar seu nome e confirmar em OK."""
    texto_digitado = ""
    erro = False
    largura_button_ok = 120
    altura_button_ok = 42
    centro_x = tamanho[0] // 2
    centro_y = tamanho[1] // 2

    caixa_rect = pygame.Rect(0, 0, 360, 48)
    caixa_rect.center = (centro_x, centro_y - 10)

    while True:
        ok_button = pygame.Rect(0, 0, largura_button_ok, altura_button_ok)
        ok_button.center = (centro_x, centro_y + 65)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if len(texto_digitado.strip()) > 0:
                        return texto_digitado.strip()
                    erro = True
                elif evento.key == pygame.K_BACKSPACE:
                    texto_digitado = texto_digitado[:-1]
                    erro = False
                elif evento.unicode and evento.unicode.isprintable() and evento.unicode not in ("\r", "\n", "\t"):
                    if len(texto_digitado) < 20:
                        texto_digitado += evento.unicode
                        erro = False
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if ok_button.collidepoint(evento.pos):
                    largura_button_ok = 112
                    altura_button_ok = 38
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                largura_button_ok = 120
                altura_button_ok = 42
                if ok_button.collidepoint(evento.pos):
                    if len(texto_digitado.strip()) > 0:
                        return texto_digitado.strip()
                    erro = True

        tela.fill(PRETO)
        desenhar_texto_centralizado(tela, "Digite o Nome do Jogador:", fonteTitulo, BRANCO, centro_x, centro_y - 70)

        pygame.draw.rect(tela, BRANCO, caixa_rect, 2, border_radius=8)
        cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else ""
        desenhar_texto_centralizado(tela, texto_digitado + cursor, fonteMenu, BRANCO, caixa_rect.centerx, caixa_rect.centery)

        ok_button = pygame.Rect(0, 0, largura_button_ok, altura_button_ok)
        ok_button.center = (centro_x, centro_y + 65)
        pygame.draw.rect(tela, BRANCO, ok_button, border_radius=15)
        desenhar_texto_centralizado(tela, "OK", fonteMenu, PRETO, ok_button.centerx, ok_button.centery)

        if erro:
            desenhar_texto_centralizado(tela, "Digite um nome válido!", fonteMenu, VERMELHO, centro_x, centro_y + 115)

        pygame.display.update()
        relogio.tick(60)


def como_jogar(tela, relogio, tamanho, fonteMenu, fonteTitulo, nome):
    """Exibe tela preta com boas-vindas em PT-BR, resumo de bases/comoJogar.txt e botão Entendi."""
    with open("bases/comoJogar.txt", "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read().strip()

    falar_boas_vindas(nome)

    centro_x = tamanho[0] // 2
    linhas_titulo = quebrar_texto_em_linhas(f"Seja bem-vindo Astronauta {nome} a Apollo 12", fonteTitulo, 900)
    linhas_texto = quebrar_texto_em_linhas(conteudo, fonteMenu, 860)

    largura_button_entendi = 180
    altura_button_entendi = 48
    centro_y_botao = 565

    espacamento_linha = 32
    altura_bloco = len(linhas_texto) * espacamento_linha
    y_texto_inicial = 355 - altura_bloco // 2

    while True:
        entendi_button = pygame.Rect(0, 0, largura_button_entendi, altura_button_entendi)
        entendi_button.center = (centro_x, centro_y_botao)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if entendi_button.collidepoint(evento.pos):
                    largura_button_entendi = 170
                    altura_button_entendi = 44
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                largura_button_entendi = 180
                altura_button_entendi = 48
                if entendi_button.collidepoint(evento.pos):
                    return

        tela.fill(PRETO)

        for indice, linha_titulo in enumerate(linhas_titulo):
            desenhar_texto_centralizado(tela, linha_titulo, fonteTitulo, BRANCO, centro_x, 95 + indice * 36)

        for indice, linha in enumerate(linhas_texto):
            if linha:
                desenhar_texto_centralizado(tela, linha, fonteMenu, BRANCO, centro_x, y_texto_inicial + indice * espacamento_linha)

        entendi_button = pygame.Rect(0, 0, largura_button_entendi, altura_button_entendi)
        entendi_button.center = (centro_x, centro_y_botao)
        pygame.draw.rect(tela, BRANCO, entendi_button, border_radius=15)
        desenhar_texto_centralizado(tela, "Entendi", fonteMenu, PRETO, entendi_button.centerx, entendi_button.centery)

        pygame.display.update()
        relogio.tick(60)


def dead(tela, relogio, tamanho, fonteMenu, fundoDead, explosaoSound, acao_jogar_novamente, acao_reiniciar):
    """Exibe a tela de fim de jogo com o recorde e opções de Jogar Novamente ou Reiniciar Jogo."""
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    texto_recorde = formatar_maior_pontuador()
    largura_button_novamente = 220
    altura_button_novamente = 44
    largura_button_reiniciar = 220
    altura_button_reiniciar = 44

    while True:
        jogar_novamente_button = pygame.Rect(0, 0, largura_button_novamente, altura_button_novamente)
        jogar_novamente_button.center = (365, 650)
        reiniciar_button = pygame.Rect(0, 0, largura_button_reiniciar, altura_button_reiniciar)
        reiniciar_button.center = (635, 650)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if jogar_novamente_button.collidepoint(evento.pos):
                    largura_button_novamente = 210
                    altura_button_novamente = 40
                if reiniciar_button.collidepoint(evento.pos):
                    largura_button_reiniciar = 210
                    altura_button_reiniciar = 40
            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                largura_button_novamente = 220
                altura_button_novamente = 44
                largura_button_reiniciar = 220
                altura_button_reiniciar = 44
                if jogar_novamente_button.collidepoint(evento.pos):
                    acao_jogar_novamente()
                if reiniciar_button.collidepoint(evento.pos):
                    acao_reiniciar()

        tela.fill(BRANCO)
        tela.blit(fundoDead, (0, 0))

        desenhar_texto_centralizado(tela, texto_recorde, fonteMenu, BRANCO, tamanho[0] // 2, 600, sombra=True)

        jogar_novamente_button = pygame.Rect(0, 0, largura_button_novamente, altura_button_novamente)
        jogar_novamente_button.center = (365, 650)
        pygame.draw.rect(tela, BRANCO, jogar_novamente_button, border_radius=15)
        desenhar_texto_centralizado(tela, "Jogar Novamente", fonteMenu, PRETO, jogar_novamente_button.centerx, jogar_novamente_button.centery)

        reiniciar_button = pygame.Rect(0, 0, largura_button_reiniciar, altura_button_reiniciar)
        reiniciar_button.center = (635, 650)
        pygame.draw.rect(tela, BRANCO, reiniciar_button, border_radius=15)
        desenhar_texto_centralizado(tela, "Reiniciar Jogo", fonteMenu, PRETO, reiniciar_button.centerx, reiniciar_button.centery)

        pygame.display.update()
        relogio.tick(60)
