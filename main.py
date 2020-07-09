from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from datetime import datetime
from os import path

import json
import getInfo
import config
import time
import unicodedata
import os


# Função para tirar as acentuações das palavras. Usada de forma a garantir que o usuário conseguirá pesquisar,
# por exemplo, pelo bairro "Sé" se digitar tanto "Sé" quanto "Se"
def TiraAcento(antiga):
    strnova = ''.join(ch for ch in unicodedata.normalize('NFKD', antiga)
                      if not unicodedata.combining(ch))
    return strnova


# Função para formatar o json de forma a ser exibido de uma maneira mais agradável de se ver
def formatjson(json_sort):
    json_sort = json_sort.replace(',', ',\n   ')
    json_sort = json_sort.replace(': [{', ': [\n  {')
    json_sort = json_sort.replace('   "Im', '"Im')
    json_sort = json_sort.replace('{"I', '{\n    "I')
    json_sort = json_sort.replace('},     {', '\n  },\n  {')
    json_sort = json_sort.replace('  {', '{')
    json_sort = json_sort.replace('[\n{', '[\n  {')
    json_sort = json_sort.replace('},', '\n  },')
    json_sort = json_sort.replace('}]}', '\n  } ]\n}')
    return json_sort


def main():
    clear = lambda: os.system('cls')  # definindo comando para limpar a tela
    inputinicial = '0'
    while inputinicial != '1':
        clear()
        print('Bem-vindo ao web scraper de dados do site vivareal.com.br!')
        print('O que deseja fazer?')
        print('')
        print('1 - Consultar imóveis a serem alugados em São Paulo - SP')
        print('2 - Configurações do web scraper')
        print('3 - Sair')
        inputinicial = input('Digite o número correspondente: ')

        if inputinicial == '2':  # Chama a função config para modificar as configurações
            cfg = config.config()
        elif inputinicial == '1':
            configtxt = open('config.txt', 'r+')
            cfg = configtxt.readlines()
            cfg = config.checacfg(cfg)  # Chama a função config para checar se as configurações estão num formato válido
            cfg[5] = int(cfg[5])  # Como a constante de carregamento é utilizada em operações, a convertemos para int
            configtxt.close()
        elif inputinicial == '3':
            exit()
        else:
            print('Digite um número válido.')
            time.sleep(1)

    clear()
    lbairroraw = []  # Cria lista para bairro sem acentos
    try:
        arquivobairros = 'bairro_' + cfg[2] + '.txt'  # Abre um dos dois arquivos disponíveis baseado na config.
        arquivobairros = open(arquivobairros, "r", encoding="utf-8")
    except Exception as e:
        print('Houve um erro ao ler a lista de bairros.')
        print('Cheque se os arquivos bairro_completa.txt e bairro_reduzida.txt estão na pasta deste programa.')
        print('Se não estiverem, tente fazer o download dos arquivos (ou de todo projeto) novamente.')
        print('')
        print('Pressione enter para encerrar o programa.')
        input('')
        exit()

    lbairro = arquivobairros.readlines()  # Atribui cada bairro do arquivo a um campo da lista
    arquivobairros.close()
    lbairro = [x.replace('\n', '') for x in lbairro]  # Retira os \n da string
    for i in range(len(lbairro)):
        lbairroraw.append(TiraAcento(lbairro[i]))  # Cria uma lista de bairros sem acento, assim
        # o usuário pode pesquisar com ou sem acentos e obter o resultado correto.

    acha_bairro = False
    while acha_bairro is False:
        # Formata e exibe a lista de bairros no console
        for i in range(0, len(lbairro)):
            if (i + 1) % int(cfg[3]) == 0:  # Define o número de resultados por linha baseado na configuração
                print(i + 1, ' - ', lbairro[i], '; ', sep='')
            else:
                print(i + 1, ' - ', lbairro[i], '; ', sep='', end='')
        print('')

        # Input do bairro
        print('Realizando busca de imóveis para alugar em São Paulo - SP.')
        input_bairro = input('Digite o nome do bairro, o ID do bairro ou digite 0 para sair: ')
        input_bairro = TiraAcento(input_bairro)  # Padroniza o input para poder ser comparado com a lista lbairrosraw

        # Faz a busca pelo bairro através do número ou nome
        # Manipula as variáveis para garantir que a pesquisa seja feita independentemente de erros na acentuação
        if input_bairro.isdigit():
            input_bairro = int(input_bairro)
            if input_bairro < 0 or input_bairro > (len(lbairroraw)):
                print('')
                print('ID de bairro inválido.')
                time.sleep(1)
            elif input_bairro == 0:
                exit()
            else:
                bairro = lbairro[input_bairro - 1] + ' São Paulo'  # Adicionando São Paulo no fim da variável bairro
                # isso garante que a pesquisa seja feita exclusiva para a cidade de São Paulo; caso o programa fosse
                # para qualquer cidade do Brasil, bastava adicionar um novo input de cidade e substituir o trecho
                # + ' São Paulo' para + cidade.
                acha_bairro = True
        else:
            if input_bairro in lbairroraw:
                bairro = lbairro[lbairroraw.index(input_bairro)] + ' São Paulo'  # Transforma a variável bairro de
                # tal forma com que os acentos estejam colocados de maneira correta
                acha_bairro = True
            else:
                print('')
                print('Bairro "', input_bairro, '" não encontrado.', sep='')
                print('Tente novamente.')
                time.sleep(2)

    # Define os argumentos. Os três primeiros são para melhorar a performance.
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-application-cache')
    option.add_argument('--disable-infobars')
    option.add_argument('--full-memory-crash-report')
    option.add_argument('--start-maximized')  # Faz com que o Chrome inicie já maximizado.

    # Ao invés de colocar ='Não carregar', coloquei !='Carregar' pois, já que a instrução padrão é não carregar imagens,
    # qualquer valor diferente de 'Carregar' será interpretado como o padrão (ou seja, 'Não carregar').
    if cfg[4] != 'Carregar':
        chrome_prefs = {}  # Define as opções de maneira com que as imagens não sejam carregadas.
        option.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}

    chromedriver = 'chromedriver' + cfg[1]
    if path.exists(chromedriver+'.exe') is True:
        try:
            driver = webdriver.Chrome(chromedriver, options=option)
        except Exception as e:
            print('Verifique se a versão do seu Google Chrome é compatível com o driver.')
            print('O driver utilizado se refere a versão', cfg[1], 'do Chrome, cheque o README.md para informações.')
            input('Pressione enter para sair.')
            exit()

    driver.get("https://www.vivareal.com.br/aluguel")  # Entra no site da vivareal com o Chrome
    time.sleep(1 + cfg[5])  # Os timers são postos em muitas situações a partir daqui pois, caso o programa tente fazer
    # leituras em partes do site que ainda não foram carregadas, isso pode resultar em erros; para garantir a estabili-
    # dade, os timers foram inseridos, de forma com que o site possa ser carregado antes de qualquer coisa.

    i2=1
    while i2<4:  # Caso haja problemas de conexão ou na hora de abrir o Chrome, é comum o programa ter problemas nessa
        # parte; então vale atribuir três tentativas por precaução
        try:
            inputbairro = driver.find_element_by_id('filter-location-search-input')  # Encontra o campo para digitar o bairro
            inputbairro.send_keys(bairro)  # Insere o conteúdo da variável "bairro" no campo em questão
            time.sleep(2 + cfg[5])
            driver.find_element_by_id('filter-location-search-input').send_keys(Keys.RETURN)  # Confirma a pesquisa do bairro
            time.sleep(3 + cfg[5])
            i2=4
        except Exception as e:
            if i2==3:
                print('Ocorreu um erro na inserção do bairro no sistema. Tente novamente.')
                print('Pressione enter para encerrar o programa.')
                exit()
            else:
                print('Houve um erro na inserção do bairro. Tentativa',i2+1)
                print('Reabrindo o navegador, por favor aguarde.')

    clear()

    try:  # Faz a leitura do código-fonte da página
        content = driver.page_source
        print('Pesquisando por imóveis a serem alugados em ', bairro.replace('São Paulo', ''), sep='')
        soup = BeautifulSoup(content, features='html5lib')
        total_resultados = soup.find('strong', attrs={'class': 'results-summary__count js-total-records'})
        total_resultados = total_resultados.text
        total_resultados = int("".join(filter(str.isdigit, total_resultados)))
    except Exception as e:
        print('Houve um problema ao inserir o bairro desejado no site. Tente novamente.')
        print('Pressione enter para encerrar o programa.')
        exit()

    if total_resultados > 500000:
        print('Houve um problema ao inserir o bairro desejado no site. Tente novamente.')
        input('Pressione enter para encerrar o programa.')
        exit()
    if total_resultados > 2000:  # Para pesquisas com um alto número de resultados, o consumo de memória do selenium é bem alto
        print(
            'Atenção! Como o número de resultados para essa consulta é maior do que 2000, o segmento do endereço '
            'especificando "São Paulo - SP" será removido do endereço para evitar problemas de memória.')
        print(total_resultados,
              'resultados encontrados. A consulta pode demorar um pouco devido ao alto volume de dados.')
    else:
        print(total_resultados, 'resultados encontrados.')

    # Prepara o nome do arquivo em .json a ser criado como output do programa
    agr = str(datetime.now())
    agr = ''.join(ch for ch in agr if ch.isdigit())
    nome_arquivo = (bairro + '' + agr + '.json')
    out_file = open(nome_arquivo, 'w', encoding='utf-8')  #

    # Insere o começo do arquivo .json em uma variável
    write_json = ('{'
                  '"Cidade": "São Paulo - SP",'
                  '"Imóveis":'
                  '[ \n')

    pag = 1
    stop = False

    # Cria um indicador de progresso utilizando uma previsão do total de páginas (cada página contém 36 resultados)
    pag_total = (total_resultados // 36) + 1
    print('Pesquisando... 0%', end='')

    while stop is False:
        b = soup.find('div', attrs={'class': 'results-list js-results-list'})  # Faz leitura do código-fonte dos resultados

        # Como muitas vezes há valores replicados até mesmo de endereço (quando, por exemplo, o número não é informado,
        # apenas a rua) o único parâmetro que é único para cada resultado é seu ID, que é apenas exibido no código-fonte
        id = []
        for tag in b.findAll(True, {'id': True}):
            id.append(tag['id'])

        # Apesar de toda página ter teoricamente 36 resultados, não é correto assumir que len(id)==36 sempre. Primeiramente
        # porque a última página dificilmente terá 36 resultados. Outro fator importante é que certos anúncios são tratados
        # como resultados no código-fonte; eles, porém, não tem ID, então utilizei os IDs para identificar os reais resultados.
        for i in range(len(id)):
            if id[i].isdigit():  # Atribui os parâmetros do resultados às variáveis
                infoid = b.find('div', id=id[i])
                endereco = (getInfo.getInfo(infoid, 'endereco'))
                quarto = (getInfo.getInfo(infoid, 'quarto'))
                suite = (getInfo.getInfo(infoid, 'suite'))
                banheiro = (getInfo.getInfo(infoid, 'banheiro'))
                garagem = (getInfo.getInfo(infoid, 'garagem'))
                preco = (getInfo.getInfo(infoid, 'preco'))
                condominio = (getInfo.getInfo(infoid, 'condominio'))
                area = (getInfo.getInfo(infoid, 'area'))

                dict1 = {  # Cria um dicionário para formatação dos dados em formato .json
                    'ID': id[i],
                    'Endereço': endereco,
                    'Área': area,
                    'Preço': preco,
                    'Condominio': condominio,
                    'Preço + condominio': preco + condominio,
                    'Quartos': quarto,
                    'Suítes': suite,
                    'Banheiros': banheiro,
                    'Vagas na garagem': garagem
                }

                dict2 = json.dumps(dict1, ensure_ascii=False)  # Usa o dicionário para gerar os dados no formato correto
                dict2 = dict2 + ',' + '\n'  # Formata as linhas para se encaixarem no .json
                write_json = write_json + dict2  # Adiciona os resultados à string que será gravada no arquivo resultante

        # Atualiza a barra de progresso
        print('', end='\r')
        load = (pag / pag_total) * 100
        load = round(load, 1)
        if load > 100:
            load = 100
        print('Pesquisando... ', load, '%', sep='', end='')

        pag = pag + 1
        # Favor checar o o README para melhor explicação deste segmento
        try:
            link = driver.find_element_by_link_text(str(pag))
            link.click()
        except Exception as e:
            try:
                time.sleep(3 + cfg[5])
                link = driver.find_element_by_link_text(str(pag))
                link.click()
            except Exception as e:
                if load < 100:
                    print('Houve um erro inesperado ao exibir os demais resultados.')
                    print('Gerando arquivo com os resultados já obtidos...')
                stop = True

        time.sleep(1 + cfg[5])
        url = driver.current_url  # Salva o valor da url da nova página

        # Como o selenium utiliza muita memória, ele foi configurado para fechar e reabrir a cada 50 páginas
        # de pesquisa, desta forma liberando um grande espaço na memória.
        if pag % 50 == 0:
            driver.quit()
            print('', end='\r')
            print('Liberando espaço na memória. Favor aguardar.', end='')
            time.sleep(5)
            print('', end='\r')
            print('Pesquisando... ', load, '%', sep='', end='')
            chromedriver = 'chromedriver' + cfg[1]  # Reabre o Chrome
            driver = webdriver.Chrome(chromedriver, options=option)
            driver.get(url)

        # Faz a leitura do código-fonte da nova página
        content = driver.page_source
        soup = BeautifulSoup(content, features='html5lib')

    driver.quit()  # Fecha o Chrome assim que a pesquisa é concluída.

    # Escreve o final da string referente ao .json
    write_json = write_json[:-2]
    write_json = write_json + (']'
                               '}')

    clear()
    if cfg[0] == '1':  # Neste caso a configuração é para o padrão do site; já que é a ordem lida naturalmente, não há necessidade de ordenar.
        write_json = json.dumps(write_json, ensure_ascii=False)
        print(write_json)  # Mostra a lista no console
        out_file.close()
        print('Os resultados também foram gravados no arquivo', nome_arquivo)
        input('Pressione enter para sair.')
        exit()

    # Interpreta a string como um .json para podermos ordená-la usando seus parâmetros
    arq = json.loads(write_json)
    json_sort = dict(arq)

    # Ordena os resultados da maneira citada no arquivo de configurações
    if cfg[0] == '2':
        json_sort['Imóveis'] = sorted(json_sort['Imóveis'], key=lambda k: k['Preço + condominio'])
    elif cfg[0] == '3':
        json_sort['Imóveis'] = sorted(json_sort['Imóveis'], key=lambda k: k['Preço + condominio'], reverse=True)
    elif cfg[0] == '4':
        json_sort['Imóveis'] = sorted(json_sort['Imóveis'], key=lambda k: k['Preço'])
    elif cfg[0] == '5':
        json_sort['Imóveis'] = sorted(json_sort['Imóveis'], key=lambda k: k['Preço'], reverse=True)
    elif cfg[0] == '6':
        json_sort['Imóveis'] = sorted(json_sort['Imóveis'], key=lambda k: k['Área'], reverse=True)
    else:
        print(write_json)
        print('')
        print('Houve um problema na hora de ordenar os resultados. Exibindo os resultados na ordenação padrão.')
        exit()

    # Grava o resultado no arquivo .json
    json_sort = json.dumps(json_sort, ensure_ascii=False)
    json_sort = formatjson(json_sort)
    print(json_sort)
    out_file.write(json_sort)
    out_file.close()

    print('')
    print('Os resultados foram gravados no arquivo', nome_arquivo)
    input('Pressione enter para finalizar o programa.')
    exit()


main()

#######
# {1} Uma das peculiaridades do site é que, apesar de ser possível fazer a pesquisa de primeira página de resultados de um
# bairro utilizando apenas manipulação de url, não é possível utilizar o mesmo método para trocar de página; ao digitar
# a url referente a página seguinte, o site redirecionará para a primeira página da pesquisa. A única forma que encontrei
# de conseguir acessar a url de uma página é acessando ela diretamente ao abrir o chrome (que é o que é usado, por exemplo,
# a cada 50 páginas ao fechar o browser para liberar memória). O único lado possivelmente ruim é que isso nos impossibilita
# de "esconder" o Chrome para que ele rode apenas em segundo plano, já que o código requer que o sistema efetue cliques,
# o que não é possível caso o Chrome não esteja em uma "zona clicável"; apesar dos pesares, é um problema apenas estético,
# a não ser que o usuário tente fazer algum tipo de ação no Chrome, algo que pode ser evitado minimizando o browser.
#######
# {2} A maneira do programa detectar seu fim é ao não conseguir clicar na próxima página, o que obviamente gera um erro.
# Esse erro, porém, também pode ser gerado caso seja feita uma consulta para uma quantidade muito grande de dados (segundo
# testes, esse erro acontece aproximadamente a partir de 9000 resultados) ou caso a página não tenha sido completamente
# carregada. O erro da página não carregada é simples de evitar gerando um outro request de click dentro do except, caso
# consiga, sabemos que a página carregou e que há páginas seguintes, então o programa continua, caso não, temos o possível
# erro de memória. Esse último erro é analisado a partir da barra de progresso, se ela estiver no 100%, significa que
# todas as páginas foram lidas e que de fato não há uma próxima página; se ela não estiver no 100%, então significa que
# houve um problema causado por alguma ação do usuário, da instabilidade de sua internet ou um problema de memória do
# próprio selenium. Como esses dois últimos problemas podem ter sido causados no fim de uma pesquisa muito demorada,
# optei por gerar um arquivo com os resultados parciais, o que faz com que o programa siga normalmente.
#######
