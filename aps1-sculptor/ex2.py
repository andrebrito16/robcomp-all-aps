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


def realca_caixa_vermelha(bgr): 
    """Não mude ou renomeie esta função
        deve receber uma imagem bgr
        e fazer alguma filtragem / seleção de modo a obter uma imagem
        de saída grayscale
        em que somente os pixels da caixa estão brancos e todo o restante está preto
        Dica: Use mais de um canal, por exemplo R e B
    """


    res = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    
    cores_r, cores_g, cores_b = cv2.split(res)

    mask_red = np.zeros_like(cores_r)
    mask_red[cores_r > 200] = 255

    mask_green = np.zeros_like(cores_g)
    mask_green[cores_g < 120] = 255

    mask_blue = np.zeros_like(cores_b)
    mask_blue[cores_b < 150] = 255

    mask = cv2.bitwise_and(mask_blue, mask_green, mask=mask_red)
    mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)

    return mask


    return gray


if __name__ == "__main__":
    img = cv2.imread("cena_canto_sala.jpg")
    
    # Faz o processamento
    saida = realca_caixa_vermelha(img)
    cv2.imwrite( "saida_ex2.png", saida)


    # NOTE que a OpenCV terminal trabalha com BGR
    cv2.imshow('entrada', img)

    cv2.imshow('saida', saida)

    cv2.waitKey()
    cv2.destroyAllWindows()

