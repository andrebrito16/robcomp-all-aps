#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import biblioteca

print("Baixe o arquivo a seguir para funcionar: ")
print("https://github.com/Insper/robot202/raw/master/projeto/centro_massa/video.mp4")

cap = cv2.VideoCapture('yellow.mp4')

while(True):
    # Capture frame-by-frame
    ret, img = cap.read()
    # frame = cv2.imread("frame0000.jpg")
    # ret = True
    
    if ret == False:
        print("Codigo de retorno FALSO - problema para capturar o frame")
        break
    else:
        mask = img.copy()

        # Segmenta linha amarela
        mask = biblioteca.segmenta_linha_amarela(mask)

        # Encontra os contornos
        contornos = biblioteca.encontrar_contornos(mask)

        # Centro de massa
        img, X, Y = biblioteca.encontrar_centro_dos_contornos(img, contornos)

        # Regressão linear
        if X is not None and Y is not None:
        ## Regressão pelo centro
            X = np.array(X)
            Y = np.array(Y)
            try:
                img, lm = biblioteca.regressao_por_centro(img, X,Y)
            except:
                pass
        else: lm = None

        # Angulo
        if lm is not None:
            angulo = biblioteca.calcular_angulo_com_vertical(img, lm)
        else:
            angulo = 0.0
        cv2.putText(img, f"Angulo: {angulo:.2f}", (100,100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,255), 1)

        # Imagem original
        cv2.imshow('img',img)

        # Stop execution if q key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

