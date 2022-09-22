import os
import requests
import mysql.connector
from datetime import datetime

BATCH_ID = datetime.timestamp(datetime.now())

def lambda_handler(event, context):
    response = get_market_prices();
    if response.status_code == 200:
        save_response = save_results(response.json()['result'])

    return {
        'statusCode': response.status_code,
        'response': save_response
    }

def get_market_prices():
    return requests.get('https://api.cryptowat.ch/markets/prices');

def save_results(results):
    try:
        db = mysql.connector.connect(
            host = os.environ.get('DB_HOST','mc-db'),
            user = os.environ.get('DB_USER','root'),
            password = os.environ.get('DB_PASSWORD','password'),
            database = os.environ.get('DB_DATABASE','mc_task')
        )
        cursor = db.cursor()
        query = build_query(results)
        tic = datetime.timestamp(datetime.now())
        cursor.execute(query)
        toc = datetime.timestamp(datetime.now())
        db.commit()
        return {
            'affected_rows': cursor._affected_rows,
            'insert_duration': toc - tic
        }
    except mysql.connector.Error as error:
        print(error)
        return False

def build_query(results):
    query = 'insert into quotes (exchange, pair, price, batch_id) values '
    query_values = ''
    for key in results:
        values = process_result(key, results[key])
        if (values):
            query_values += '''('%s', '%s', %s, '%s'),'''%(
                values['exchange'],
                values['pair'],
                values['price'],
                BATCH_ID
            )
    query += query_values[:-1]
    return query


def process_result(priceEntity, price):
    if priceEntity.split(':')[0] != 'market':
        return {}

    return {
        'exchange': priceEntity.split(':')[1],
        'pair': priceEntity.split(':')[2],
        'price': price
    }
