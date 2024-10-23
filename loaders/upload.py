import clean_web_loader, local_data_loader
import requests


def upload_data(web_url=None, web_depth=None, local_path=None):
    url = 'http://localhost:8000/api/document/'
    docs = []
    
    if web_url:
        web_loader = clean_web_loader.CleanWebLoader(web_url, depth=web_depth)
        docs.extend(web_loader.load())
        
    if local_path:
        local_loader = local_data_loader.LocalDataLoader(local_path)
        docs.extend(local_loader.load())

    for doc in docs:
        requests.post(url, json=doc)
        