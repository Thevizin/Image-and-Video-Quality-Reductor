from image_resize import ImageResize
from video_reductor import VideoReductor
from audio_quality_reductor import AudioQualityReductor  
import os

def handle_image_video():
    while True:
        choice = input(
            "\nEscolha uma opção:\n"
            "1. Reduzir/Ampliar Imagem\n"
            "2. Reduzir Vídeo\n"
            "3. Processar Áudio (compressão ou earrape)\n"
            "4. Sair\n"
            "Opção: "
        ).strip()

        if choice == '1':
            path = input("Caminho da imagem: ").strip()
            try:
                fator = int(input("Fator (ex: 2 para metade ou dobro): ").strip())
                action = input("Deseja reduzir ou ampliar? (r/a): ").lower().strip()
                is_reduction = action == 'r'

                img_resizer = ImageResize(path)
                nova_imagem = img_resizer.reduction_amplifier_pixel(is_reduction, fator)

                save_path = input("Digite o nome/caminho para salvar a nova imagem: ").strip() or "saida.png"
                img_resizer.save_image(save_path)

                print(f"✅ Operação concluída. Imagem salva em {save_path}")
            except Exception as e:
                print(f"❌ Erro ao processar a imagem: {e}")

        elif choice == '2':
            path = input("Caminho do vídeo: ").strip()
            try:
                fps_input = input("FPS do novo vídeo (padrão 30): ").strip()
                fps = int(fps_input) if fps_input else 30

                fator = int(input("Fator de redução (ex: 2 para reduzir pela metade): ").strip())

                # Pergunta sobre processamento de áudio
                audio_choice = input(
                    "Deseja processar o áudio do vídeo?\n"
                    "1. Comprimir\n"
                    "2. Deixar estourado (earrape)\n"
                    "3. Nenhum\n"
                    "Opção: "
                ).strip()

                duracao_video = None  # Calcularemos após a redução do vídeo

                vid_reductor = VideoReductor(path)
                vid_reductor.make_frame()
                vid_reductor.diminuivideo(final_frames_path="final_frames", fps=fps, fator=fator)

                print("✅ Vídeo reduzido com sucesso.")

                # Processa áudio se escolhido
                if audio_choice in ['1', '2']:
                    # Pega duração do vídeo
                    num_frames = len([f for f in os.listdir("final_frames") if f.endswith(('.png', '.jpg'))])
                    duracao_video = num_frames / fps

                    output_audio_path = input("Digite o caminho/nome do áudio de saída: ").strip() or "audio_processado.mp3"
                    modo = "compress" if audio_choice == '1' else "earrape"

                    AudioQualityReductor.process_audio(
                        audio_path=path,
                        output_path=output_audio_path,
                        duracao_video=duracao_video,
                        modo=modo
                    )

            except Exception as e:
                print(f"❌ Erro ao processar o vídeo: {e}")

        elif choice == '3':
            path = input("Caminho do arquivo de áudio (MP3 ou MP4): ").strip()
            try:
                duracao_video = int(input("Duração do trecho em segundos: ").strip())
                modo_input = input(
                    "Escolha o modo:\n"
                    "1. Comprimir áudio\n"
                    "2. Deixar estourado (earrape)\n"
                    "Opção: "
                ).strip()
                modo = "compress" if modo_input == '1' else "earrape"

                output_audio_path = input("Digite o caminho/nome do áudio de saída: ").strip() or "audio_processado.mp3"

                AudioQualityReductor.process_audio(
                    audio_path=path,
                    output_path=output_audio_path,
                    duracao_video=duracao_video,
                    modo=modo
                )
            except Exception as e:
                print(f"❌ Erro ao processar o áudio: {e}")

        elif choice == '4':
            print("👋 Saindo...")
            break

        else:
            print("⚠️ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    try:
        handle_image_video()
    except KeyboardInterrupt:
        print("\n Cliente desconectado.")
    except Exception as e:
        print(f"❌ Erro no cliente: {e}")
