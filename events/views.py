from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
# Create your views here.
class Login(APIView):
    def post(self, request):
        username=request.data.get('username')
        password=request.data.get('password')
        user = authenticate(
        request,
        username=username,
        password=password,
    )
        if user is None:
            return JsonResponse({'error':'Failed to login. Invalid credentials'}, status=401)
        login(request, user) 
        return JsonResponse({'detail':'Logged in', 'session_key':request.session.session_key})