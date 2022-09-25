#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np
import math
from math import *

def encontrar_foco(D,H,h):
    """Não mude ou renomeie esta função
    Entradas:
       D - distancia real da câmera até o objeto (papel)
       H - a distancia real entre os circulos (no papel)
       h - a distancia na imagem entre os circulos
    Saída:
       f - a distância focal da câmera
    """
    # Calcular o foco 
    # H/D = h/f
    # H = D*h/f

    f = D*(h/H)

    return f

def segmenta_circulo_ciano(hsv): 
    """Não mude ou renomeie esta função
    Entrada:
        hsv - imagem em hsv
    Saída:
        mask - imagem em grayscale com tudo em preto e os pixels do circulos ciano em branco
    """
    mask = hsv[:,:,0]

    menor_ciano = (int(160/2), 50, 50)
    maior_ciano = (int(190/2), 255, 255)
    # menor_ciano = (int(210/2), 100, 80)
    # maior_ciano = (int(270/2), 255, 255)

    mask = cv2.inRange(hsv, np.asarray([int(160/2), 50, 50]), np.asarray([int(190/2), 255, 255]))

    
    return mask

def segmenta_circulo_magenta(hsv):
    """Não mude ou renomeie esta função
    Entrada:
        hsv - imagem em hsv
    Saída:
        mask - imagem em grayscale com tudo em preto e os pixels do circulos magenta em branco
    """



    mask = hsv[:,:,0]
    
    menor_magenta = (int(290/2), 50, 50)
    maior_magenta = (int(320/2), 255, 255)

    # menor_magenta = (int(330/2), 50, 50)
    # maior_magenta = (int(360/2), 255, 255)

    mask = cv2.inRange(hsv, np.asarray([int(290/2), 50, 50]), np.asarray([int(320/2), 255, 255]))
    
    return mask
def encontrar_maior_contorno(segmentado):
    """Não mude ou renomeie esta função
    Entrada:
        segmentado - imagem em preto e branco
    Saída:
        contorno - maior contorno obtido (APENAS este contorno)
    """

    contours, arvore = cv2.findContours(segmentado.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    maior_contorno = None
    maior_area = 0
    for c in contours:
        area = cv2.contourArea(c)
        if area > maior_area:
            maior_area = area
            maior_contorno = c
   
    return maior_contorno

def encontrar_centro_contorno(contorno):
    """Não mude ou renomeie esta função
    Entrada:
        contorno: um contorno (não o array deles)
    Saída:
        (Xcentro, Ycentro) - uma tuple com o centro do contorno (no formato 'int')!!! 
    """ 

    M = cv2.moments(contorno)

    centro_x = int(M['m10']/M['m00'])
    centro_y = int(M['m01']/M['m00'])

    Xcentro = centro_x
    Ycentro = centro_y
    
    return (Xcentro, Ycentro)

def calcular_h(centro_ciano, centro_magenta):
    """Não mude ou renomeie esta função
    Entradas:
        centro_ciano - ponto no formato (X,Y)
        centro_magenta - ponto no formato (X,Y)
    Saída:
        distancia - a distancia Euclidiana entre os pontos de entrada 
    """
    
    centro_ciano_x = centro_ciano[0]
    centro_ciano_y = centro_ciano[1]

    centro_magenta_x = centro_magenta[0]    
    centro_magenta_y = centro_magenta[1]

    distancia = math.sqrt((centro_ciano_x - centro_magenta_x)**2 + (centro_ciano_y - centro_magenta_y)**2)
    return distancia

def encontrar_distancia(f,H,h):
    """Não mude ou renomeie esta função
    Entrada:
        f - a distância focal da câmera
        H - A distância real entre os pontos no papel
        h - a distância entre os pontos na imagem
    Saída:
        D - a distância do papel até câmera
    """
    D = (H*f)/h
    return D

def calcular_distancia_entre_circulos(img):
    """Não mude ou renomeie esta função
    Deve utilizar as funções acima para calcular a distancia entre os circulos a partir da imagem BGR
    Entradas:
        img - uma imagem no formato BGR
    Saídas:
        h - a distância entre os os circulos na imagem
        centro ciano - o centro do círculo ciano no formato (X,Y)
        centro_magenta - o centro do círculo magenta no formato (X,Y)
        img_contornos - a imagem com os contornos desenhados
    """
    img_contornos = img.copy()

    img_contornos_hsv = cv2.cvtColor(img_contornos, cv2.COLOR_BGR2HSV)

    segmentado_ciano = segmenta_circulo_ciano(img_contornos_hsv)
    segmentado_magenta = segmenta_circulo_magenta(img_contornos_hsv)

    maior_contorno_ciano = encontrar_maior_contorno(segmentado_ciano)
    maior_contorno_magenta = encontrar_maior_contorno(segmentado_magenta)

    centro_ciano = encontrar_centro_contorno(maior_contorno_ciano)
    centro_magenta = encontrar_centro_contorno(maior_contorno_magenta)

    h = calcular_h(centro_ciano, centro_magenta)
  
    return h, centro_ciano, centro_magenta, img_contornos

def calcular_angulo_com_horizontal_da_imagem(centro_ciano, centro_magenta):
    """Não mude ou renomeie esta função
        Deve calcular o angulo, em graus, entre o vetor formato com os centros do circulos e a horizontal.
    Entradas:
        centro_ciano - centro do círculo ciano no formato (X,Y)
        centro_magenta - centro do círculo magenta no formato (X,Y)
    Saídas:
        angulo - o ângulo entre os pontos em graus
    """

    # Vetor ciano, magenta
    Vc = (centro_ciano[0]-centro_magenta[0], centro_ciano[1]-centro_magenta[1])

    Vh = (1, 0)

    angulo = degrees(acos((Vc[0]*Vh[0] + Vc[1]*Vh[1])/(sqrt(Vc[0]**2 + Vc[1]**2))*sqrt(Vh[0]**2 + Vh[1]**2)))

    return angulo
