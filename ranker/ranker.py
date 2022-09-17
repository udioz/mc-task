from email.policy import default
import json
from unittest.mock import DEFAULT
import mysql.connector
import statistics

DEFAULT_EXCHANGE = 'kraken'

db = mysql.connector.connect(
  host='localhost',
  user='root',
  password='password',
  database='mc-nest'
)

cursor = db.cursor(dictionary=True)

def lambda_handler(event, context):    
    results = get_exchange_pairs()
    for pair_record in results:
        pair = pair_record.get('pair')
        pair_prices = get_pair_prices(pair)

        prices = []
        for price in pair_prices:
            prices.append(price.get('price'))

        upsert_pair_stdev(pair,statistics.stdev(prices))
        
    calc_rank()

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def get_exchange_pairs(exchange = DEFAULT_EXCHANGE):
    query = '''
        select distinct pair 
        from rawQuotes 
        where exchange = "%s" 
        and createdAt > now() - interval 24 hour
    '''%exchange
    cursor.execute(query)
    return cursor.fetchall()

def get_pair_prices(pair, exchange = DEFAULT_EXCHANGE):
    query = '''
        select price 
        from rawQuotes 
        where exchange = '%s' 
        and pair = '%s'
        and createdAt > now() - interval 24 hour
    '''%(exchange,pair)
    cursor.execute(query)
    return cursor.fetchall()

def upsert_pair_stdev(pair, stdev, exchange = DEFAULT_EXCHANGE):
    query = '''
        insert into quoteRanks (
        exchange, pair, standardDeviation) 
        values ('%s','%s', %s) 
        on duplicate key update 
        standardDeviation = %s
    '''%(exchange,pair,stdev,stdev)
    cursor.execute(query)
    db.commit()

def calc_rank(exchange = DEFAULT_EXCHANGE):
    query = 'SET @r=0'
    cursor.execute(query)
    
    query = '''
        update quoteRanks
        set rank = @r:= (@r+1) 
        where exchange = '%s'
        order by standardDeviation desc
    '''%exchange
    cursor.execute(query)
    db.commit()

lambda_handler({},{})