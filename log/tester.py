def exchange(val, currency, target = 'USD'):
    rate = {
        'KZT' : 0.0022,
        'EUR' : 1.06,
        'RUB' : 0.013,
        'USD' : 1
    }
    
    usd = val * rate[currency]
    if target == "USD":
        return round(usd, 1)
    
    else:
        return round(usd / rate[target], 1)
    
    
print(exchange(100, 'USD', 'EUR'))