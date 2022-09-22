import os
import mysql.connector
import statistics

DEFAULT_EXCHANGE = 'kraken'

try:
    db = mysql.connector.connect(
        host = os.environ.get('DB_HOST','localhost'),
        user = os.environ.get('DB_USER','root'),
        password = os.environ.get('DB_PASSWORD','password'),
        database = os.environ.get('DB_DATABASE','mc-nest')
    )

    cursor = db.cursor(dictionary=True)
except mysql.connector.Error as error:
    print(error)

def lambda_handler(event, context):    
    results = get_exchange_pairs()
    pair_stdev = []
    for pair_record in results:
        pair = pair_record.get('pair')
        pair_prices = get_pair_prices(pair)
        if (len(pair_prices) < 2):
            continue

        prices = []
        for price in pair_prices:
            prices.append(price.get('price'))
        
        pair_stdev.append({
            'pair': pair,
            'stdev': statistics.stdev(prices)
        })

    upsert_pair_stdev(pair_stdev)
    calc_rank()
    return {
        'statusCode': 200,
    }

def get_exchange_pairs(exchange = DEFAULT_EXCHANGE):
    query = '''
        select distinct pair 
        from quotes 
        where exchange = "%s" 
        and created_at > now() - interval 24 hour
        limit 5
    '''%exchange
    cursor.execute(query)
    return cursor.fetchall()

def get_pair_prices(pair, exchange = DEFAULT_EXCHANGE):
    query = '''
        select price 
        from quotes 
        where exchange = '%s' 
        and pair = '%s'
        and created_at > now() - interval 24 hour
    '''%(exchange,pair)
    cursor.execute(query)
    return cursor.fetchall()

def upsert_pair_stdev(pair_stdev, exchange = DEFAULT_EXCHANGE):
    query = '''
        insert into ranks 
        (exchange, pair, standard_deviation) values 
    '''

    for item in pair_stdev:        
        query += '''('%s','%s', %s),'''%(exchange,item.get('pair'),item.get('stdev'))
    
    query = query[:-1]
    query += '''
        on duplicate key update 
        standard_deviation = values(standard_deviation)
    '''
    cursor.execute(query)
    return db.commit()

def calc_rank():
    query = '''
        update ranks as r
        join (select exchange,pair,dense_rank() OVER ( partition by exchange order by standard_deviation desc) as 'dense_rank' from ranks) as rr
        on r.exchange = rr.exchange and r.pair = rr.pair
        set r.the_rank = rr.dense_rank
    '''
    cursor.execute(query)
    db.commit()

lambda_handler({},{})