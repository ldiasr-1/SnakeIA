import random
import pygame
import numpy as np

pygame.init()
pygame.display.set_caption('Snake')
largura, altura = 600, 400
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

preto = (0, 0, 0)
branco = (255, 255, 255)
verde = (0, 255, 0)
vermelho = (255, 0, 0)

tamanho_quadrado = 20
velocidade_jogo = 60


def gerar_comida(pixels):
    while True:
        comida_x = round(random.randrange(0, largura - tamanho_quadrado) / 20.0) * 20.0
        comida_y = round(random.randrange(0, altura - tamanho_quadrado) / 20.0) * 20.0
        if [comida_x, comida_y] not in pixels:
            return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, vermelho, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixels):
    # Verifica se há pelo menos um segmento na cobra
    if pixels:
        # Desenha a cabeça da cobra com uma cor diferente
        pygame.draw.rect(tela, verde, [pixels[0][0], pixels[0][1], tamanho, tamanho])
        
        # Desenha o corpo da cobra com uma cor ligeiramente diferente
        for pixel in pixels[1:]:
            pygame.draw.rect(tela, (0, 200, 0), [pixel[0], pixel[1], tamanho, tamanho])


def desenhar_texto(texto):
    fonte = pygame.font.SysFont("Arial", 25)
    texto_renderizado = fonte.render(texto, True, branco)
    tela.blit(texto_renderizado, [1, 1])

class SnakeGame:
    def __init__(self):
        self.fim_jogo = False
        self.x = largura / 2
        self.y = altura / 2
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.tamanho_cobra = 1
        self.pixels = []
        self.comida_x, self.comida_y = gerar_comida(self.pixels)
        self.steps_since_last_change = 0
        self.max_steps_same_direction = 10
    

    def reset(self):
        self.__init__()
        return self.get_state()
    
    def step(self, action):
        if action == 0:
            self.velocidade_x, self.velocidade_y = -tamanho_quadrado, 0
        elif action == 1:
            self.velocidade_x, self.velocidade_y = tamanho_quadrado, 0
        elif action == 2:
            self.velocidade_x, self.velocidade_y = 0, -tamanho_quadrado
        elif action == 3:
            self.velocidade_x, self.velocidade_y = 0, tamanho_quadrado
        
        self.x += self.velocidade_x
        self.y += self.velocidade_y
        self.pixels.append([self.x, self.y])
        
        if len(self.pixels) > self.tamanho_cobra:
            del self.pixels[0]
        
        reward = 0
        done = False
        
        if self.x < 0 or self.x >= largura or self.y < 0 or self.y >= altura:
            done = True
            reward = -10
        
        for pixel in self.pixels[:-1]:
            if pixel == [self.x, self.y]:
                done = True
                reward = -10
        
        if self.x == self.comida_x and self.y == self.comida_y:
            self.tamanho_cobra += 1
            reward = 10
            self.comida_x, self.comida_y = gerar_comida(self.pixels)
        
        state = self.get_state()
        return state, reward, done
    
    def get_state(self):
        state = [
            self.x,
            self.y,
            self.comida_x,
            self.comida_y,
            self.velocidade_x,
            self.velocidade_y
        ]
        return np.array(state, dtype=np.float32)
    
    def render(self, generation):
        tela.fill(preto)
        desenhar_comida(tamanho_quadrado, self.comida_x, self.comida_y)
        desenhar_cobra(tamanho_quadrado, self.pixels)
        desenhar_texto(f"Geração: {generation}")
        pygame.display.update()
        relogio.tick(velocidade_jogo)
