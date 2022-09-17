import json
import requests
import mysql.connector

mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  password='password',
  database='mc-nest'
)

mycursor = mydb.cursor()


def lambda_handler(event, context):
    response = requests.get('https://api.cryptowat.ch/markets/prices');
    process_results(response.json()['result'])

    return {
        'statusCode': response.status_code,
        'body': json.dumps('Hello from Lambda!')
    }

def process_results(results):
    query = build_query(results)
    print(query)
    mycursor.execute(query)
    mydb.commit()


def build_query(results):
    query = 'insert into rawQuotes (exchange, pair, price) values '
    for key in results:
        values = process_result(key, results[key])
        query = query + '("%s", "%s", %s),'%(values['exchange'], values['pair'], values['price'])
    query = query[:-1]
    return query


def process_result(priceEntity, price):
    print(priceEntity, price)
    if priceEntity.split(':')[0] != 'market':
        return

    return {
        'exchange': priceEntity.split(':')[1],
        'pair': priceEntity.split(':')[2],
        'price': price
    }    

lambda_handler({},{})