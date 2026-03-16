# Importando bibliotecas
import requests
import pygame  # biblioteca de jogos
import random  # biblioteca geradora de números aleatórios
pygame.init()

# Tela
largura, altura = 900, 800  # tamanho da tela
margem_topo = 60
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Snake")

# pontos
pontos = 0

# Cores e Blocos
verde = (0, 255, 0)
# vermelho = (255, 0, 0)
preto = (0, 0, 0)
branco = (255, 255, 255)
laranja = (255, 165, 0)
cinza = (200, 200, 200)
tam = 20

#Carregar as imagens
maca_img = pygame.image.load("assets/maca_vermelha.png")
maca_img = pygame.transform.scale(maca_img,(30, 30))
snake_img = pygame.image.load("assets/cobrinha.png")
snake_img = pygame.transform.scale(snake_img,(30, 30))
fundo_img = pygame.image.load("assets/background.png")
fundo_img = pygame.transform.scale(fundo_img,(largura, altura - margem_topo))
cobra_corpo_img = pygame.image.load("assets/corpo.png")
cobra_corpo_img = pygame.transform.scale(cobra_corpo_img,(30,30))
# Fonte
fonte = pygame.font.SysFont("Arial", 60)
fonte_P = pygame.font.SysFont("Verdana", 25)

# Função Gerar comida
def gerar_comida(snake):
    while True:
        x = random.randrange(0, largura - tam, tam)
        y = random.randrange(margem_topo, altura - tam, tam)
        if (x, y) not in snake:
            return (x, y)
# Função Enviar Pontuação para o servidor
def enviar_pontuacao(nome, pontos):
    try:
        url = "http://localhost:5000/registrar"
        payload = {"nome": nome, "pontos": pontos}
        requests.post(url, json=payload, timeout=2)
        print("Pontuação enviada com sucesso!")
    except:
        print("Servidor de ranking offline.")

#Função Game Over
def game_over():
    tela.fill(preto)
    texto = fonte.render("GAME OVER", True, branco)
    placar_game_over = pygame.font.SysFont("Arial", 30).render(f"Pontuação: {pontos}", True, branco)
    instrucoes = pygame.font.SysFont("Arial", 30).render("Pressione qualquer tecla para sair ou", True, branco)
    placar_final = fonte_P.render("Clique no botão para reiniciar!!", True, branco)
    enviar_pontuacao("Marcos", pontos)
    # Exibir mensagens no centro da tela
    tela.blit(texto, (largura // 2 - texto.get_width() // 2, altura // 2 - 100))
    tela.blit(placar_game_over, (largura // 2 - placar_game_over.get_width() // 2, altura // 2 - 40))
    tela.blit(instrucoes, (largura // 2 - instrucoes.get_width() // 2, altura // 2 + 5))
    tela.blit(placar_final, (largura // 2 - placar_final.get_width() // 2, altura // 2 + 40))

    # Botão (abaixo das mensagens)
    botao_largura, botao_altura = 220, 50
    botao_x = largura // 2 - botao_largura // 2
    botao_y = altura // 2 + 100
    botao_rect = pygame.Rect(botao_x, botao_y, botao_largura, botao_altura)
    pygame.draw.rect(tela, cinza, botao_rect)
    pygame.draw.rect(tela, preto, botao_rect, 2)
    texto_botao = fonte_P.render("Reiniciar o Jogo", True, preto)
    tela.blit(texto_botao, (
        botao_rect.centerx - texto_botao.get_width() // 2,
        botao_rect.centery - texto_botao.get_height() // 2
    ))

    pygame.display.update()

    # Loop de espera
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):
                    esperando = False
            elif evento.type == pygame.KEYDOWN:
                esperando = False


# Posição inicial
snake = [(500, 500)]
dx, dy = tam, 0

# Comida
comida = (random.randrange(0, largura, tam), random.randrange(0, altura, tam))

# Função jogar
def jogar():
    global pontos
    snake = [(500, margem_topo + tam)]
    dx, dy = tam, 0
    comida = gerar_comida(snake)
    pontos = 0
    rodando = True
    clock = pygame.time.Clock()

    while rodando:
        tela.fill(preto)
        tela.blit(fundo_img,(0,margem_topo))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -tam, 0
                elif evento.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = tam, 0
                elif evento.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -tam
                elif evento.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, tam

        # Movimento
        x, y = snake[-1]
        nova_cabeca = (x + dx, y + dy)
        snake.append(nova_cabeca)

        # Se comeu a comida
        if nova_cabeca == comida:
            comida = gerar_comida(snake)
            pontos += 1
        else:
            snake.pop(0)

        # Finalizar o jogo - Se encostar na borda ou nela mesma
        if (x < 0 or x >= largura or y < 0 or y >= altura) or nova_cabeca in snake[:-1]:
            #game_over()  # Aqui chamamos a função game_over
            rodando = False

        # Desenhar a cobra
        for i, part in enumerate(snake):
            #pygame.draw.rect(tela, laranja, (*part, tam, tam))
            if i == len(snake) - 1:
                tela.blit(snake_img,(part[0], part[1]))
            else: 
                tela.blit(cobra_corpo_img,(part[0],part[1]))

        # Desenhar a comida
        #pygame.draw.rect(tela, branco, (*comida, tam, tam))
        tela.blit(maca_img, (comida))

        # Mostrar placar durante o jogo
        placar = fonte_P.render(f"Pontos: {pontos}", True, branco)
        tela.blit(placar, (10, 10))

        pygame.display.update()
        clock.tick(10)

# Loop principal que permite reiniciar o jogo
while True:
    jogar()
    # Depois que `jogar()` termina, exibe tela de Game Over
    game_over()
