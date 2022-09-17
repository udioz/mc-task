import requests
import mysql.connector

db = mysql.connector.connect(
  host='localhost',
  user='root',
  password='password',
  database='mc-nest'
)

cursor = db.cursor()


def lambda_handler(event, context):
    response = get_market_prices();
    save_results(response.json()['result'])

    return {
        'statusCode': response.status_code,
    }

def get_market_prices():
    return requests.get('https://api.cryptowat.ch/markets/prices');

def save_results(results):
    query = build_query(results)
    print(cursor.execute(query))
    print(db.commit())


def build_query(results):
    query = 'insert into rawQuotes (exchange, pair, price) values '
    for key in results:
        values = process_result(key, results[key])
        query = query + '''('%s', '%s', %s),'''%(values['exchange'], values['pair'], values['price'])
    query = query[:-1]
    return query


def process_result(priceEntity, price):
    if priceEntity.split(':')[0] != 'market':
        return

    return {
        'exchange': priceEntity.split(':')[1],
        'pair': priceEntity.split(':')[2],
        'price': price
    }    

lambda_handler({},{})