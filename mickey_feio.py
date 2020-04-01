#!/bin/python

import instaloader
import datetime
import os
import glob
import json
from xopen import xopen


now = datetime.datetime.now()
hastag = "#mickeyfeio" + str(now.year)

separador = os.path.sep

# ============================================
# Função que faz o donwload de todas as imagens
# do instagram com a hastag
# ============================================
def download_from_instagram():
	# Aqui ele usa a lib externa 'instaloader' para baixar asimagens do instagram
	# baseado na hastag
	loader = instaloader.Instaloader()

	for post in loader.get_hashtag_posts('mickeyfeio' + str(now.year)):
		# post is an instance of instaloader.Post
		loader.download_post(post, target=hastag)

# ============================================
# Função que deleta alguns arquivos sem uso pra esse script.
# - os arquivos .txt vem com a legenda da foto, não precisa.
# - e os arquivos .json são os comentários da foto, também não precisa
# ============================================
def delete_unused_files():
	# Aqui ele deleta a lista de arquivos desnecessários
	fileListTxt = glob.glob(hastag + separador + "*.txt")
	fileListJson = glob.glob(hastag + separador + "*.json")

	fileList = fileListTxt + fileListJson

	# Deleta todos os arquivos .txt e .json
	for filePath in fileList:
		try:
				os.remove(filePath)
		except:
			print("Error while deleting file: ", filePath)

# ============================================
# Função que extrai as informações do arquivo:
# como o autor da foto, e o arquivo .xz referente
# ============================================
def extract_info():
	fileListXz = glob.glob(hastag + separador + "*.xz")
	dados_list = []

	# itera em todos os arquivos .xz
	for filexz in fileListXz:
		# abre o arquivo
		with xopen(filexz) as file:
			content = file.read()

			# inicializa o dicionário auxiliar
			dados = {"username":None, "filename":None}

			# extrai o autor da foto
			json_object = json.loads(content)
			dados["username"] = json_object["node"]["owner"]["username"]

			# salva no dicionário o nome do arquivo .xz referente
			# daquela foto, sem extensão., apenas o nome.
			file_without_extension = os.path.splitext(filexz)[0]
			file_without_extension = os.path.splitext(file_without_extension)[0]
			dados["filename"] = file_without_extension

			# adiciona tudo numa lista de dicionários
			dados_list.append(dados)

		# fecha o descritor de arquivo, e deleta o arquivo .xz,
		# a partir desse ponto, não precisamos mais dele
		file.close()
		os.remove(filexz)

	return dados_list


# ============================================
# Função que renomeia os arquivos de imagem
# adicionando o nome do autor da foto, no nome
# do arquivo de imagem.
# ============================================
def rename_files():
	# pega a lista de dicionários que contém o autor e o arquivo referente à foto.
	dados_list = extract_info()

	# itera em todos os arquivos do diretório gerado (nesse ponto, só sobrou as imagens)
	for image in os.scandir(hastag):
		image = image.path

		# separa em duas variáveis, o nome do arquivo e a extensão.
		image_without_extention, extension = os.path.splitext(image)

		# cria um outro loop, pra iterar na lista de dicionários auxiliar
		for info in dados_list:

			# compara se o nome da imagem (sem extensão) começa com a string do
			# nome do arquivo .xz (sem extensão tb).
			# Se for verdade, então renomeie o arquivo com o nome do autor, e interrompa o loop.
			xz_file = info["filename"]
			if image_without_extention.startswith(xz_file):
				user = info["username"]
				new_name = f"{image_without_extention}.{user}{extension}"
				os.rename(image, new_name)
				break

# ============================================
# Função Main
# ============================================
if __name__ == '__main__':
		download_from_instagram()
		delete_unused_files()
		rename_files()
