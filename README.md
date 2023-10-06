DeepScan - README

Descrição do Projeto

Este é um programa de busca de palavras-chave em arquivos dentro de pastas e subpastas. Ele permite aos usuários selecionar pastas para escanear e procurar por palavras-chave em todos os arquivos contidos dentro dessas pastas. Os resultados da busca são apresentados em um painel de resultados, mostrando o nome do arquivo e o conteúdo da linha em que a palavra-chave foi encontrada. Além disso, o programa oferece a capacidade de salvar um relatório com todos os resultados encontrados. Útil para análise forense de dados, uma vez que muitos usuários e invasores podem salvar dados sensíveis em arquivos inesperados ou até mesmo a má codificação de um arquivo em relação a um programa. 

Funcionalidades

Escaneia arquivos em pastas especificadas em busca de palavras-chave.
Apresenta resultados em tempo real no painel de resultados.
Permite salvar um relatório com todos os resultados encontrados.
Oferece uma interface intuitiva para adicionar e gerenciar pastas de busca.
Utiliza a sintaxe do grep do unix para procurar em uma mesma linha, ex: palavra.*numero.*um

Como Usar

Configuração Inicial
Clone este repositório para a sua máquina local.
Certifique-se de ter as dependências necessárias instaladas (lista de dependências no arquivo requirements.txt).
Execute o programa principal (main.py) para iniciar a interface do usuário.

Adicionando Pastas para Busca
Clique no botão "directory" para procurar a pasta desejada, ou simplesmente escreva o caminho dela na caixa de texto.
Clique no botão "+" para adicionar a pasta na lista de busca, lembrando que buscará todos arquivos na pasta e subpastas.
Pode também adicionar uma pasta à lista de exclusão, clicando no botão "-", caso deseje remover da busca uma subpasta do seu diretório escolhido.
Há um botão "V", onde expande a lista dos diretórios adicionados.


Configurações de Busca
Defina as palavras-chave que deseja buscar e adicione utilizando o botão de "+".
Pode ativar o case sensitive para buscar palavras exatas, ou deixar desabilitado (Padrão), onde não fará distinção de letras maiúsculas e minúsculas.
Botão "V" expande a lista de palavras-chaves que serão procuradas nos arquivos.
Para fazer uma busca com mais de um conteúdo na mesma linha, pode se utilizar o .* onde entre uma palavra e outra irá ignorar o conteúdo entre as palavras. Ex: suponha uma linha "Existe uma casa verde no bosque ao lado", para fazer uma busca utilizando duas palavras que contenham na linha, podemos utilizar a palavra-chave como "casa.*bosque", onde irá procurar nos arquivos, todas as linhas que contenham as palavras "casa" e "bosque" consecutivamente na mesma linha.

Iniciando a Busca
Clique no botão Start.
O programa começará a escanear os arquivos nas pastas especificadas.

Resultados da Busca
Os resultados da busca serão exibidos em tempo real no painel de resultados.
Cada resultado incluirá o nome do arquivo e o conteúdo da linha em que a palavra-chave foi encontrada.

Salvando um Relatório
Após a busca estar completa, você pode optar por salvar um relatório com todos os resultados encontrados.

Requisitos do Sistema

Python 3.x
Kivy
Functools
Plyer
Platform


Contribuindo

Se você deseja contribuir para este projeto, sinta-se à vontade para abrir problemas (issues) ou enviar pull requests. Toda contribuição é bem-vinda!

Autor

Guilherme Capelleto Restani

<img width="1005" alt="Captura de Tela 2023-10-05 às 22 20 51" src="https://github.com/guicapelleto/DeepScan/assets/125845072/d69b7831-88e0-4869-a6a6-7934355842a7">

