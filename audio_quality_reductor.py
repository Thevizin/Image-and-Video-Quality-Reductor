import os

class AudioQualityReductor:
    @staticmethod
    def process_audio(audio_path, output_path, duracao_video, modo="compress", ganho_dB=20, inicio_seg=0, bitrate="64k"):
        """
        Processa áudio de MP3 ou MP4 usando apenas FFmpeg.

        audio_path: caminho do arquivo de entrada (MP3 ou MP4)
        output_path: caminho do arquivo final (MP3)
        duracao_video: duração do trecho em segundos
        modo: "compress" ou "earrape"
        ganho_dB: aumento de volume para earrape (apenas se modo="earrape")
        inicio_seg: segundo inicial do trecho
        bitrate: taxa de compressão (apenas se modo="compress")
        """

        # Define arquivo temporário se for MP4
        ext = os.path.splitext(audio_path)[1].lower()
        if ext == ".mp4":
            temp_audio = "temp_audio.wav"
            os.system(f'ffmpeg -y -i "{audio_path}" -vn -acodec pcm_s16le -ar 44100 "{temp_audio}"')
            input_file = temp_audio
        else:
            input_file = audio_path

        # Define filtros FFmpeg
        filters = []
        # Trecho do áudio
        filters.append(f"atrim=start={inicio_seg}:duration={duracao_video}")
        filters.append("asetpts=PTS-STARTPTS")  # reseta timestamps

        # Se earrape, aplica ganho
        if modo == "earrape":
            filters.append(f"volume={ganho_dB}dB")

        filter_str = ",".join(filters)

        # Comando final
        if modo == "compress":
            cmd = f'ffmpeg -y -i "{input_file}" -af "{filter_str}" -b:a {bitrate} "{output_path}"'
        else:  # earrape
            cmd = f'ffmpeg -y -i "{input_file}" -af "{filter_str}" "{output_path}"'

        # Executa
        os.system(cmd)

        # Remove temporário se existir
        if ext == ".mp4":
            os.remove(temp_audio)

        print(f"✅ Áudio processado em: {output_path}")
