#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 17 21:36:19 2022

@author: valdomiro, Samuel
"""
import afinador as af
import obter_audio

taxa_amostragem = 44100 #amostras coletadas por segundo

# obtem todos os frames do audio capturado via microfone e gera um arquivo com
# o audio capturado
frames = obter_audio.captura_de_audio(taxa_amostragem)
# Efetua a plotagem no dominio do tempo e retorna um vetor com os sinais digitais
# provenientes dos frames
sinal, tempo = obter_audio.plot_dominio_tempo(frames, taxa_amostragem)

# Efetua a plotagem no dominio da frequencia do audio que foi capturado
F,w = obter_audio.plot_dominio_freq(sinal, taxa_amostragem)


'''Descomente a função abaixo caso queira comparar a nossa fft com a disponivel
 na biblioteca numpy '''
F_npfft, w_npfft = obter_audio.plot_dominio_freq_npfft(sinal, taxa_amostragem)

# Efetua a anulação de frequencias que não serão utilizadas no afinador. É
# implementado uma passa faixa simples, que zera frequencias que não serão 
# estudadas para a afinação do ukulele
pos = af.filtra_audio(F, w,taxa_amostragem)
# imprime a maior frequencia obtida, informando se o instrumento está afinado
# ou necessita de afinação
af.afina(w, pos)