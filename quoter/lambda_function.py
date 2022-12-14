import os
import mysql.connector

DEFAULT_EXCHANGE = 'kraken'

try:
    db = mysql.connector.connect(
        host = os.environ.get('DB_HOST'),
        user = os.environ.get('DB_USER'),
        password = os.environ.get('DB_PASSWORD'),
        database = os.environ.get('DB_DATABASE')
    )

    cursor = db.cursor(dictionary=True)
except mysql.connector.Error as error:
    print(error)


def lambda_handler(event, context):
    pair = event['queryStringParameters']['pair']
    quotes = get_pair_quotes(pair)
    rank = get_pair_rank(pair)
    return {
        'statusCode': 200,
        'body': { 'quotes' : quotes, 'rank': rank }
    }

def get_pair_quotes(pair, exchange = DEFAULT_EXCHANGE):
  query = '''
    select exchange, pair, price, unix_timestamp(created_at) as timestamp
    from quotes
    where exchange = '%s'
    and pair = '%s'
    and created_at > now() - interval 24 hour
  '''%(exchange, pair)

  cursor.execute(query)
  return cursor.fetchall()

def get_pair_rank(pair, exchange = DEFAULT_EXCHANGE):
  query = '''
    select the_rank 
    from ranks
    where exchange = '%s'
    and pair = '%s' 
  '''%(exchange, pair)
  cursor.execute(query)
  return cursor.fetchone()
