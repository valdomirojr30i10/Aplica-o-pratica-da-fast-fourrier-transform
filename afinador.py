#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 20:20:15 2022

@author: valdomiro, Samuel
"""
import numpy as np
from matplotlib import pyplot as plt

# Mantem as frequencias marginais as que o ukulele possui em cada corda, 
# zerando frequencias desnecessarias
def filtra_audio(F,w,taxa_amostragem):
    n_amostras = len(F)
    # H será um vetor de mesmo tamanho que o vetor as amplitudes filtradas
    # Nele, será atribuido valores que zeram frequencias irrelevantes para este
    # projeto de filtro, de forma similar ao que uma serie de filtros 
    # passa-faixas faria para solucionar esse problema
    H = np.zeros(n_amostras)
    for k in range(n_amostras):
        if(k > 1250) and (k < 1350):
            H[k] = 1.0    
        elif(k > 1600) and (k < 1700):
            H[k] = 1.0    
        elif(k > 1900) and (k < 2000):
            H[k] = 1.0    
        elif(k > 2150) and (k < 2250):
            H[k] = 1.0    
        
        else:
            H[k] = 0.0
    # Nessa etapa, pega-se o valor absoluto do vetor de amplitudes (obtido
    # pela fft) e o divide pelo numero de amostras
    Fabs = 2*np.abs(F)/taxa_amostragem
    
    # É efetuada uma multiplicação entre o vetor H e o vetor Fabs, gerando 
    # a convolução no dominio da frequencia entre H e Fabs 
    Fabs *= H
    
    # Os proximos passos buscam a maior frequencia gravada, a fim de se
    # saber qual a afinação de uma das cordas do ukulele. É efetuada uma
    # varredura entre a menor e maior frequencia proxima da afinação 
    # de cada corda desse instrumento musical
    atual = 0
    pos = 0
    atual = Fabs[1250]
    for k in range(1250,2250):
        if(Fabs[k+1] > atual):
            atual = Fabs[k+1]
            pos = k+1
    
    plt.title('frequencias marginais de cada corda do ukulele')
    plt.axis([250,460,0,5e3])
    plt.plot(w,Fabs)
    return pos

# imprime a frequencia da corda tocada, e informa a afinação esperada, caso
# a corda não esteja afinada!
def afina(w,pos):
    if (w[pos] > 250) and (w[pos] < 270):
        print("Corda em dó [3ª corda]. Afinação atual: ", w[pos]," Hz")
        if(w[pos] > 261) and (w[pos] < 262.5):
            print("corda afinada!")
        else:
            print("afinação esperada: 262 Hz")
    elif (w[pos] > 320) and (w[pos] < 340):
        print("Corda em mi [2ª corda]. Afinação atual: ", w[pos]," Hz")
        if(w[pos] > 329) and (w[pos] < 330.5):
            print("corda afinada!")
        else:
            print("afinação esperada: 330 Hz")
    elif (w[pos] > 280) and (w[pos] < 400):
        print("Corda em Sol [4ª corda]. Afinação atual: ", w[pos]," Hz")
        if(w[pos] > 391) and (w[pos] < 392.5):
            print("corda afinada!")
        else:
            print("afinação esperada: 392 Hz")
    elif (w[pos] > 440) and (w[pos] < 460):
        print("Corda em lá [1ª corda]. Afinação atual: ", w[pos]," Hz")
        if(w[pos] > 439) and (w[pos] < 441.5):
            print("corda afinada!")
        else:
            print("afinação esperada: 440 Hz")
    return

# frames, taxa_amostragem = obter_audio.captura_de_audio()
# sinal, tempo = obter_audio.plot_dominio_tempo(frames, taxa_amostragem)
# F,w = obter_audio.plot_dominio_freq(sinal, taxa_amostragem)
# F_npfft, w_npfft = obter_audio.plot_dominio_freq_npfft(sinal, taxa_amostragem)

# pos = filtra_audio(F, w,taxa_amostragem)
# afina(w, pos)