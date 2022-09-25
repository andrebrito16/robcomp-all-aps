#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math

def segmenta_linha_branca(bgr):
    """Não mude ou renomeie esta função
        deve receber uma imagem e segmentar as faixas brancas
    """
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    res = np.zeros(bgr.shape[:-1], dtype=np.uint8)
    res[gray > 235] = 255

    return res

def estimar_linha_nas_faixas(img, mask):
    """Não mude ou renomeie esta função
        deve receber uma imagem preta e branca e retorna dois pontos que formen APENAS uma linha em cada faixa. Desenhe cada uma dessas linhas na iamgem.
         formato: [[(x1,y1),(x2,y2)], [(x1,y1),(x2,y2)]]
    """
    lines = cv2.HoughLinesP(mask, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
    # Encontrar a linha da esquerda e da direita
    left_line = None
    right_line = None
    for line in lines:
        x1, y1, x2, y2 = line[0]
        if x1 < img.shape[1]//2:
            left_line = line
        else:
            right_line = line

    # Desenha os pontos a partir das linhas
    cv2.line(img, (left_line[0][0], left_line[0][1]), (left_line[0][2], left_line[0][3]), (255, 0, 255), 2)
    cv2.line(img, (right_line[0][0], right_line[0][1]), (right_line[0][2], right_line[0][3]), (255, 0, 255), 2)

    return [[(left_line)], [(right_line)]]

def calcular_equacao_das_retas(linhas):
    """Não mude ou renomeie esta função
        deve receber dois pontos que estejam em cada uma das
        faixas e retornar as equacões das duas retas, 
        onde y = h + m * x. Formato: [(m1,h1), (m2,h2)]
    """
    m1 = (linhas[0][0][0][3] - linhas[0][0][0][1]) / (linhas[0][0][0][2] - linhas[0][0][0][0])
    h1 = linhas[0][0][0][1] - m1 * linhas[0][0][0][0]


    # # Equacao da reta 2
    m2 = (linhas[1][0][0][3] - linhas[1][0][0][1]) / (linhas[1][0][0][2] - linhas[1][0][0][0])
    h2 = linhas[1][0][0][1] - m2 * linhas[1][0][0][0]      
    return [(m1,h1), (m2,h2)]
    
def calcular_ponto_de_fuga(img, equacoes):
    """Não mude ou renomeie esta função
        deve receber duas equacoes de retas e retornar o ponto de encontro entre elas. Desenhe esse ponto na imagem.
    """
    m1 = equacoes[0][0]
    h1 = equacoes[0][1]

    m2 = equacoes[1][0]
    h2 = equacoes[1][1]

    x = (h2 - h1) / (m1 - m2)
    y = m1 * x + h1

    cv2.circle(img, (int(x), int(y)), 5, (255, 0, 0), -1)
    ponto_de_fuga = (int(x), int(y))
    return img.copy(), ponto_de_fuga

        
