from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from requests.auth import HTTPBasicAuth
from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from .models import MpesaPayment

def getAccessToken(request):
    consumer_key = 'QF2ectS95whw90wkbiYAS0bJfMPHy9vdG0IbULEpevL2X24U'
    consumer_secret = 'YGpbPMFye7gAiz9LUBrwvQ5KLS7mlJhBzzJresNAtsIOhiLw9TtHANbeeJW5nqQ9'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)


from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests


from django.http import JsonResponse
import json

@csrf_exempt
def lipa_na_mpesa_online(request):
 
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed', status=405)

    # Get JSON data from the request body
    try:
        json_data = json.loads(request.body)
        mpesa_number = float(json_data.get('mpesa_number'))
        total_price = float(json_data.get('total_price'))
    except json.JSONDecodeError:
        return HttpResponse('Invalid JSON data', status=400)

    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}

    if total_price is None:
        return HttpResponse('Total price is missing', status=400)
    
    try:
        total_price = float(total_price)
    except ValueError:
        return HttpResponse('Invalid total price', status=400)

    request_data = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": total_price,
        "PartyA": int(mpesa_number),
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": int(mpesa_number),
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Live In Nairobi",
        "TransactionDesc": "Testing stk push"
    }

    response = requests.post(api_url, json=request_data, headers=headers)
    
    if response.status_code == 200:
        call_back(request)
        validation(request)
        confirmation(request)
        return HttpResponse('success')
    else:
        return HttpResponse('Failed to initiate STK push', status=response.status_code)


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {
        "ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
        "ResponseType": "Completed",
        "ConfirmationURL": "https://8f0d-102-213-48-6.ngrok-free.app/payments/c2b/confirmation",
        "ValidationURL": "https://8f0d-102-213-48-6.ngrok-free.app/payments/c2b/validation"
    }
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)

from django.http import JsonResponse

@csrf_exempt
def call_back(request):
    if request.method == 'POST':
        mpesa_body = request.body.decode('utf-8')
        mpesa_payment = json.loads(mpesa_body)
        transaction_id = mpesa_payment.get('TransactionID')
        amount = mpesa_payment.get('Amount')
        response_data = {"ResultCode": 0, "ResultDesc": "Callback received successfully", "mpesa_payment": mpesa_payment}
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

@csrf_exempt
def validation(request):
    context = {"ResultCode": 0, "ResultDesc": "Accepted"}
    return JsonResponse(dict(context))

def confirmation(request):
    pass


