#Give alerts based on crypto price threshold (alerts.txt)
import os
import requests
import json
from datetime import datetime
import time
import os
from gtts import gTTS

convert = 'USD'
listings_url = 'https://api.coinmarketcap.com/v2/listings/?convert=' + convert
url_end = '?structure=array&convert=' + convert

request = requests.get(listings_url)
results = request.json()
data = results['data']

ticker_url_pairs = {}
for currency in data:
    symbol = currency['symbol']
    url = currency['id']
    ticker_url_pairs[symbol] = url

print()
print("ALERTS TRACKING...")
print()

already_hit_symbols = []

while True:
    with open('alerts.txt') as inp:
        for line in inp:
            ticker, amount = line.split()
            ticker = ticker.upper()

            ticker_url = 'https://api.coinmarketcap.com/v2/ticker/' + str(ticker_url_pairs[ticker]) + '/' + url_end

            request = requests.get(ticker_url)
            results = request.json()

            currency = results['data'][0]
            name = currency['name']
            last_updated = currency['last_updated']
            symbol = currency['symbol']
            quotes = currency['quotes'][convert]
            price = quotes['price']

            if float(price) >= float(amount) and symbol not in already_hit_symbols:
                #os.system('say ' + name + ' hit ' + str(amount))

                #myobj = gTTS(text = name + ' hit ' + str(amount), lang='en', slow=False)
                #myobj.save("alert.mp3")
                #os.system("mpg321 alert.mp3")
                last_updated_string = datetime.fromtimestamp(last_updated).strftime('%D %d, %Y at %I:%M%p')
                print(name + ' hit ' + amount + ' on ' + last_updated_string)
                already_hit_symbols.append(symbol)

    print("...")
    time.sleep(300)
