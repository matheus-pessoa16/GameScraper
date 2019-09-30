import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_restful import Resource, Api, reqparse
from urllib import parse
from datetime import datetime
import json


app = Flask(__name__)
api = Api(app)


class GameSearch(Resource):

    def search_game(self, term):

        url = 'https://www.game.co.uk/webapp/wcs/stores/servlet/AjaxCatalogSearch?langId=44&storeId=10151&catalogId=10201&categoryId=&pageView=image&pageSize=48&inStockOnly=true&listerOnly=true&contentOnly=&storeOnly=&provenance=&resultCatEntryType=2&catgrpSchemaType=&RASchemaType=&searchTerm=' + \
            term+'&searchType=&searchTermOperator=&searchTermScope=&filterTerm=&filterType=&filterTermOperator=&catGroupId=&categoryType=&sType=SimpleSearch&minPrice=&maxPrice=&sortBy=RELEVANCE&submitSortBy=Submit'

        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')

        resultRow = soup.find_all('article', 'product')

        results = []

        for i, row in enumerate(resultRow):

            if (row.find('span', {'class': 'platformLogo'}).text):

                gameUrl = row.a['href']
                title = row.find('h2').text

                releaseDate = None
                if row.find(id='preorderReleaseDate'):
                    releaseDate = row.find(id='preorderReleaseDate').text.split(
                        ' ')[-1].strip(' \t\n\r')

                imgUrl = row.select('a img')[0].get('data-src')

                price = None

                price = row.find('span', {'class': 'value'}).text

                discountedPrice = None

                createDate = json.dumps(datetime.now().isoformat())

                platform = row.find(
                    'span', {'class': 'platformLogo'}).text.strip(' \t\n\r')

                results.append({
                    'gameUrl': gameUrl,
                    'title': title,
                    'releaseDate': releaseDate,
                    'imgUrl': imgUrl,
                    'price': price,
                    'discountedPrice': discountedPrice,
                    'createDate' : createDate,
                    'source' : 'Game',
                    'platform': platform
                })

        print(len(results))
        return results


class SteamSearch(Resource):

    def search_game(self, term):

        url = 'https://store.steampowered.com/search/?term=' + term

        page = requests.get(url)

        soup = BeautifulSoup(page.text, "html.parser")

        resultRow = soup.find_all("a", "search_result_row")

        results = []

        for row in resultRow:

            platforms = []

            for platform in row.find_all('span'):
                if platform.get('class') is not None:
                    if platform.get('class')[0] == 'platform_img':
                        platforms.append(platform.get('class')[1])

            gameUrl = row.get('href')
            title = row.find('span', 'title').text
            releaseDate = row.find('div', 'search_released').text
            imgUrl = row.select('div.search_capsule img')[0].get('src')
            price = None
            discountedPrice = None
            createDate = json.dumps(datetime.now().isoformat())

            if row.select('div.search_price_discount_combined div.search_price'):
                price = row.select('div.search_price_discount_combined div.search_price')[
                    0].text.strip(' \t\n\r')
                if row.select('search_price_discount_combined div.search_discount'):
                    rawDiscount = row.select('div.search_price_discount_combined div.search_discount')[
                        0].strip(' \t\n\r')
                    discountedPrice = rawDiscount.replace(price, '')

            results.append({
                'gameUrl': gameUrl,
                'title': title,
                'releaseDate': releaseDate,
                'imgUrl': imgUrl,
                'price': price,
                'discountedPrice': discountedPrice,
                'createDate' : createDate,
                'source' : 'Steam',
                'platform': platforms
            })
        print(len(results))
        return results


class GameSearchListing(Resource):

    def get(self, term):
        response = []

        steam = SteamSearch()
        gameCo = GameSearch()
        steam_list = steam.search_game(term)
        game_list = gameCo.search_game(term)

        response = steam_list + game_list
        return response


api.add_resource(GameSearchListing, '/game_search/<string:term>')

if __name__ == '__main__':
    app.run(debug=True)
