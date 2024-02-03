import requests
import json

from . models import Subscription

### Visitar developer.paypal.com

def  get_access_token():
    #  preparar una carga útil de datos para enviarla a la API de PayPal, que indicará específicamente que la solicitud es para obtener un token de acceso utilizando el tipo de concesión de credenciales de nuestro cliente.
    data = {'grant_type':'client_credentials'}
    #  especificar que el cliente esperará que la API responda con datos en formato Json a través del encabezado de aceptación.
    headers = {'Accept': 'application/json', 'Accept-Language':'en_US'}
    # codigo de cliente que me da Paypal esta en el txt
    client_id = 'AcHtRS1ntpopmDWrp3m6HsRKvHIfh_z0VW8LWGpXqLihY0tGxfOXxXmiJS6qEKrq2ajTNnjd3txStsjU'
    # secrey key que me da Paypal esta en el txt
    secret_id = 'EOGHtm-xv2wQpzPcfokzOCbk74EqaelRxbgZLtwYRo7TCgidZDDYBVTGisdE1gySYGhaiMRlYmTl8leR'
    
    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    
    r = requests.post(
        url,
        auth=(client_id, secret_id),
        headers=headers,
        data=data
        ).json()
    
    #finalmente obtenemos el token
    access_token = r['access_token']
    return access_token

def cancel_subscription_paypal(access_token, subID):
    
    #con el espacio al final de Bearer
    bearer_token = 'Bearer ' + access_token
    
    headers = {
        
        'Content-Type':'application/json',
        'Authorization': bearer_token,
        
    }
    
    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + subID + '/cancel'
    
    r = requests.post(
        url,
        headers=headers
        )
    
    print(r.status_code)
    print(r.status_code)
    print(r.status_code)
    print(r.status_code)
    
    
    
    
    
    
    
    