from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.io.wavfile import write
from IPython.display import Audio

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
    
    def reduction_amplifier_pixel(self, is_reduction, fator, imagem=None):
        if imagem is None:
            if self.image is None:
                raise ValueError("Nenhuma imagem fornecida ou carregada.")
            imagem = np.array(self.image)
        else:
            imagem = np.array(imagem)
            
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
        if not local:
            os.makedirs("output", exist_ok=True)
            local = os.path.join("output", "saida.png")

        # Converte a imagem processada para objeto PIL e salva
        img_to_save = Image.fromarray(self.nova_imagem)
        img_to_save.save(local)
        print(f"✅ Imagem salva em: {local}")

