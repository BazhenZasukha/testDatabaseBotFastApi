import requests


# all available methods
class Method: type=None

class Get(Method): type='GET'
class Post(Method): type='POST'
class Put(Method): type='PUT'
class Delete(Method): type='DELETE'


class Connector:
    def __init__(self):
        pass

    def ask(self, url: str, method: Method=Get, header: dict|None=None, body: dict|None=None) -> str|dict|int:
        session = requests.Session()
        if header: session.headers.update(header)

        if method == Get: req = session.get(url, params=body)
        elif method == Post: req = session.post(url, json=body)
        elif method == Put: req = session.put(url, json=body)
        elif method == Delete: req = session.delete(url, json=body)
        else: raise Exception('Method not supported, please choose one from Get, Post, Put, Delete')

        if req.status_code == 200:
            try: return req.json()
            except: return req.text()
        else: return req.status_code

