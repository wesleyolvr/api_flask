from datetime import timedelta
import redis

redis_con = redis.Redis(host='localhost', port=6379, db=0)

def set_item(artista_nome, items):
    time = timedelta(days=7)
    return redis_con.set(artista_nome, items, ex=time)
    
def get_item(artista_nome):
    return redis_con.get(artista_nome)

def delete_item(artista_nome):
    return redis_con.delete(artista_nome)