import requests
from projetos.core.app import genius_search_url, client_access_token



def test_status_code_200_request_api_token_valido():
    artist = "seu jorge"
    response = requests.get(genius_search_url.format(artist,client_access_token))
    assert True if response.status_code == 200 else False, response.status_code

def test_status_code_200_request_api():
    artist = "marcos almeida"
    response = requests.get(genius_search_url.format(artist,client_access_token))
    assert True if response.status_code == 200 else False, response.status_code


def test_status_code_200_request_api_sem_artist():
    artist = ""
    response = requests.get(genius_search_url.format(artist,client_access_token))
    assert True if response.status_code == 200 else False, response.status_code


def test_status_code_401_request_api_token_invalido():
    artist = "marcos almeida"
    response = requests.get(genius_search_url.format(artist,client_access_token+'invalido'))
    assert True if response.status_code == 401 else False, response.status_code


def test_status_code_401_request_api_url_invalida():
    genius_search_url.replace('search?','')
    client_access_token=''
    artist = "marcos almeida"
    response = requests.get(genius_search_url.format(artist,client_access_token))
    assert True if response.status_code == 401 else False, response.status_code
    

def test_request_api_sem_conexao_internet():
    artist = "marco telles"
    try:
        response = requests.get(genius_search_url.format(artist,client_access_token))
        assert True if response.status_code == 200 else False, response.status_code
    except requests.ConnectionError as e:
        print('msg error :', e.strerror)
        assert True