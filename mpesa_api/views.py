from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from requests.auth import HTTPBasicAuth
from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from .models import MpesaPayment

def getAccessToken(request):
    consumer_key = 'cHnkwYIgBbrxlgBoneczmIJFXVm0oHky'
    consumer_secret = '2nHEyWSD4VjpNh2g'
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
        "ConfirmationURL": "https://79372821.ngrok.io/api/v1/c2b/confirmation",
        "ValidationURL": "https://79372821.ngrok.io/api/v1/c2b/validation"
    }
    response = requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)

@csrf_exempt
def call_back(request):
    return HttpResponse("Callback received successfully")

@csrf_exempt
def validation(request):
    context = {"ResultCode": 0, "ResultDesc": "Accepted"}
    return JsonResponse(dict(context))

@csrf_exempt
def confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],
    )
    payment.save()
    context = {"ResultCode": 0, "ResultDesc": "Accepted"}
    return JsonResponse(dict(context))
