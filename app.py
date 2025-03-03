from flask import Flask, request, jsonify, render_template
import os
from bs4 import BeautifulSoup
import requests
import threading

app = Flask(__name__)

def baixar_imagens_mercadolivre(url_anuncio, pasta_destino, progresso_callback):
    # (Código da função baixar_imagens_mercadolivre)
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url_anuncio, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        figuras = soup.find_all("figure", class_="ui-pdp-gallery__figure")

        if not os.path.exists(pasta_destino):
            os.makedirs(pasta_destino)

        total_imagens = len(figuras)
        for i, figura in enumerate(figuras):
            imagem = figura.find("img")

            if imagem:
                link_imagem = imagem.get("data-zoom")
                if not link_imagem:
                    link_imagem = imagem.get("src")

                if link_imagem:
                    link_imagem = link_imagem.strip()
                    nome_arquivo = f"imagem_{i+1}.webp"
                    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

                    try:
                        imagem_response = requests.get(link_imagem, headers=headers, stream=True)
                        imagem_response.raise_for_status()

                        with open(caminho_arquivo, "wb") as arquivo:
                            for chunk in imagem_response.iter_content(chunk_size=8192):
                                arquivo.write(chunk)

                        print(f"Imagem {i+1} salva em: {caminho_arquivo}")
                    except requests.exceptions.RequestException as e:
                        print(f"Erro ao baixar imagem {i+1}: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página do anúncio: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

def alterar_extensao_webp_para_jpg(pasta, progresso_callback):
    # (Código da função alterar_extensao_webp_para_jpg)
    try:
        arquivos = os.listdir(pasta)
        total_arquivos = len(arquivos)
        arquivos_renomeados = 0

        for arquivo in arquivos:
            if arquivo.endswith(".webp"):
                novo_nome = arquivo[:-5] + ".jpg"
                caminho_antigo = os.path.join(pasta, arquivo)
                caminho_novo = os.path.join(pasta, novo_nome)
                os.rename(caminho_antigo, caminho_novo)
                arquivos_renomeados += 1
                print(f"Arquivo renomeado: {arquivo} -> {novo_nome}")

        print("Processo concluído!")

    except FileNotFoundError:
        print(f"Erro: Pasta '{pasta}' não encontrada.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/baixar_imagens", methods=["POST"])
def baixar_imagens():
    data = request.get_json()
    url_anuncio = data.get("url_anuncio")
    pasta_destino = data.get("pasta_destino")

    if not url_anuncio or not pasta_destino:
        return jsonify({"erro": "URL e pasta de destino são obrigatórias."}), 400

    def progresso_callback(valor):
        print(f"Progresso: {valor}%")  # Simulação de progresso

    thread = threading.Thread(target=baixar_imagens_mercadolivre, args=(url_anuncio, pasta_destino, progresso_callback))
    thread.start()

    return jsonify({"mensagem": "Download das imagens iniciado!"})

@app.route("/renomear_arquivos", methods=["POST"])
def renomear_arquivos():
    data = request.get_json()
    pasta_imagens = data.get("pasta_imagens")

    if not pasta_imagens:
        return jsonify({"erro": "Pasta de imagens é obrigatória."}), 400

    def progresso_callback(valor):
        print(f"Progresso: {valor}%")  # Simulação de progresso

    thread = threading.Thread(target=alterar_extensao_webp_para_jpg, args=(pasta_imagens, progresso_callback))
    thread.start()

    return jsonify({"mensagem": "Renomeação de arquivos iniciada!"})

if __name__ == "__main__":
    app.run(debug=True)