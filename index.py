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
    # response = requests.get('https://api.github.com/');
    results = response.json()['result']
    
    for key in results:
        process_result(key, results[key])

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def process_result(key, value):
    print(key, value)
    if key.split(':')[0] != 'market':
        return

    exchange = key.split(':')[1]
    pair = key.split(':')[2]

    sql = "INSERT INTO rawQuotes (exchange, pair, price) VALUES (%s, %s, %s)"
    val = [exchange, pair, value]
    mycursor.execute(sql, val)

    mydb.commit()

    print(mycursor.rowcount, "record inserted.")
    



print(lambda_handler({},{}))