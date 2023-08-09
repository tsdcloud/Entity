import http.client
import json

from common.constants import ENDPOINT_USER


def auth_middleware(get_response):
    """ récupère l'utilisateur authentifié """
    
    def middleware(request):
        authorization = request.headers.get('Authorization', 'e')
        conn = http.client.HTTPSConnection(ENDPOINT_USER)
        payload = ''
        headers = {
            "Authorization" : authorization
        }
        conn.request("GET", "/profil/myprofil/", payload, headers)
        response = conn.getresponse()
        data = json.loads(response.read())
        if data.get('uuid',0) != 0:
            request.infoUser = data
        else:
            request.infoUser = None

        response = get_response(request)


        return response

    return middleware