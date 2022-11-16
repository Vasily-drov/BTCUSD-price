import sys, requests

def fetch_orders(order_type):

    orders = {}
    
    cbpro = requests.get('https://api.pro.coinbase.com/products/BTC-USD/book?level=2')
    if (cbpro.status_code == 200):
        for order in cbpro.json()[order_type]:
                price = order[0]
                amount = order[1]
                orders[float(price)] = amount
    else : print('Something wrong with COINBASE API')
      
    gemini = requests.get('https://api.gemini.com/v1/book/BTCUSD')
    if (gemini.status_code == 200):
        for order in gemini.json()[order_type]:
            price = order['price']
            amount = order['amount']
            try: orders[float(price)] =+ float(amount)    
            except KeyError: orders[float(price)] = amount
    else : print('Something wrong with GEMINI API')
    
    kraken = requests.get('https://api.kraken.com/0/public/Depth?pair=XBTUSD')
    if (kraken.status_code == 200):
        for order in kraken.json()['result']['XXBTZUSD'][order_type]:
            price = order[0][:-3]
            amount = order[1]
            try: orders[float(price)] =+ float(amount)    
            except KeyError: orders[float(price)] = amount
    else : print('Something wrong with KRAKEN API')
        
    result = {order_type: orders}
    return result


def best_price(orders, quantity):

    order_type = list(orders.keys())[0]
    orders = orders[order_type]
    keys_list = [float(key) for key in orders]
    if order_type == 'bids':
        sorted_orders  = sorted(keys_list, reverse=True)
        
            
    if order_type == 'asks':
        sorted_orders  = sorted(keys_list)
        
    curent_quantity = 0.0
    best_price = 0
    
    for order in sorted_orders:
        
        if curent_quantity < quantity:
            curent_quantity += float(orders[order])
            best_price += float(order) * float(orders[order])
        else:
            overlap = curent_quantity - quantity
            best_price -= (float(order) * overlap)
            break

        
    if order_type == 'bids':
        print('BEST PRICE TO SELL ', quantity, ' BTC IS ', best_price)
    if order_type == 'asks':
        print('BEST PRICE TO BUY ', quantity, ' BTC IS ', best_price)

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        raise ValueError('Please provide a quantity to calculate price for')
 
    quantity = float(sys.argv[1])
    asks = fetch_orders('asks')
    best_price(asks,quantity)
    bids = fetch_orders('bids')
    best_price(bids,quantity)
    
    

