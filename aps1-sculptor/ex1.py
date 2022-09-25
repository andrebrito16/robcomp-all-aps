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


def equaliza(gray): 
    """Não mude ou renomeie esta função
        deve receber uma imagem e devolver uma imagem nova com o histograma equalizado
    """
    res = gray.copy()
    nova = np.zeros_like(res)

    x1 = res.min()
    x2 = res.max()

    y1 = 0
    y2 = 255
   

    for i in range(res.shape[0]):
        for j in range(res.shape[1]):
            nova[i][j] = y1 + (y2-y1)*((res[i][j]-x1)/(x2-x1))

    
    return nova


if __name__ == "__main__":
    img = cv2.imread("RinTinTin.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Faz o processamento
    saida = equaliza(img)
    cv2.imwrite("saida_ex1.png", saida)


    # NOTE que a OpenCV terminal trabalha com BGR
    cv2.imshow('entrada', img)

    cv2.imshow('saida', saida)

    cv2.waitKey()
    cv2.destroyAllWindows()



    