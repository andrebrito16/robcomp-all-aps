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


def antartida(bgr): 
    """Não mude ou renomeie esta função
        deve receber uma imagem bgr e devolver o recorte da imagem da antartida
    """
    res = bgr.copy()
    rgb = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)

    cores_r, cores_g, cores_b = cv2.split(rgb)
    mask_blue = np.where((cores_r < 200) & (cores_g < 200) & (cores_b > 50))

    min_x_blue = np.min(mask_blue[1])
    min_y_blue = np.min(mask_blue[0])

    max_x_blue = np.max(mask_blue[1])
    max_y_blue = np.max(mask_blue[0])

    img_crop = rgb[min_y_blue:max_y_blue, min_x_blue:max_x_blue]
    img_crop_rgb = cv2.cvtColor(img_crop, cv2.COLOR_RGB2BGR)
    return img_crop_rgb

def canada(bgr): 
    """Não mude ou renomeie esta função
        deve receber uma imagem bgr e devolver o recorte da imagem do canadá
    """
    res = bgr.copy()
    rgb = cv2.cvtColor(res, cv2.COLOR_BGR2RGB)

    cores_r, cores_g, cores_b = cv2.split(rgb)

    mask_red = np.where((cores_r > 200) & (cores_g < 200) & (cores_b < 200))

    min_x_red = np.min(mask_red[1])
    min_y_red = np.min(mask_red[0])

    max_x_red = np.max(mask_red[1])
    max_y_red = np.max(mask_red[0])

    img_crop = rgb[min_y_red:max_y_red, min_x_red:max_x_red]
    img_crop_rgb = cv2.cvtColor(img_crop, cv2.COLOR_RGB2BGR)
    return img_crop_rgb

if __name__ == "__main__":
    img = cv2.imread("ant_canada_250_160.png")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Faz o processamento
    antartida = antartida(img)
    canada = canada(img)
    cv2.imwrite( "ex4_antartida_resp.png", antartida)
    cv2.imwrite("ex5_canada_resp.png", canada)


    # NOTE que a OpenCV terminal trabalha com BGR
    cv2.imshow('entrada', img)

    cv2.imshow('antartida', antartida)
    cv2.imshow('canada', canada)

    cv2.waitKey()
    cv2.destroyAllWindows()


