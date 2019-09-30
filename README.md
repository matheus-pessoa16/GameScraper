# GameScraper

Projeto utilizando as bibliotecas requests e BeautifulSoup para fazer web scraping em dois sites de jogos. Os dados são estruturados em JSON e retornados através de uma API rest usando Flask. 
Esse projeto possui apenas fins de estudo.

## Installation

Instale as dependências necessárias para executar o projeto.

```bash
pip install beautifulsoup
pip install requests
pip install flask
pip install flask-restful
pip install datetime
```

## Usage

Para adicionar o nome do jogo utilize '+' no lugar de espaços. Ex:
the+witcher

Também é possível pesquisar com apenas uma parte do nome do jogo. Ex:
witcher

```bash
python3 scraper.py

curl http://127.0.0.1:5000/game_search/<jogo_desejado>
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
