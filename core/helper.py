import dotenv
from os import getenv


dotenv.load_dotenv(dotenv.find_dotenv())

client_access_token = getenv('CLIENT_ACCESS_TOKEN', None)


