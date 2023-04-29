from django.shortcuts import render

def home(request):
    return render(request, 'home.html')
def login(request):
    return render(request, 'login.html')
def autenticacion (request):
    return render(request, 'auth.html')
def confirmacion(request):
    return render(request, 'confirmacion.html')
