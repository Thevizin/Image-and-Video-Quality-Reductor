from PIL import Image
import cv2
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
from image_resize import ImageResize

class VideoReductor:
        
    def __init__(self, path=None):
        self.video = None
        self.output_folder = 'frames'
        self.count_frame = 0
        self.novo_video = None
        self.output_vid='reduct_video.mp4'
        self.resizer = ImageResize()
        if path:
            self.videoReciever(path)

    def videoReciever(self, local_video):
        self.novo_video = cv2.VideoCapture(local_video)
        return self.novo_video
    
    def make_frame(self, output_folder="frames"):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        while(self.novo_video.isOpened()):
            ret, frame = self.novo_video.read()
            if ret:
                # Define o nome do arquivo de saída para cada frame
                frame_filename = os.path.join(output_folder, f"frame_{self.count_frame}.png")
                cv2.imwrite(frame_filename, frame)
                self.count_frame += 1
                if self.count_frame % 10 == 0:
                    print(f"{self.count_frame} frames processados...")
            else:
                break
        self.novo_video.release()
        print("Extração de frames concluída.")

    @staticmethod
    def extrair_numero(filename):
        numeros = re.findall(r'\d+', filename)
        return int(numeros[0]) if numeros else -1
    
    @staticmethod
    def tempo_video(fps, num_frames):
        return num_frames / fps

    def diminuivideo(self, final_frames_path, fps=30, fator=10):
        if not os.path.exists(final_frames_path):
            os.makedirs(final_frames_path)
        count = 0    
        for filename in os.listdir(self.output_folder):
            count += 1
            if filename.endswith(".png"):
                img = cv2.imread(os.path.join(self.output_folder, filename))
                img_reduzida = self.resizer.reduction_amplifier_pixel(is_reduction=True, imagem=img, fator=fator)
                cv2.imwrite(os.path.join(final_frames_path, filename), img_reduzida)
                if count % 10 == 0:
                    print(f"{count} frames processados...")

        # Corrigido: listar arquivos da pasta corretamente
        imagens = [f for f in os.listdir(final_frames_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
        imagens.sort(key=VideoReductor.extrair_numero)

        primeira_imagem = cv2.imread(os.path.join(final_frames_path, imagens[0]))
        altura, largura, canais = primeira_imagem.shape

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # para .mp4
        video = cv2.VideoWriter(self.output_vid, fourcc, fps, (largura, altura))

        for img_nome in imagens:
            img_path = os.path.join(final_frames_path, img_nome)  # usar final_frames_path
            frame = cv2.imread(img_path)
            video.write(frame)

        video.release()
        print("Vídeo criado com sucesso!")

        num_frames = len(imagens)
        duracao_video = num_frames / fps
        print(f"Duração do vídeo: {duracao_video:.2f} segundos")

