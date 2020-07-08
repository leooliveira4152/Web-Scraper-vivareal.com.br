# Web-Scraper-vivareal.com.br
Um web scraper para pesquisar imóveis a serem alugados em São Paulo - SP
Um web scraper é um método de extração de dados de websites de maneira automatizada e, por sua vez, de uma maneira muito mais rápida.
Este web scraper é para coleta de dados do site vivareal.com.br, um site para anúncios de venda e aluguel de imóveis. A versão utilizada é específica para aluguel de imóveis em São Paulo - SP, mas o código pode ser alterado de maneira relativamente simples tanto para realizar consultas de imóveis a venda quanto para realizar buscas em outras cidades.

O código só funciona em versões específicas do Google Chrome (81, 83 e 84) e só pôde ser testado no Windows 10; as instruções são para esse sistema. Para conferir sua versão do Chrome, abra-o, clique em Ajuda > Sobre o Google Chrome.


## Programas necessários
### Executável (main.exe):
- Nenhum programa necessário.

### Arquivo em python (main.py):
- Python, versão 3.7 ou superior;
- pip
- selenium (pip install selenium);
- bs4 (pip install bs4);
- html5lib (pip install html5lib);
- psutil (pip install psutil)


## Como utilizar
### Caso queira executar o arquivo executável, acesse a pasta dist/main/main.exe
### Caso queira executar o arquivo em python, há alguns pré-requisitos:
- Primeiramente baixe o Python em versão 3.7 ou superior. Caso queira um link: https://www.python.org/ftp/python/3.8.3/python-3.8.3.exe
- Ao instalar o Python, se certifique que a opção "add Python x.x to PATH" está marcada
- Com o Python devidamente instalado, clique com o botão direito no arquivo "install" (está na raiz da pasta do projeto) e selecione a opção "Executar com o Power Shell"
- Caso tenha algum problema com o passo acima, reinicie o computador e tente novamente; caso não tenha, execute o programa "main.py" (na raiz do projeto)

- Antes de começar a utilizar o webscraper, configura as configurações (apertando 2) para personalizá-lo; entre em cada opção para compreender melhor suas funções.
- Quando estiver pronto, acesse a opção referente a consultar imóveis (apertando 1 na tela inicial). A lista de bairros a ser exibida pode ser modificada nas opções.
- Ao digitar o bairro/ID, o programa abrirá um processo do Google Chrome e vai maximizá-lo; para estabilidade do programa, minimize a janela do Chrome que foi aberta e evite mexer nela.
- Os resultados serão exibidos na tela e em um arquivo .json criado na pasta onde estava o programa (.exe ou .py).


## Sobre os pacotes
- Selenium é o pacote responsável por abrir o processo do Chrome e administrá-lo.
- bs4 é utilizado para fazer a leitura do código-fonte do site.
- html5lib interpreta e formata o código-fonte para ser interpretado.

## Observações
-Uma das peculiaridades do site é que, apesar de ser possível fazer a pesquisa de primeira página de resultados de um bairro utilizando apenas manipulação de url, não é possível utilizar o mesmo método para trocar de página; ao digitar a url referente a página seguinte, o site redirecionará para a primeira página da pesquisa. A única forma que encontrei de conseguir acessar a url de uma página é acessando ela diretamente ao abrir o chrome (que é o que é usado, por exemplo, a cada 50 páginas ao fechar o browser para liberar memória). O único lado possivelmente ruim é que isso nos impossibilita de "esconder" o Chrome para que ele rode apenas em segundo plano, já que o código requer que o sistema efetue cliques, o que não é possível caso o Chrome não esteja em uma "zona clicável"; apesar dos pesares, é um problema apenas estético, a não ser que o usuário tente fazer algum tipo de ação no Chrome, algo que pode ser evitado minimizando o browser.
  
-A maneira do programa detectar seu fim é ao não conseguir clicar na próxima página, o que obviamente gera um erro. Esse erro, porém, também pode ser gerado caso seja feita uma consulta para uma quantidade muito grande de dados (segundo testes, esse erro acontece aproximadamente a partir de 9000 resultados) ou caso a página não tenha sido completamente carregada. O erro da página não carregada é simples de evitar gerando um outro request de click dentro do except, caso consiga, sabemos que a página carregou e que há páginas seguintes, então o programa continua, caso não, temos o possível erro de memória. Esse último erro é analisado a partir da barra de progresso, se ela estiver no 100%, significa que todas as páginas foram lidas e que de fato não há uma próxima página; se ela não estiver no 100%, então significa que houve um problema causado por alguma ação do usuário, da instabilidade de sua internet ou um problema de memória do próprio selenium. Como esses dois últimos problemas podem ter sido causados no fim de uma pesquisa muito demorada, optei por gerar um arquivo com os resultados parciais, o que faz com que o programa siga normalmente.

