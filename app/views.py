# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse

#REGISTRO NUEVOS USUARIOS
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    images = services.getAllImages()
    favourite_list = []

    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list})

def search(request):
    search_msg = request.POST.get('query', '')

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        images = services.getAllImages(input=search_msg)
    else:
        return redirect('home')   
    return render(request, 'home.html', {'images':images})


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    pass

@login_required
def deleteFavourite(request):
    pass

@login_required
def logout(request):
    pass


#REGISTRO DE NUEVOS USUARIOS
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    else:
        #pregunta si las contraseñas coinciden
        if request.POST['password1'] == request.POST['password2']:
            #pregunta si el usuario existe (devuelve True o False)
            if existeUser(request.POST['username']):
                return HttpResponse("el usuario ya existe")
            else:
                # se registra el usuario
                user = User.objects.create_user(
                    username=request.POST['username'],
                    email=request.POST['email'],
                    password=request.POST['password1'],
                    )
                user.first_name=request.POST['name'],
                user.last_name=request.POST['surname'],
                user.save()
                # se envia el email
                email = request.POST['email']
                asunto = 'Registro Exitoso'
                mensaje = f'Hola {request.POST["name"]},\n\nTe registrase exitosamente en nuestro sitio.'
                send_mail(
                    asunto,
                    mensaje,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )
                messages.success(request, 'Correo de confirmación enviado correctamente.')
                return redirect('home')
        else:
            return HttpResponse("no coinciden las contraseñas")
        
def existeUser(username):
    return User.objects.filter(username=username).exists()