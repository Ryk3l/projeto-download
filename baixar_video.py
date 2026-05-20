import yt_dlp
import os
import sys

def barra_progresso(d):
    if d['status'] == 'downloading':
        # Pega a string de porcentagem (ex: " 10.5%")
        perc_str = d.get('_percent_str', '0%').strip()
        
        # Limpa para pegar apenas o número (remove % e espaços)
        perc_clean = ''.join(c for c in perc_str if c.isdigit() or c == '.')
        
        try:
            # Garante que o valor seja float e esteja entre 0 e 100
            perc = float(perc_clean)
            if perc > 100: perc = 100
        except:
            perc = 0
        
        # DEFINA AQUI O TAMANHO FIXO DA BARRA
        barra_total = 30 
        
        # A conta agora é forçada a ficar dentro do limite de barra_total
        qtd_cheia = int((perc / 100) * barra_total)
        qtd_vazia = barra_total - qtd_cheia
        
        barra = '#' * qtd_cheia + '-' * qtd_vazia
        
        # Corta o título para não quebrar a linha do terminal (máximo 20 caracteres)
        titulo = d.get('filename', 'Video').split(os.sep)[-1][:20]
        eta = d.get('eta', '?')

        # Monta a linha e usa o \r para sobrescrever a mesma linha
        # O " " * 10 no final limpa resíduos de texto mais longo anterior
        sys.stdout.write(f"\r[{barra}] {perc:5.1f}% | {titulo} | ETA: {eta}s          ")
        sys.stdout.flush()

    elif d['status'] == 'finished':
        # Limpa a linha completamente antes de avisar que terminou
        sys.stdout.write("\r" + " " * 100 + "\r")
        titulo = d.get('filename', 'Video').split(os.sep)[-1]
        sys.stdout.write(f"✔ Concluído: {titulo}\n")
        sys.stdout.flush()

def baixar_videos_disponiveis(link_url, formato_escolhido):
    pasta = "downloads"
    os.makedirs(pasta, exist_ok=True)

    # Configurações para garantir que o yt-dlp não interfira no terminal
    dl_opts_base = {
        "quiet": True,
        "no_warnings": True,
        "noprogress": True, # ESSENCIAL: desativa a barra nativa do yt-dlp
        "progress_hooks": [barra_progresso],
        "outtmpl": os.path.join(pasta, "%(title)s.%(ext)s"),
    }

    if formato_escolhido == '2': # MP3
        dl_opts_base.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        })
    else: # MP4
        dl_opts_base.update({
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        })

    print(f"\n--- Processando link: {link_url} ---")
    
    with yt_dlp.YoutubeDL(dl_opts_base) as ydl:
        try:
            ydl.download([link_url])
        except Exception as e:
            print(f"\nErro no link {link_url}: {e}")

if __name__ == "__main__":
    arquivo_links = "links.txt"

    if not os.path.exists(arquivo_links):
        with open(arquivo_links, "w") as f: pass
        print(f"Arquivo '{arquivo_links}' criado. Adicione os links e reinicie.")
        sys.exit()

    with open(arquivo_links, "r") as f:
        links = [linha.strip() for linha in f if linha.strip()]

    if not links:
        print("Adicione links ao arquivo links.txt")
        sys.exit()

    print(f"Links para baixar: {len(links)}")
    print("1 - MP4 | 2 - MP3")
    escolha = input("Opção: ").strip()

    for link in links:
        baixar_videos_disponiveis(link, escolha)

    print(f"\n✔ Processo concluído com sucesso!")