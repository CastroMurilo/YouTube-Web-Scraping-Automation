# Youtube Scraper

Este projeto é uma ferramenta de scraping que coleta informações sobre vídeos do YouTube com base em uma pesquisa específica. Utiliza `PySimpleGUI` para a interface do usuário, `BotCity` para automação web e `pandas` para manipulação de dados em Excel.

## Funcionalidades

- Pesquisa vídeos no YouTube com base em uma palavra-chave fornecida pelo usuário.
- Coleta informações como nome do canal, nome do vídeo, visualizações, link, data de publicação e descrição.
- Armazena os dados coletados em um arquivo Excel.

## Requisitos

- Python 3.7 ou superior
- As seguintes bibliotecas Python:
  - `PySimpleGUI`
  - `botcity-web`
  - `webdriver_manager`
  - `openpyxl`
  - `pandas`

Você pode instalar todas as dependências usando o comando:

```bash
pip install PySimpleGUI botcity-web webdriver_manager openpyxl pandas
