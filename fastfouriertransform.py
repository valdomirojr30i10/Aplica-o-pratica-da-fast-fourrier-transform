#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 12 16:17:37 2022

@author: valdomiro, Samuel
"""

#  implementação do algotirmo de Cooley-Tukey FFT em Python
import numpy as np
import matplotlib.pyplot as plt
# função que cria uma lista 'Y' de valores recebidos por um vetor 'y' e aplica
# a transformada rapida de fourrier pelo algoritmo de Cooley-Tukey 
def fft(y):
    Y = list()
    for i in range(len(y)):
	    Y.append(complex(y[i], 0))
    Y = fft_recursiva(Y)
    return Y


# função análoga a função 'fft', calcula a transformada inversa de fourrier 
# pelo algoritmo de Cooley-Tukey 
def ifft(y):
    Y = list()
    for i in range(len(y)):
	    Y.append(complex(y[i], 0))
    Y = ifft_recursiva(Y)
    return Y

def fft_recursiva(y):
    N = len(y)
    
    # Termo utilizado como condição de parada da recursão.
    # Quando o tamanho do vetor recebido foi 1 ou menor, a recursão para
    # e os valores calculados pelo laço de repetição a seguir são retornados
    if(N > 1):
        # Divide o vetor y em um vetor par e outro vetor impar
        par = np.array( y[0:N:2])
        impar = np.array( y[1:N:2])
        # Efetua chamada recursiva da função para cada parte do vetor dividido 
        fft_recursiva(par)
        fft_recursiva(impar)
        w = (np.exp(complex(0,2*np.pi*(1/N))))
        for i in range(0,N//2):
            y[i] = par[i] + (w**i)*impar[i]
            y[N//2 + i] = par[i] - (w**i)*impar[i]
    return y

# Transformada inversa recursiva
def ifft_recursiva(y):
    N = len(y)
    
    # Termo utilizado como condição de parada da recursão.
    # Quando o tamanho do vetor recebido foi 1 ou menor, a recursão para
    # e os valores calculados pelo laço de repetição a seguir são retornados
    if(N > 1):
        # Divide o vetor y em um vetor par e outro vetor impar
        par = np.array( y[0:N:2])
        impar = np.array( y[1:N:2])
        # Efetua chamada recursiva da função para cada parte do vetor dividido 
        ifft_recursiva(par)
        ifft_recursiva(impar)
        # Apenas este termo é modificado com relação a fft_recursiva
        w = ((1/N)*np.exp(complex(0,-2*np.pi*(1/N))))
        for i in range(0,N//2):
            y[i] = par[i] + (w**i)*impar[i]
            y[N//2 + i] = par[i] - (w**i)*impar[i]
    return y

# exemplo que utiliza e valida a transformada rapida de fourier implementada 
# nesse arquivo
def exemplo(N):
    taxa_amostragem = 16
    T1 = 8
    T2 = 16
    y = np.zeros(N)
    for i in range(N):
        y[i] = 5*np.sin(((2*np.pi*i)/T1))
        y[i] += 8*np.sin(((2*np.pi*i)/T2))
    plt.title("Sinal no dominio do tempo")
    plt.plot(y)
    plt.show()
    
    Y = fft(y)
    amplitude_total = np.abs(np.divide(Y, N//2))
    amplitude = amplitude_total[0:N//2]
    w = np.divide(np.multiply(taxa_amostragem/16, np.arange(0,N/2)), N)
    plt.title("Sinal no dominio da frequencia (autoria propria)")
    plt.axis([0,0.2,0,8])
    plt.plot(w, amplitude)
    plt.show()

# exemplo que utiliza a transformada rapida de fourier disponivel na biblioteca
# numpy. Função abaixo foi criada a fim de se comparar o algoritmo implementado
# com o algoritmo disponivel na biblioteca numpy. 
def npfft(N):
    T1 = 8
    T2 = 16
    y = np.zeros(N)
    for i in range(N):
        y[i] = 5*np.sin(((2*np.pi*i)/T1))# f = 0.125Hz
        y[i] += 8*np.sin(((2*np.pi*i)/T2))#f = 0.0625Hz
    plt.title("Sinal no dominio do tempo")
    plt.plot(y)
    plt.show()
    F = np.fft.fft(y)
    w = np.fft.fftfreq(len(y))
    plt.title("Sinal no dominio da frequencia (disponivel em np.fft)")
    plt.plot(w, np.abs(F)/(N//2))
    plt.axis([0,0.2,0,8])
    plt.show()
    return

# print(" nossa fft:")
# exemplo(128)
# print("\n\n numpy fft:")
# npfft(128)