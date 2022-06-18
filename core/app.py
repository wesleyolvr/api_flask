import json
import uuid

import requests
from dotenv import dotenv_values
from flask import Flask, jsonify, make_response, request


from projetos.core import cache,bd_controller

config = dotenv_values(".env")

client_access_token = config['CLIENT_ACCESS_TOKEN']
genius_search_url = "http://api.genius.com/search?q={}&access_token={}"
app = Flask(__name__)

@app.route("/hits", methods=['GET'])
def get_10_hits_from_artist():
    
    try:
        search_term = request.args.get("artista_nome")
        CACHE = request.args.get("cache")
        if CACHE == 'false':
            cache.delete_item(search_term)
            response_items = search_api(search_term)
            bd_controller.load_items(response_items)
            return buid_response(response_items)
        
        artista_no_cache = artista_esta_no_cache(search_term)
        if artista_no_cache:
            print('artista_no_cache',artista_no_cache)
            return buid_response(json.loads(artista_no_cache))
        artista_no_banco = artista_esta_no_banco(search_term)
        if artista_no_banco:
            return buid_response(artista_no_banco)
        
        #pesquisar na API
        items_response = search_api(search_term)
        if items_response.get('error'):
            return items_response
        
        bd_controller.load_items(items_response)
        cache.set_item(search_term, json.dumps(items_response))
        
        return buid_response(items_response)
    
    
    except Exception as e:
        raise e
    
    
    
    
def search_api(search_term):
    try:
        response = requests.get(genius_search_url.formart(search_term))
        if response.status_code == 200:
            id_transacao = str(uuid.uuid4())
            json_data = response.json()
            hits = [song['result']['full_title'] for song in json_data['response']['hits']]
            response_hits = {
                "id": id_transacao,
                "artist": search_term,
                "hits": hits
                }
            return response_hits
        else:
            return jsonify({"error": "Não encontrado"})
    except Exception as e:
        return jsonify({"error": e})
        
        
        
def buid_response(items):
    if items:
        response = make_response(
                jsonify(
                    items
                ),
                200,
            )
        return response
    else:
        return jsonify({"error": "Não encontrado"})

def artista_esta_no_cache(artist_name):
    return cache.get_item(artist_name)


def artista_esta_no_banco(artist_name):
    item = bd_controller.get_item(artist_name)
    return item.get('Item')



if __name__ == "__main__":
    app.run(use_reloader=True)
