#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import biblioteca_cow

cap = cv2.VideoCapture('cow_wolf/cow_wolf.mp4')

# Classes da MobileNet
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",\
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]

# Carregar Rede
net = biblioteca_cow.load_mobilenet()

# Detectar
CONFIDENCE = 0.7
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

while(True):
    # Capture frame-by-frame
    ret, img = cap.read()
    
    if ret == False:
        print("Codigo de retorno FALSO - problema para capturar o frame")
        break
    else:
        ## Desenvolva o Codigo Aqui
        saida, resultados = biblioteca_cow.detect(net, img, CONFIDENCE, COLORS, CLASSES)
        saida, animais = biblioteca_cow.separar_caixa_entre_animais(img, resultados)
        biblioteca_cow.checar_perigo(saida, animais)
        cv2.imshow('img',saida)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()