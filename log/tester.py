def exchange(val, currency, target = 'USD'):
    rate = {
        'KZT' : 0.0022,
        'EUR' : 1.06,
        'RUB' : 0.013,
        'USD' : 1
    }
    
    usd = val * rate[currency]
    if target == "USD":
        return usd
    
    else:
        return usd / rate[target]
    
a = exchange(733, 'KZT', 'USD')
print(a)
b = exchange(a, 'USD', 'KZT')
print(b)