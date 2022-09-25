#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())


def recorta_leopardo(bgr): 
    """Não mude ou renomeie esta função
        deve receber uma imagem bgr e devolver uma nova imagem com tudo em preto e o os pixels da caixa em granco
    """
    res = bgr.copy()
    rgb = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)

    cores_r, cores_g, cores_b = cv2.split(rgb)

    mask_red = np.where((cores_r == 255) & (cores_g < 100) & (cores_b < 100))
    mask_blue = np.where((cores_r == 0) & (cores_g == 0) & (cores_b == 255))

    max_x_red = np.max(mask_red[1])
    max_y_red = np.max(mask_red[0])

    min_x_blue = np.min(mask_blue[1])
    min_y_blue = np.min(mask_blue[0])


    recorte = rgb[min_y_blue:max_y_red, min_x_blue:max_x_red]
    recorte = cv2.cvtColor(recorte, cv2.COLOR_RGB2BGR)

    return recorte


if __name__ == "__main__":
    img = cv2.imread("snowleopard_red_blue_600_400.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Faz o processamento
    saida = recorta_leopardo(img)
    cv2.imwrite("ex3_recorte_leopardo.png", saida)


    # NOTE que a OpenCV terminal trabalha com BGR
    cv2.imshow('entrada', img)

    cv2.imshow('saida', saida)

    cv2.waitKey()
    cv2.destroyAllWindows()

