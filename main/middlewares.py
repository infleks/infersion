'''
from datetime import datetime
from django.shortcuts import render, redirect

class SessionExpiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_request(self,request):
        last_activity = request.session['last_activity']
        now = datetime.now()

        if 'user_id' in request.session.keys():
            last_activity = now.minutes + 10
            request.session['last_activity'] = last_activity

        if not request.is_ajax():
            request.session['last_activity'] = now
'''
from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

class SessionExpiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)
        
    def process_request(self, request):
        if 'user_id' in request.session:
            request.session.set_expiry(60*60)