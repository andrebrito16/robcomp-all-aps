#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

import cv2
import os,sys, os.path
from cv2 import COLOR_BGR2HSV
import numpy as np
import fotogrametria

# ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-

def calcular_angulo_e_distancia_na_image_da_webcam(img, f):
    """Não mude ou renomeie esta função
        ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-
        deve receber a imagem da camera e retornar uma imagems com os contornos desenhados e os valores da distancia e o angulo.
    """

    H = 14
    try:
        h, centro_ciano, centro_magenta, contornos_img = fotogrametria.calcular_distancia_entre_circulos(img)
        D = fotogrametria.encontrar_distancia(f,H,h)
        angulo = fotogrametria.calcular_angulo_com_horizontal_da_imagem(centro_ciano, centro_magenta)
    except:
        D = 0
        angulo = 0

    return img, D, angulo

def desenhar_na_image_da_webcam(img, distancia, angulo):
    """Não mude ou renomeie esta função
        ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-
        deve receber a imagem da camera e retornar uma imagems com os contornos desenhados e a distancia e o angulo escrito em um canto da imagem.
    """
    img_contornos = img.copy()
    img_bgr = img.copy()
    img_hsv = cv2.cvtColor(img_bgr, COLOR_BGR2HSV)

    # Segmentação do ciano
    ciano_segmentado = fotogrametria.segmenta_circulo_ciano(img_hsv)

    # Segmentação do magenta
    magenta_segmentado = fotogrametria.segmenta_circulo_magenta(img_hsv)

    # Contorno ciano
    contorno_ciano = fotogrametria.encontrar_maior_contorno(ciano_segmentado)

    # Contorno magenta
    contorno_magenta = fotogrametria.encontrar_maior_contorno(magenta_segmentado)

    if contorno_ciano is None or contorno_magenta is None:
        cv2.putText(img, "Nao foi possivel encontrar os circulos", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


    if contorno_ciano is not None and contorno_magenta is not None:
        centro_ciano = fotogrametria.encontrar_centro_contorno(contorno_ciano)
        centro_magenta = fotogrametria.encontrar_centro_contorno(contorno_magenta)
        # Desenha na imagem
        cv2.drawContours(img, [contorno_ciano], -1, (0,255,255), 3)
        cv2.drawContours(img, [contorno_magenta], -1, (0,0,255), 3)

        cv2.line(img, centro_ciano, centro_magenta, (0, 255, 0), thickness=3, lineType=8)

        cv2.putText(img, "Angulo: " + str(angulo), (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
        # Coloca a distancia na tela
        cv2.putText(img, "Distancia: " + str(distancia), (100,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)




    
    return img

if __name__ == "__main__":
    cv2.namedWindow("preview")
    vc = cv2.VideoCapture(0)

    ## -> Mude o Foco <- ##
    f = fotogrametria.encontrar_foco(30, 14, 420)

    if vc.isOpened(): # try to get the first frame
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        img, distancia, angulo = calcular_angulo_e_distancia_na_image_da_webcam(frame, f)
        img = desenhar_na_image_da_webcam(img, distancia, angulo)
        cv2.imshow("preview", img)
        rval, frame = vc.read()
        key = cv2.waitKey(20)
        if key == 27: # exit on ESC
            break

    cv2.destroyWindow("preview")
    vc.release()