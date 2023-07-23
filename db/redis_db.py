import redis
import datetime

r = redis.Redis()
r.mset({'Croatia': 'Zagreb',
        'Russia': 1,
        'Bahamas': 'Nassau'}
       )

today = datetime.date.today()
addreses = {'lenina', 'komarova', 'narodnaya'}
stoday = today.isoformat()
r.sadd(stoday, *addreses)
print(r.smembers(stoday))
print(r.keys())
