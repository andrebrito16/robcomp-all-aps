#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

# Arquivos necessários
# Baixe o arquivo em:
# https://github.com/Insper/robot20/blob/master/media/dominoes.mp4
    
video = "dominoes.mp4"


if __name__ == "__main__":

    # Inicializa a aquisição da webcam
    cap = cv2.VideoCapture(video)


    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == False:
            #print("Codigo de retorno FALSO - problema para capturar o frame")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
            #sys.exit(0)

        # Our operations on the frame come here
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Segmenta o branco
        branco_min = np.array([0, 0, 200])
        branco_max = np.array([int(360/2), 50, 255])

        mask_white = cv2.inRange(hsv, branco_min, branco_max)

        # Morph para remover ruídos
        kernel = np.ones((5,5),np.uint8)
        mask_white = cv2.morphologyEx(mask_white, cv2.MORPH_OPEN, kernel)

        # Encontra os dois contornos maiores brancos
        contornos_mask = mask_white.copy()
        contornos, _ = cv2.findContours(contornos_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contornosSorted = sorted(contornos, key=cv2.contourArea, reverse=True)

        domino_numeros = []
        # Pega os dois maiores e crop em duas imagens
        for i in [0, 1]:
            x, y, w, h = cv2.boundingRect(contornosSorted[i])
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # Separa em duas imagens
            crop = contornos_mask[y:y+h, x:x+w]
            # Segmenta o preto no crop
            contornos_preto, _ = cv2.findContours(crop, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            # Filtra por contornos com area > 100
            contornos_filtered = filter(lambda c: cv2.contourArea(c) > 100, contornos_preto)
            # Put number on the image
            domino_numeros.append(len(list(contornos_filtered))-1)

          
            cv2.imshow(f"Parte {i+1}", crop)
        cv2.putText(frame, f"{domino_numeros[1]} x {domino_numeros[0]}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.imshow('imagem', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


