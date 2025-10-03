from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import re
from moviepy.editor import VideoFileClip, AudioFileClip
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft, fftfreq, fftshift
from scipy.io.wavfile import write
from IPython.display import Audio
from moviepy.editor import AudioFileClip
from pydub import AudioSegment

class ImageResize:

    def __init__(self, path=None):
        self.image = None
        if path:
            self.imageReciever(path)

    def imageReciever(self, local_image):
        if not os.path.exists(local_image):
            raise FileNotFoundError(f"Arquivo não encontrado: {local_image}")
        self.image = Image.open(local_image)
        return self.image
    
    def reduction_amplifier_pixel(is_reduction, self, fator):
        imagem = np.array(self.image)
        H, W = imagem.shape[:2]
        if is_reduction:
            # Reduzindo: nova dimensão = original / fator
            new_H = max(1, H // fator)
            new_W = max(1, W // fator)
        else:
            # Ampliando: nova dimensão = original * fator
            new_H = H * fator
            new_W = W * fator

        # Criando matriz para nova imagem
        if imagem.ndim == 3:  # imagem colorida
            self.nova_imagem = np.zeros((new_H, new_W, imagem.shape[2]), dtype=imagem.dtype)
        else:  # imagem em escala de cinza
            self.nova_imagem = np.zeros((new_H, new_W), dtype=imagem.dtype)

        # Calculando incremento relativo
        delta_H = H / new_H
        delta_W = W / new_W

        # Mapeando cada pixel da nova imagem para o pixel mais próximo da original
        for i in range(new_H):
            for j in range(new_W):
                orig_i = min(round(i * delta_H), H - 1)
                orig_j = min(round(j * delta_W), W - 1)
                self.nova_imagem[i, j] = imagem[orig_i, orig_j]

        return self.nova_imagem

    def save_image(self, local=None):
        if local:
            self.imageReciever(local)
        else:
            local = input('Digite o local do arquivo: ')

