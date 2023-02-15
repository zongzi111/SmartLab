from django.contrib.auth.models import User
from django.shortcuts import render
from .models import Instrument
from django.http import JsonResponse
from django.core import serializers

import json

def dashboard(request):
    user_count = User.objects.count()
    instrument_count = Instrument.objects.count()

    context = { 'user_count': user_count, 'instrument_count': instrument_count }
    return render(request, 'instrument/dashboard.html',context)

def all_instrument(request):
    response = {}
    try:
        instruments = Instrument.objects.filter()
        response['list']  = json.loads(serializers.serialize("json", instruments))
        response['msg'] = 'success'
        response['error_num'] = 0
    except Exception as e:
        response = {
            'msg': str(e),
            'error_num': 1,
        }

    return JsonResponse(response)