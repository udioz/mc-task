import mysql.connector

DEFAULT_EXCHANGE = 'kraken'

db = mysql.connector.connect(
  host='localhost',
  user='root',
  password='password',
  database='mc-nest'
)

cursor = db.cursor(dictionary=True)

def lambda_handler(event, context):
    pair = event['pair']
    quotes = get_pair_quotes(pair)
    rank = get_pair_rank(pair)
    print(rank, quotes)
    return {
        'statusCode': 200,
        'body': quotes
    }

def get_pair_quotes(pair, exchange = DEFAULT_EXCHANGE):
  query = '''
    select exchange, pair, price
    from rawQuotes
    where exchange = '%s'
    and pair = '%s'
    and createdAt > now() - interval 24 hour
  '''%(exchange, pair)

  cursor.execute(query)
  return cursor.fetchall()

def get_pair_rank(pair, exchange = DEFAULT_EXCHANGE):
  query = '''
    select rank 
    from quoteRanks
    where exchange = '%s'
    and pair = '%s' 
  '''%(exchange, pair)
  cursor.execute(query)
  return cursor.fetchone()

lambda_handler({ 'pair': 'btcusd' },{})