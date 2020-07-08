import os
import time
import os.path
from os import path

# Opções de ordenação dos resultados
input1options = ['Padrao do site', 'Preço do aluguel + condomínio (menor para maior)',
                 'Preço do aluguel + condomínio (maior para menor)', 'Preço do aluguel (menor para maior)',
                 'Preço do aluguel (maior para menor)', 'Área do imóvel']


# Confere se a configuração é válida. Se não for, restaura ela aos valores padrão
def checacfg(cfg):
    if len(cfg) != 6:
        print('Ocorreu um erro na leitura das configurações. Restaurando ao padrão...')
        time.sleep(1.5)
        cfg = ['1', '83', 'completa', '3', 'Nao carregar', '0']
    cfg = [x.replace('\n', '') for x in cfg]
    return cfg


# Define a maneira de ordenar os resultados
def input1():
    print('Como deseja ordenar?')
    for i in range(len(input1options)):
        print(i + 1, '-', input1options[i])
    input1 = input('Digite o número correspondente: ')
    try:
        input1 = int(input1)
        if 0 < input1 < 7:
            return input1
        else:
            print('Digite um número válido')
            time.sleep(1)
            return 1
    except Exception as e:
        print('Digite um número válido')
        time.sleep(1)
        return 1


# Há diferentes webdrivers para diferentes versões do Chrome, essa função configura isso
def input2():
    print('Lembrando que as versões suportadas são a 81, 83 e 84!')
    input2 = input('Digite a versão do seu Google Chrome: ')
    input2str = 'chromedriver' + input2 + '.exe'
    if path.exists(input2str) is True:  # Apenas retorna o número se houver um arquivo correspondente na pasta
        return int(input2)
    else:
        print('Digite um número compatível.')
        print('Talvez o driver não esteja na pasta correta? Cheque o README para mais informações.')
        input('Pressione enter para voltar às configurações.')
        return 83


# Modelo de lista de bairros a ser exibida, a versão completa tem uma quantidade maior de bairros, mas é mais difícil
# de visualizar, a versão reduzida é mais estética e prática.
def input3():
    print('1 - Versão Completa (aproximadamente 630 bairros)')
    print('2 - Versão Reduzida (aproximadamente 90 bairros)')
    input3 = input('Digite o número correspondente: ')
    if input3 == '1':
        return 'completa'
    elif input3 == '2':
        return 'reduzida'
    else:
        print('Digite um número válido')
        time.sleep(1)
        return 'completa'


# Modifica a maneira de listar os bairros
def input4():
    input4 = input('Digite um número de bairros por linha (de 1 a 10): ')
    # Números maiores começam a distorcer a lista.
    if input4.isdigit():
        if int(input4) < 1 or int(input4) > 10:
            print('Digite um número de 1 a 10')
            time.sleep(1)
            return '3'
        else:
            return input4
    else:
        print('Digite um número válido')
        time.sleep(1)
        return '3'


# Apesar de pouco estético, deixar de carregar imagens tem uma melhora considerável na estabilidade do programa.
def input5():
    print('Você deseja deixar de carregar imagens?')
    print('Deixar de carregar imagens pode melhorar significativamente a capacidade de processamento,')
    print('principalmente na hora de fazer consultas em bairros com muitos imóveis!')
    print('1 - Carregar imagens')
    print('2 - Não carregar imagens')
    input5 = input('Digite o número correspondente: ')
    if input5 == '1':
        return 'Carregar'
    elif input5 == '2':
        return 'Nao carregar'
    else:
        print('Digite um número válido')
        time.sleep(1)
        return 'Nao carregar'


# Função utilizada para momentos de instabilidade de rede
def input6():
    print('A constante de carregamento é um valor adicionado ao timer em alguns momentos da pesquisa.')
    print(
        'Para computadores com capacidade de processamento menor ou internet instável, é recomendável aumentar o valor dessa constante para uma melhor estabilidade no processo.')
    print('(aumentar o valor, mesmo que em uma unidade, pode aumentar significativamente o tempo da consulta!)')
    print('Qual valor deseja utilizar? (Padrão:0, valor máximo recomendado: 3)')
    input6 = input('Digite o número correspondente: ')
    if input6.isdigit():
        if int(input6) < 0:
            print('Digite um número maior do que zero.')
            time.sleep(1)
            return 0
        else:
            return input6
    else:
        print('Digite um número válido.')
        time.sleep(1)
        return 0


# Função-mãe para definir as configurações
def config():
    configtxt = open('config.txt', 'r+')
    cfg = configtxt.readlines()
    cfg = checacfg(cfg)  # Checa se o arquivo tem formato válido
    input0 = 0
    while input0 != '8':
        clear = lambda: os.system('cls')
        clear()
        print(cfg[0])
        print('O que deseja configurar?')
        print('1 - Ordenação da pesquisa. [Agora ordenando por: ', input1options[int(cfg[0]) - 1], ']', sep='')
        print('2 - Versão do Google Chrome. [Versão configurada: ', cfg[1], ']', sep='')
        print('3 - Formato da lista de bairros. [Agora listando a versão ', cfg[2], ']', sep='')
        print('4 - Bairros por linha. [Agora listando: ', cfg[3], ' por linha]', sep='')
        print('5 - Exibição de imagens. [Agora: ', cfg[4], ' imagens]', sep='')
        print('6 - Constante de carregamento. [Agora: ', cfg[5], ' segundos]', sep='')
        print('7 - Restaurar para os padrões')
        print('8 - Sair das configurações')
        input0 = input('Digite o número correspondente: ')
        clear()
        if input0 == '1':
            cfg[0] = input1()
        elif input0 == '2':
            cfg[1] = input2()
        elif input0 == '3':
            cfg[2] = input3()
        elif input0 == '4':
            cfg[3] = input4()
        elif input0 == '5':
            cfg[4] = input5()
        elif input0 == '6':
            cfg[5] = input6()
        elif input0 == '7':
            cfg = ['1', '83', 'completa', '3', 'Nao carregar', '0']
            print('Configurações restauradas ao padrão')
            time.sleep(1)
        elif input0 != '8':
            print('Digite um número válido.')
            time.sleep(1)

    # Limpa o contéudo do arquivo de texto
    configtxt.seek(0)
    configtxt.truncate()

    # Grava as configurações no arquivo de texto
    for i in range(6):
        if i == 5:
            configtxt.write(cfg[i])
        else:
            configtxt.write("%s\n" % cfg[i])

    configtxt.close()

    return cfg
