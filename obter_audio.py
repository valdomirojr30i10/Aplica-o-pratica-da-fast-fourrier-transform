#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 22:28:53 2022

@author: valdomiro, Samuel
"""

import wave
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import fastfouriertransform as myfft

# Função que efetua a captação de audio pelo microfone do notebook, grava por
# tempo especificado, gera um arquivo de audio no formato 'wav' e gera uma lista
# com todos os frames obtidos da captação.
def captura_de_audio(taxa_amostragem):
    # formato de amostras coletadas
    formato = pyaudio.paInt16
    
    bloco_amostras = 1024
    # Atribui o tempo em segundos para a gravação do audio
    tempo_gravacao = 5
    duracao_gravacao = int((taxa_amostragem/bloco_amostras) * (tempo_gravacao))
        
    audio = pyaudio.PyAudio()
    streamMic = audio.open(format = formato, channels = 1, rate = taxa_amostragem, input = True, frames_per_buffer = bloco_amostras)
    
    # obtendo dados do audio ambiente pelo microfone a seguir:
    # cria lista que receberá as amostras coletadas
    frames_obtidos = []
    print("Gravando por: ", tempo_gravacao, "s")
    
    # os frames do audio são obtidos por blocos de 1024 amostras cada e após a
    # obtenção destes frames, é efetuada uma concatenação de todas as amostras
    # para um unico bloco
    for i in range(duracao_gravacao):
        dadosMic = streamMic.read(bloco_amostras)    
        frames_obtidos.append(dadosMic)
    
    streamMic.stop_stream()
    streamMic.close()
    audio.terminate()    
    juntar_frames = b''.join(frames_obtidos)

    #Etapa de salvamento do audio obtido em um arquivo
    arquivoWav = wave.open("out.wav", 'wb')
    arquivoWav.setsampwidth(audio.get_sample_size(formato))
    arquivoWav.setnchannels(1)
    arquivoWav.setframerate(taxa_amostragem)
    arquivoWav.writeframes(juntar_frames)
    arquivoWav.close()
    return juntar_frames

# Gera uma imagem com o sinal capturado pelo microfone, no dominio do tempo
def plot_dominio_tempo(frames, taxa_amostragem):     
    sinal = np.frombuffer(frames, np.int16)
    tempo=np.linspace(0, len(sinal)/taxa_amostragem, num=len(sinal))
    plt.title('Sinal no dominio do tempo')
    plt.plot(tempo,sinal)
    plt.show()   
    return sinal, tempo

    # Gera uma imagem com o sinal capturado pelo microfone, no dominio da
    # frequencia, usando nossa implementação do algoritmo de Cooley-Tukey-FFT
def plot_dominio_freq(sinal, taxa_amostragem):
    # Chama a função que efetua a transformada rapida de fourrier, e retorna
    # um vetor com as amplitudes
    F = myfft.fft(sinal)
    # gera um vetor de frequencias de mesmo tamanho que o vetor das amplitudes.
    w1 = np.linspace(0, (taxa_amostragem), len(sinal))
    # A remover valores negativos da plotagem, é utilizada a função np.abs()
    # no vetor F.
    F1 = 2*np.abs(F)
    # etapa de plotagem da figura
    plt.title('Sinal no dominio da frequencia')
    plt.axis([0,1000,0,5e3])
    plt.plot(w1, F1/(taxa_amostragem))
    plt.show()
    return F,w1

    # Gera uma imagem com o sinal capturado pelo microfone, no dominio da
    # frequencia, utilizando a np.fft.fft(), para efeitos de comparação com
    # o algoritmo implementado
def plot_dominio_freq_npfft(sinal, taxa_amostragem):
    F = np.abs(np.fft.fft(sinal))
    w = np.fft.fftfreq(len(sinal))
    plt.title('Sinal no dominio da frequencia - numpy')
    plt.plot(w*taxa_amostragem,F/(taxa_amostragem//2))
    plt.axis([0,1000,0,5e3])
    # print("len_npfft: ", len(F),len(F/(taxa_amostragem//2)), len(w))
    plt.show()
    return F,w