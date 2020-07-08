from selenium import webdriver
from bs4 import BeautifulSoup


def checkint(x):
    if x is None:
        return 0
    x=x.text
    x=x.replace(' ','')
    x=x.replace('\n','')
    if x.isdigit():
        return int(x)
    else:
        return 0


def getInfo(infoid, func):
    if func == 'quarto':
        quartos = infoid.find('span', attrs={'class': 'property-card__detail-value js-property-card-value'})
        quartos = checkint(quartos)
        return quartos
    elif func == 'suite':
        infoid2 = infoid.find('li', attrs={'class': 'property-card__detail-item property-card__detail-item-extra js-property-detail-suites'})
        if infoid2 is None:
            return 0
        suite = infoid2.find('span', attrs={'class': 'property-card__detail-value js-property-card-value'})
        suite = checkint(suite)
        return suite
    elif func == 'banheiro':
        infoid2 = infoid.find('li', attrs={'class': 'property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom'})
        if infoid2 is None:
            return 0
        banheiro = infoid2.find('span', attrs={'class': 'property-card__detail-value js-property-card-value'})
        banheiro = checkint(banheiro)
        return banheiro
    elif func == 'garagem':
        infoid2 = infoid.find('li', attrs={'class': 'property-card__detail-item property-card__detail-garage js-property-detail-garages'})
        if infoid2 is None:
            return 0
        garagem = infoid2.find('span', attrs={'class': 'property-card__detail-value js-property-card-value'})
        garagem = checkint(garagem)
        return garagem
    elif func == 'endereco':
        endereco = infoid.find('span', attrs={'class': 'property-card__address js-property-card-address js-see-on-map'})
        if endereco is None:
            return '--'
        else:
            endereco = endereco.text
            endereco = endereco.replace('\n                ','')
            endereco = endereco.replace('\n              ','')
            endereco = endereco.replace(',',';')
            return endereco
    elif func == 'preco':
        preco = infoid.find('div', attrs={'class': 'property-card__price js-property-card-prices js-property-card__price-small'})
        if preco is None:
            return 0
        else:
            preco = preco.text
            preco = ''.join(ch for ch in preco if ch.isdigit())
            if preco.isdigit():
                return int(preco)
            else:
                return 0
    elif func == 'condominio':
        condominio = infoid.find('strong', attrs={'class': 'js-condo-price'})
        if condominio is None:
            return 0
        else:
            condominio = condominio.text
            condominio = ''.join(ch for ch in condominio if ch.isdigit())
            if condominio.isdigit():
                return int(condominio)
            else:
                return 0
    elif func == 'area':
        area = infoid.find('span', attrs={'class': 'property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area'})
        if area is None:
            return 0
        else:
            area = area.text
            area = ''.join(ch for ch in area if ch.isdigit())
            if area.isdigit():
                return int(area)
            else:
                return 0