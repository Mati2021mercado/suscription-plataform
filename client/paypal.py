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
    
    
    
def update_subscription_paypal(access_token, subID):
    
    #con el espacio al final de Bearer
    bearer_token = 'Bearer ' + access_token
    
    headers = {
        
        'Content-Type':'application/json',
        'Authorization': bearer_token,
    }
    
    subDetails = Subscription.objects.get(paypal_subscription_id=subID)
    
    # obtengo el plan actual del usuario/cliente
    
    current_sub_plan = subDetails.subscription_plan
    
    if current_sub_plan == 'Standard':
        
        new_sub_plan_id = 'P-7FN8721886700203NMXA5UNA' # A premium
        
    elif current_sub_plan == 'Premium':
        
        new_sub_plan_id = 'P-2NY579910G678903UMXA5S7Q' # A Standard
        
    
    url = 'https://api.sandbox.paypal.com/v1/billing/subscriptions/' + subID + '/revise'
    
    revision_data = {
        
        "plan_id": new_sub_plan_id
            
    }
    
    # Crear a POST request a Paypal API para editar/revisar la subscripcion
    
    r = requests.post(
        url,
        headers=headers,
        data=json.dumps(revision_data)
    )
    
    # la respuesta de Paypal
    
    response_data = r.json()
    print(response_data)
    
    approve_link = None
    
    for link in response_data.get('link', []):
        
        if link.get('rel') == 'approve':
            approve_link = link['href']
    
    if r.status_code == 200:
        print("Request was a success")
        return approve_link
    
    else:
        print("Sorry, an error occured")
        
        
        
def get_current_subscription(access_token, subID):
    
    bearer_token = 'Bearer ' + access_token
    
    headers = {
        
        'Content-Type':'application/json',
        'Authorization': bearer_token,
    }
    
    url = f'https://api.sandbox.paypal.com/v1/billing/subscriptions/{subID}'
    
    r = requests.get(
        url,
        headers=headers
        )
    
    #si fue iniciada con éxito
    if r.status_code == 200:
        
        #convierto la respuesta en formato json
        subscription_data = r.json()
        # agarro la key que contiene el ID del plan
        current_plan_id = subscription_data.get('plan_id')
        # retorno la key
        return current_plan_id
    
    else:
        print("Failed to retrieve subscription details")
        return None