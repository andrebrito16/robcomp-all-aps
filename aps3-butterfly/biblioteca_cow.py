#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import math
import os

# Check https://www.fypsolutions.com/opencv-python/ssdlite-mobilenet-object-detection-with-opencv-dnn/

COCO_labels = { 0: 'background',
    1: '"person"', 2: 'bicycle', 3: 'car', 4: 'motorcycle',
    5: 'airplane', 6: 'bus', 7: 'train', 8: 'truck', 9: 'boat',
    10: 'traffic light', 11: 'fire hydrant',12: 'street sign', 13: 'stop sign', 14: 'parking meter',
    15: 'zebra', 16: 'bird', 17: 'cat', 18: 'dog',19: 'horse',20: 'sheep',21: 'cow',22: 'elephant',
    23: 'bear', 24: 'zebra', 25: 'giraffe', 26: 'hat', 27: 'backpack', 28: 'umbrella',29: 'shoe',
    30: 'eye glasses', 31: 'handbag', 32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis',
    36: 'snowboard', 37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',
    41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle', 45: 'plate',
    46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon', 51: 'bowl', 52: 'banana',
    53: 'apple', 54: 'sandwich', 55: 'orange', 56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza',
    60: 'donut', 61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed', 66: 'mirror',
    67: 'dining table', 68: 'window', 69: 'desk', 70: 'toilet', 71: 'door', 72: 'tv', 73: 'laptop',
    74: 'mouse', 75: 'remote', 76: 'keyboard', 78: 'microwave', 79: 'oven', 80: 'toaster', 81: 'sink',
    82: 'refrigerator', 83: 'blender', 84: 'book', 85: 'clock', 86: 'vase', 87: 'scissors',
    88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush', 91: 'hair brush'}

def load_mobilenet():
    """Não mude ou renomeie esta função
        Carrega o modelo e os parametros da MobileNet. 
        Retorna a rede carregada.
    """
    proto = "./mobilenet_detection/MobileNetSSD_deploy.prototxt.txt" # descreve a arquitetura da rede
    model = "./mobilenet_detection/MobileNetSSD_deploy.caffemodel" # contém os pesos da rede em si
    net = cv2.dnn.readNetFromCaffe(proto, model)
    return net


def detect(net, frame, CONFIDENCE, COLORS, CLASSES):
    """
        Recebe - uma imagem colorida BGR
        Devolve: objeto encontrado
    """
    image = frame.copy()
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()

    results = []

    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
        # extract the confidence (i.e., probability) associated with the
        # prediction
        confidence = detections[0, 0, i, 2]

        # filter out weak detections by ensuring the `confidence` is
        # greater than the minimum confidence


        if confidence > CONFIDENCE:
            # extract the index of the class label from the `detections`,
            # then compute the (x, y)-coordinates of the bounding box for
            # the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # display the prediction
            label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
            print("[INFO] {}".format(label))
            cv2.rectangle(image, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

            results.append((CLASSES[idx], confidence*100, (startX, startY),(endX, endY) ))

    # show the output image
    return image, results


def separar_caixa_entre_animais(img, resultados):
    """Não mude ou renomeie esta função
        recebe o resultados da MobileNet e retorna dicionario com duas chaves, 'vaca' e 'lobo'.
        Na chave 'vaca' tem uma lista de cada caixa que existe uma vaca, no formato: [ [min_X, min_Y, max_X, max_Y] , [min_X, min_Y, max_X, max_Y] , ...]. Desenhe um retângulo azul em volta de cada vaca
        Na chave 'lobo' tem uma lista de uma unica caixa que engloba todos os lobos da imagem, no formato: [min_X, min_Y, max_X, max_Y]. Desenhe um retângulo vermelho em volta dos lobos

    """
    img = img.copy()
    animais = {}
    animais['vaca'] = []
    lobos = []

    for resultado in resultados:
        if resultado[0] == "cow":
            minX = resultado[2][0]
            minY = resultado[2][1]
            maxX = resultado[3][0]
            maxY = resultado[3][1]
            animais['vaca'].append([minX, minY, maxX, maxY])
            img = cv2.rectangle(img, (minX, minY), (maxX, maxY), [255, 0, 0], 5)
        
        if resultado[0] == "horse" or resultado[0] == "dog" or resultado[0] == "sheep":
            minX = resultado[2][0]
            minY = resultado[2][1]
            maxX = resultado[3][0]
            maxY = resultado[3][1]
            lobos.append([minX, minY, maxX, maxY])
    
    X_primeiro_lobo = img.shape[1]
    Y_primeiro_lobo = img.shape[0]
    X_ultimo_lobo = 0
    Y_ultimo_lobo = 0
    for lobo in lobos:
        if lobo[0] < X_primeiro_lobo:
            X_primeiro_lobo = lobo[0]
        if lobo[1] < Y_primeiro_lobo:
            Y_primeiro_lobo = lobo[1]
        if lobo[2] > X_ultimo_lobo:
            X_ultimo_lobo = lobo[2]
        if lobo[3] > Y_ultimo_lobo:
            Y_ultimo_lobo = lobo[3]

    img = cv2.rectangle(img, (X_primeiro_lobo, Y_primeiro_lobo), (X_ultimo_lobo, Y_ultimo_lobo), [0, 0, 255], 5)
    animais['lobo'] = [X_primeiro_lobo, Y_primeiro_lobo, X_ultimo_lobo, Y_ultimo_lobo]
    return img, animais

def calcula_iou(boxA, boxB):
    """Não mude ou renomeie esta função
        Calcula o valor do "Intersection over Union" para saber se as caixa se encontram
    """
    	# determine the (x, y)-coordinates of the intersection rectangle
    xA = min(boxA[0], boxB[0])
    yA = min(boxA[1], boxB[1])
    xB = max(boxA[2], boxB[2])
    yB = max(boxA[3], boxB[3])
	# compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
	# compute the area of both the prediction and ground-truth
	# rectangles
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
	# compute the intersection over union by taking the intersection
	# area and dividing it by the sum of prediction + ground-truth
	# areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
	# return the intersection over union value
    return iou

def checar_perigo(image, animais):
    """Não mude ou renomeie esta função
        Recebe as coordenadas das caixas, se a caixa de uma vaca tem intersecção com as do lobo, ela esta em perigo.
        Se estiver em perigo, deve escrever na imagem com a cor vermlha, se não, escreva com a cor azul.
        *Importante*: nesta função, não faça cópia da imagem de entrada!!
        
        Repita para cada vaca na imagem.
    """
    boxLobo = animais['lobo']
    for vaca in animais['vaca']:
            boxVaca = vaca
            iou = calcula_iou(boxLobo, boxVaca)
            if iou > 0.5:
                cv2.putText(image, "EM PERIGO", (vaca[0],vaca[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,0,255), 3)
            else:
                cv2.putText(image, "Nao em perigo", (vaca[0],vaca[1]), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255,0,0), 3)


    return image