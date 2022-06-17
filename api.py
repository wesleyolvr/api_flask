import uuid
import cache
import json
import requests
from dotenv import dotenv_values
from flask import Flask, jsonify, make_response, request
import bd_controller

config = dotenv_values(".env")

client_access_token = config['CLIENT_ACCESS_TOKEN']

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
            return return_response(response_items)
        
        
        
        artista_no_cache = artista_esta_no_cache(search_term)
        if artista_no_cache:
        
            return return_response(artista_no_cache)
        artista_no_banco = artista_esta_no_banco(search_term)
        if artista_no_banco:
        
            return return_response(artista_no_banco)
        
        #pesquisar na API
        items_response = search_api(search_term)
        
        bd_controller.load_items(items_response)
        
        cache.set_item(search_term, json.dumps(items_response))
        
        return return_response(items_response)
    
    
    except Exception as e:
        raise e
    
    
    
    
def search_api(search_term):
    genius_search_url = f"http://api.genius.com/search?q={search_term}&access_token={client_access_token}"
    response = requests.get(genius_search_url)
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
        
        
        
def return_response(items):
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
    return bd_controller.get_item(artist_name)
