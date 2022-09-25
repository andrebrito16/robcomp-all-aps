#!/usr/bin/python
# -*- coding: utf-8 -*-

from imp import IMP_HOOK
import cv2
import math
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RANSACRegressor

def segmenta_linha_amarela(bgr):
    """Não mude ou renomeie esta função
        deve receber uma imagem bgr e retornar uma máscara com os segmentos amarelos do centro da pista em branco.
        Utiliza a função cv2.morphologyEx() para limpar ruidos na imagem
    """
    img = bgr.copy()
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    min = (50/2, 50, 50)
    max = (70/2, 255, 255)

    yellow_mask = cv2.inRange(img_hsv, min, max)


    cleaned = cv2.morphologyEx(yellow_mask, cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

    return cleaned

def encontrar_contornos(mask):
    """Não mude ou renomeie esta função
        deve receber uma imagem preta e branca e retornar todos os contornos encontrados
    """
    # Encontra os contornos
    contornos, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


   
    return contornos

def crosshair(img, point, size, color):
    """ Desenha um crosshair centrado no point.
        point deve ser uma tupla (x,y)
        color é uma tupla R,G,B uint8
    """
    x,y = point
    x = int(x)
    y = int(y)
    cv2.line(img,(x - size,y),(x + size,y),color,2)
    cv2.line(img,(x,y - size),(x, y + size),color,2)

def encontrar_centro_dos_contornos(bgr, contornos):
    """Não mude ou renomeie esta função
        deve receber uma lista de contornos e retornar, respectivamente,
        a imagem com uma cruz no centro de cada segmento e o centro de cada. 
        formato: img, x_list, y_list
    """

    img = bgr.copy()

    x_list = []
    y_list = []

    for contorno in contornos:
        # Centro do contorno
        M = cv2.moments(contorno)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        x_list.append(cx)
        y_list.append(cy)

        # Desenha uma cruz 
        crosshair(img, (cx, cy), 8, (0, 0, 255))

    
    return img, x_list, y_list


def desenhar_linha_entre_pontos(bgr, X, Y, color):
    """Não mude ou renomeie esta função
        deve receber uma lista de coordenadas XY, e retornar uma imagem com uma linha entre os centros EM SEQUENCIA do mais proximo.
    """
    img = bgr.copy()
    for i in range(len(X)-1):
        cv2.line(img, (X[i], Y[i]), (X[i+1], Y[i+1]), color, 2)

    return img

def regressao_por_centro(bgr, x_array, y_array):
    """Não mude ou renomeie esta função
        deve receber uma lista de coordenadas XY, e estimar a melhor reta, utilizando o metodo preferir, que passa pelos centros. Retorne a imagem com a reta e os parametros da reta
        
        Dica: cv2.line(img,ponto1,ponto2,color,2) desenha uma linha que passe entre os pontos, mesmo que ponto1 e ponto2 não pertençam a imagem.
    """
    img = bgr.copy()

    try:

        reg = LinearRegression()
        ransac = RANSACRegressor(reg)
        yr = y_array.reshape(-1,1) 
        xr = x_array.reshape(-1,) 

        ransac.fit(yr, xr)
        reg = ransac.estimator_
        
    except:
        reg = LinearRegression()
        xr = x_array.reshape(-1,)
        yr = y_array.reshape(-1, 1)
        reg.fit(yr, xr)        

    coef_angular, coef_linear = reg.coef_, reg.intercept_

    y_min = int(min(y_array))
    y_max = int(max(y_array))

    x_min = int(coef_angular*y_min+coef_linear)
    x_max = int(coef_angular*y_max+coef_linear) 

    cv2.line(img, (x_min, y_min), (x_max, y_max), (255,255,0), thickness=3);    
      
    return img, reg

def calcular_angulo_com_vertical(img, lm):
    """Não mude ou renomeie esta função
        deve receber uma imagem contendo uma reta, 
        além do modelo de reggressão linear e determinar o ângulo da reta 
        com a vertical, em graus, utilizando o método que preferir.
    """
    coef_angular = lm.coef_
    angulo = math.degrees(math.atan(coef_angular))
    return angulo

if __name__ == "__main__":
    print('Este script não deve ser usado diretamente')