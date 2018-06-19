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
        return self.get_response(request)
        
    def process_request(self,request):
        last_activity = request.session['last_activity']
        now = datetime.now()

        if (now - last_activity).minutes > 10:
            try:
                del request.session['user_id']
            except KeyError:
                pass
            return render(request, 'registration/login.html', {})

        if not request.is_ajax():
            request.session['last_activity'] = now