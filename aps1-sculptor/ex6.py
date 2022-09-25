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


def substitui_x_por_branco(gray): 
    """
        Localiza todas as posições em que há um X 3x3 na imagem de entrada e pinta estas posições com tom de cinza 127. 
        Na saída deve ficar um quadrado cinza onde havia X 
    """

    res = gray.copy()
    saida = res.copy()

    brancos = np.where(res == 255)

    # Find X in the image

    for i in range(1, res.shape[0]-1):
        for j in range(1, res.shape[1]-1):
            if res[i,j] == 255 \
                and res[i-1,j-1] == 255 \
                and res[i-1,j] == 0 \
                and res[i-1,j+1] == 255 \
                and res[i,j-1] == 0 \
                and res[i,j+1] == 0 \
                and res[i+1,j-1] == 255 \
                and res[i+1,j] == 0 \
                and res[i+1,j+1] == 255:
                cv2.rectangle(saida, (j-1,i-1), (j+1,i+1), 127, -1)
                    


    return saida



if __name__ == "__main__":
    img = cv2.imread("black_white_dots_cross_80_60.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Faz o processamento
    saida = substitui_x_por_branco(gray)
    cv2.imwrite("ex6_troca_x.png", saida)


    # NOTE que a OpenCV terminal trabalha com BGR
    cv2.imshow('entrada', img)
    cv2.moveWindow('entrada',200,200)
    cv2.imshow('saida', saida)
    cv2.moveWindow('saida',800,200)

    cv2.waitKey()
    cv2.destroyAllWindows()

