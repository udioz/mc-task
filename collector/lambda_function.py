import os
import requests
import mysql.connector

def lambda_handler(event, context):
    response = get_market_prices();
    if response.status_code == 200:
        save_results(response.json()['result'])

    return {
        'statusCode': response.status_code,
    }

def get_market_prices():
    return requests.get('https://api.cryptowat.ch/markets/prices');

def save_results(results):
    try:
        db = mysql.connector.connect(
            host = os.environ.get('DB_HOST','localhost'),
            user = os.environ.get('DB_USER','root'),
            password = os.environ.get('DB_PASSWORD','password'),
            database = os.environ.get('DB_DATABASE','mc-nest')
        )
    
        cursor = db.cursor()

        query = build_query(results)
        cursor.execute(query)
        db.commit()
        return True
    except mysql.connector.Error as error:
        print(error)
        return False


def build_query(results):
    query = 'insert into quotes (exchange, pair, price) values '
    for key in results:
        values = process_result(key, results[key])
        if (values):
            query = query + '''('%s', '%s', %s),'''%(values['exchange'], values['pair'], values['price'])
    query = query[:-1]
    return query


def process_result(priceEntity, price):
    if priceEntity.split(':')[0] != 'market':
        return {}

    return {
        'exchange': priceEntity.split(':')[1],
        'pair': priceEntity.split(':')[2],
        'price': price
    }
