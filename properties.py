# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from requests import get
from datetime import datetime

agora = datetime.now()

def subprocessamento(web_adress):
	try:
		site = get(web_adress)
		sitesp = bs(site.content, 'lxml')
		title = sitesp.find(class_="property-card__title js-cardLink js-card-title").get_text().strip()
		address = sitesp.find(class_="property-card__address js-property-card-address js-see-on-map").get_text().strip()
		value = sitesp.find(class_="property-card__price js-property-card-prices js-property-card__price-small").get_text().strip()
		print(str(title) + ';' + str(address) + ';' + str(value).replace('\n','').strip())
		return(str(title) + ';' + str(address) + ';' + str(value).replace('\n','').strip())
	except AttributeError:
		with open('log','a') as error:
			error.write(str(AttributeError) + " " + str(web_adress) + '\n')

def processamento(web_adress):
	try:
		lista = [];line = []
		site = get(web_adress)
		line.append(subprocessamento(web_adress))
		sitesp = bs(site.content, 'lxml')
		for link in sitesp.find_all("li"):
			if str(link.get('title')).find('None')==-1:
				lista = str(link.get_text()).split('\n')
				lista = [x.strip() for x in lista]
				if len(lista)<2:
					pass
				else:
					line.append(" ".join(lista))
		save(line)
	except TypeError:
		with open('log','a') as error:
			error.write(str(TypeError) + " " + str(web_adress) + '\n')
	
def save(lista):
	with open('imoveis.csv','a') as file:
		file.write(";".join(lista)+ '\n')

def situation(page):
	print("page {0}\t{1}".format(page,datetime.now() - agora))

def queue(web_adress, number):
	anterior = ''
	for page in range(1,number):
		situation(page)
		site = get(web_adress + '/venda/sp/ribeirao-preto/?pagina=' + str(page) + '#onde=BR-Sao_Paulo-NULL-Ribeirao_Preto')
		sitesp = bs(site.content,'lxml')
		for link in sitesp.find_all("a"):
			if str(link.get('href')).find('id-')!=-1:
				if str(link.get('href')) == anterior:
					pass
				else:
					processamento(web_adress + str(link.get('href')))
					anterior = link.get('href')

if __name__ == "__main__":
	with open('imoveis.csv','w') as file, open('log','w') as log:
		file.write('Anúncio;Endereço;Valor;Área;Quartos;Banheiros;Garagem\n')
	web_adress = 'https://www.vivareal.com.br'
	number = int(input('How many pages ?'))
	queue(web_adress, number + 1)